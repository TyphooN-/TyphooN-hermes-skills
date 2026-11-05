---
name: rust-workspace-dependency-refresh
description: Use when refreshing Rust workspace dependencies.
version: 0.1.0
author: TyphooN (TyphooN-), Hermes Agent
license: GPL-3.0-only
platforms:
- linux
- macos
x-local-maintainer: TyphooN (TyphooN-)
---


# Rust workspace dependency refresh

## Portable scope

This copy preserves a locally developed workflow, not transferable approval. Resolve the current task, repository, active Hermes profile, tools and ownership on this machine first. Historical project choices and TyphooN-specific executor/build policies are context, not permission to start services, run targets, modify security settings or publish. Project-root variables are documented in the collection's `PORTABILITY.md`; unset variables are not usable paths. Installing a skill installs no external tools or plugins.

## Ownership

Delegate nontrivial sweeps to Claude Opus Max while included usage is available. During hard lockout, continue without paid fallback. Preserve dirty paths in an isolated worktree, record base and an immutable baseline lockfile before resolver operations. Use requested compilation parallelism (TyphooN dependency sweeps: `CARGO_BUILD_JOBS=44`, `-j 44`); serialize workspace builds. Do not commit or push without authorization.

## Complete inventory and resolver

- Enumerate every manifest, normal/dev/build/target dependency, inactive vendor declaration and CI/tooling pin. Follow the repository ADR index: append durable existing decisions rather than invent session-log ADRs.
- Query primary upstream sources for every name, including removed baseline names and disabled vendor dependencies. Checkpoint bounded concurrent sparse-index retrieval to JSON; assert no missing/error rows.
- Select greatest non-yanked stable SemVer. Detect prereleases only BEFORE `+`: build metadata such as `+spec-1.1.0` is not a prerelease.
- Produce a CSV with baseline, selected, latest stable, manifest scopes, source URLs/timestamps and exact blocking parent requirements.
- Build retained requirements from structured per-version records and join complete entries. Append a rendered string as one list element; `list.extend(string)` splits it into characters and destroys multi-version boundaries.
- Round-trip the emitted CSV and validate every retained entry against the exact metadata graph. Matching row counts and crate versions does not prove provenance cells are readable or correct.
- Match parent requirements to resolved edges by package, kind, target, and rename/library name. Same-name inactive dev declarations are not active parent constraints; package names can differ from exported library names (for example, xml-rs exports xml).
- A blanket `cargo update` can introduce avoidable duplicates. Inspect broad-range Windows support families and use precise `cargo update -p name@old --precise selected` probes; retain exact diagnostics/exits.
- Count packages, unique names, true duplicate families and extra versions programmatically. Repeated host/target units in `cargo tree -d` are not necessarily distinct lockfile packages.
- Preserve latest owner releases instead of fake semver compatibility, cosmetic downgrades or unnecessary forks. Document unavoidable splits and each owner's unblock condition honestly.
- Remove stale exact duplicate exceptions, keep deny-by-default and do not add advisory ignores. Test a negative control with a temporary config, not by weakening repository policy.

## Vendored GUI/GPU migrations

- Coordinate egui/eframe/plot/CommonMark/wgpu generations; the direct wgpu feature selector must match egui-wgpu.
- Verify vendor archive SHA-256 against registry checksum. Compare rebased vendor with pristine new upstream so local differences stay in documented patch files. Preserve upstream fixes during conflict resolution.
- Trace feature changes for behavior: egui/eframe 0.36 browser links became optional and must be explicitly preserved where used.
- Wgpu 30 mapped-range getters return Result. Trace every caller and mapping ownership. Unmapping an already-unmapped Vulkan buffer is a validation error: do not promise cleanup without known successful mapping and exclusive ownership.
- Run tiny explicit Vulkan copy/remap/failure tests. Populate reuse checks through the GPU queue; mapped-at-creation host bytes need not survive lazy GPU initialization.
- Egui 0.36 texture deltas must be consumed. Headless tests with intentionally no painter explicitly clear their deltas; runtime rendering must still apply them.

## Acceptance

Run focused proofs, workspace tests/build/check/clippy, unignored RustSec audits and duplicate gates. Retain failed logs separately. Explicitly run hardware-dependent proofs during migrations when available. Broad GPU/background-rendering or security changes need independent review; obtain user agreement before substituting a reviewer during Opus lockout. Resolve findings, preserve dirty paths, inspect full diff and integrate only with fresh proof. Record exact commands/exits, base, changed paths, ADR/inventory and outstanding decisions in a compact handoff.

Major upgrades must be traced through every supported platform's implementation, not just compared on the host: a directory crate can keep Linux APIs unchanged while silently relocating Windows implicit configuration. Preserve legacy operator configuration and explicit-path precedence; test legacy-only, new-only, both, neither and unavailable-directory cases without mutating the host environment.

Parse the final failure list and aggregate for concurrent `--nocapture` negative tests. Per-test output can interleave with panic/backtrace text, so an anchored `... FAILED` line parser can miss genuine failures. Require the expected canonical failure names, command exit and source restoration hash.

Check new untracked files too: use an evidence-only temporary `GIT_INDEX_FILE`, add explicit owned paths, and run `git diff --cached --check`. A working-tree `git diff --check` skips new files and can miss an entire CRLF CSV. Emit inventory CSV with `lineterminator="\n"`; verify CSV semantic round-trip if integration normalizes line endings. Do not infer byte-level normalization from a successful text patch: newline-preserving edit tools can keep CRLF unchanged. Use a scoped line-ending formatter when necessary, then verify raw CRLF counts, parsed value equality, and the alternate-index whitespace gate before claiming success.

Require successful Git command exits before interpreting status or diff output. Put global options before the subcommand (`git --no-optional-locks status ...`), or set `GIT_OPTIONAL_LOCKS=0` for read-only inspection. Empty stdout from a failed command is not a clean tree; read-only closeout must not refresh or alter the user's staged index.

Use a private `GIT_INDEX_FILE` initialized to the verified base when publishing owned changes alongside unrelated staged work. Verify its exact owned path set and tree, commit from it, then reconcile only committed owned paths into the real index. Compare unowned staged blob/mode entries and the cached binary patch before and after; HEAD changes mean whole-index byte identity is not a valid post-commit preservation claim.

Pin identical diff prefixes when comparing snapshot and committed-tree fingerprints. `diff.mnemonicPrefix` can produce `c/` and `i/` for a cached diff but `a/` and `b/` for a tree diff. Match the recorded presentation explicitly and also verify tree, blob hashes, modes, paths and parent; do not mistake header-only differences for source drift or amend a correct commit.

Recognize a remote tip already equal to the exact verified intended commit as an already-published state, not a diverged base requiring another commit or rebase. Perform the authorized normal pinned-ref push and read back the exact remote ref; do not infer who published it first or claim unrelated incoming history was authorized.

Use the exact already-executed workspace test binary for a tight diagnostic when `cargo test -p` changes feature unification and triggers expensive recompilation. Record that binary path/hash and its source binding; use normal Cargo for final proof. A focused command that times out during compilation executed no tests and does not reproduce a test failure.

Inspect per-thread kernel wait channels before extending a stalled network test's timeout. FD-table-growth/RCU waits are host evidence, not a demonstrated repository bug; preserve the candidate and stop new verification while test-owned threads remain unreapable. Do not change kernel or security settings to manufacture a pass.

Preserve each recovered command's environment as well as its argv and expected exit; in particular, keep the recorded separate MSRV target directory instead of triggering a needless cross-toolchain rebuild. Bind a new receipt set to the current boot, and classify a boot-ID preflight failure as zero tests executed, not interrupted or passing test proof.

Summarize ignored cleanup paths by directory before printing them; use directory-level Git listings or filter build artifacts before output. Preserve unique non-build ignored artifacts such as a standalone fuzz lockfile before removing a completed worktree, and leave shared build caches alone.

Recover interrupted proof from the original command list and observed receipts, not a newly generated resume script. Do not `eval` an assignment-shaped script block or assume every check expects zero: preserve each command's exact expected exit and intended diagnostic, including policy-negative controls. Confirm pinned audit executable/options and configs before rerunning; an invented audit command cannot close the security gate.
