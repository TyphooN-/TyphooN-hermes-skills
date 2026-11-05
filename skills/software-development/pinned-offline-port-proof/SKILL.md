---
name: pinned-offline-port-proof
description: Use when finishing a pinned offline source port.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags:
    - verification
    - offline
    - worktrees
platforms:
- linux
- macos
x-local-maintainer: TyphooN (TyphooN-)
---


# Pinned offline port proof

## Portable scope

This copy preserves a locally developed workflow, not transferable approval. Resolve the current task, repository, active Hermes profile, tools and ownership on this machine first. Historical project choices and TyphooN-specific executor/build policies are context, not permission to start services, run targets, modify security settings or publish. Project-root variables are documented in the collection's `PORTABILITY.md`; unset variables are not usable paths. Installing a skill installs no external tools or plugins.

## When to Use

Use for a scoped continuation on transferred existing worktrees when the base, source path map, offline proof, and ownership are already fixed.

## Procedure

- Validate the transferred path/hash map and pinned HEAD before testing; do not rediscover or chase a newer base during a bounded continuation.
- On a reboot-unstable host, fsync edited source files and their parent directories before launching proof, then retain the exact candidate manifest. A verified tool write or page-cache read does not establish reboot durability; if recovery matches the earlier RED manifest exactly, restore the lost edit rather than classifying an unchanged-source rerun as a failed fix.
- Read the saved owned delta first and send only necessary changed-symbol windows from large overlap files into model context; mechanical whole-file hashing/parsing is cheaper than repeatedly ingesting unrelated source.
- Preserve the recorded interpreter and invoke the checkout's canonical test runner with its actual isolation guards, serial workers, retries disabled, and private ignored HOME/HERMES_HOME/TMPDIR outside the real home.
- Validate receipt settings against the actual assigned checkouts instead of hardcoding an older template: role unit tests may use the second checkout's private home, and a CPU cap is distinct from pytest's serial `-j 1`. Require the baseline and candidate settings to match; do not rerun passing tests to fix a parent collector assumption.
- Parse verbose unittest method identities with their recorded runtime format and validate the successful terminal suite count/exit. Progress output can split a test's start from its `ok`; preserving the merged log and suite footer avoids falsely dropping that method or appending its name twice.
- Verify named runner artifacts actually exist before invocation; transfer packets can contain stale filenames. Use the existing audited runner and passing receipts, record the correction, and do not fabricate a replacement stub.
- Read the runner's publication contract before retrying proof. Use a new unique label when receipts, producer logs or per-run scratch are create-only; a reboot can leave scratch/producer state without a terminal receipt. Preserve that incomplete attempt and its unknown result instead of overwriting it, deleting it or repeatedly retrying the same label. Filter producer metadata separately from terminal receipt JSON when collecting proof, because their schemas differ.
- Calibrate per-file deadlines from passing receipts; parametrized policy files can exceed a short smoke-test timeout without demonstrating a source defect.
- Treat a nonzero runner exit or any timed-out file as failure even when its aggregate reports zero failed tests; partial dots and estimated collection counts are not completed tests.
- Extract a unique schema-identified terminal JSON document from merged caller-probe stdout/stderr; expected negative-path warnings can precede valid proof. Preserve the complete log and collector failure, validate receipt/log/source hashes, and repair finalization without rerunning completed immutable tests.
- Reap only owned process groups and verify no owned descendants remain before another launch; stop on an unreapable child and preserve the checkpoint.
- Prove import origins from the assigned checkouts and exercise real callers through disposable fake transport; model-shaped fixture bytes never qualify a model.
- Trace virtual-model loader contracts before accepting a numerical regression: metadata tensor overrides can supply types without populating the weight map queried for architecture-specific dimensions. Repair the synthetic fixture locally, verify typed initialization and executed operator provenance, and reject setup failures as RED.
- Resolve cast semantics from the pinned operator implementation instead of assuming a CAST opcode; a cast may be represented as a copy with a changed result type. Check both typed-to-reference conversion and the unchanged native reference path.
- Construct complete patches from pinned-base tracked binary diffs plus explicit sorted untracked additions, preserving commands, segment hashes, source maps, and reverse-apply checks without staging.
- Reuse source-review notes only for hash-identical paths and keep implementer selfreview separate from independent acceptance, host stability, qualification, integration, and activation.
- Match delayed native owner-exit notices to their exact delegation ID before recovery. A stale notice does not determine a replacement lane's outcome. If complete terminal source judgments survive a reboot, validate every disposition, input/artifact hash, source scope and process release before recovering that judgment; retain unknown native final/exit status separately and do not rerun a completed source review merely to obtain prose.
