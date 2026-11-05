---
name: claude-code
description: Delegate coding to Claude Code CLI (features, PRs).
version: 2.2.1
author: Hermes Agent + Teknium
license: MIT
platforms:
- linux
- macos
- windows
metadata:
  hermes:
    tags:
    - Coding-Agent
    - Claude
    - Anthropic
    - Code-Review
    - Refactoring
    - PTY
    - Automation
    related_skills:
    - codex
    - hermes-agent
    - opencode
x-local-maintainer: TyphooN (TyphooN-)
---


# Claude Code — Hermes Orchestration Guide

## Portable scope

This copy preserves a locally developed workflow, not transferable approval. Resolve the current task, repository, active Hermes profile, tools and ownership on this machine first. Historical project choices and TyphooN-specific executor/build policies are context, not permission to start services, run targets, modify security settings or publish. Project-root variables are documented in the collection's `PORTABILITY.md`; unset variables are not usable paths. Installing a skill installs no external tools or plugins.

Delegate coding tasks to [Claude Code](https://code.claude.com/docs/en/cli-reference) (Anthropic's autonomous coding agent CLI) via the Hermes terminal. Claude Code v2.x can read files, write code, run shell commands, spawn subagents, and manage git workflows autonomously.

## When to Use

Use for non-trivial repository implementation, focused build/test/debug loops, and independent code-review lanes routed through Claude Code. Keep Hermes on intent, ownership, approvals, process control, integration and reporting; use the recovery procedure below when the executor becomes unavailable. Load topical references only for the relevant launch, review or recovery step.

## TyphooN execution contract

Treat generic CLI examples below as syntax references, not this operator's model, budget or permission policy. For TyphooN repository lanes, explicitly use `--model opus --effort max` and set `ANTHROPIC_MODEL=opus`, `CLAUDE_CODE_EFFORT_LEVEL=max`, and `CLAUDE_CODE_SUBAGENT_MODEL=opus` on every launch/resume. If initialization omits effort, record `not emitted; max pinned in CLI/env` and report Max as pinned, not independently observed; reject an explicitly reported non-Max effort. Validate the emitted Opus family rather than hardcoding a previously observed Opus version, because the explicit `opus` alias can advance without violating the lane contract. Fail closed on non-Opus initialization; never use automatic selection or `--fallback-model`. Omit `--max-turns` by default so a bounded end-to-end task is not cut off mid-proof. Prefer `--permission-mode auto`; adapt once to `acceptEdits` if auto is unavailable, without host-checkout permission bypasses.

Resolve executor authorization before announcing a switch, probing availability, launching Claude or scheduling a reset-time return:

1. Treat an instruction to finish all remaining work without Claude as a task-level exclusion covering implementation, independent review and later quota resets until explicitly superseded.
2. Treat a reset announcement as availability information, not permission to lift that exclusion. Ask one focused routing question only if the new message leaves the choice genuinely ambiguous; never ask again after an explicit choice settles it.
3. Bind an explicit routing decision or answered clarification to its actual user message, then save that scoped approval before dispatch. Apply the change only to the named task or workflow: a task-specific exception neither authorizes other excluded tasks nor revokes their separate approvals. Update the current decision in its owning memory store instead of adding a competing preference; archive superseded replayable decisions when supported, preserve their historical content and frozen lane packets, and read back the effective decision. If a rejected patch returns a different current entry, reconcile that entry rather than overwriting it from stale context; leave compatible or concurrent decisions intact, because competing recalled instructions can reverse an authorized handoff. An optional memory-registration failure does not erase the in-chat answer: retain the local approval receipt and repair only its metadata, rather than re-asking or widening authorization.
4. Once Claude is permitted, recover the latest accepted objective and execution mode, establish prior ownership release, and launch the first missing admitted obligation. Choose implementation for an accepted repair, or a restricted reader for a named unresolved source contract or user-requested analysis; a reset is not a reason for another full audit. Explicitly override obsolete executor text in reused packets without widening their other approvals. Returning to Claude must not resurrect a superseded formal gate when the user selected diagnostics only.
5. Separate human authorization, architecture choices and technical acceptance before choosing that obligation. Reconcile an assistant-generated `approval_required` field or checklist blocker with the actual user authorization; model output cannot create a new human-permission boundary. Keep missing independent verdicts as gates on their dependent integration or activation, not automatic blockers on unfinished safe implementation. Respect a known semantic blocker that really needs that judgment. When an unresolved compatibility or security-policy choice exceeds settled intent, present one concrete decision after closing its named evidence gaps instead of chaining read-only assessments to postpone the choice.

Capture `claude auth status` with `subprocess.run([entry, 'auth', 'status'], capture_output=True, text=True, check=True)` and parse its JSON before returning output to the supervisor. Emit or retain only the route allowlist `loggedIn`, `authMethod`, `apiProvider`, and `subscriptionType`; raw status can include account and organization identifiers even when no token is shown. Require the included `claude.ai`/first-party route without printing the raw object or enabling paid/API fallback. Keep the reasoning-effort requirement separate from the subscription-tier label: Max effort does not mean `subscriptionType` must equal `max`; verify included authentication and the actual Opus/effort settings independently. Record model initialization and useful tool activity separately from actual verification completion. A print-mode session still enforces permissions; skipping interactive dialogs is not an unrestricted write grant.

For authorized commits, omit Claude coauthor trailers; this user does not want Claude listed as a commit coauthor.

## Automatic continuation on Claude exhaustion

- Exhaustion is not a stop request. The user explicitly expects autonomous continuation: recover state from session history, saved checkpoints, and the current filesystem, then execute the next useful permitted obligation in the same turn. Do not end a turn with a subscription countdown, a "wait for reset" note, or a re-ask for a goal the session already established. A terse `.` from the user means "continue from the saved checkpoint," not a new request.
- Classify subscription limits from the actual rate-limit status and terminal API result. A terminal envelope can report `subtype: success` while `is_error: true` and its result states a usage limit; that is a failed provider turn, not a completed review. Inspect the error flag, public result and rejection status together. `allowed_warning` is not a hard lockout; `overageStatus: rejected` with `overageEnabled: false` describes unavailable paid extra usage, not rejection of included usage. Inspect `rate_limit_info.unifiedWindows` when present and identify the applicable rejected interval together with the terminal error: an allowed `five_hour` window does not clear a rejected `seven_day` window. Preserve the binding limit type and its dated/timezoned reset rather than scheduling the shorter window's reset. Stop retries only when an actual limit is reached; never enable overage.
- Treat a confirmed Claude usage lockout as executor unavailability, not a stop request: continue the same accepted task automatically through Hermes's current user-selected driving model and tools, or another capable, already authorized executor. After ownership release, execute the first useful permitted source/test obligation in the resumed turn rather than ending with a subscription countdown or saving "wait for Claude" as the next action. Keep only genuinely provider-dependent acceptance steps open. This rule is model/provider-agnostic; do not require another "continue", a GPT-specific authorization, or the quota reset before doing useful permitted work.
- Establish the exhausted lane's completion quorum before transferring ownership; preserve its exact error/reset, session, base, dirty state, changed paths, source-bound proof and remaining-work ledger. A live descendant still owns its checkout.
- Recover the latest accepted task, including later scope changes and approvals, from the conversation and saved checkpoint when the user sends a terse continuation such as `.` or the frontend interrupts. Bind recovery to the current Hermes session and its explicitly assigned project before choosing work: generic “all remaining work” does not import other sessions' projects from recalled memory or shared evidence directories. Preserve explicit session-separation rulings through compaction and executor changes; an out-of-session checkpoint is a reference to hand off, not ownership or dispatch authority. Check the recorded owner first: a live useful lane keeps ownership; reconcile its existing completion signal instead of launching a duplicate. Read the compact continuation pointer, accepted checklist and source-bound handoff before searching history. After a reboot, read both the durable checklist projection and the live native todo list before a partial merge: an empty native list can replace the preserved full projection with only the patched items. If runtime state was lost, restore the complete accepted list in its single owning tool, retaining every unfinished obligation and exactly one active item. Reconcile each workstream's successor records and source-bound receipt frontier before choosing its candidate: an intact older snapshot can still be superseded. Bind the complete production, test and fixture generation, not just the latest changed files; overlaying a new fix onto an older GREEN tree can silently discard intervening accepted repairs. Establish lineage from declared parent/source relationships and matching hashes, not directory modification time or the largest test count; a later component lab can coexist with an unfinished review of a different candidate. Use the reconstruction and paired-receipt procedure in [Process and observer recovery](references/process-recovery.md) when retained trees disagree. Bind every resumed review to its own exact candidate and keep complementary component proof separate. Retain a fresh in-launch ownership guard, because another current-boot owner can start during preparation. Retrieve only an unresolved scope or approval question: use query-only `session_search` discovery, then an anchored `session_id` + `around_message_id` window. Do not combine a query with an unanchored session ID when seeking a narrow match, because that selects a whole-session read and can replay the current recovery's own tool output. Otherwise re-establish source bindings once, carry completed discovery and valid proof forward, and execute the first missing admitted obligation. Do not respond with a generic request to resend an already understood task, repeat a resolved approval question, repeatedly hash unchanged files, restart completed work or probe a locked account instead of doing available work.
- Preserve original scope, approvals, safety, billing and qualification boundaries during failover. Never silently switch the driving model, activate paid fallback, weaken permissions, downgrade a Claude lane below Opus-Max, or claim an incomplete review passed.
- Keep required independent review independent. Preserve a completed, source-bound judgment when its provider later becomes unavailable: a new quota limit changes executor availability, not the validity of an already verified verdict. Treat a terminal HOLD or BLOCK as a completed review with unresolved acceptance, not as a missing review to restart. Separate demonstrated code defects from omitted-source findings: assign the concrete regression/fix first and supply the missing dependency bodies without manufacturing unrelated source changes. Preserve the rejected candidate and verdict under their original fingerprints; green tests on revised source do not clear that gate before a new source-bound judgment. Re-review changed or invalidated scope, not an unchanged accepted checkpoint. Use an already approved, scope-enforced alternative for missing review when available; if a gate genuinely needs new approval or unavailable capability, keep that gate open while continuing other useful authorized work. A Claude quota alone is not a blanket project blocker.
- Apply the execution-routing rule above before an authorized return to included Opus-Max. First inspect any approved alternative's handle and result: a reset does not cancel its live review or invalidate its completed source-bound verdict. Preserve that review to terminal completion and consume a valid judgment without repeating it on Opus merely because capacity returned. Assign Opus only a genuinely distinct admitted obligation with separate ownership and no dependency on the unfinished judgment; do not create another lane merely to stay busy. Transfer ownership at a clean boundary, supersede the durable routing decision only when the user changes it, and carry that decision into the packet. Preserve frozen historical lane metadata instead of rewriting it or treating its obsolete route as current authority; a current executor decision and historical evidence serve different purposes. Retain the successor's verified progress and all independent static/runtime, preservation, billing and publication limits.

## Prerequisites

- **Resolve the CLI entry:** retain the PATH-selected executable or wrapper in the actual invocation and record its symlink chain separately. Do not substitute `Path(entry).resolve()` as the executable: version-manager and multicall shims can dispatch by invocation name. Use `terminal` to validate the selected entry with `claude --version` and minimal `claude auth status` before launch. Carry that exact observed entry into code-mode preparation as data: the orchestration kernel can have a different PATH and return `None` from `shutil.which('claude')`. Assert the checkpoint entry is a nonempty existing executable before dispatch; a null-entry `Popen` failure is an unlaunched configuration error, not a model/quota failure.
- If the selected version-manager shim stalls during metadata discovery, classify it as local launch plumbing rather than provider lockout. Establish the old probe's terminal state, resolve the exact previously selected installed executable without changing global configuration, and validate its version plus minimal included-auth metadata once before using that explicit entry for the lane. Record the bypassed shim and observed executable; never invoke the resolved multicall shim as if it were Claude, guess a replacement version, or change credentials/billing.
- When a permission probe is required, prove both an evidence-file write and a harmless command under the intended directory, model, effort and permission flags. After its non-error final result, observed exit and descendant quorum, resume that exact session with the real task; keep probe evidence separate from implementation and product verification. Do not repeat a still-applicable probe merely for a continuation. Use the [permission-probe handoff recipe](references/process-recovery.md#permission-probe-to-implementation-handoff) for the ordered checks.
- Bound timeout cleanup as well as the initial subprocess wait. A convenience `subprocess.run(timeout=...)` can block indefinitely while reaping an uninterruptible child after cancellation; use recorded process identity, bounded terminate/kill/reap stages and an explicit unreaped outcome before any successor.
- **Install:** `npm install -g @anthropic-ai/claude-code`
- **Auth:** run `claude` once to log in (browser OAuth for Pro/Max, or set `ANTHROPIC_API_KEY`)
- **Console auth:** `claude auth login --console` for API key billing
- **SSO auth:** `claude auth login --sso` for Enterprise
- **Check status:** `claude auth status` (JSON) or `claude auth status --text` (human-readable)
- **Health check:** `claude doctor` — checks auto-updater and installation health
- **Version check:** `claude --version` (requires v2.x+)
- **Update:** `claude update` or `claude upgrade`

## Two Orchestration Modes

Hermes interacts with Claude Code in two fundamentally different ways. Choose based on the task.

### Mode 1: Print Mode (`-p`) — Non-Interactive (PREFERRED for most tasks)

Use print mode for a bounded end-to-end task without a PTY. Finish task, wrapper and checkpoint preparation first, then launch the tracked wrapper with `terminal(command="<absolute-python> -I -B <evidence>/run_lane.py", workdir="<evidence>", background=true, notify=true)`. Persist the returned handle and reported wrapper PID before querying liveness or PGID. Treat `ProcessLookupError` during enrichment as a possible fast exit: record the unavailable observation and inspect saved child metadata, result and exit artifacts instead of aborting the observer. Retain the child PID/PGID, session and transcript paths from their own launch records; a wrapper disappearing does not determine whether its child completed. Launch the long-running wrapper with background=true and notify=true. A foreground timeout kills that wrapper and its Claude child together; an observer wait is not the review deadline. After a timeout, inspect the recorded PID and transcript before resuming. A LAUNCHING record whose PID is dead and whose transcript is empty is a failed start, not a live owner. Verify the startup model/tool boundary once, then use the armed completion notification as the wait mechanism. If a bounded wait returns with the process still running, do independent work or yield an explicitly RUNNING status rather than chaining waits or treating the observer limit as the executor's deadline. Reserve further metadata reads for a decision-changing progress check, a user-requested status, a suspected stall or completion reconciliation. Attribute lane-created edits against the captured initial working-tree preimages, including untracked files, not against HEAD: a large inherited diff can otherwise look like new progress while added tests disappear from the diffstat. Before handing a standalone verification wrapper to a live Claude writer, inspect its ownership guard: a guard that rejects every Claude process in the checkout will reject the authorized executor too. Use the source-bound recorder directly under the lane's serialized ownership, or adapt the guard once to admit the exact tracked owner; do not disable source-drift or unreaped-child checks. Keep this progress delta separate from the complete original-base diff required for final review.

Save the prepared task packet as a private UTF-8 file and feed it through stdin; keep model, effort and other compact control arguments in argv. This avoids both variadic-flag ambiguity and operating-system argument-size limits. The underlying invocation must retain the operator's model and effort settings:

```
ANTHROPIC_MODEL=opus CLAUDE_CODE_EFFORT_LEVEL=max CLAUDE_CODE_SUBAGENT_MODEL=opus \
  claude -p --name "$SLUG" --add-dir "$EVIDENCE_DIR" \
  --model opus --effort max --output-format stream-json --verbose \
  --permission-mode auto < "$TASK_FILE"
```

Create the private evidence directory and record the checkout checkpoint before launching. Label artifact roles in the task packet: task/checkpoint files are inputs, the live transcript is a diagnostic output sink, and the handoff is the required result. Instruct the executor not to read its own growing transcript or prompt-bearing runner/lane dumps for routine discovery; these can embed earlier transcript dumps and recursively consume context without advancing the task. When diagnosing a specific failure, have the supervisor extract only the relevant bounded events instead. For implementation, permit the tools needed for the complete edit/test loop; a `Read,Edit`-only task cannot exercise its own tests. When adapting a reader runner for a separately authorized implementation lane, audit its command and initialization guards together: remove reader-only tool restrictions, review-output schemas and old review-session resumption, then start a fresh implementation session. Preserve the subscription, Opus-Max, fallback, source and ownership guards; copying a reader wrapper must neither strand the executor without test tools nor turn the independent reviewer into its own fixer.

**When to use print mode:**
- One-shot coding tasks (fix a bug, add a feature, refactor)
- CI/CD automation and scripting
- Structured data extraction with `--json-schema`
- Piped input processing (`cat file | claude -p "analyze this"`)
- Any task where you don't need multi-turn conversation

**Print mode is non-interactive, not permission-free.** The permission layer can still deny an operation or require a configured handler. Where installed help supports `--permission-prompts none`, it means nobody answers prompts and prompting operations are denied; it does not authorize those operations. Classify a denial before adapting the task, rather than switching tools or actors to bypass it.

### Mode 2: Interactive PTY via tmux — Multi-Turn Sessions

Interactive mode gives you a full conversational REPL where you can send follow-up prompts, use slash commands, and watch Claude work in real time. **Requires tmux orchestration.**

```
# Start a tmux session
terminal(command="tmux new-session -d -s claude-work -x 140 -y 40")

# Launch Claude Code inside it
terminal(command="tmux send-keys -t claude-work 'cd /path/to/project && claude' Enter")

# Wait for startup, then send your task
# (after ~3-5 seconds for the welcome screen)
terminal(command="sleep 5 && tmux send-keys -t claude-work 'Refactor the auth module to use JWT tokens' Enter")

# Monitor progress by capturing the pane
terminal(command="sleep 15 && tmux capture-pane -t claude-work -p -S -50")

# Send follow-up tasks
terminal(command="tmux send-keys -t claude-work 'Now add unit tests for the new JWT code' Enter")

# Exit when done
terminal(command="tmux send-keys -t claude-work '/exit' Enter")
```

**When to use interactive mode:**
- Multi-turn iterative work (refactor → review → fix → test cycle)
- Tasks requiring human-in-the-loop decisions
- Exploratory coding sessions
- When you need to use Claude's slash commands (`/compact`, `/review`, `/model`)

## PTY Dialog Handling (CRITICAL for Interactive Mode)

Claude Code presents up to two confirmation dialogs on first launch. You MUST handle these via tmux send-keys:

### Dialog 1: Workspace Trust (first visit to a directory)
```
❯ 1. Yes, I trust this folder    ← DEFAULT (just press Enter)
  2. No, exit
```
**Handling:** First inspect the actual requested checkout and trust boundary. Accept only a specific authorized trust request; do not send Enter merely because the default selection looks convenient.

### Dialog 2: Individual Permission Prompts (normal flow)

Each tool use that needs approval (file write, shell command, network) shows a prompt. Answer that one prompt — this is different from disabling prompts for the whole run:
```
# Read the prompt before answering it
terminal(command="tmux capture-pane -t <session> -p -S -30")
# Allow this one action (Enter = default "Yes"); Esc declines it
terminal(command="tmux send-keys -t <session> Enter")
```
Never send a blind `Enter` on a timer to approve prompts you have not read — that is the bypass flag with extra steps.

A narrower opt-in than the full bypass is `--permission-mode acceptEdits`: file edits in the working directory are accepted, shell and other tool calls still prompt. Use it only in a dedicated worktree after reviewing the task.

### Dialog-aware handling pattern

Capture the actual prompt before answering it; a fixed sleep does not prove which dialog is displayed.

```
terminal(command="tmux capture-pane -t claude-work -p -S -30")
```

If the captured question is a specific authorized trust or per-operation request, answer that request once. Otherwise leave it unanswered and resolve the blocker. Never use a timed Enter sequence to handle startup or permission dialogs.

**Note:** After the first trust acceptance for a directory, the trust dialog won't appear again.

### Permission bypass boundary

Do not use `--dangerously-skip-permissions` or `bypassPermissions` on the host checkout. A throwaway Git worktree is not an operating-system sandbox: shell commands still reach the host, credentials and network. Prefer normal permission modes and explicitly scoped tools; isolated test fixtures must enforce their own filesystem, network and live-resource boundaries. Any exception requires the active authorization and actual isolation, not an automatic confirmation sequence.

## CLI Subcommands

| Subcommand | Purpose |
|------------|---------|
| `claude` | Start interactive REPL |
| `claude "query"` | Start REPL with initial prompt |
| `claude -p "query"` | Print mode (non-interactive, exits when done) |
| `cat file \| claude -p "query"` | Pipe content as stdin context |
| `claude -c` | Continue the most recent conversation in this directory |
| `claude -r "id"` | Resume a specific session by ID or name |
| `claude auth login` | Sign in (add `--console` for API billing, `--sso` for Enterprise) |
| `claude auth status` | Check login status (returns JSON; `--text` for human-readable) |
| `claude mcp add <name> -- <cmd>` | Add an MCP server |
| `claude mcp list` | List configured MCP servers |
| `claude mcp remove <name>` | Remove an MCP server |
| `claude agents` | List configured agents |
| `claude doctor` | Run health checks on installation and auto-updater |
| `claude update` / `claude upgrade` | Update Claude Code to latest version |
| `claude remote-control` | Start server to control Claude from claude.ai or mobile app |
| `claude install [target]` | Install native build (stable, latest, or specific version) |
| `claude setup-token` | Set up long-lived auth token (requires subscription) |
| `claude plugin` / `claude plugins` | Manage Claude Code plugins |
| `claude auto-mode` | Inspect auto mode classifier configuration |

## Print Mode Deep Dive

### Structured JSON Output
```
terminal(command="claude -p 'Analyze auth.py for security issues' --output-format json --max-turns 5", workdir="/project", timeout=120)
```

Returns a JSON object with:
```json
{
  "type": "result",
  "subtype": "success",
  "result": "The analysis text...",
  "session_id": "75e2167f-...",
  "num_turns": 3,
  "total_cost_usd": 0.0787,
  "duration_ms": 10276,
  "stop_reason": "end_turn",
  "terminal_reason": "completed",
  "usage": { "input_tokens": 5, "output_tokens": 603, ... },
  "modelUsage": { "claude-sonnet-4-6": { "costUSD": 0.078, "contextWindow": 200000 } }
}
```

**Interpret the result in order:** observed process exit, `is_error`, `terminal_reason`, available status/error fields, required output-schema and exact source-binding validation, then the actual judgment and required artifacts. For schema-backed reader reviews, consume `structured_output`: `terminal_reason: completed` may legitimately accompany `stop_reason: tool_use` when `StructuredOutput` is the final tool. Do not require `end_turn` or a model-written handoff file from a reader-only lane; require its complete structured judgment and parent completion/source-binding checks instead. Reject a malformed or mismatched report before treating its verdict as a completed source-bound judgment; successful execution and unchanged inputs do not validate the returned report. `subtype: success` can coexist with an API/authentication error and exit 1. A missing `api_error_status` does not establish quota exhaustion; classify the reported error rather than carrying an older lockout forward. Record `session_id` for resumption and distinguish initialization, useful tool activity, executed verification and a final acceptance verdict. A resumed CLI can emit an early empty `result` with `subtype: success`, zero turns and queued-result metadata while continuing useful tools; that envelope is not completion. Keep the lane active until the tracked process exit, descendant quorum and actual final judgment/handoff establish the terminal outcome. Keep per-request HTTP retries separate from lane attempts: exhausting retries on one later request does not mean the whole review was attempted that many times or never started. Preserve earlier useful activity as partial progress, not acceptance. Treat `total_cost_usd` and `costBasis: list` as reported usage-equivalent estimates, not proof that an included subscription was billed. Establish the effective auth/provider route separately; cost metadata neither proves a charge nor authorizes paid usage.

### Streaming JSON Output
For real-time token streaming, use `stream-json` with `--verbose`:
```
terminal(command="claude -p 'Write a summary' --output-format stream-json --verbose --include-partial-messages", timeout=60)
```

Returns newline-delimited JSON events. Filter with jq for live text:
```
claude -p "Explain X" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

Stream events include `system/api_retry` with `attempt`, `max_retries`, and `error` fields (e.g., `rate_limit`, `billing_error`).

### Bidirectional Streaming
For real-time input AND output streaming:
```
claude -p "task" --input-format stream-json --output-format stream-json --replay-user-messages
```
`--replay-user-messages` re-emits user messages on stdout for acknowledgment.

### Piped Input
```
# Pipe a file for analysis
terminal(command="cat src/auth.py | claude -p 'Review this code for bugs' --max-turns 1", timeout=60)

# Pipe multiple files
terminal(command="cat src/*.py | claude -p 'Find all TODO comments' --max-turns 1", timeout=60)

# Pipe command output
terminal(command="git diff HEAD~3 | claude -p 'Summarize these changes' --max-turns 1", timeout=60)
```

### JSON Schema for Structured Extraction
```
terminal(command="claude -p 'List all functions in src/' --output-format json --json-schema '{\"type\":\"object\",\"properties\":{\"functions\":{\"type\":\"array\",\"items\":{\"type\":\"string\"}}},\"required\":[\"functions\"]}' --max-turns 5", workdir="/project", timeout=90)
```

Parse `structured_output` from the JSON result. Claude validates output against the schema before returning.

### Session Continuation
```
# Start a task
terminal(command="claude -p 'Start refactoring the database layer' --output-format json --max-turns 10 > ~/.hermes/cache/scratch/session.json", workdir="/project", timeout=180)

# Resume with session ID
terminal(command="claude -p 'Continue and add connection pooling' --resume $(cat ~/.hermes/cache/scratch/session.json | python -c 'import json,sys; print(json.load(sys.stdin)[\"session_id\"])') --max-turns 5", workdir="/project", timeout=120)

# Or resume the most recent session in the same directory
terminal(command="claude -p 'What did you do last time?' --continue --max-turns 1", workdir="/project", timeout=30)

# Fork a session (new ID, keeps history)
terminal(command="claude -p 'Try a different approach' --resume <id> --fork-session --max-turns 10", workdir="/project", timeout=120)
```

### Bare Mode for CI/Scripting
```
terminal(command="claude --bare -p 'Run all tests and report failures' --allowedTools 'Read,Bash' --max-turns 10", workdir="/project", timeout=180)
```

`--bare` skips hooks, plugins, MCP discovery, and CLAUDE.md loading. Fastest startup. Requires `ANTHROPIC_API_KEY` (skips OAuth).

To selectively load context in bare mode:
| To load | Flag |
|---------|------|
| System prompt additions | `--append-system-prompt "text"` or `--append-system-prompt-file path` |
| Settings | `--settings <file-or-json>` |
| MCP servers | `--mcp-config <file-or-json>` |
| Custom agents | `--agents '<json>'` |

### Availability is not fallback authorization

Keep Opus-Max fail-closed; never add `--fallback-model` to recover an unavailable lane. Preserve the real error, source checkpoint and completion evidence. Transfer the task only through an already authorized executor route after the old owner is terminal; obtain explicit agreement for a different required independent-review route. Model initialization or a route change does not supply missing review acceptance.

Apply **Automatic continuation on Claude exhaustion** above for the failover procedure and this user's continuation preference; keep that workflow canonical rather than maintaining a second copy here. Classify API timeouts separately from hard quota limits. A required independent review still needs its own terminal verdict: transferring unfinished work does not transfer acceptance or authorize a different review route.

## Complete CLI Flags Reference

### Session & Environment
| Flag | Effect |
|------|--------|
| `-p, --print` | Non-interactive one-shot mode (exits when done) |
| `-c, --continue` | Resume most recent conversation in current directory |
| `-r, --resume <id>` | Resume specific session by ID or name (interactive picker if no ID) |
| `--fork-session` | When resuming, create new session ID instead of reusing original |
| `--session-id <uuid>` | Use a specific UUID for the conversation |
| `--no-session-persistence` | Don't save session to disk (print mode only) |
| `--add-dir <paths...>` | Grant Claude access to additional working directories |
| `-w, --worktree [name]` | Run in an isolated git worktree at `.claude/worktrees/<name>` |
| `--tmux` | Create a tmux session for the worktree (requires `--worktree`) |
| `--ide` | Auto-connect to a valid IDE on startup |
| `--chrome` / `--no-chrome` | Enable/disable Chrome browser integration for web testing |
| `--from-pr [number]` | Resume session linked to a specific GitHub PR |
| `--file <specs...>` | File resources to download at startup (format: `file_id:relative_path`) |

### Model & Performance
| Flag | Effect |
|------|--------|
| `--model <alias>` | Model selection: `sonnet`, `opus`, `haiku`, or full name like `claude-sonnet-4-6` |
| `--effort <level>` | Reasoning depth: `low`, `medium`, `high`, `xhigh`, `max` |
| `--max-turns <n>` | Limit agentic loops (print mode only; prevents runaway) |
| `--max-budget-usd <n>` | Cap API spend in dollars (print mode only) |
| `--fallback-model <model>` | Auto-fallback when default model is overloaded (print mode only) |
| `--betas <betas...>` | Beta headers to include in API requests (API key users only) |

### Permission & Safety
| Flag | Effect |
|------|--------|
| `--dangerously-skip-permissions` | Disables permission checks; prohibited on the host checkout. A Git worktree alone does not provide OS isolation. |
| `--allow-dangerously-skip-permissions` | Enable bypass as an *option* without enabling it by default |
| `--permission-mode <mode>` | Select a mode supported by installed `claude --help`; use `auto` for autonomous lanes or the permitted `acceptEdits` adaptation, not bypass modes. |
| `--allowedTools <tools...>` | Whitelist specific tools (comma or space-separated) |
| `--disallowedTools <tools...>` | Blacklist specific tools |
| `--tools <tools...>` | Override built-in tool set (`""` = none, `"default"` = all, or tool names) |

### Output & Input Format
| Flag | Effect |
|------|--------|
| `--output-format <fmt>` | `text` (default), `json` (single result object), `stream-json` (newline-delimited) |
| `--input-format <fmt>` | `text` (default) or `stream-json` (real-time streaming input) |
| `--json-schema <schema>` | Force structured JSON output matching a schema |
| `--verbose` | Full turn-by-turn output |
| `--include-partial-messages` | Include partial message chunks as they arrive (stream-json + print) |
| `--replay-user-messages` | Re-emit user messages on stdout (stream-json bidirectional) |

### System Prompt & Context
| Flag | Effect |
|------|--------|
| `--append-system-prompt <text>` | **Add** to the default system prompt (preserves built-in capabilities) |
| `--append-system-prompt-file <path>` | **Add** file contents to the default system prompt |
| `--system-prompt <text>` | **Replace** the entire system prompt (use --append instead usually) |
| `--system-prompt-file <path>` | **Replace** the system prompt with file contents |
| `--bare` | Skip hooks, plugins, MCP discovery, CLAUDE.md, OAuth (fastest startup) |
| `--agents '<json>'` | Define custom subagents dynamically as JSON |
| `--mcp-config <path>` | Load MCP servers from JSON file (repeatable) |
| `--strict-mcp-config` | Only use MCP servers from `--mcp-config`, ignoring all other MCP configs |
| `--settings <file-or-json>` | Load additional settings from a JSON file or inline JSON |
| `--setting-sources <sources>` | Comma-separated sources to load: `user`, `project`, `local` |
| `--plugin-dir <paths...>` | Load plugins from directories for this session only |
| `--disable-slash-commands` | Disable all skills/slash commands |

### Debugging
| Flag | Effect |
|------|--------|
| `-d, --debug [filter]` | Enable debug logging with optional category filter (e.g., `"api,hooks"`, `"!1p,!file"`) |
| `--debug-file <path>` | Write debug logs to file (implicitly enables debug mode) |

### Agent Teams
| Flag | Effect |
|------|--------|
| `--teammate-mode <mode>` | How agent teams display: `auto`, `in-process`, or `tmux` |
| `--brief` | Enable `SendUserMessage` tool for agent-to-user communication |

### Tool Name Syntax for --allowedTools / --disallowedTools
```
Read                    # All file reading
Edit                    # File editing (existing files)
Write                   # File creation (new files)
Bash                    # All shell commands
Bash(git *)             # Only git commands
Bash(git commit *)      # Only git commit commands
Bash(npm run lint:*)    # Pattern matching with wildcards
WebSearch               # Web search capability
WebFetch                # Web page fetching
mcp__<server>__<tool>   # Specific MCP tool
```

## Settings & Configuration

### Settings Hierarchy (highest to lowest priority)
1. **CLI flags** — override everything
2. **Local project:** `.claude/settings.local.json` (personal, gitignored)
3. **Project:** `.claude/settings.json` (shared, git-tracked)
4. **User:** `~/.claude/settings.json` (global)

### Permissions in Settings
```json
{
  "permissions": {
    "allow": ["Bash(npm run lint:*)", "WebSearch", "Read"],
    "ask": ["Write(*.ts)", "Bash(git push*)"],
    "deny": ["Read(.env)", "Bash(rm -rf *)"]
  }
}
```

### Memory Files (CLAUDE.md) Hierarchy
1. **Global:** `~/.claude/CLAUDE.md` — applies to all projects
2. **Project:** `./CLAUDE.md` — project-specific context (git-tracked)
3. **Local:** `.claude/CLAUDE.local.md` — personal project overrides (gitignored)

Use the `#` prefix in interactive mode to quickly add to memory: `# Always use 2-space indentation`.

## Interactive Session: Slash Commands

### Session & Context
| Command | Purpose |
|---------|---------|
| `/help` | Show all commands (including custom and MCP commands) |
| `/compact [focus]` | Compress context to save tokens; CLAUDE.md survives compaction. E.g., `/compact focus on auth logic` |
| `/clear` | Wipe conversation history for a fresh start |
| `/context` | Visualize context usage as a colored grid with optimization tips |
| `/cost` | View token usage with per-model and cache-hit breakdowns |
| `/resume` | Switch to or resume a different session |
| `/rewind` | Revert to a previous checkpoint in conversation or code |
| `/btw <question>` | Ask a side question without adding to context cost |
| `/status` | Show version, connectivity, and session info |
| `/todos` | List tracked action items from the conversation |
| `/exit` or `Ctrl+D` | End session |

### Development & Review
| Command | Purpose |
|---------|---------|
| `/review` | Request code review of current changes |
| `/security-review` | Perform security analysis of current changes |
| `/plan [description]` | Enter Plan mode with auto-start for task planning |
| `/loop [interval]` | Schedule recurring tasks within the session |
| `/batch` | Auto-create worktrees for large parallel changes (5-30 worktrees) |

### Configuration & Tools
| Command | Purpose |
|---------|---------|
| `/model [model]` | Switch models mid-session (use arrow keys to adjust effort) |
| `/effort [level]` | Set reasoning effort: `low`, `medium`, `high`, `xhigh`, or `max` |
| `/init` | Create a CLAUDE.md file for project memory |
| `/memory` | Open CLAUDE.md for editing |
| `/config` | Open interactive settings configuration |
| `/permissions` | View/update tool permissions |
| `/agents` | Manage specialized subagents |
| `/mcp` | Interactive UI to manage MCP servers |
| `/add-dir` | Add additional working directories (useful for monorepos) |
| `/usage` | Show plan limits and rate limit status |
| `/voice` | Enable push-to-talk voice mode (20 languages; hold Space to record, release to send) |
| `/release-notes` | Interactive picker for version release notes |

### Custom Slash Commands
Create `.claude/commands/<name>.md` (project-shared) or `~/.claude/commands/<name>.md` (personal):

```markdown
# .claude/commands/deploy.md
Run the deploy pipeline:
1. Run all tests
2. Build the Docker image
3. Push to registry
4. Update the $ARGUMENTS environment (default: staging)
```

Usage: `/deploy production` — `$ARGUMENTS` is replaced with the user's input.

### Skills (Natural Language Invocation)
Unlike slash commands (manually invoked), skills in `.claude/skills/` are markdown guides that Claude invokes automatically via natural language when the task matches:

```markdown
# .claude/skills/database-migration.md
When asked to create or modify database migrations:
1. Use Alembic for migration generation
2. Always create a rollback function
3. Test migrations against a local database copy
```

## Interactive Session: Keyboard Shortcuts

### General Controls
| Key | Action |
|-----|--------|
| `Ctrl+C` | Cancel current input or generation |
| `Ctrl+D` | Exit session |
| `Ctrl+R` | Reverse search command history |
| `Ctrl+B` | Background a running task |
| `Ctrl+V` | Paste image into conversation |
| `Ctrl+O` | Transcript mode — see Claude's thinking process |
| `Ctrl+G` or `Ctrl+X Ctrl+E` | Open prompt in external editor |
| `Esc Esc` | Rewind conversation or code state / summarize |

### Mode Toggles
| Key | Action |
|-----|--------|
| `Shift+Tab` | Cycle permission modes (Normal → Auto-Accept → Plan) |
| `Alt+P` | Switch model |
| `Alt+T` | Toggle thinking mode |
| `Alt+O` | Toggle Fast Mode |

### Multiline Input
| Key | Action |
|-----|--------|
| `\` + `Enter` | Quick newline |
| `Shift+Enter` | Newline (alternative) |
| `Ctrl+J` | Newline (alternative) |

### Input Prefixes
| Prefix | Action |
|--------|--------|
| `!` | Execute bash directly, bypassing AI (e.g., `!npm test`). Use `!` alone to toggle shell mode. |
| `@` | Reference files/directories with autocomplete (e.g., `@./src/api/`) |
| `#` | Quick add to CLAUDE.md memory (e.g., `# Use 2-space indentation`) |
| `/` | Slash commands |

### Pro Tip: "ultrathink"
Use the keyword "ultrathink" in your prompt for maximum reasoning effort on a specific turn. This triggers the deepest thinking mode regardless of the current `/effort` setting.

## PR Review Pattern

### Freeze an uncommitted candidate before independent review

1. Record BASE and HEAD even when equal, plus the complete tracked/untracked source overlay and its hashes; a commit range alone omits uncommitted implementations.
2. Materialize the reviewer checkout from the recorded base and a validated frozen archive, not by copying a live writer's files one by one; mixed generations can make a review unreproducible. Include the baseline, semantic diff and full added-file contents.
3. For a justified high-risk review alongside implementation, give the reviewer only the frozen candidate, explicit requirements, a distinct threat model and evidence-directory ownership. Keep it read-only on repository sources and require disposable reproductions to stay in its evidence directory; a worktree alone is not enforcement or a security sandbox.
4. Serialize workspace-wide verification with the implementation lane. Permit only noncontending standalone proofs during overlap, and record deferred real-crate commands as unexecuted rather than implying they passed.
5. Require a terminal reviewer verdict and exact reviewed hashes. Snapshot preparation and Opus initialization prove neither review completion nor acceptance; revalidate the reviewed paths against the final candidate before reusing the judgment.

### Quick Review (Print Mode)
```
terminal(command="cd /path/to/repo && git diff main...feature-branch | claude -p 'Review this diff for bugs, security issues, and style problems. Be thorough.' --max-turns 1", timeout=60)
```

### Deep Review (Interactive + Frozen Worktree)

Prepare and hash the frozen candidate using the preceding procedure before opening the interactive reviewer. Launch the explicitly pinned route:

```
terminal(command="tmux new-session -d -s review -x 140 -y 40")
terminal(command="tmux send-keys -t review 'cd /path/to/frozen-review && ANTHROPIC_MODEL=opus CLAUDE_CODE_EFFORT_LEVEL=max CLAUDE_CODE_SUBAGENT_MODEL=opus claude --model opus --effort max --permission-mode auto' Enter")
terminal(command="tmux capture-pane -t review -p -S -60")
```

Inspect the actual workspace-trust or operation prompt and authorize only that specific request when it is within scope; never send a timer-driven Enter. Once the ready prompt is observed, send a read-only task naming the recorded base, overlay manifest, requirements and evidence directory. Monitor with `tmux capture-pane`, and require the same terminal verdict/source bindings as print-mode review.

### PR Review from Number
```
terminal(command="claude -p 'Review this PR thoroughly' --from-pr 42 --max-turns 10", workdir="/path/to/repo", timeout=120)
```

### Claude Worktree with tmux
```
terminal(command="claude -w feature-x --tmux", workdir="/path/to/repo")
```
Creates an isolated git worktree at `.claude/worktrees/feature-x` AND a tmux session for it. Uses iTerm2 native panes when available; add `--tmux=classic` for traditional tmux.

## Parallel Claude Instances

Run multiple independent Claude tasks simultaneously:

```
# Task 1: Fix backend
terminal(command="tmux new-session -d -s task1 -x 140 -y 40 && tmux send-keys -t task1 'cd ~/project && claude -p \"Fix the auth bug in src/auth.py\" --allowedTools \"Read,Edit\" --max-turns 10' Enter")

# Task 2: Write tests
terminal(command="tmux new-session -d -s task2 -x 140 -y 40 && tmux send-keys -t task2 'cd ~/project && claude -p \"Write integration tests for the API endpoints\" --allowedTools \"Read,Write,Bash\" --max-turns 15' Enter")

# Task 3: Update docs
terminal(command="tmux new-session -d -s task3 -x 140 -y 40 && tmux send-keys -t task3 'cd ~/project && claude -p \"Update README.md with the new API endpoints\" --allowedTools \"Read,Edit\" --max-turns 5' Enter")

# Monitor all
terminal(command="sleep 30 && for s in task1 task2 task3; do echo '=== '$s' ==='; tmux capture-pane -t $s -p -S -5 2>/dev/null; done")
```

## CLAUDE.md — Project Context File

Claude Code auto-loads `CLAUDE.md` from the project root. Use it to persist project context:

```markdown
# Project: My API

## Architecture
- FastAPI backend with SQLAlchemy ORM
- PostgreSQL database, Redis cache
- pytest for testing with 90% coverage target

## Key Commands
- `make test` — run full test suite
- `make lint` — ruff + mypy
- `make dev` — start dev server on :8000

## Code Standards
- Type hints on all public functions
- Docstrings in Google style
- 2-space indentation for YAML, 4-space for Python
- No wildcard imports
```

**Be specific.** Instead of "Write good code", use "Use 2-space indentation for JS" or "Name test files with `.test.ts` suffix." Specific instructions save correction cycles.

### Rules Directory (Modular CLAUDE.md)
For projects with many rules, use the rules directory instead of one massive CLAUDE.md:
- **Project rules:** `.claude/rules/*.md` — team-shared, git-tracked
- **User rules:** `~/.claude/rules/*.md` — personal, global

Each `.md` file in the rules directory is loaded as additional context. This is cleaner than cramming everything into a single CLAUDE.md.

### Auto-Memory
Claude automatically stores learned project context in `~/.claude/projects/<project>/memory/`.
- **Limit:** 25KB or 200 lines per project
- This is separate from CLAUDE.md — it's Claude's own notes about the project, accumulated across sessions

## Custom Subagents

Define specialized agents in `.claude/agents/` (project), `~/.claude/agents/` (personal), or via `--agents` CLI flag (session):

### Agent Location Priority
1. `.claude/agents/` — project-level, team-shared
2. `--agents` CLI flag — session-specific, dynamic
3. `~/.claude/agents/` — user-level, personal

### Creating an Agent
```markdown
# .claude/agents/security-reviewer.md
---
name: security-reviewer
description: Security-focused code review
model: opus
tools: [Read, Bash]
---
You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication/authorization flaws
- Secrets in code
- Unsafe deserialization
```

Invoke via: `@security-reviewer review the auth module`

### Dynamic Agents via CLI
```
terminal(command="claude --agents '{\"reviewer\": {\"description\": \"Reviews code\", \"prompt\": \"You are a code reviewer focused on performance\"}}' -p 'Use @reviewer to check auth.py'", timeout=120)
```

Claude can orchestrate multiple agents: "Use @db-expert to optimize queries, then @security to audit the changes."

## Hooks — Automation on Events

Configure in `.claude/settings.json` (project) or `~/.claude/settings.json` (global):

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write(*.py)",
      "hooks": [{"type": "command", "command": "ruff check --fix $CLAUDE_FILE_PATHS"}]
    }],
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{"type": "command", "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -q 'rm -rf'; then echo 'Blocked!' && exit 2; fi"}]
    }],
    "Stop": [{
      "hooks": [{"type": "command", "command": "echo 'Claude finished a response' >> ~/.hermes/cache/scratch/claude-activity.log"}]
    }]
  }
}
```

### All 8 Hook Types
| Hook | When it fires | Common use |
|------|--------------|------------|
| `UserPromptSubmit` | Before Claude processes a user prompt | Input validation, logging |
| `PreToolUse` | Before tool execution | Security gates, block dangerous commands (exit 2 = block) |
| `PostToolUse` | After a tool finishes | Auto-format code, run linters |
| `Notification` | On permission requests or input waits | Desktop notifications, alerts |
| `Stop` | When Claude finishes a response | Completion logging, status updates |
| `SubagentStop` | When a subagent completes | Agent orchestration |
| `PreCompact` | Before context memory is cleared | Backup session transcripts |
| `SessionStart` | When a session begins | Load dev context (e.g., `git status`) |

### Hook Environment Variables
| Variable | Content |
|----------|---------|
| `CLAUDE_PROJECT_DIR` | Current project path |
| `CLAUDE_FILE_PATHS` | Files being modified |
| `CLAUDE_TOOL_INPUT` | Tool parameters as JSON |

### Security Hook Examples
```json
{
  "PreToolUse": [{
    "matcher": "Bash",
    "hooks": [{"type": "command", "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -qE 'rm -rf|git push.*--force|:(){ :|:& };:'; then echo 'Dangerous command blocked!' && exit 2; fi"}]
  }]
}
```

## MCP Integration

Add external tool servers for databases, APIs, and services:

```
# GitHub integration
terminal(command="claude mcp add -s user github -- npx @modelcontextprotocol/server-github", timeout=30)

# PostgreSQL queries
terminal(command="claude mcp add -s local postgres -- npx @anthropic-ai/server-postgres --connection-string postgresql://localhost/mydb", timeout=30)

# Puppeteer for web testing
terminal(command="claude mcp add puppeteer -- npx @anthropic-ai/server-puppeteer", timeout=30)
```

### MCP Scopes
| Flag | Scope | Storage |
|------|-------|---------|
| `-s user` | Global (all projects) | `~/.claude.json` |
| `-s local` | This project (personal) | `.claude/settings.local.json` (gitignored) |
| `-s project` | This project (team-shared) | `.claude/settings.json` (git-tracked) |

### MCP in Print/CI Mode
```
terminal(command="claude --bare -p 'Query database' --mcp-config mcp-servers.json --strict-mcp-config", timeout=60)
```
`--strict-mcp-config` ignores all MCP servers except those from `--mcp-config`.

Reference MCP resources in chat: `@github:issue://123`

### MCP Limits & Tuning
- **Tool descriptions:** 2KB cap per server for tool descriptions and server instructions
- **Result size:** Default capped; use `maxResultSizeChars` annotation to allow up to **500K** characters for large outputs
- **Output tokens:** `export MAX_MCP_OUTPUT_TOKENS=50000` — cap output from MCP servers to prevent context flooding
- **Transports:** `stdio` (local process), `http` (remote), `sse` (server-sent events)

## Monitoring Interactive Sessions

### Reading the TUI Status
```
# Periodic capture to check if Claude is still working or waiting for input
terminal(command="tmux capture-pane -t dev -p -S -10")
```

Look for these indicators:
- `❯` at bottom = waiting for your input (Claude is done or asking a question)
- `●` lines = Claude is actively using tools (reading, writing, running commands)
- `⏵⏵ bypass permissions on` = status bar showing permissions mode
- `◐ medium · /effort` = current effort level in status bar
- `ctrl+o to expand` = tool output was truncated (can be expanded interactively)

### Context Window Health
Use `/context` in interactive mode to see a colored grid of context usage. Key thresholds:
- **< 70%** — Normal operation, full precision
- **70-85%** — Precision starts dropping, consider `/compact`
- **> 85%** — Hallucination risk spikes significantly, use `/compact` or `/clear`

## Environment Variables

| Variable | Effect |
|----------|--------|
| `ANTHROPIC_API_KEY` | API key for authentication (alternative to OAuth) |
| `CLAUDE_CODE_EFFORT_LEVEL` | Default effort: `low`, `medium`, `high`, `max`, or `auto` |
| `MAX_THINKING_TOKENS` | Cap thinking tokens (set to `0` to disable thinking entirely) |
| `MAX_MCP_OUTPUT_TOKENS` | Cap output from MCP servers (default varies; set e.g., `50000`) |
| `CLAUDE_CODE_NO_FLICKER=1` | Enable alt-screen rendering to eliminate terminal flicker |
| `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` | Strip credentials from sub-processes for security |

## Efficiency and budget

1. Keep Opus at Max effort; conserve supervisor context through a compact task packet, bounded artifact reads and one coherent executor session, not model downgrades.
2. Omit arbitrary turn caps by default. Define a bounded objective and stop condition; preserve progress before lengthy verification so interruption does not force rediscovery.
3. Start recovery with the smallest admitted current-source/dependency check, using non-executing checks when runtime proof is held; changed external native inputs can make old integration proof irrelevant even when the task checkout is unchanged. Reuse proof whose source, commands, exits, producers and logs still bind, then give the executor only remaining obligations and compact status with artifact pointers. Inspect only the definitions, callers and invariants needed for the next coherent correction before editing; do not reread an unchanged corpus or every historical fixture, because discovery can exhaust a refreshed allowance before producing a source checkpoint. Reuse the inspected guarded runner and refresh its checkpoint inputs instead of rewriting launch plumbing for cosmetic changes, because preparation churn consumes the reset window without advancing the task. After launch, inspect lane metadata and a compact draft handoff before opening transcript contents. Distinguish initialization, source inspection, source edits, exercised checks and terminal acceptance; event counts alone establish none of the later stages. Require the first recovery checkpoint to include the first missing check's actual command/result, or a source-linked finding for a source-only reader, because another discovery-only restart can consume the recovered allowance without advancing implementation. Choose the next implementation slice around the first missing exercised obligation, not the whole backlog. When recovery has retained a failing current-source check, give its exact argv, failure location and log to the executor before broader feature work; preserve unchanged backend proof rather than rerunning it on every continuation. If that first check exposes a repairable prerequisite mismatch, make its bounded repair and discriminating regression the first deliverable, and save the patch plus draft handoff before investigating downstream features. Do not spend the recovered allowance auditing unrelated mechanisms while the known prerequisite still prevents their tests from running; discovery-only recoveries can consume the allowance without producing an artifact. Keep whole-checkout hash maps in private evidence rather than repeated supervisor output.
   Recover verification as explicit argv, cwd and required environment assignments from the producer receipt or maintained runner. Never reconstruct it by splitting shell text on `&&`, taking its last fragment, stripping `time`, or discarding a pipeline: those transformations can run a different command and return zero without exercising the intended tests. If only shell source survives, inspect its full control flow and record a newly reconstructed explicit invocation, not a replay of the original. Capture the producer's own return code before filtering its saved log; keep wrapper exit separate, because a successful wrapper can report a failed compiler or test. Require the intended testcase identities and a nonzero executed count for behavioral proof; label a successful `--no-run` invocation as compilation only.
   Supply the verified baseline testcase identity set and its source-bound receipt reference directly when paired proof is required. Do not make a recovered executor hunt through old JUnit/catalogs again; its first checkpoint should advance implementation rather than repeat a completed baseline audit.
4. For a bounded runtime-verification lane, require the first compact checkpoint to identify the actual preflight result and next maintained execution command before bespoke harness work. Exercise cheap metadata/parser/admission paths first, then reuse the existing serializer, transport, validators and execution primitives; constructing a second policy/provenance framework can exhaust refreshed usage without dispatching a case. Select the tool set for the task's real acceptance criteria. A source-only reader needs fewer tools than a reviewer required to execute an isolated discriminating proof.
5. Preserve session persistence when resumption may be needed. Start a fresh lane when the base or assumptions materially diverge, not merely because a notification arrived late.
6. Keep the included subscription route. Do not use `--bare` as an OAuth workaround or enable API/extra-usage billing; its different authentication requirements are not a free fallback.
7. Enforce source-only review with installed `--restricted` support, `--tools Read,Glob,Grep` and empty strict MCP configuration; verify initialization exposes only those readers and schema-only `StructuredOutput`. Give it a frozen candidate, separate inventories of implementation files and explicitly admitted review metadata, and an output contract it can fulfill without file writes. Use this same reader boundary for architectural synthesis or missing-evidence triage whenever edits and execution are outside scope, not only after failed fixes. For preservation-restricted inputs, launch from a private admitted snapshot rather than the original media directory. Carry accepted judgments forward unchanged and assign the first unresolved question; label new synthesis as an assessment or proposal, not renewed acceptance. Keep source judgments, reused tests and new execution distinct, require terminal completion and source bindings for the returned result, and obtain any required architecture decision before implementation. Use [Restricted source-only analysis and reviews](references/source-only-reviews.md) for snapshot assembly, launch, structured handoff, acceptance and architectural-reset procedures; reader restrictions are not an OS sandbox or a substitute for required dynamic verification.

## Pitfalls & Gotchas

### Supply restricted reader directories explicitly

Pass every explicitly admitted external helper/source/evidence directory through `--add-dir` before launch when using `--restricted`; enabling Bash does not expand the file tools' directory scope. On a missing-scope denial, preserve the error, classify it as configuration, and correct the narrow directory list once after completion quorum. Never retry the same denied file read through Bash or another spelling. Keep original inputs immutable and never broaden to credential stores or whole-host access.

### Keep task packets out of argv

Feed full task/source packets through stdin rather than expanding `TASK.md` into a positional argument. An operating system can limit each argument independently of the total command size, so correct quoting or a generous total argv budget does not make a large packet safe. In a Python launcher, open the prepared packet in binary mode and pass that file handle as `Popen(stdin=...)`; keep its byte hash in the checkpoint and retain normal stdout/stderr tracking. Do not rebuild an already validated packet merely to change its transport.

`--allowedTools`, `--disallowedTools`, `--tools`, `--add-dir`, and `--mcp-config` also accept multiple values. A compact positional task appended immediately after them can be parsed as another tool, directory, or MCP-config path. Put a compact task immediately after `-p` and before variadic flags, or use stdin. Classify argument-size or pre-initialization parse failures as local launch configuration, not provider/quota failures. Preserve the failed attempt, establish ownership release if a process started, and correct the transport once before retrying.

### Scope process guards to the owned lane

Filter process metadata by the owned checkout/worktree, tracked PID/PGID and exact session-id argv tokens before returning it to model context. Enumerate actual PGID equality and PPID descendants; never approximate group membership with a numerical PID range, because process-group members need not have nearby PIDs. On Linux, filter candidates using `/proc/PID/comm` and `stat` before reading task memory or resolving cwd. A host-wide `cmdline` walk can block the launcher itself in `__access_remote_vm`, even if its output is later filtered. Never read unrelated D-state cmdline/maps; inspect cwd only for scoped, resolvable candidates and preserve uncertain ownership rather than hanging or ignoring it. Print only relevant PID/PPID/PGID, comm, cwd, state, start ticks and progress counters; do not dump host-wide `ps ... args`, because unrelated build commands flood context and argv can contain secrets. Exclude the inspector and its known ancestors without blanket exemptions. Do not reject every `claude` process on the host: unrelated user lanes are not competing writers. Correct an overbroad guard rather than stopping unrelated work. When a primary-checkout guard encounters a persistent inference consumer or parent observer, do not equate its cwd or a path mentioned in argv with source-writing ownership. For independently authorized disjoint work, materialize an isolated checkout from the recorded immutable HEAD plus preserved dirty-file preimages, then verify the complete expected path/byte/mode/hash inventory before launch. Do not copy a changing writer's files one by one, because that can mix source generations. Preserve the isolated baseline-relative delta and integrate only after ownership release and source-bound proof. Never stop the consumer, broadly exempt all Python/server processes, or weaken host permissions to make a launcher pass.

Separate process identity from progress observations. Guard a generation with boot ID, PID/start ticks and the required executable/argv bindings; record scheduler state, CPU time and elapsed time separately. Do not compare entire process snapshots for identity equality, because an ordinary runnable/sleeping transition can falsely invalidate the same process. Still inspect zombie leaders and live threads for completion quorum; stable identity alone does not prove exit.

Classify a persistent parent execution kernel separately from a repository writer after an explicit parent-released checkpoint; cwd alone can falsely block a later scheduled lane. Exempt only the recorded PID plus command hash plus boot identity, keep the frozen-content preflight, and reject PID reuse or any unknown writer. Never blanket-exempt Python processes or infer ownership release from an empty work step.

Inspect `/proc/PID/task/*/stat` when a process leader is a zombie but its wrapper still waits: live uninterruptible threads can remain behind that zombie leader. A PID/PGID scan that excludes `Z` leaders can falsely declare the group dead. Follow the owned descendant tree as well as the original PGID, because tool shells can create separate process groups and retain the output pipe after a final API-error result. For justified cancellation, bind each target to its recorded generation and use Linux pidfds where available; preserve the provider error separately from the cancellation exit. After SIGKILL, bound the reap wait and preserve an unreaped/incomplete state rather than blocking forever or claiming completion. Kernel recovery, reboot and security-setting changes still require explicit approval. Use [Process and observer recovery](references/process-recovery.md) for the bounded probe, cancellation and ownership-transfer sequence.

Treat a frontend interruption banner, observer timeout or unavailable terminal process handle as an observer/control-plane event, not proof of worker exit, provider failure or revoked approval; a managed worker can continue after the caller stops. Derive completion filenames and fields from the retained runner/checkpoint rather than guessing `review.json` or a generic verdict filename, then inspect those artifacts and the recorded PID/PGID/session once. Preserve a live useful worker without relaunching it; consume a completed bound result instead of restarting discovery. Keep unknown exit status and termination cause unknown: callback counts and a missing final envelope cannot distinguish an interrupted request from failure while persisting a returned result. Confirm ownership release before resuming or replacing the relevant session.

When a user-systemd submission stops acknowledging, inspect the owned controller and `/proc` before another D-Bus request; a manager timeout is not a Claude timeout or exit. Do not repeat service launches against a blocked manager. Use the authorized tracked native CLI transport only after the previous queued start cannot produce another writer: establish prior-boot ownership release with no surviving restart, or preserve and fence the owned pending entry before provider/source actions, then confirm no process already loaded the unfenced entry. Preserve the original launcher, unknown exit and transfer evidence. If that exclusion cannot be proved, keep ownership unresolved rather than launching a duplicate. Never stop the shared manager, reboot, change permissions, or treat a transport fallback as an approval workaround. Use the actual observed tool hard cap rather than a requested timeout when selecting the runner. Keep a foreground control-plane wait comfortably below that cap; if the auxiliary observer times out, inspect the separately tracked Claude PID/PGID and exit artifacts rather than attributing the observer's timeout to the lane. A background command or saved handle is not proof that the job survives a TUI lifecycle boundary; for authorized delayed continuation, use a verified owned runtime unit and disclose reboot and local-delivery limits.

### Distinguish native error envelopes from model output

Apply the Opus guard to actual initialization and provider assistant output. Recognize the narrow API-error shape: `message.model: "<synthetic>"`, `is_api_error_message: true`, an error code, zero input/output tokens and text-only content. Preserve the real error/result and let the process emit its final result rather than treating this envelope as a model switch. Reject actual non-Opus generation, unmarked synthetic records and synthetic tool-use records. In stream-json, `is_api_error_message` and `error` belong to the outer assistant event; `model`, `usage` and `content` belong to its nested `message`. Require zero input/output tokens and text-only content for the narrow native-error exception. Test the guard with the actual saved error envelope and non-Opus/unsafe negatives before launch; a guard-triggered SIGTERM can otherwise obscure the real lockout classification. A wrapper's mistaken synthetic-envelope classification does not override a retained terminal `usage_limit_reached` result or authorize another provider attempt.

### Built-in refusal fallback is an explicit route change

Inspect `system/model_refusal_fallback` before admitting subsequent output, even when no `--fallback-model` was supplied. Both model names can contain `opus`, so an Opus-family-only guard cannot enforce the no-fallback boundary. Preserve the trigger, API refusal category/explanation, original/fallback model names and exact event; stop only the identity-verified owned lane, then establish completion quorum and revalidate its frozen inputs. Admit no fallback answer and keep a missing terminal verdict at HOLD.

Record provider availability, this task's refusal and review completion separately: successful included usage or `allowed_warning` can coexist with a refused task. Attribute a guard-issued SIGTERM and its exit to the controller, retaining the provider refusal as the initiating cause; do not relabel that termination as quota exhaustion, authentication failure, timeout or completed review. Report the task-local blocker without declaring Claude globally unavailable. Do not respond with obfuscated prompts, lower-model retries or permission changes. Require documented approval-preserving no-fallback behavior before reusing that lane. Label offline detector tests and a successful live guard stop as guard evidence, not a repaired provider route or an accepted review.

### Error-only startup sessions may not be resumable

Locate retained session files by their exact UUID under the recorded Claude projects directory rather than synthesizing the directory name from the checkout path: punctuation as well as slashes can be normalized. Check each lane's session independently: a durable supervisor transcript does not prove that Claude's own session file is nonempty or usable. Preserve a confirmed missing, zero-byte or malformed session artifact and start a fresh checkpoint-bound session instead of knowingly issuing an unusable `--resume`; retain the original attempt and any partial source findings without promoting them to acceptance. Resume compatible surviving sessions by their exact UUID. A guessed pathname miss alone is not proof that the conversation was lost.

Do not assume an emitted session UUID guarantees a persisted conversation. A startup OAuth-refresh collision can end before useful tool activity and leave no resumable session. Classify it as a transient authentication/runtime error, not quota exhaustion; preserve the packet and unchanged source checkpoint, establish completion quorum, and permit one ordinary CLI retry without changing credentials, security settings or billing. If `--resume` reports `No conversation found with session ID` before model initialization, record that as a local configuration/persistence failure and start a fresh session with the same bounded packet and checkpoint. That local refusal is not a second provider attempt. Stop repeated provider retries if the actual retry fails; continue authorized work through Hermes while keeping any unavailable independent-review gate open.

### Reset-time subscription activation

Schedule the provider's latest reported reset, not an assumed five-hour cadence. Record its raw reset text, the UTC observation time and any relative delay. Do not turn a bare `HH:MM` into `retry_after_utc`: establish its date/timezone and convert with time tools first; otherwise retain the clock as unresolved instead of scheduling it as UTC. A real useful task attempt may report a newer reset; record the hard limit, session, exact exit, base, clean/dirty checkpoint and remaining group members, then stop probes until that reset. Never enable paid extra usage or API fallback.

Use the native scheduler only when its ticker is observed alive. If an explicitly authorized one-shot requires an owned user timer instead, verify the unit parser, enabled/active state, exact next-elapse timestamp, timezone and catch-up policy after activation. A JSON preparation file, successful `systemd-run`, or asserted timer name is not proof a schedule exists or a Claude task started. Keep controller and child service names distinct, launch the long lane in its own service, and avoid combining `git worktree add --detach` with `-b`.

Use an explicit interpreter in a Python service's `ExecStart` when the script is a non-executable evidence artifact; enabling a unit does not prove it ran. Read back `ExecMainStatus`/`Result` and classify status 203/EXEC as a launch/configuration failure, not a provider error. Cancel and remove only verified lane-owned schedules when the user changes the review route, retaining their evidence copies.

Require a parent-released checkpoint before switching a checkout from Hermes to Claude. Do not infer ownership release from a child handoff, PID absence, or a timer firing. Test overlap refusal, idempotence and fail-closed preflight without making provider calls. After the task starts, distinguish process/init from useful Opus output and from completed verified work.

Preserve a one-shot reset receipt that skipped on active ownership; do not erase its idempotence marker or pretend it launched useful work. After the parent confirms the previous owner is terminal, launch a fresh uniquely identified recovery lane with the current verified checkpoint and record the skipped occurrence separately.

Recover artifact state after a native implementation or review worker fails before dispatching a successor. A failed child may have saved source edits, reports, regression specifications and useful logs; verify them against their pinned inputs, but never turn partial output or a missing terminal verdict into acceptance. Inventory the exact owned files with raw `git status --porcelain=v1 -uall` and bounded hashes, then compare them with the newest coherent source-bound receipt set: a stale DRAFT/WORKING handoff can predate substantial edits and is not the complete source-state ledger. Attribute each check to its actual producing lane, not a filename such as `verified-*`; parent hash validation establishes preservation of saved proof, not parent test execution or independent review. Validate receipt fields against their actual schema: unittest receipts can store `errors`, `failures` and `skipped` as arrays, so test emptiness rather than assuming numeric zero. Inspect unfamiliar artifacts' keys and field types first, then print only a whitelisted control-plane summary: status, candidate identity, commands/exits, test counts, artifact paths and next gate. Validate large source maps, testcase inventories and logs in code and retain them as artifacts; a small per-file byte limit or truncation does not bound a batch of full JSON dumps. Derive counts from the producer's actual schema: a missing collection key means unknown or schema mismatch, not an empty collection. Claim a new execution only when its own command, exit and log were actually recorded.

Preserve matching partial code and partition the recovery packet into implemented work with reusable proof, remaining admitted implementation, and parent-owned acceptance/live-action gates. Label untested partial edits, especially schema changes, explicitly provisional; give the successor the known failing testcase and first verification command rather than treating the checkpoint as an accepted design. Assign only unfinished obligations; an implemented helper with stale documentation needs finalization, not another implementation pass.

For a partially edited recovery, bind the new runner's initial-source map and required candidate fingerprint to the actual current tree, not the earlier accepted baseline. Retain the accepted baseline and its proof under separately named identities; a post-GREEN edit is provisional until current proof covers it. Validate every required state field before launching so a missing fingerprint or stale map remains an unlaunched configuration failure, not another provider attempt. Preserve the exact original session UUID for `--resume`; put recovery labels in the lane/session name, never append them to the UUID.

Explicitly supersede stale checkout, evidence, session and initial-dirty-state references when reusing an earlier task contract, while preserving its safety and approval boundaries; the old packet can otherwise misassign new task-owned files or send outputs to a predecessor's directory. Name the complete inherited owned delta, including untracked files, and keep unrelated dirty paths user-owned.

Correct stale RUNNING ownership records only after ownership release is established, retain unknown exits as unknown, preserve predecessor evidence and give the successor compact checkpoint pointers rather than an exhaustive rediscovery assignment.

Handle delayed completion notifications by the recorded attempt/session identity. If that attempt's exit, descendant scan and result have already been reconciled, acknowledge the late notice without resuming it, relaunching discovery or disturbing its replacement; a notification can arrive after ownership has transferred.

### Private graphical tests can affect shared desktop sockets

Treat a claimed isolated display as unproved until socket/lock ownership is checked. `Xvfb -displayfd` can allocate the desktop's display number and unlink its filesystem-only Xwayland socket. Require explicit unused high displays and peer/lock PID checks, not just a different DISPLAY value. When a worker reports a shared-resource side effect or denied repair, inspect the exact live target, pause or stop only the verified owned lane if needed, and request explicit approval before repair; do not change actors to bypass the denial. Record an already exited worker as exited rather than claiming it was paused. Verify any approved pathname repair by reading the exact inode/owner/peer back and exercising a read-only client without desktop restart or input.

### Empty MCP isolation config

For an invocation that intentionally disables unrelated MCP servers, use `--strict-mcp-config --mcp-config '{"mcpServers":{}}'`. A bare `{}` fails CLI schema validation before provider initialization (`mcpServers: expected record, received undefined`); classify it as configuration failure, preserve the failed attempt, confirm completion quorum, and correct the invocation rather than interpreting it as quota lockout.

### Preserve checkpoint and handoff identities

Finalize artifact contents and private permissions before recording mode-inclusive bindings, including references in parent acceptance/handoff indexes. Use this order: write the referenced artifact, set its final permissions, compute its path/byte-length/mode/SHA256 reference, publish the parent index, then verify every declared reference against final disk state. A later chmod changes the bound identity even when the byte hash is unchanged.

If only an unfrozen parent-owned index is stale and the original reviewer/source bindings remain valid, repair that index and recheck its complete catalog rather than rerunning inference or rewriting the reviewer verdict. Preserve frozen preimages. If preparation instead caused a prelaunch mismatch, preserve the failed startup, prove source/HEAD/index/content unchanged, and refresh only those known preparation-file identities once; never relax the guard. Fsync repaired checkpoints and their containing directory when reboot durability is required.

Capture `git status --porcelain=v1` directly into a private artifact or JSON-encode its stdout before passing it through a terminal response. Terminal results can strip the first status line's leading space and the final newline, making an unchanged checkout fail an exact prelaunch comparison. Keep strict HEAD/status/hash guards. If capture trimming caused a refusal before provider initialization, prove the original raw status from a retained multi-command artifact matches current raw status and all source hashes still match, then correct the recorded capture once; do not weaken the guard or attribute this configuration failure to quota.

### Disposable code-mode state

Use the print-mode background-launch procedure above rather than shell `nohup`, `disown`, or `&`; keep preparation code separate from the long-running wrapper. The `execute_code` adapter exposes only foreground `terminal()`; prepare artifacts there, then launch via native `terminal(background=true, notify=true)`. Never use a short foreground timeout as a launch probe: it can terminate the wrapper and Claude before a result, leaving the child exit unknown. Construct a prefixed path as `Path(prefix + slug)` or `parent / slug`, never by adding two `Path` objects. If preparation fails before subprocess creation, fix the constructor once and verify process truth before retry; a prepared script is not a launched lane.

Keep authoritative lane/session/ownership/checkpoint metadata in private files, not only code-mode variables. An interruption or user interjection can reopen execution with a fresh interpreter; reconstruct from the recorded artifact and verify source/process truth before continuing, rather than restarting discovery or assuming that a missing variable released ownership.

Respect the task list's state owner during recovery: if `omh_todo advance` returns `state_kept` because native `todo_list` owns the plan, update the native list instead of repeating mirror writes. When context recovery leaves that native list empty but the accepted checklist survives in the preserved OMH projection or user handoff, restore the complete accepted list once with its existing IDs and evidence-backed states, then verify the mirror has exactly one active item. A restored checklist is still a declaration, not execution evidence.

Handle cancellation before child creation as well as during execution. A wrapper waiting on resource acquisition must terminate its own wait and close descriptors when no child exists; a handler that only forwards to a child can ignore SIGTERM indefinitely in that phase. Once a child exists, forward cancellation only to its owned group, persist the actual exit or unknown reaping state, and verify descendants before transferring ownership.

### Bound repository searches before traversing

Exclude weights, model trees, virtualenvs, vendored/upstream checkouts and evidence before traversal. Use Hermes `search_files` with explicit source paths; constrain Claude's native searches to explicit source directories or tracked files. Never run a root-wide recursive search and filter excluded paths afterward. Post-filtering only hides the output: the search already read large model files and can create heavy I/O during an ostensibly source-only lane. Include this boundary explicitly in recovery task packets when a checkout contains local weights.

Keep foreground observers below the tool's observed hard cap, not merely its advertised or requested timeout. A long observer timing out does not terminate or time out the separately tracked executor; inspect its PID/PGID, exit receipt and boot identity before any resume, and shorten subsequent observations.

### Hosts that reboot during a lane

On a requested reboot wrap-up, stop new dispatches and verification launches first, checkpoint or stop only owned workers at a safe boundary, and flush the complete accepted-work ledger plus owned source/evidence and checkpoint directories. Preserve every lane's proof, ownership, unresolved obligations and next action; do not replace a multi-task checkpoint with only the most recent task's summary. Report verified agent-work checkpointing, not whole-machine shutdown readiness, and leave unrelated builds and services untouched. On an explicit continuation, merge the latest per-lane state into a fresh parent-labelled continuation pointer, retain frozen predecessors, clear the human reboot deferral, and execute the first missing admitted obligation after checking boot and ownership.

For a recovered wave, read the current boot ID once and compare every lane's saved generation before querying its old terminal handle. Classify a mismatch as reboot interruption, not a source failure or quota lockout; stale `RUNNING` JSON is not a live-process observation. Record missing exits/results as unknown, verify candidate/evidence integrity and exclude any current-boot conflicting owner or scheduled restart before transferring ownership. Create fresh current-boot launch records without rewriting frozen predecessor metadata. Apply the session-persistence check separately to each lane, then launch only its unfinished admitted work. Keep the strict boot guard for the short preparation-to-launch interval; never repeatedly assert an old lane's boot ID while trying to recover valid source.

When a completed audit's volatile report is lost but its exact Claude session survives, recover only the public `Write` tool-use payloads for an explicit report-path allowlist from that session's project JSONL. Save them as parent-labelled recovered artifacts with their original session/path provenance; distinguish recovered report content from lost reproduction scripts, and revalidate source relevance instead of rerunning the whole audit or ingesting private reasoning.

A host reboot kills the lane; evidence on volatile storage such as a tmpfs-backed `/tmp` does not survive it. A process handle disappearing is not successful completion. A checkpoint path can survive as a zero-byte or truncated file: validate nonempty JSON and its source/schema bindings before reuse, preserve the damaged artifact, and record missing evidence/unknown exit rather than treating file presence as acceptance. Preserve a private checkpoint and transcript under the active Hermes home's `cache/verification/` when reboot instability is observed, and pass that directory with `--add-dir`. Record the boot ID, PID/PGID, session ID, source base, initial dirty paths, and exact owned outputs. Flush/fsync checkpoints and completed evidence before a reboot can erase unwritten data. Resolve required task/runner artifacts and verify they are nonempty before creating another lane checkpoint; sync newly written packets, wrappers and their parent directories, because a verified write alone is not reboot durability. Capture the boot/source checkpoint and activate its guarded runner in the same bounded control-plane invocation when practical, rather than leaving a long preparation gap. During observed reboot instability, fsync each complete transcript event (or an explicitly bounded durable batch), not just at normal process exit: flushing alone can leave a zero-byte JSONL after reboot even while fsynced lane metadata records activity. After reboot, verify no original descendants remain before resuming. Record a reboot-interrupted exit as unknown rather than inventing a status. Inspect lane-created build objects for zero-length outputs and regenerate only those proven disposable artifacts. Never clear shared build caches or touch the live libraries to repair an isolated lane.

1. **Interactive mode REQUIRES tmux** — Claude Code is a full TUI app. Using `pty=true` alone in Hermes terminal works but tmux gives you `capture-pane` for monitoring and `send-keys` for input, which is essential for orchestration.
2. **Do not automate a permission-bypass dialog** — reject timed Down/Enter recipes; inspect and authorize ordinary per-operation requests instead
3. **`--max-budget-usd` minimum is ~$0.05** — system prompt cache creation alone costs this much. Setting lower will error immediately.
4. **`--max-turns` is print-mode only** — ignored in interactive sessions.
5. **Resolve the project interpreter before verification** — pass its exact executable in subprocess argv and receipts, because a generic `python` name can select a different environment.
   Reuse the maintained test runner and its exact recorded argv before trying a generic unittest invocation, especially for source/mock fixtures with audit or entry-point tripwires. Running a test-definition module directly can exit zero without exercising tests. Python `-I` ignores `PYTHONPATH` and removes the working-directory import shortcut, so repeating `-I -m unittest module` with a new PYTHONPATH does not repair discovery. Plain discovery can also bypass required guards and cause misleading failures or real negative-control operations. Treat those as runner failures, not product proof; require an observed nonzero test count, expected guard accounting and the maintained receipt.
6. **Session resumption requires same directory** — `--continue` finds the most recent session for the current working directory.
7. **`--json-schema` needs enough `--max-turns`** — Claude must read files before producing structured output, which takes multiple turns. Omit a `$schema` meta-schema URI such as draft 2020-12: the CLI rejects that key before model initialization (`no schema with key or ref`). Use a self-contained object schema, classify the rejection as launch configuration, clear the dead lane record, and correct the schema once.
8. **Trust dialog only appears once per directory** — first-time only, then cached.
9. **Background tmux sessions persist** — always clean up with `tmux kill-session -t <name>` when done.
10. **Slash commands (like `/commit`) only work in interactive mode** — in `-p` mode, describe the task in natural language instead.
11. **`--bare` skips OAuth** — requires `ANTHROPIC_API_KEY` env var or an `apiKeyHelper` in settings.
12. **Context degradation is real** — AI output quality measurably degrades above 70% context window usage. Monitor with `/context` and proactively `/compact`.

## Rules for Hermes Agents

1. **Prefer print mode (`-p`) for single tasks** — cleaner, no dialog handling, structured output
2. **Use tmux for multi-turn interactive work** — the only reliable way to orchestrate the TUI
3. **Always set `workdir`** — keep Claude focused on the right project directory
4. **Omit arbitrary turn caps by default** — use a bounded task objective and preserve checkpoints rather than cutting off an edit/test/review loop
5. **Monitor tmux sessions** — use `tmux capture-pane -t <session> -p -S -50` to check progress
6. **Look for the `❯` prompt** — indicates Claude is waiting for input (done or asking a question)
7. **Clean up tmux sessions** — kill them when done to avoid resource leaks
8. **Report results to user** — after completion, summarize what Claude did and what changed
9. **Don't kill slow sessions** — Claude may be doing multi-step work; check progress instead
10. **Use `--allowedTools`** — restrict capabilities to what the task actually needs
