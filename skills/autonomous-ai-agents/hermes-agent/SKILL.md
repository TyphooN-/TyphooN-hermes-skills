---
name: hermes-agent
description: Use, configure, theme, extend, and orchestrate Hermes Agent.
version: 3.2.0
author: Hermes Agent + Teknium
license: MIT
platforms:
- linux
- macos
- windows
metadata:
  hermes:
    tags:
    - hermes
    - setup
    - configuration
    - multi-agent
    - spawning
    - cli
    - gateway
    - bots
    - bot-mode
    - features
    - themes
    - skins
    - desktop-plugins
    - tui-widgets
    - petdex
    - development
    homepage: https://github.com/NousResearch/hermes-agent
    related_skills:
    - claude-code
    - codex
    - opencode
x-local-maintainer: TyphooN (TyphooN-)
---


# Hermes Agent

## Portable scope

This copy preserves a locally developed workflow, not transferable approval. Resolve the current task, repository, active Hermes profile, tools and ownership on this machine first. Historical project choices and TyphooN-specific executor/build policies are context, not permission to start services, run targets, modify security settings or publish. Project-root variables are documented in the collection's `PORTABILITY.md`; unset variables are not usable paths. Installing a skill installs no external tools or plugins.

Hermes Agent is an open-source AI agent framework by Nous Research that runs in your terminal, a native desktop app, messaging platforms, and IDEs. It's in the same category as Claude Code (Anthropic), Codex (OpenAI), and OpenClaw — autonomous coding and task-execution agents that use tool calling to interact with your system. Hermes works with any LLM provider (OpenRouter, Anthropic, OpenAI, Google, DeepSeek, xAI, local models, and 20+ others) and runs on Linux, macOS, Windows, and WSL.

What makes Hermes different:

- **Self-improving through skills** — Hermes learns from experience by saving reusable procedures as skills that load into future sessions.
- **Persistent memory across sessions** — remembers who you are, your preferences, environment details, and lessons learned. Pluggable memory backends.
- **Multi-platform gateway** — the same agent runs on Telegram, Discord, Slack, WhatsApp, iMessage, Signal, Matrix, Teams, Email, and a dozen more platforms with full tool access, not just chat.
- **Many surfaces** — the same agent core drives the CLI, the Ink TUI, a native Electron desktop app, a web dashboard, and an ACP server for IDEs (VS Code / Zed / JetBrains).
- **Provider-agnostic** — swap models and providers mid-workflow; credential pools rotate across multiple API keys automatically.
- **Profiles** — run multiple independent Hermes instances with isolated configs, sessions, skills, and memory.
- **Extensible & themeable** — plugins, MCP servers, custom tools, webhook triggers, cron scheduling, skins that theme every surface, desktop UI plugins, TUI widgets, and pet mascots.

**This skill is a hub.** The body covers identity, quick start, spawning/orchestration, and hard invariants. Everything else lives in reference files — **load the matching reference (below) before answering**; do not answer detail questions from the body alone.

**Docs:** https://hermes-agent.nousresearch.com/docs/

## Scope & Verification

This skill is a concise operating guide, not the complete source of truth for every Hermes feature. If a Hermes feature, command, or setting is not mentioned here or in a reference, do not treat that absence as evidence that it does not exist. Check the live repository and official docs before giving a negative answer.

Good verification targets, cheapest first:

- **Every shipped feature, one line each: https://hermes-agent.nousresearch.com/docs/llms.txt.** Start here for any "can Hermes do X?" or "how do I do X?" — it indexes the entire documentation set with a link to the page that answers. It is generated from the docs tree on every build, so it is never behind the product. Fetch it with `web_extract`, or `curl -s https://hermes-agent.nousresearch.com/docs/llms.txt` when web tools are off. The whole documentation set in one file is at `/docs/llms-full.txt`.
- CLI commands: `hermes --help`, `hermes <command> --help`, and `hermes_cli/main.py`
- Source tree: https://github.com/NousResearch/hermes-agent

Never answer "Hermes can't do that" from memory. Hermes ships far more than this skill body describes, and the index exists so a negative answer is always checkable.

### Urgent local restoration

When the user explicitly prioritizes getting local sessions working again, complete the next missing authorized repair or activation step before upstream packaging or optional broader audits. Do not stop at a tested candidate when local application is authorized and no acceptance or activation boundary remains. Keep required independent review, but scope it to the smallest complete causal dependency closure rather than unrelated subsystems. Report source integration, fresh-import verification, gateway reload and observed session recovery separately; a queued application is not an installed fix. Assign an upstream proposal to the implementation that owns the defect, not whichever workflow plugin happened to be active.

### Credential-pool incidents

Diagnose rotation through the actual resumed-session-to-agent route, not quota widgets or isolated pool methods. Require endpoint, account and availability restrictions across every credential-bearing fallback and refresh path; rejecting the primary pool rung does not prevent a lower resolver from borrowing the same credentials or bypassing cooldown/quarantine. Resolve the authoritative owning store before rotating a single-use grant, and require its replacement generation to be durably committed there before reporting recovery. Verify each named affected session separately without changing its intended route or replaying its project requests. Use the ordered diagnosis and regression matrix in `references/providers-and-models.md`; use `references/cli-reference.md` for retaining a local repair across source updates.

### Deleted-session recovery

Preserve current history while recovering the requested conversation; never roll the active database back wholesale to an older snapshot. Bind the target using its title/aliases, session ID and repository/cwd, then preserve the confirmed donor before further investigation. Check installed deletion fences before choosing a destination ID: when the old ID is retired, recover under a fresh ID rather than clearing the fence. Treat stored history, active model context and live execution ownership as separate data. Recovering a conversation does not authorize restarting its project or replaying pending work. Report located, archived, rehearsed and live-restored stages separately, with the last recovered message timestamp. Use `references/troubleshooting.md` for the ordered discovery and restoration checks.

### Build-only repair acceptance

For build-only WebUI work, stop once the supported frontend build succeeds; verify the maintained receipt before claiming the installed product is current. Keep supplementary Python checks and dashboard runtime QA separate rather than turning them into new acceptance blockers. Preserve failed or unfinished checks as explicit verification limits, reconcile the checklist, and return to the original priority when the user accepts the build. Use the ordered proof in `references/cli-reference.md` instead of prolonging manual hash investigation.

### Source-local MCP work

Honor the user's selected source checkout/revision rather than silently substituting a published package pin. Keep the original checkout intact and qualify a fixed snapshot. For an update recommendation, first use the advisory three-revision comparison in `requesting-code-review`; do not automatically run the activation pipeline. Report build, manifest validation, direct compiled-server MCP proof, translated local-adapter proof, independent acceptance and fresh installed-profile activation separately. A passing direct server does not verify an untested plugin overlay or installed registration, and an inner success with a failed reporting runner is not completed proof. Use the ordered procedure in `references/native-mcp.md#source-local-plugin-verification`.

## Quick Start

```bash
# Install (shell installer — bootstraps PM, Python, dependencies, and the launcher)
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# Interactive chat (default surface; set display.interface: tui to launch the Ink TUI instead)
hermes

# Single query
hermes chat -q "What is the capital of France?"

# Setup wizard  /  pick model+provider  /  health check
hermes setup
hermes model
hermes doctor

# Other surfaces
hermes desktop                 # launch the native desktop app (alias: hermes gui)
hermes dashboard               # web admin panel + embedded chat
hermes proxy                   # OpenAI-compatible local proxy backed by your OAuth provider
```

## Key Paths

```
~/.hermes/config.yaml       Main configuration (settings — never secrets)
~/.hermes/.env              API keys and secrets ONLY (under $HERMES_HOME if set)
$HERMES_HOME/skills/        Installed skills
~/.hermes/skins/            Custom themes (see references/themes.md)
~/.hermes/desktop-plugins/  Desktop app UI plugins (see references/desktop-plugins.md)
~/.hermes/tui-widgets/      TUI widget apps (see references/tui-widgets.md)
~/.hermes/pets/             Installed pet mascots (see references/petdex.md)
~/.hermes/state.db          Canonical session store (SQLite + FTS5)
~/.hermes/sessions/         Gateway routing index, request dumps, *.jsonl transcripts
~/.hermes/logs/             Gateway and error logs
~/.hermes/auth.json         OAuth tokens and credential pools
~/.hermes/hermes-agent/     Source code (if git-installed)
```

Profiles use `~/.hermes/profiles/<name>/` with the same layout. When a profile is active, resolve the real home from `$HERMES_HOME` — never hardcode `~/.hermes`.

## Routing Table — load the reference for the task

| User wants... | Load |
|---|---|
| **Anything not listed below — "can Hermes do X?", "how do I set up X?"** | **https://hermes-agent.nousresearch.com/docs/llms.txt** |
| Bots that chat, run routines, or message each other; the Bots tab | docs: `/user-guide/bot-mode` |
| CLI commands, subcommands, flags, "how do I run X" | `references/cli-reference.md` |
| In-session slash commands | `references/slash-commands.md` |
| Provider setup, API keys, OAuth, quota/pool failover | `references/providers-and-models.md` |
| config.yaml sections, toolsets, voice/STT/TTS | `references/configuration.md` |
| AGENTS.md / .hermes.md / CLAUDE.md project rules | `references/project-context-files.md` |
| Secret redaction, PII, approval modes, "reset permissions" | `references/security-privacy.md` |
| Delegation, cron, curator, kanban | `references/background-systems.md` |
| MCP servers (add, catalog, `hermes mcp`) | `references/native-mcp.md` |
| Webhook routes and event-driven runs | `references/webhooks.md` |
| A custom theme/skin ("synthwave theme", "change the gold ●") | `references/themes.md` + `templates/skin.yaml` |
| A desktop app UI element (pane, widget, ⌘K command, page) | `references/desktop-plugins.md` + `templates/plugin.js` |
| A live TUI panel or modal widget (ticker, clock, dashboard) | `references/tui-widgets.md` + `templates/clock.mjs` |
| Pet mascots — install, select, scale, diagnose | `references/petdex.md` |
| Windows-specific issues (keybinds, WinError 10106, BOM) | `references/windows-quirks.md` |
| Missing/deleted conversations or recovery from session snapshots | `references/troubleshooting.md` + `references/cli-reference.md` |
| Recover an accidentally deleted conversation | Load `hermes-session-recovery` |
| Debugging: voice, tools missing, gateway, aux models | `references/troubleshooting.md` |
| Contributing code: adding tools, slash commands, tests | `references/contributor-guide.md` |
| delegate_task "capped at N" reports | `references/delegate-task-concurrency-diagnosis.md` |
| "Can app X use my Nous Portal subscription/OAuth?" | `references/portal-auth-for-third-party-apps.md` |
| Connecting a messaging platform (Telegram, Discord, Slack, WhatsApp, …) | docs: `/user-guide/messaging` |

The reference list above is not the feature list — it is the set of topics that
need more than their docs page. For everything else Hermes ships, fetch
`llms.txt` and it maps the question to the page that answers it.

Two theming rules that hold even without loading the reference: **you apply skins yourself** (`hermes config set display.skin <name>` — every surface repaints live within ~a second; don't tell the user to run `/skin`), and **to tweak one color, edit the ACTIVE skin** (`hermes skin set <key> <hex>`) — never fork `default`, which drops the palette and resets the background.

## Spawning Additional Hermes Instances

Run additional Hermes processes as fully independent subprocesses — separate sessions, tools, and environments.

### When to Use This vs delegate_task

| | `delegate_task` | Spawning `hermes` process |
|-|-----------------|--------------------------|
| Isolation | Separate conversation, shared process | Fully independent process |
| Duration | Minutes (bounded by parent loop) | Hours/days |
| Tool access | Subset of parent's tools | Full tool access |
| Interactive | No | Yes (PTY mode) |
| Use case | Quick parallel subtasks | Long autonomous missions |

### One-Shot Mode

```
terminal(command="hermes chat -q 'Research GRPO papers and write summary to ~/research/grpo.md'", timeout=300)

# Background for long tasks:
terminal(command="hermes chat -q 'Set up CI/CD for ~/myapp'", background=true)
```

### Interactive PTY Mode (via tmux)

Hermes uses prompt_toolkit, which requires a real terminal. Use tmux for interactive spawning:

```
# Start
terminal(command="tmux new-session -d -s agent1 -x 120 -y 40 'hermes'", timeout=10)

# Wait for startup, then send a message
terminal(command="sleep 8 && tmux send-keys -t agent1 'Build a FastAPI auth service' Enter", timeout=15)

# Read output
terminal(command="sleep 20 && tmux capture-pane -t agent1 -p", timeout=5)

# Send follow-up
terminal(command="tmux send-keys -t agent1 'Add rate limiting middleware' Enter", timeout=5)

# Exit
terminal(command="tmux send-keys -t agent1 '/exit' Enter && sleep 2 && tmux kill-session -t agent1", timeout=10)
```

### Multi-Agent Coordination

```
# Agent A: backend
terminal(command="tmux new-session -d -s backend -x 120 -y 40 'hermes -w'", timeout=10)
terminal(command="sleep 8 && tmux send-keys -t backend 'Build REST API for user management' Enter", timeout=15)

# Agent B: frontend
terminal(command="tmux new-session -d -s frontend -x 120 -y 40 'hermes -w'", timeout=10)
terminal(command="sleep 8 && tmux send-keys -t frontend 'Build React dashboard for user management' Enter", timeout=15)

# Check progress, relay context between them
terminal(command="tmux capture-pane -t backend -p | tail -30", timeout=5)
terminal(command="tmux send-keys -t frontend 'Here is the API schema from the backend agent: ...' Enter", timeout=5)
```

### Session Resume

```
# Resume most recent session
terminal(command="tmux new-session -d -s resumed 'hermes --continue'", timeout=10)

# Resume specific session
terminal(command="tmux new-session -d -s resumed 'hermes --resume 20260225_143052_a1b2c3'", timeout=10)
```

### Tips

- **Close user-facing tool turns with a result** — consume the returned outcomes and give a concise, nonempty disposition: what they establish, what remains open and any action actually taken. Do not end a tool-driven user turn with a blank final or a generic request to resend recoverable work. Internal completion notices are not new user instructions: reconcile their original handles against retained receipts, and if a visible turn was started, close it with a brief result-consumed or unchanged-status message rather than replaying an earlier answer or relaunching its task.
- **Resume accepted work on continuity requests** — bind the requested predecessor using session lineage and repository/cwd, then recover its accepted objective, checkpoint, tracked owner and checklist from compact metadata before replaying history or rebuilding launch mechanics. Resolve ambiguous domain terms against the originating user report and session title before treating them as scheduling instructions or search symbols; a round-robin account-rotation defect is not a request to cycle through unrelated repositories. Treat a dirty-repository inventory or assistant-written checklist as provisional scope, not user acceptance. If it conflicts with the originating request, recover the exact user/task anchor with query-only `session_search` discovery followed by `session_id` + `around_message_id`, then correct the checklist before dispatch. For an all-work recovery, account for each requested workstream separately with its latest authority, owner, checkpoint and next missing obligation; recent-session results are an inventory, not permission to take over another live TUI's work. One repository's handoff is not the complete cross-session picture. Label missing workstreams unresolved rather than claiming full reconstruction. Do not treat an empty process-local checklist as an empty task when retained scope exists; reconcile it using `references/background-systems.md` without dropping unfinished requirements or inventing completion. Treat reboot and compression checkpoints as pauses within the accepted plan, not replacement plans: retain unfinished outcomes beyond the immediate restart/review step, because a shorter recovery checklist can silently erase the work the user expects continued. Perform one bounded ownership/source check per recovery decision, including the controlling session rather than only its subprocesses. If current bytes differ from the retained manifest, follow exact changed symbols or checkpoint paths to a successor before treating the difference as corruption or unowned work; a newer same-boot TUI may still be preparing the repair without a child PID. Preserve that parent's ownership and record an observer-only handoff instead of duplicating its writer, review or installation. Once the checkpoint matches and both worker and controlling-parent ownership are released, dispatch the first missing authorized stage rather than producing another readiness-only reply; repeated preparation can leave a task unstarted indefinitely. If its sole writer is active, preserve ownership and the asynchronous delivery contract instead of launching a duplicate. When that live result genuinely blocks parent acceptance, record the dependency and task handle in the owning checklist before yielding; polling or a readiness summary is not milestone advancement. Continue separately authorized independent work only when it does not conflict with that ownership, and clear the dependency after verifying the returned result.
- **Preserve explicit approval across interruptions** — check retained approval receipts and approved project decision records before raw-history retrieval or another approval question; verify that the project, action, actor and latest restrictions match. Bind an in-chat approval to the concrete pending question and save its exact scope before dispatch. A failed assistant reply or frontend interruption does not erase the user's answer; resume that approved work on a terse continuation instead of asking again. Record conditions such as prior independent acceptance separately from permission: a conditional approval is not spent execution admission, and parent-only provisioning permission does not transfer to a source/mock child. Clear a stale approval blocker once the answer is recovered, without expanding review approval into installation, activation, commit or publication authority.
- **Claude availability and failover** — honor the user's latest explicit executor exclusion before applying quota-reset or availability-retry policy; an exclusion is not permission to probe again when a timer expires. Otherwise load `claude-code` and follow its canonical **Automatic continuation on Claude exhaustion** procedure for quota classification, safe continuation and return to the permitted executor.
- **Do not infer provider recovery from continuation wording** — “use the current model until GPT is available” permits current-model work; it does not confirm a GPT reset. A reset estimate only makes one bounded permitted availability attempt eligible after that time. Do not mark a provider recovered from elapsed time alone or label an inherited local child as GPT; verify the constructed route and attributable result, preserve contradictory older metadata, and append a correction.
- **Record launch state from execution, not intent** — save `PREPARED` before launching; record `DISPATCHED` only after the launch returns a real delegation handle or tracked process identity, and `RUNNING` only from managed liveness. Leave unknown handles null rather than inventing placeholder IDs. A packet, timestamp or pinned route cannot prove a dispatch occurred, so preserve rejected or never-attempted launches as such. On reboot-prone hosts, retain the exact observed boot UUID and content-bound source/index baselines in private persistent evidence; never replace the boot value with an instruction to read it next time, because recovery needs both identities. Fsync the small approval/dispatch/checkpoint files plus containing directories before yielding; a tool-verified write is not a crash-durability guarantee. Follow `references/background-systems.md` for recovery without duplicate writers.
- **Scope reboot readiness to the owned task** — checkpoint owned work, name any surviving owned processes and disclose observed unrelated workloads without touching them. Say that the task is checkpointed rather than declaring the whole machine safe to reboot: an empty task process set does not establish host health, completion of another session or safety of interrupting a user build.
- **Choose delegation by enforced scope** — prefer native `delegate_task` for bounded subtasks, but verify that the current runtime can enforce any required read-only boundary. A read-only prompt or a toolset label is not proof that writes are unavailable. For a complete bounded text packet, reuse the qualified zero-tool review branch rather than constructing a filesystem reader or repeatedly rewriting launch/validation scripts. Regenerate candidate-specific roots, task, manifests and schema constants as data; retain the qualified runner when its runtime and enforcement contract are unchanged. Use `references/background-systems.md` for both restricted alternatives without changing shared approvals.
- **Distinguish reviewer configuration from useful execution** — verify the constructed provider, model, effort, tool names and fallback state before dispatch, then bind the terminal result to that runtime. Constructor metadata establishes the configured route, not provider acceptance, model generation, source reading or a completed review; claim those only from attributable response/progress evidence and a valid terminal verdict. Keep requested, configured and server-reported model identities separate; an absent or null `served_model` remains unreported, not silently filled from the requested model. In recorder code, preserve `result.get('served_model')` directly: `result.get('model')` may be a configured/requested alias and is not a substitute. Preserve a historical mislabeled record and append a provenance correction rather than rewriting it under an existing verdict. A parent model switch or dispatch label establishes neither execution nor acceptance.
- **Use `-w` (worktree mode)** when spawning agents that edit code — prevents git conflicts
- **Set timeouts** for one-shot mode — complex tasks can take 5-10 minutes
- **Use `hermes chat -q` for fire-and-forget** — no PTY needed
- **Use tmux for interactive sessions** — raw PTY mode has `\r` vs `\n` issues with prompt_toolkit
- **For scheduled tasks**, use the `cronjob` tool instead of spawning — handles delivery and retry
- **"delegate_task is capped at N" reports** — see `references/delegate-task-concurrency-diagnosis.md`. Three real cap paths in Hermes; if none fired, the model is self-limiting and rationalising it as "the runtime caps."
- **"Can $external_app use my Nous Portal subscription / OAuth?"** — see `references/portal-auth-for-third-party-apps.md`. Walk the user through three layers (plugin-vs-app, what Portal actually exposes, local-broker-proxy option).

## Surfaces (quick orientation)

- **Desktop app** (`hermes desktop` / `hermes gui`) — native Electron app for macOS/Linux/Windows: streaming chat, session list, Cmd+K palette, drag-and-drop files, native notifications, per-profile remote-gateway login. Extend it with UI plugins — `references/desktop-plugins.md`.
- **Web dashboard** (`hermes dashboard`) — full admin panel: messaging channels, MCP catalog, webhooks, memory, profile builder, plus an embedded `hermes --tui` chat. Secured behind an OAuth/token gate.
- **Ink TUI** (`hermes --tui` or `display.interface: tui`) — terminal UI with docked widget apps — `references/tui-widgets.md`.
- **OpenAI-compatible proxy** (`hermes proxy`) — a local OpenAI API backed by whichever OAuth provider you're signed into. Point Codex CLI, Aider, Cline, or any script at it — no API key.

## Hard Invariants (never violate, regardless of what you loaded)

- **Never break prompt caching** — don't change past context, toolsets, or the system prompt mid-conversation. The only exception is context compression.
- **Message role alternation** — never two assistant or two user messages in a row; only `tool` results can repeat.
- **Secrets in `.env`, settings in `config.yaml`** — never tell a user to put a non-credential setting in `.env`.
- **Profile-safe paths** — `get_hermes_home()` in code, `$HERMES_HOME` when resolving paths in a session.
- **Never hand-edit `config.yaml` for the user** — use `hermes config set KEY VAL`; a stray indent can corrupt the file and break the live gateway.
