---
name: codex
description: Delegate coding to OpenAI Codex CLI (features, PRs).
version: 1.0.1
author: Hermes Agent
license: MIT
platforms:
- linux
- macos
- windows
metadata:
  hermes:
    tags:
    - Coding-Agent
    - Codex
    - OpenAI
    - Code-Review
    - Refactoring
    related_skills:
    - claude-code
    - hermes-agent
x-local-maintainer: TyphooN (TyphooN-)
---


# Codex CLI

## Portable scope

This copy preserves a locally developed workflow, not transferable approval. Resolve the current task, repository, active Hermes profile, tools and ownership on this machine first. Historical project choices and TyphooN-specific executor/build policies are context, not permission to start services, run targets, modify security settings or publish. Project-root variables are documented in the collection's `PORTABILITY.md`; unset variables are not usable paths. Installing a skill installs no external tools or plugins.

Delegate coding tasks to [Codex](https://github.com/openai/codex) via the Hermes terminal. Codex is OpenAI's autonomous coding agent CLI.

## When to use

- Building features
- Refactoring
- PR reviews
- Batch issue fixing

Requires an installed, authenticated Codex CLI. For immutable non-Git evidence, use `exec --skip-git-repo-check`; do not initialize Git solely to run a review.

## Prerequisites

- Codex installed: `npm install -g @openai/codex`
- OpenAI auth configured: either `OPENAI_API_KEY` or Codex OAuth credentials
  from the Codex CLI login flow
- Check installed `codex exec --help`: modern CLI supports `--skip-git-repo-check` for non-Git evidence.
- Use a PTY for the interactive TUI. `codex exec` is non-interactive and supports piped stdin plus `--json`; a tracked wrapper can capture its streams without a child PTY.

For Hermes itself, `model.provider: openai-codex` uses Hermes-managed Codex
OAuth after `hermes auth add openai-codex`. The standalone CLI maintains its
own login; do not infer its identity or allowance from the supervisor's
credential pool, or infer missing auth from an absent `OPENAI_API_KEY`.

### Establish the route before a useful dispatch

1. Run `codex login status` and retain only the needed login-method metadata; do not print credential files or account identifiers. For this user's included route, confirm ChatGPT login and reject API-key/base-URL overrides rather than silently using billed inference.
2. Treat login status as authentication evidence, not allowance evidence. If this exact route's availability is unknown and it is already authorized, make one bounded useful-task attempt after the old owner is terminal. Do not copy a different route's quota/reset state or repeatedly probe an exhausted route.
3. Classify failure from the saved final event and actual exit before changing executors. Credit/quota exhaustion is a budget blocker, not permission to purchase credits, change credentials or weaken isolation. Preserve the source checkpoint and completion quorum, then continue through an available authorized executor; verify its actual model initialization and useful tool activity separately from feature completion.

## One-Shot Tasks

```
terminal(command="codex exec 'Add dark mode toggle to settings'", workdir="~/project", pty=true)
```

For disposable non-Git scratch work, choose an explicit workspace and keep the sandbox:
```
terminal(command="codex exec --skip-git-repo-check --sandbox workspace-write 'Build a snake game in Python'", workdir="/explicit/disposable/workspace", background=true, notify=true)
```

## Background Mode (Long Tasks)

```
# Start in background with PTY
terminal(command="codex exec --sandbox workspace-write 'Refactor the auth module'", workdir="~/project", background=true, pty=true)
# Returns session_id

# Monitor progress
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# Send input if Codex asks a question
process(action="submit", session_id="<id>", data="yes")

# Kill if needed
process(action="kill", session_id="<id>")
```

## Key Flags

| Flag | Effect |
|------|--------|
| `exec "prompt"` | One-shot execution, exits when done |
| `--sandbox workspace-write` (`-s`) | Selects writable filesystem scope; choose the approval policy separately and explicitly, such as `-a on-request` where supported. |
| `--dangerously-bypass-approvals-and-sandbox` | Disables both protections; never use as an automatic recovery shortcut or on the host checkout. |
| `--sandbox danger-full-access` | Removes Codex isolation; not a namespace-error workaround without explicit approval for the changed boundary. |

> **Deprecated:** `--full-auto` still works but the live CLI warns to use `--sandbox workspace-write` instead.

## Hermes Gateway Caveat

When invoking the Codex CLI from a Hermes gateway/service context (for example,
Telegram-driven agent sessions), Codex `workspace-write` sandboxing may fail even
when the same command works in the user's interactive shell. A typical symptom is
bubblewrap/user-namespace errors such as `setting up uid map: Permission denied`
or `loopback: Failed RTM_NEWADDR: Operation not permitted`.

In that context, preserve the exact sandbox initialization failure and stop the lane. Do not automatically switch to `danger-full-access`, bypass approvals, or change host permissions to get a task through. A weaker isolation route requires explicit agreement; directory names and a narrow prompt are not a sandbox.

For static acceptance, prefer `--sandbox read-only` with bytecode writes disabled. Validate the actual command exits and immutable input hashes; a model-authored review summary alone is not proof.

## PR Reviews

Clone to a temp directory for safe review:

```
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && gh pr checkout 42 && codex review --base origin/main", pty=true)
```

## Parallel Issue Fixing with Worktrees

```
# Create worktrees
terminal(command="git worktree add -b fix/issue-78 ~/.hermes/cache/scratch/issue-78 main", workdir="~/project")
terminal(command="git worktree add -b fix/issue-99 ~/.hermes/cache/scratch/issue-99 main", workdir="~/project")

# Launch Codex in each
terminal(command="codex --sandbox workspace-write exec 'Fix issue #78: <description>. Commit when done.'", workdir="~/.hermes/cache/scratch/issue-78", background=true, pty=true)
terminal(command="codex --sandbox workspace-write exec 'Fix issue #99: <description>. Commit when done.'", workdir="~/.hermes/cache/scratch/issue-99", background=true, pty=true)

# Monitor
process(action="list")

# After completion, push and create PRs
terminal(command="cd ~/.hermes/cache/scratch/issue-78 && git push -u origin fix/issue-78")
terminal(command="gh pr create --repo user/repo --head fix/issue-78 --title 'fix: ...' --body '...'")

# Cleanup
terminal(command="git worktree remove ~/.hermes/cache/scratch/issue-78", workdir="~/project")
```

## Batch PR Reviews

```
# Fetch all PR refs
terminal(command="git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'", workdir="~/project")

# Review multiple PRs in parallel
terminal(command="codex exec 'Review PR #86. git diff origin/main...origin/pr/86'", workdir="~/project", background=true, pty=true)
terminal(command="codex exec 'Review PR #87. git diff origin/main...origin/pr/87'", workdir="~/project", background=true, pty=true)

# Post results
terminal(command="gh pr comment 86 --body '<review>'", workdir="~/project")
```

## Tracked read-only acceptance

- After native reviewers repeatedly lose their owner before a verdict, preserve their partial artifacts and unknown termination, then use one tracked CLI review rather than repeating the same native dispatch. Record PID/PGID, boot ID, thread ID, transcript and exact exit; verify completion quorum before accepting.
- Distinguish the supervisor's persistent execute-code kernel from a competing checkout worker before launch. Exclude only the kernel PID emitted by the current tool, independently bound to its boot ID, start time and command-line hash; excluding all Python processes or trusting an idle state can hide a real writer.
- Apply the prerequisite route check to reviews as well as implementation. When supported, `--ignore-user-config` isolates per-invocation model/sandbox defaults while retaining auth; it is not a credential change. Do not ignore security rules or bypass hook trust.
- Pin a model and supported reasoning effort from maintained local CLI metadata; a cached model entry is capability evidence, not a completed invocation. Confirm a thread and useful command results from the JSON stream.
- Record requested and effective approval policy separately. A noninteractive exec turn can emit `never` despite root-level `on-request`; with the intended enforced sandbox intact, `never` denies prompting rather than granting it and is not a permission bypass. Preserve a verifier's overly strict equality failure, qualify the actual denial semantics, and do not weaken permissions or restart a useful lane solely to obtain the expected label.
- Validate runtime sandbox metadata using the exact canonical identifier emitted by the installed CLI: Codex 0.162.1 emits `sandbox_policy.type: "read-only"`, not `"read_only"`. A spelling-only controller mismatch is not a policy failure; stop/reap the owned lane, retain the failed evidence, recheck immutable inputs, and correct the parser once without changing sandbox or approval settings.
- Verify each resume against a newly emitted local turn context, not merely the last historical context in the reused session file. Preserve the pre-resume metadata snapshot and compare context count or invocation time before attesting model, effort and sandbox; an old matching context cannot prove that new resume flags took effect.
- When unified asynchronous command sessions return neither stdout nor exits, retain an INCOMPLETE/HOLD and confirm the old owner is terminal before testing a new lane. If installed feature metadata supports it, test `--disable unified_exec` per invocation while preserving the exact model/effort, included auth and read-only sandbox; require a tiny completed interpreter probe before continuing. A successful synchronous path is an execution-mode workaround, not proof of a kernel/root-cause fix. Never change global flags or weaken sandbox/approvals to recover output.
- For immutable evidence, combine `--sandbox read-only`, `--skip-git-repo-check`, `PYTHONDONTWRITEBYTECODE=1`, `--json`, and `--output-schema`/`--output-last-message`. The CLI/controller may save the final result in the private evidence directory while model-generated commands remain read-only. Preserve actual tool outputs and validate final claims against them.
- `--no-daemon`, when supported, isolates a tracked one-shot from the shared app-server daemon. Neither this flag nor a background handle proves survival across host reboot; preserve checkpoints and unknown exits honestly.
- If a host reboot follows an already saved successful final result, establish exit/result/hash/process quorum from the retained artifacts rather than resuming just to repeat the verdict. Keep earlier unknown-exit interruptions distinct from the successful later invocation.
- Preserve non-returning command attempts as incomplete rather than successful. After ownership is terminal, validate the unchanged inputs and test `codex -s read-only sandbox /usr/bin/printf ...` locally without a model call. If the native sandbox works but the unified executor still returns no command results, one per-invocation `-c 'features.unified_exec=false'` retry is a bounded compatibility option when installed feature metadata supports it; preserve read-only/model/provider/effort controls and do not change global permissions or bypass isolation. Judge recovery by completed command exits, not initialization alone.
- For strict Codex output schemas, omit `uniqueItems`: the Responses API rejects it before generation. Preserve the configuration error and check uniqueness/full file coverage in the parent validator instead; do not relabel a schema 400 as quota exhaustion.
- If kernel-blocked sandbox commands prevent source inspection, do not bypass the sandbox or infer a review from initialization. A source-only alternative within the same approved route can supply a hash-bound complete frozen text corpus directly, disable installed `shell_tool`, `unified_exec`, `shell_snapshot`, `code_mode_host`, agents and other unnecessary tools per invocation, and retain read-only/never approvals. Guard against any tool attempt, require literal manifest/source identities and complete coverage, and label this context-only source review: parent execution and binary-image metadata are not independent runtime or pixel review.
- Bind numeric PID/PGID checks to the recorded boot and process identity. After a reboot, match session/path/checkout markers instead of stale numbers; require worker-type AND lane association, not worker-type OR lane association, so unrelated Python/shell services cannot be mistaken for descendants.
- On credit/quota exhaustion of a tracked read-only review lane after partial discovery, preserve INCOMPLETE/HOLD and useful source-bound findings, confirm the old owner terminal, and re-verify source/mode/head/index bindings before an authorized successor. A controller-written checkpoint may document missing work but must never synthesize an independent terminal acceptance from partial discovery or substitute its own inspection for the required reviewer verdict.
- Start independent acceptance in a fresh session, never by copying a resume command from the investigator or another reviewed slice. Before launch, verify the subject path, schema path, output path, and fresh-versus-resume arguments; a copied runner is preparation, not a correct dispatch.
- After any external review lane (successful or exhausted), re-run full source binding + git head/index + mode preservation checks before accepting any verdict or advancing the plan. Controller may write handoff.json post-facto when CLI fails to emit it.
- Discover the retained session event shape before inferring missing execution. Codex 0.163 can record `custom_tool_call`/`custom_tool_call_output` and `event_msg/item_completed` containing `CommandExecution`, not only `function_call` or exec-named events. Bind intrinsic execution IDs, literal file-URI cwd, argv and exits to the CLI records; keep reviewer-local chunk labels separate. A parser yielding no calls despite completed CLI records is a format mismatch to investigate, not proof that checks never ran. Never inspect reasoning payloads to recover command metadata.
- Bind each final review check to actual completed JSON command records and exits. A reported shell body can differ from its CLI-emitted `/usr/bin/bash -lc` wrapper; compare the exact parsed body, retain the original full command, and label the representation rather than silently rewriting it. Count unit tests, in-memory adversarial controls and source anchors separately; aggregate outputs can be truncated and are not full execution logs.
- Bind actual working directories to local session `event_msg/item_completed/CommandExecution` metadata when available; retain the literal file URI and decode it explicitly. Controller `initial_cwd` and narrative event labels are not substitutes for the command's recorded cwd or intrinsic ID. Preserve swapped narrative labels as separate reporting qualifications without rewriting the original verdict.
- Parse proof receipts only from the specific completed commands known to emit them. Successful inspection output can contain code fragments or Python literals beginning with `{`; treating arbitrary diagnostic lines as JSON manufactures a verifier failure unrelated to the underlying proof.
- Keep author-local check labels distinct from intrinsic CLI event IDs. Derive an explicit crosswalk from emitted structured receipts or exact diagnostic markers, preserve unsuccessful discovery/harness attempts, and do not edit the original result to hide mismatches. Separate mutable controller-metadata hash snapshots from immutable analyzed sources; changing lane status is not source corruption. Constrain canonical model/effort fields with schema enums and place provenance qualifications in separate fields rather than decorating an identifier.

## Rules

1. **Use a PTY for interactive mode** — modern `codex exec` is non-interactive; use JSON streams and a tracked wrapper for bounded autonomous tasks.
2. **Preserve non-Git inputs** — use `exec --skip-git-repo-check` when supported; never initialize Git in an immutable project to satisfy an obsolete CLI assumption.
3. **Use `exec` for one-shots** — `codex exec "prompt"` runs and exits cleanly
4. **Select sandbox and approvals independently** — use `--sandbox workspace-write` for authorized builds and explicitly retain the intended approval policy; filesystem scope does not itself grant approval.
5. **Background for long tasks** — use `background=true` and monitor with `process` tool
6. **Don't interfere** — monitor with `poll`/`log`, be patient with long-running tasks
7. **Parallel is fine** — run multiple Codex processes at once for batch work
