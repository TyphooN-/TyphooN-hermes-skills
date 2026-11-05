---
name: systematic-debugging
description: '4-phase root cause debugging: understand bugs before fixing.'
version: 1.1.0
author: Hermes Agent (adapted from obra/superpowers)
license: MIT
platforms:
- linux
- macos
- windows
metadata:
  hermes:
    tags:
    - debugging
    - troubleshooting
    - problem-solving
    - root-cause
    - investigation
    related_skills:
    - test-driven-development
    - subagent-driven-development
x-local-maintainer: TyphooN (TyphooN-)
---


# Systematic Debugging

## Portable scope

This copy preserves a locally developed workflow, not transferable approval. Resolve the current task, repository, active Hermes profile, tools and ownership on this machine first. Historical project choices and TyphooN-specific executor/build policies are context, not permission to start services, run targets, modify security settings or publish. Project-root variables are documented in the collection's `PORTABILITY.md`; unset variables are not usable paths. Installing a skill installs no external tools or plugins.

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## The Feedback Loop Rule

The feedback loop is the debugging work. Before reading code to build a theory, create or identify a **tight** command that can go red on the user's exact symptom and green when the bug is fixed. A tight loop is fast, deterministic, agent-runnable, and specific enough to catch this bug — not merely "doesn't crash".

When a clean repro is hard, spend disproportionate effort building the loop. Guessing without a red-capable loop is the failure mode this skill exists to prevent.

Verify that the command collects the intended nonempty test scope and retain the actual test child's exit/log; a wrong-directory run or a piped summary can report success while executing no relevant tests or masking a nonzero exit. Resolve required fixture/preimage paths before dispatch rather than guessing snapshot filenames. Distinguish setup, test-child and recorder failures: a missing preimage before subprocess creation is not a product RED, and a recorder error after a completed test does not replace the test's result. Use direct execution or a checked subprocess return code, then reconcile observed node identities. Label lexical checks as source-contract evidence, not a native/backend reproduction; they can expose missing source guards without exercising the runtime behavior.

Before diagnosing a test timeout as a product hang, inspect the maintained runner's default and the boundary it caps: a whole-file budget can include fresh-interpreter startup for every testcase. Keep assertion counts separate from file completion and the suite exit; zero failed assertions does not establish that a timed-out file finished. If a convenience recorder introduced a shorter cap than the project default, preserve that failure, confirm its process tree has ended, and rerun only the affected file under the maintained default with unchanged source and isolation. Retain valid passing-file proof separately. Do not extend a user-mandated deadline or relax per-test, network, filesystem or private-home guards to obtain green.

For process-global initialization failures, identify the failing test executable/PID and the first installer exception before interpreting later `Once`-poisoning panics. Cargo runs distinct test executables as separate processes; libtest functions within one executable normally share process-global state and may run on different threads. Do not attribute shared globals to different binaries without evidence of an in-process harness. A `Once` already serializes its closure, so investigate the actual competing installer or earlier panic rather than assuming concurrent callers install it twice. Do not add `#[ignore]` merely to obtain a green suite; a skip removes coverage and does not establish a repair.

For machine summaries of `node --test`, select a supported explicit reporter or recognize the observed format: spec output can use `ℹ tests` where TAP uses `# tests`. A summary-parser failure after successful child checks is a reporting failure; preserve the original exits/logs and repair the projection rather than rerunning tests or labeling source behavior failed.

For `runpy.run_path` fixture remapping, verify the loaded function's actual `__globals__` points to the fixture before invoking it; the returned namespace can be a different dictionary. Mutating only that returned copy can leave the verifier reading genuine completed evidence while the test edits unused synthetic copies, producing a false guard-failure diagnosis. Preserve the failed harness receipt, repair only the remap, and rerun the positive and discriminating negative controls.

For a negative guarantee such as no dispatch or no write, record attempted entrypoints with counters or fixture events and assert them outside the production exception handler. Do not rely only on a throwing sentinel: a broad catch can convert the forbidden attempt into the same expected error outcome, leaving a broken guard apparently green. Confirm the observation would detect a deliberate forbidden call before crediting the negative-path test.

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Someone wants it fixed NOW (systematic is faster than thrashing)

## The Four Phases

You MUST complete each phase before proceeding to the next.

---

## Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

### 1. Read Error Messages Carefully

- Don't skip past errors or warnings
- They often contain the exact solution
- Read stack traces completely
- Note line numbers, file paths, error codes

**Action:** Use `read_file` on the relevant source files. Use `search_files` to find the error string in the codebase.

### Docker completion versus runtime and reboot readiness

- When a restart succeeds but its verifier fails or the session is interrupted, inspect current service state and the persisted pre-operation baseline before repeating the restart. A verifier error is not proof that the state-changing command failed; unnecessary retries cause additional downtime.
- Compare like representations in verification: hash the newly inspected configuration with the same canonical serialization used for its stored digest. Comparing a configuration object directly with a hash string creates a false failure even when Docker preserved configuration.
- On continuation, inspect the persisted completion state and exact local image ID before launching another build. A source-bound, fully verified image needs its missing container/runtime proof, not another build or repeated discovery.
- Keep image completeness, runtime health, HTTP behavior and mount independence separate. For a required self-contained image, verify final source coverage/content hashes, start that exact image, read back empty mounts and the intended loopback binding, and exercise pages/assets and failure responses through HTTP.
- Do not equate `restart=unless-stopped` with immediate boot availability. Check Docker service and socket enablement separately: an enabled socket can leave the daemon waiting for the first Docker request. Report that boundary and the bounded start command rather than silently changing host boot/security configuration.
- Compare the complete serving-root file set and hashes with the intended public tree, for example by inspecting a `docker cp ... -` tar stream without extracting it to the host. Docker `COPY public/` overlays the base image and does not remove stock files such as Nginx's `50x.html`; remove only identified stock build-image files, then require exact coverage and protected-source-path HTTP checks.
- Verify cache policy on real error responses: Nginx `expires` does not apply to 4xx/5xx, so `expires -1` alone cannot establish no-cache/no-store for a custom 404. Keep error Cache-Control at server scope with an always-applied status map when appropriate, and test 200 assets, internal 404 redirects and 503 responses together; a location-level `add_header` can silently drop inherited CSP/security headers.

### Browser-managed requests versus form sends

- Do not infer form submission from a change in the browser's total request count: favicon and web-manifest/icon fetches may arrive after document load. Record method, exact target and body presence, and permit only fixed declared browser assets fetched by bodyless GET; never ignore arbitrary GET/image traffic. Observe JavaScript transport attempts before forwarding real calls so production catches cannot hide them, check prevented native submissions/navigation separately, and prove the guard detects deliberate synthetic loopback attempts outside the default-traffic measurement window.

### Dart/Flutter dependency-resolution pitfall

When Pub says an exact package version “doesn't match any versions,” verify publisher metadata and inspect verbose resolver output before changing SDK or dependency pins. A zero-byte cached `pubspec.yaml` can make a published version appear nonexistent. Inventory empty manifests in the affected hosted cache, preserve only confirmed damaged package directories in a private quarantine, and let Pub redownload with integrity verification. Do not wipe the whole cache or bypass hashes. Verify the original Flutter bootstrap and actual application build separately; successful dependency resolution alone is not build completion. Multiple truncated cache packages establish content damage, not its storage/kernel cause.

### Kernel-blocked test or probe safety

- Stop new reproductions when an owned test/probe stays in uninterruptible D-state with SIGKILL already pending. A shell timeout does not reclaim that task; repeating the test can accumulate unreapable processes rather than improve proof.
- Persist PID/PGID, start identity, command hash and deadline before waiting on a namespace probe; record partial evidence when `TimeoutExpired` occurs. A `subprocess.run` timeout kills only its direct child, so explicitly account for forked namespace-init descendants instead of treating the exception as process-group cleanup.
- Read owned PID/start identity, pending-signal masks and wait channels without signaling unrelated processes. Check whether PID 1, RCU workers or unrelated workloads share the blockage before attributing it to application code; D-state alone does not establish disk failure or a specific kernel bug.
- Preserve an infrastructure HOLD when setup blocks before application dispatch. Do not skip high-FD/concurrency checks, clear production caches or promote earlier fixture passes to completed acceptance.
- Bind kernel fault evidence to the current boot after recovery. Fresh BAD_PAGE/page-release errors in unrelated processes or kernel workers are a live host-integrity concern even when old D-state tasks have vanished. Decode taint from the primary kernel documentation: S is not proof of overclocking, and B can indicate hardware or a kernel bug. Do not use HardwareCorrupted=0, a fresh reboot, or quiet process listings as host clearance.
- Preserve source hashes and a private durable recovery ledger before requesting host recovery. Reboot, forced shutdown, sysrq, boot/kernel changes and shared-process termination need explicit approval; access-denied kernel logs are a diagnostic limit, not permission to change security settings. If `dmesg` is denied, try the already-permitted current-boot kernel journal without privilege escalation, validate its `_BOOT_ID`, and record the bounded query coverage. Keep unreadable marker counts null, not zero; a current-boot BAD_PAGE entry and D-state tasks preserve the host HOLD without identifying hardware versus kernel cause.

### Linux Flutter / plaintext keyring persistence

- Check secret readability, not just service availability or `Locked=false`; a GNOME collection and item can be present while that item's secret is unreadable.
- For Omarchy's textual default keyring, compare GLib whole-file parsing with `g_key_file_get_string` for the app-owned secret. GNOME Keyring's textual writer can use `g_key_file_set_value` while its reader uses `get_string`; nested JSON's escaped quotes then fail with key-file error 5 after reload. Reproduce with synthetic nested JSON and compare `set_value` versus `set_string` serialization before blaming SQLCipher or resetting an app.
- Keep keys, tokens, whole keyring files, and raw parser error messages out of tool output; parser messages can contain the entire secret. Report only structural flags/error codes and use private evidence with core dumps disabled for sensitive probes.
- Preserve a private checkpoint before remediation and require explicit approval for shared-keyring/password/security changes. Do not launch the live app if its error recovery deletes databases; encrypted SQLite error 26 alone does not establish corruption.
- Validate isolated keyring tests with short Unix-socket paths, a private D-Bus/HOME/XDG environment, and the actual Secret Service owner PID. Restarting only a launcher process is not a keyring-restart or reboot acceptance test.

### Privacy-preserving acquisition diagnosis

- Treat recovery/corruption language in a catch-all error as a hypothesis, not a diagnosis. Locate the earliest failing guard and exercise the smallest authorized metadata-only boundary before opening a database or invoking the full producer; a file-size or ownership refusal can occur before history is inspected.
- Preserve the original data, reviewed limits and live-operation boundaries. Never delete records, shrink a database, reset a journal or relax a guard merely to make a reader pass. Require separate authority for real database access, including read-only SQLite, which can interact with locks/WAL/SHM.
- Record only source-bound call locations, exception classes and reviewed constant messages; arbitrary exception payloads and frame locals can expose private data. Keep diagnostic guard failures separate from product failures.
- State the exact tested boundary. A synthetic metadata control that passes preflight proves neither SQLite acquisition nor recovery/publication, and the absence of another preflight error is a valid result rather than a reason to invent a downstream failure.

Use [Read-only preflight diagnosis](references/read-only-preflight-diagnosis.md) for the ordered probe, instrumentation controls and receipt shape.

### 2. Build a Tight Feedback Loop

- Can you trigger the user's exact symptom with one command?
- Does the command fail for this bug and only pass once the bug is fixed?
- Is it fast enough to run repeatedly?
- Is it deterministic? For flaky bugs, can you raise the reproduction rate high enough to debug?
- If not reproducible → gather more data, don't guess.

**Ways to construct a loop — try in roughly this order:**

1. **Failing test** at the seam that reaches the bug: unit, integration, or end-to-end.
2. **HTTP script / curl** against a running dev server.
3. **CLI invocation** with fixture input, diffing stdout/stderr against expected output.
4. **Headless browser script** (Playwright/Puppeteer) asserting on DOM, console, or network.
5. **Replay a captured trace**: HAR, request payload, event log, queue message, or webhook body.
6. **Throwaway harness** that boots the smallest useful slice of the system and calls the failing path.
7. **Property / fuzz loop** when the bug is intermittent wrong output over a broad input space.
8. **Bisection harness** suitable for `git bisect run` when the bug appeared between two known states.
9. **Differential loop** comparing old vs new version, two configs, two providers, or two datasets.
10. **Human-in-the-loop script** only as a last resort: script the human steps and capture their result so the loop stays structured.

**Tighten the loop once it exists:**

- Make it faster: cache setup, narrow scope, skip unrelated initialization.
- Make the signal sharper: assert the exact symptom, not generic success.
- Make it more deterministic: pin time, seed randomness, isolate filesystem, freeze network.

For non-deterministic bugs, the immediate goal is a higher reproduction rate, not perfection. Run the trigger 100x, parallelize, add stress, narrow timing windows, or inject sleeps. A 50% flake is debuggable; a 1% flake usually is not.

**Action:** Use the `terminal` tool to run the tight loop:

```bash
# Run a specific failing test
pytest tests/test_module.py::test_name -v

# Or run a scripted repro
python scripts/repro_bug.py

# Or run a high-repetition flaky repro
for i in {1..100}; do pytest tests/test_flake.py::test_name -q || break; done
```

### 3. Check Recent Changes

- What changed that could cause this?
- Git diff, recent commits
- New dependencies, config changes
- Reproduce the same failure on a source-pinned baseline under matching inputs/toolchain, or retain equivalent prior proof, before calling it pre-existing or environmental. A generic I/O error or an unrelated passing subset is not causal evidence; keep the attribution unresolved when the comparison is missing.

**Action:**

```bash
# Recent commits
git log --oneline -10

# Uncommitted changes
git diff

# Changes in specific file
git log -p --follow src/problematic_file.py | head -100
```

### 4. Gather Evidence in Multi-Component Systems

**WHEN system has multiple components (API → service → database, CI → build → deploy):**

**BEFORE proposing fixes, add diagnostic instrumentation:**

For EACH component boundary:
- Log what data enters the component
- Log what data exits the component
- Verify environment/config propagation
- Check state at each layer

Run once to gather evidence showing WHERE it breaks.
THEN analyze evidence to identify the failing component.
THEN investigate that specific component.

### 5. Trace Data Flow

**WHEN error is deep in the call stack:**

- Where does the bad value originate?
- What called this function with the bad value?
- Keep tracing upstream until you find the source
- Fix at the source, not at the symptom

**Action:** Use `search_files` to trace references:

```python
# Find where the function is called
search_files("function_name(", path="src/", file_glob="*.py")

# Find where the variable is set
search_files("variable_name\\s*=", path="src/", file_glob="*.py")
```

### Phase 1 Completion Checklist

- [ ] Error messages fully read and understood
- [ ] A tight loop command exists and has been run at least once
- [ ] Loop is red-capable: it asserts the user's exact symptom, not a nearby failure
- [ ] Loop is deterministic, or a flaky bug has a high enough reproduction rate to debug
- [ ] Recent changes identified and reviewed
- [ ] Evidence gathered (logs, state, data flow)
- [ ] Problem isolated to specific component/code
- [ ] Root cause hypotheses can be stated and tested

**STOP:** Do not proceed to Phase 2 until you understand WHY it's happening.

---

## Phase 2: Pattern Analysis

**Find the pattern before fixing:**

### 0. Minimize the Reproduction

Once the loop is red, shrink the repro to the smallest scenario that still goes red. Cut inputs, callers, config, data, and steps **one at a time**, re-running the loop after each cut. Keep only what is load-bearing for the failure.

Done when removing any remaining element makes the loop go green. A minimal repro narrows the hypothesis space and often becomes the cleanest regression test.

### 1. Find Working Examples

- Locate similar working code in the same codebase
- What works that's similar to what's broken?

**Action:** Use `search_files` to find comparable patterns:

```python
search_files("similar_pattern", path="src/", file_glob="*.py")
```

### 2. Compare Against References

- If implementing a pattern, read the reference implementation COMPLETELY
- Don't skim — read every line
- Understand the pattern fully before applying

### 3. Identify Differences

- What's different between working and broken?
- List every difference, however small
- Don't assume "that can't matter"

### 4. Understand Dependencies

- What other components does this need?
- What settings, config, environment?
- What assumptions does it make?

---

## Phase 3: Hypothesis and Testing

**Scientific method:**

### 1. Form Ranked Falsifiable Hypotheses

- When the cause is still unknown, generate a short ranked set of plausible hypotheses. When a current source-bound receipt already identifies a failing guard, test that concrete prediction first instead of inventing alternatives or repeating completed discovery.
- Rank unresolved hypotheses by likelihood and cheapness to falsify; reopen a retained diagnosis when current evidence contradicts its source or input assumptions.
- State the prediction each hypothesis makes: "If X is the cause, then changing or observing Y should make Z happen."
- Discard or sharpen any hypothesis that does not make a testable prediction.

If the user is present, show the ranked list before testing. They may have domain knowledge that instantly re-ranks it. If the user is AFK, proceed with your ranking.

### 2. Test Minimally

- Test the highest-ranked hypothesis with the smallest possible probe.
- Change one variable at a time.
- Don't fix multiple things at once.
- Prefer debugger/REPL inspection when available; one breakpoint beats ten logs.
- If you add logs, tag every temporary line with a unique prefix such as `[DEBUG-a4f2]` so cleanup is a single search.

### 3. Verify Before Continuing

- Did it work? → Phase 4
- Didn't work? → Form NEW hypothesis
- DON'T add more fixes on top

### 4. When You Don't Know

- Say "I don't understand X"
- Don't pretend to know
- Ask the user for help
- Research more

---

## Phase 4: Implementation

**Fix the root cause, not the symptom:**

### 1. Create Failing Test Case

- Simplest possible reproduction
- Automated test if possible
- MUST have before fixing
- Use the `test-driven-development` skill

### 2. Implement Single Fix

- Address the root cause identified
- ONE change at a time
- No "while I'm here" improvements
- No bundled refactoring

### 3. Verify Fix

```bash
# Run the specific regression test
pytest tests/test_module.py::test_regression -v

# Run full suite — no regressions
pytest tests/ -q
```

### 4. If Fix Doesn't Work — The Rule of Three

- **STOP.**
- Count: How many fixes have you tried?
- If < 3: Return to Phase 1, re-analyze with new information
- **If ≥ 3: STOP and question the architecture (step 5 below)**
- DON'T attempt Fix #4 without architectural discussion

### 5. If 3+ Fixes Failed: Question Architecture

**Pattern indicating an architectural problem:**
- Each fix reveals new shared state/coupling in a different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

**STOP and question fundamentals:**
- Is this pattern fundamentally sound?
- Are we "sticking with it through sheer inertia"?
- Should we refactor the architecture vs. continue fixing symptoms?

**Discuss with the user before attempting more fixes.**

This is NOT a failed hypothesis — this is a wrong architecture.

---

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals a new problem in a different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (Phase 4 step 5).

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question the pattern, don't fix again. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence, trace data flow | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare, identify differences | Know what's different |
| **3. Hypothesis** | Form theory, test minimally, one variable at a time | Confirmed or new hypothesis |
| **4. Implementation** | Create regression test, fix root cause, verify | Bug resolved, all tests pass |

## Hermes Agent Integration

### Investigation Tools

Use these Hermes tools during Phase 1:

- **`search_files`** — Find error strings, trace function calls, locate patterns
- **`read_file`** — Read source code with line numbers for precise analysis
- **`terminal`** — Run tests, check git history, reproduce bugs
- **`web_search`/`web_extract`** — Research error messages, library docs

### With delegate_task

For complex multi-component debugging, dispatch investigation subagents:

```python
delegate_task(tasks=[{
    "goal": "Investigate why [specific test/behavior] fails",
    "context": """
    Follow systematic-debugging skill:
    1. Read the error message carefully.
    2. Run the smallest authorized reproduction.
    3. Trace the data flow to find root cause.
    4. Report findings; do not fix yet.

    Error: [sanitized error]
    File: [path to failing code]
    Test command: [exact command and required isolation]
    Scope: [allowed actions, paths and stop condition]
    """
}])
# This assigns a task; it does not enforce read-only access or pin a provider.
# Use the approved restricted executor when those boundaries are required.
```

### With test-driven-development

When fixing bugs:
1. Write a test that reproduces the bug (RED)
2. Debug systematically to find root cause
3. Fix the root cause (GREEN)
4. The test proves the fix and prevents regression

## Real-World Impact

From debugging sessions:
- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common

**No shortcuts. No guessing. Systematic always wins.**
