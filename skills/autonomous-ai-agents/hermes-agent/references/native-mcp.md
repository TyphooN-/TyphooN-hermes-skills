# Native MCP Client

Hermes Agent has a built-in MCP client that connects to MCP servers at startup, discovers their tools, and makes them available as first-class tools the agent can call directly. No bridge CLI needed -- tools from MCP servers appear alongside built-in tools like `terminal`, `read_file`, etc.

## When to Use

Use this whenever you want to:
- Connect to MCP servers and use their tools from within Hermes Agent
- Add external capabilities (filesystem access, GitHub, databases, APIs) via MCP
- Run local stdio-based MCP servers (npx, uvx, or any command)
- Connect to remote HTTP/StreamableHTTP MCP servers
- Have MCP tools auto-discovered and available in every conversation

For ad-hoc, one-off MCP tool calls from the terminal without configuring anything, see the `mcporter` skill instead.

## Prerequisites

- **MCP Python dependencies** — included in the standard PM install through the `all` extra. Use PM to add the `mcp` extra.
- **Node.js** -- required for `npx`-based MCP servers (most community servers)
- **uv** -- required for `uvx`-based MCP servers (Python-based servers)

Install the MCP SDK:

```bash
python -c "import pm; pm.sync_venv(['mcp'], explicit=True)"
```

## Quick Start

Add MCP servers to `~/.hermes/config.yaml` under the `mcp_servers` key:

```yaml
mcp_servers:
  time:
    command: "uvx"
    args: ["mcp-server-time"]
```

Restart Hermes Agent. On startup it will:
1. Connect to the server
2. Discover available tools
3. Register them with the prefix `mcp__time__*`
4. Inject them into all platform toolsets

You can then use the tools naturally -- just ask the agent to get the current time.

## Configuration Reference

Each entry under `mcp_servers` is a server name mapped to its config. There are two transport types: **stdio** (command-based) and **HTTP** (url-based).

### Stdio Transport (command + args)

```yaml
mcp_servers:
  server_name:
    command: "npx"             # (required) executable to run
    args: ["-y", "pkg-name"]   # (optional) command arguments, default: []
    env:                       # (optional) environment variables for the subprocess
      SOME_API_KEY: "value"
    timeout: 120               # (optional) per-tool-call timeout in seconds, default: 120
    connect_timeout: 60        # (optional) initial connection timeout in seconds, default: 60
```

### HTTP Transport (url)

```yaml
mcp_servers:
  server_name:
    url: "https://my-server.example.com/mcp"   # (required) server URL
    headers:                                     # (optional) HTTP headers
      Authorization: "Bearer sk-..."
    timeout: 180               # (optional) per-tool-call timeout in seconds, default: 120
    connect_timeout: 60        # (optional) initial connection timeout in seconds, default: 60
```

### All Config Options

| Option            | Type   | Default | Description                                       |
|-------------------|--------|---------|---------------------------------------------------|
| `command`         | string | --      | Executable to run (stdio transport, required)     |
| `args`            | list   | `[]`    | Arguments passed to the command                   |
| `env`             | dict   | `{}`    | Extra environment variables for the subprocess    |
| `url`             | string | --      | Server URL (HTTP transport, required)             |
| `headers`         | dict   | `{}`    | HTTP headers sent with every request              |
| `timeout`         | int    | `120`   | Per-tool-call timeout in seconds                  |
| `connect_timeout` | int    | `60`    | Timeout for initial connection and discovery      |

Note: A server config must have either `command` (stdio) or `url` (HTTP), not both.

## How It Works

### Startup Discovery

When Hermes Agent starts, `discover_mcp_tools()` is called during tool initialization:

1. Reads `mcp_servers` from `~/.hermes/config.yaml`
2. For each server, spawns a connection in a dedicated background event loop
3. Initializes the MCP session and calls `list_tools()` to discover available tools
4. Registers each tool in the Hermes tool registry

### Tool Naming Convention

Resolve generated names through the installed `tools.mcp_tool_schema.mcp_prefixed_tool_name` or the actual registry rather than constructing them from memory. The current naming pattern is:

```
mcp__{server_name}__{tool_name}
```

Components replace hyphens/dots with underscores. The maintained formatter also clamps overlong names to the provider's 64-character bound with a deterministic hash suffix; preserve original server/tool identifiers when calling it.

Examples:
- Server `filesystem`, tool `read_file` → `mcp__filesystem__read_file`
- Server `github`, tool `list-issues` → `mcp__github__list_issues`
- Server `my-api`, tool `fetch.data` → `mcp__my_api__fetch_data`

Distinguish server-advertised tools from registered tools plus host-generated prompt/resource helpers. Reconcile complete discovered names against the raw server catalog, the maintained name formatter and advertised capabilities; their totals need not be equal.

### Auto-Injection

After discovery, MCP tools are automatically injected into all `hermes-*` platform toolsets (CLI, Discord, Telegram, etc.). This means MCP tools are available in every conversation without any additional configuration.

### Connection Lifecycle

- Each server runs as a long-lived asyncio Task in a background daemon thread
- Connections persist for the lifetime of the agent process
- If a connection drops, automatic reconnection with exponential backoff kicks in (up to 5 retries, max 60s backoff)
- On agent shutdown, all connections are gracefully closed

### Idempotency

`discover_mcp_tools()` is idempotent -- calling it multiple times only connects to servers that aren't already connected. Failed servers are retried on subsequent calls.

## Transport Types

### Stdio Transport

The most common transport. Hermes launches the MCP server as a subprocess and communicates over stdin/stdout.

```yaml
mcp_servers:
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/absolute/path/to/projects"]
```

The subprocess inherits a **filtered** environment (see Security section below) plus any variables you specify in `env`.

### HTTP / StreamableHTTP Transport

For remote or shared MCP servers. Requires the `mcp` package to include HTTP client support (`mcp.client.streamable_http`).

```yaml
mcp_servers:
  remote_api:
    url: "https://mcp.example.com/mcp"
    headers:
      Authorization: "Bearer sk-..."
```

If HTTP support is not available in your installed `mcp` version, the server will fail with an ImportError and other servers will continue normally.

## Security

### Environment Variable Filtering

For stdio servers, Hermes does NOT pass your full shell environment to MCP subprocesses. Only safe baseline variables are inherited:

- `PATH`, `HOME`, `USER`, `LANG`, `LC_ALL`, `TERM`, `SHELL`, `TMPDIR`
- Any `XDG_*` variables

All other environment variables (API keys, tokens, secrets) are excluded unless you explicitly add them via the `env` config key. This prevents accidental credential leakage to untrusted MCP servers.

```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      # Only this token is passed to the subprocess
      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_..."
```

### Credential Stripping in Error Messages

If an MCP tool call fails, any credential-like patterns in the error message are automatically redacted before being shown to the LLM. This covers:

- GitHub PATs (`ghp_...`)
- OpenAI-style keys (`sk-...`)
- Bearer tokens
- Generic `token=`, `key=`, `API_KEY=`, `password=`, `secret=` patterns

## Troubleshooting

### "MCP SDK not available -- skipping MCP tool discovery"

The `mcp` Python package is not installed. Install it:

```bash
python -c "import pm; pm.sync_venv(['mcp'], explicit=True)"
```

### "No MCP servers configured"

No `mcp_servers` key in `~/.hermes/config.yaml`, or it's empty. Add at least one server.

### "Failed to connect to MCP server 'X'"

Common causes:
- **Command not found**: The `command` binary isn't on PATH. Ensure `npx`, `uvx`, or the relevant command is installed.
- **Package not found**: For npx servers, the npm package may not exist or may need `-y` in args to auto-install.
- **Timeout**: The server took too long to start. Increase `connect_timeout`.
- **Port conflict**: For HTTP servers, the URL may be unreachable.

### "MCP server 'X' requires HTTP transport but mcp.client.streamable_http is not available"

If the MCP dependencies are damaged, rebuild the recorded environment through PM:

```bash
hermes pm repair
```

### Tools not appearing

- Check that the server is listed under `mcp_servers` (not `mcp` or `servers`)
- Ensure the YAML indentation is correct
- Look at Hermes Agent startup logs for connection messages
- Tool names are prefixed with `mcp__{server}__{tool}` -- look for that pattern

### Connection keeps dropping

The client retries up to 5 times with exponential backoff (1s, 2s, 4s, 8s, 16s, capped at 60s). If the server is fundamentally unreachable, it gives up after 5 attempts. Check the server process and network connectivity.

## Examples

### Time Server (uvx)

```yaml
mcp_servers:
  time:
    command: "uvx"
    args: ["mcp-server-time"]
```

Registers tools like `mcp_time_get_current_time`.

### Filesystem Server (npx)

```yaml
mcp_servers:
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/absolute/path/to/documents"]
    timeout: 30
```

Registers tools like `mcp_filesystem_read_file`, `mcp_filesystem_write_file`, `mcp_filesystem_list_directory`.

### GitHub Server with Authentication

```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xxxxxxxxxxxxxxxxxxxx"
    timeout: 60
```

Registers tools like `mcp_github_list_issues`, `mcp_github_create_pull_request`, etc.

### Remote HTTP Server

```yaml
mcp_servers:
  company_api:
    url: "https://mcp.mycompany.com/v1/mcp"
    headers:
      Authorization: "Bearer sk-xxxxxxxxxxxxxxxxxxxx"
      X-Team-Id: "engineering"
    timeout: 180
    connect_timeout: 30
```

### Multiple Servers

```yaml
mcp_servers:
  time:
    command: "uvx"
    args: ["mcp-server-time"]

  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]

  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xxxxxxxxxxxxxxxxxxxx"

  company_api:
    url: "https://mcp.internal.company.com/mcp"
    headers:
      Authorization: "Bearer sk-xxxxxxxxxxxxxxxxxxxx"
    timeout: 300
```

All tools from all servers are registered and available simultaneously. Each server's tools are prefixed with its name to avoid collisions.

## Source-local plugin verification

1. **Select and freeze the requested source once.** Record the chosen checkout HEAD, any observed upstream tip and the exact commit/tree being qualified; these are different facts. Archive a fixed snapshot into private evidence without rewriting the original checkout. Reuse source-bound proof on continuation instead of chasing a moving branch. After an intentional refresh, retain older proof as historical rather than relabelling it current. If the user selects a newer revision during an active review, stop only the tracked superseded reviewer, preserve its actual exit/output and confirm ownership has ended before preparing the new review; an old verdict cannot accept new source bytes. Treat package versions as metadata, never as substitutes for the source pin.
2. **Reuse verified inputs without shared writable state.** Confirm no writer is mutating the reusable inputs, then inspect the actual install/toolchain receipt and verify its exit and log/artifact bindings; an unfinished overall handoff does not erase a completed dependency-install receipt. Reuse the qualified toolchain and dependency tree only after relevant package/lock bytes match the selected revision. Copy dependencies to a fresh private destination before tests or builds can mutate them: `cp -a --reflink=auto "$SOURCE_NODE_MODULES" "$TEST_WORKSPACE/node_modules"` provides a copy-on-write or ordinary independent copy where supported. Never use writable symlinks or hardlinks into prior evidence. Keep frozen review inputs separate from the test workspace, and check source-byte preservation after execution. Refresh changed locked inputs privately rather than blessing stale dependencies or installing global software. Dependency reuse does not carry an older build or source verdict forward to new source.
3. **Isolate both validators and children.** Use private HOME/HERMES_HOME/XDG/cache/tmp roots and a credential-free environment allowlist. Run directly imported admission checks under that same allowlist: setting only a subprocess `env` leaves supervisor `NODE_OPTIONS`/`NODE_PATH` visible to an in-process validator. Preserve strict launcher rejection; do not weaken the guard or change the user's global environment to make verification pass.
4. **Run cheap source feedback, build, then check compiled boundaries.** Resolve the package's declared commands before execution. When it provides separate source-only and preparation-aware focused runners, run the selected source cases first, then the supported build and type/lint checks, followed by exact MCP schema/status cases through the preparation-aware runner. For REA's declared scripts, invoke the recorded pinned Node/npm pair through `terminal` in this order: `npm run test:local -- SOURCE_TEST_PATHS`, `npm run build:cached`, `npm run check:fast`, then `npm run test:focused -- MCP_TEST_PATHS`. Keep each command/cwd/exit and selected case inventory in a separate receipt; source-only success cannot replace generated-catalog or SDK-conversion checks. Do not bypass missing-artifact guards with a raw test-runner invocation. Bind the fixed source commit/tree, successful build receipt, executable, required compiled entrypoints and complete immutable runtime/dependency inventory. Keep machine-specific paths and pins outside portable plugin source. Define bounds and complete membership checks, not just hashes of listed files. Document linear verification costs and the accidental-drift threat model; unkeyed hashes do not establish hostile-same-user or signed supply-chain protection. Never fall back to npm, downloads, builds or moving-HEAD resolution when local admission fails.
5. **Validate the selected configuration through maintained Hermes interfaces.** When refreshing upstream skill guides, rebase the Hermes connection/approval overlay deliberately: copy the specifically named deadline section, not the entire remaining upstream recovery tail, which can reintroduce competing client setup or npm/CLI fallback instructions. Keep contract checks for single registration and source-local no-fallback behavior, and fix conflicting prose rather than weakening those checks. Use the installed `hermes_cli.agent_plugins.load_agent_plugin` path when a CLI wrapper might bootstrap/update the live install. Validate portable and staged variants separately and retain the translated local command, args, environment and expanded paths. Do not infer portable manifest support from similarly named native-client config fields, or confuse a server startup allowance with the client's call deadline. Do not add competing setup registrations or change a live profile during staging. Once activation is authorized, verify the effective PluginManager/native MCP configuration and its single server owner: a CLI list that reads only raw `mcp_servers` can report none for an enabled portable package. Read qualified skill names and their `plugin_key`, path and frontmatter from the actual plugin skill registry; do not construct them from the MCP owner key, because the skill namespace can be separately path-hashed. Do not add a duplicate native registration to compensate.
6. **Exercise core MCP and the translated adapter as distinct boundaries.** A direct compiled-server stdio probe is useful early feedback; label it direct source-runtime proof, not staged or installed Hermes integration. Separately qualify the staged local adapter through its actual maintained translated configuration. For each claimed boundary, initialize MCP, collect every discovery page and call a bounded static synthetic fixture. Inspect the returned tool schema instead of guessing parameter names. Where identity expectations are exposed, test aligned package/path/catalog expectations, a stale version and a wrong registration path with the same package version; a matching version label cannot detect a stale source runtime. After default/detail or schema-presentation changes, check both omitted arguments and supported explicit detail modes at the actual MCP boundary; verify omission metadata and required diagnostic/capability fields rather than assuming the old response shape. Check the resulting advertised schemas against client constraints, not only their source definitions. Assert non-error structured results, exact target identity, useful operation-specific evidence, an absent target-execution sentinel and actual server exit/cleanup. If the query retains Evidence, exercise a same-session page or projection consumer and preserve its parent identity while checking that the sentinel stays absent. Source-only regression passes do not establish compiled MCP/client compatibility; direct core proof does not establish adapter integration, and catalog discovery proves neither active-profile integration nor native-engine readiness.
7. **Publish proof without rewriting earlier judgments or failed history.** Keep immutable attempt results and atomically replace only a current-result pointer, using fsync where durability is required. When verification advances beyond a hash-linked upgrade recommendation, append a continuation receipt naming the new commands, exact source, proof boundary and remaining gates; do not rewrite the earlier assessment to attribute later execution or independent acceptance to it. Exercise report replacement with an existing clearly labelled summary control. Retain inner-child and outer-runner exits separately; if reporting fails after a useful response, preserve that partial result and rerun the repaired producer rather than copying a PASS JSON over the failure. Require the complete runner to succeed before reporting end-to-end proof, then freeze the candidate and receipt bindings.
8. **Apply each remaining gate separately.** Functional candidate proof is not independent acceptance, native-provider qualification, installation or activation. Follow the skill body's approval-continuity rule, retain missing decisions/verdicts explicitly, and do not relaunch an excluded executor or broaden a review-only approval.

## Sampling (Server-Initiated LLM Requests)

Hermes supports MCP's `sampling/createMessage` capability — MCP servers can request LLM completions through the agent during tool execution. This enables agent-in-the-loop workflows (data analysis, content generation, decision-making).

Sampling is **enabled by default**. Configure per server:

```yaml
mcp_servers:
  my_server:
    command: "npx"
    args: ["-y", "my-mcp-server"]
    sampling:
      enabled: true           # default: true
      model: "gemini-3-flash" # model override (optional)
      max_tokens_cap: 4096    # max tokens per request
      timeout: 30             # LLM call timeout (seconds)
      max_rpm: 10             # max requests per minute
      allowed_models: []      # model whitelist (empty = all)
      max_tool_rounds: 5      # tool loop limit (0 = disable)
      log_level: "info"       # audit verbosity
```

Servers can also include `tools` in sampling requests for multi-turn tool-augmented workflows. The `max_tool_rounds` config prevents infinite tool loops. Per-server audit metrics (requests, errors, tokens, tool use count) are tracked via `get_mcp_status()`.

Disable sampling for untrusted servers with `sampling: { enabled: false }`.

## Notes

- MCP tools are called synchronously from the agent's perspective but run asynchronously on a dedicated background event loop
- Tool results are returned as JSON with either `{"result": "..."}` or `{"error": "..."}`
- The native MCP client is independent of `mcporter` -- you can use both simultaneously
- Server connections are persistent and shared across all conversations in the same agent process
- Adding or removing servers requires restarting the agent (no hot-reload currently)
