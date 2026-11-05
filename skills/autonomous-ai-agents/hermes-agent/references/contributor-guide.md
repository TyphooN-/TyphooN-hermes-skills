# Contributor Quick Reference

For occasional contributors and PR authors. Full developer docs: https://hermes-agent.nousresearch.com/docs/developer-guide/

### Project Layout

```
hermes-agent/
├── run_agent.py          # AIAgent — core conversation loop
├── model_tools.py        # Tool discovery and dispatch
├── toolsets.py           # Toolset definitions
├── cli.py                # Interactive CLI (HermesCLI)
├── hermes_state.py       # SQLite session store
├── agent/                # Prompt builder, context compression, memory, model routing, credential pooling, skill dispatch
├── hermes_cli/           # CLI subcommands, config, setup, commands
│   ├── commands.py       # Slash command registry (CommandDef)
│   ├── config.py         # DEFAULT_CONFIG, env var definitions
│   └── main.py           # CLI entry point and argparse
├── tools/                # One file per tool
│   └── registry.py       # Central tool registry
├── gateway/              # Messaging gateway
│   └── platforms/        # Platform adapters (telegram, discord, etc.)
├── cron/                 # Job scheduler
├── tests/                # Extensive pytest suite (run via scripts/run_tests.sh)
└── website/              # Docusaurus docs site
```

Config: `~/.hermes/config.yaml` (settings), `~/.hermes/.env` (API keys) — both under `$HERMES_HOME` when it is set.

### Adding a Tool

Two files. Auto-discovery imports any `tools/*.py` with a top-level
`registry.register()` call, but a tool is only *exposed* to an agent once
its name appears in a toolset.

**1. Create `tools/your_tool.py`:**
```python
import json, os
from tools.registry import registry

def check_requirements() -> bool:
    return bool(os.getenv("EXAMPLE_API_KEY"))

def example_tool(param: str, task_id: str = None) -> str:
    return json.dumps({"success": True, "data": "..."})

registry.register(
    name="example_tool",
    toolset="example",
    schema={"name": "example_tool", "description": "...", "parameters": {...}},
    handler=lambda args, **kw: example_tool(
        param=args.get("param", ""), task_id=kw.get("task_id")),
    check_fn=check_requirements,
    requires_env=["EXAMPLE_API_KEY"],
)
```

**2. Wire it into a toolset in `toolsets.py`** — add the name to
`_HERMES_CORE_TOOLS` (every platform) or to a specific toolset.

All handlers must return JSON strings. Use `get_hermes_home()` for paths,
never hardcode `~/.hermes`. For custom/local-only tools, write a plugin in
`~/.hermes/plugins/` instead of editing core — see the developer docs.

### Adding a Slash Command

1. Add `CommandDef` to `COMMAND_REGISTRY` in `hermes_cli/commands.py`
2. Add handler in `cli.py` → `process_command()`
3. (Optional) Add gateway handler in `gateway/run.py`

All consumers (help text, autocomplete, Telegram menu, Slack mapping) derive from the central registry automatically.

### Agent Loop (High Level)

```
run_conversation():
  1. Build system prompt
  2. Loop while iterations < max:
     a. Call LLM (OpenAI-format messages + tool schemas)
     b. If tool_calls → dispatch each via handle_function_call() → append results → continue
     c. If text response → return
  3. Context compression triggers automatically near token limit
```

### Testing

Use `scripts/run_tests.sh` for CI parity. It clears credentials, sets
`TZ=UTC`, and runs each test file in a separate subprocess through
`scripts/run_tests_parallel.py` on every platform. It does not use xdist.

```bash
scripts/run_tests.sh                          # full suite
scripts/run_tests.sh tests/tools/             # one directory
scripts/run_tests.sh tests/tools/test_x.py    # one file
scripts/run_tests.sh -v --tb=long             # pass-through pytest flags
```

- Tests auto-redirect `HERMES_HOME` to temp dirs — never touch real `~/.hermes/`.
- Reuse fixtures through existing `conftest.py` scope or a deliberately registered module-level `pytest_plugins` entry. Avoid importing a fixture into a global name then shadowing it with the test parameter: code health can flag `F811`, while a redundant same-name import alias can instead trigger `PLC0414`. Register only the intended fixture module and check its import-time effects.
- Import reusable `Test*` harness classes under a non-collectable alias such as `_RestoreHarness`; otherwise pytest can collect the imported class again and inflate the apparent proof. After fixture/helper changes, run the maintained selected-file command and `python scripts/check --base <BASE>`, and verify the expected fully qualified case identities rather than relying on an exit code or total alone.
- Keep real public `call_llm`/`async_call_llm` APIs running in bounded-helper integration tests; they contain the local-policy dispatch branch, so forbidding the API itself produces false failures rather than proving cloud exclusion. Trace and guard the actual ordinary-provider/credential boundary below it, and assert that each required guard was installed.
- Record forbidden-boundary hits outside production exception handlers and assert the record after the public consumer returns; broad `except Exception` can swallow a sentinel and yield the same output as a valid refusal. Add an injected forbidden-path regression that proves the harness itself goes red, and do not stub real config resolution to make routing tests pass.
- Re-resolve executable, source base and import origins after installation recovery; a same-named clean checkout can lack earlier local changes. Preserve the old evidence, port onto the current base and rerun source-bound proof before declaring restoration complete.
- For matched baseline/regression proof, keep the test checkout, Git metadata and its `TMPDIR` outside the real Hermes home. A linked worktree can still route recovery-marker checks into the live repository's `.git/worktrees` under that guarded home; use a standalone local clone rather than disabling the guard. The I/O isolation guard can also abort ordinary-path tests on an unrelated scratch manifest under `~/.hermes/cache/scratch`; identical aborted failure IDs do not prove compatibility. Use an owned ignored checkout scratch directory (not system `/tmp`), and distinguish guard failures from executed behavioral checks. Size the canonical runner's per-file deadline for the complete parametrized collection; preserve a timed-out attempt separately rather than crediting its passing prefix.
- Prepare Python through the PM developer workflow before building a test environment.
- Run `python -m pm.build_env --source . --out .venv --group dev --group test`.
  The output must not exist. Stop its processes and intentionally remove only
  that disposable environment before regeneration.
- The runner probes repository `.venv`, `venv`, and the standard source-install
  venv before falling back to `HERMES_PYTHON`. Each candidate must contain pytest.
- **Windows:** run the same wrapper through Git Bash. See `references/windows-quirks.md`.
- After editing `pyproject.toml`, run `hermes pm lock`, re-source `./activate`, and
  commit `pyproject.toml` with `uv.lock`.
  Do not mutate Hermes environments with raw pip or uv commands.

Host-specific tests run on the real host. Use one `@pytest.mark.platforms(...)`
marker per test, such as `@pytest.mark.platforms("windows", arch="arm64")`.
Do not fake the host by patching `sys.platform` or platform probes.

### System prompt's execution-environment block

Factual host/backend guidance (OS, `$HOME`, cwd, terminal backend, shell)
is emitted by `agent/prompt_builder.py::build_environment_hints()`. The key
invariant for prompt authors: with a **remote** terminal backend
(`docker, singularity, modal, daytona, ssh, managed_modal`), host info is
suppressed and *every* file tool runs inside the backend container — the
prompt must never describe the host the agent can't touch.

### Commit Conventions

```
type: concise subject line

Optional body.
```

Types: `fix:`, `feat:`, `refactor:`, `docs:`, `chore:`

### Key Rules

- **Never break prompt caching** — don't change context, tools, or system prompt mid-conversation
- **Message role alternation** — never two assistant or two user messages in a row
- Use `get_hermes_home()` from `hermes_constants` for all paths (profile-safe)
- Config values go in `config.yaml`, secrets go in `.env`
- New tools need a `check_fn` so they only appear when requirements are met
