---
name: source-faithful-game-ports
description: Use when porting games from source. Prove playable parity.
version: 0.1.0
author: Hermes Agent
license: MIT
platforms:
- linux
- macos
metadata:
  hermes:
    tags:
    - game-development
    - source-porting
    - differential-testing
    - preservation
x-local-maintainer: TyphooN (TyphooN-)
---


# Source-Faithful Game Ports

## Portable scope

This copy preserves a locally developed workflow, not transferable approval. Resolve the current task, repository, active Hermes profile, tools and ownership on this machine first. Historical project choices and TyphooN-specific executor/build policies are context, not permission to start services, run targets, modify security settings or publish. Project-root variables are documented in the collection's `PORTABILITY.md`; unset variables are not usable paths. Installing a skill installs no external tools or plugins.

Build playable ports of source-available games, with independently scoped reimaginings. This is an implementation workflow, not offline binary assessment; use `legacy-game-static-assessment` for a static-only preservation assignment.

## When to use

- Port an existing game's mechanics, houses/levels, resources and editing tools to a new language or platform.
- Establish whether a claimed faithful port actually preserves source behavior.
- Build an original reimagining alongside a faithful edition without mixing their simulation contracts.

## Procedure

### 1. Recover the usable checkpoint before choosing new work

Read the accepted objective, source revision, saved ownership manifest, current source inventory and exact verification receipts. Resolve the mutable active-continuation index before following historical lane checkpoints; after verifying a milestone, advance that index to the current evidence, owner handle, source identity and first unfinished obligation without rewriting frozen predecessor records. A stale active index can otherwise send the next continuation back to already repaired code or completed checks. Confirm the prior writer has released ownership before editing. Read the manifest's actual field names instead of assuming its schema. Resolve reusable pinned-source paths from the actual reference receipt or handoff and verify those files before dispatch; do not infer a sibling source directory from an evidence-lane name, because an empty or nonexistent inferred path can turn a bounded continuation into repeated source discovery.

After interruption, inventory changed, added and missing files against the saved baseline. Validate retained proof against its exact producer inputs using [the source-binding procedure](references/differential-oracles.md#6-reproduce-before-accepting-the-checkpoint). Keep whole-checkout ownership guards separate from per-check freshness: unchanged C does not validate edited Rust, and an engine edit does not invalidate unchanged C. Reuse matching proof and rerun only affected, interrupted or unbound checks. Preserve useful partial implementation even without a final handoff; executor failure is not proof that its edits failed.

When the user requests immediate continuation, salvage and verify once, then advance a real gameplay path. Do not replace implementation with repeated provider probes, status-only replies, or successive helper-only assignments. Changing executors does not waive fidelity or independent-review requirements.

After repeated native-delegation owner exits without implementation artifacts, stop redispatching the same ephemeral lane. Treat its lifetime as a dispatch-route limitation, not a game-code failure: preserve unknown exits and source bindings, then continue synchronously during Claude lockout or use an authorized tracked Claude CLI lane when availability is reported restored. Do not change global runtime/delegation settings merely to keep a worker alive.

**Exit:** a verified starting checkpoint, explicit source ownership and one next playable behavior—not a rediscovered project plan.

### 2. Define the fidelity and completion contracts

Keep a coverage matrix with: source routine/object/mode, Rust counterpart, runtime caller, proof, and unresolved dependency. Separate helper equivalence, subsystem equivalence, engine integration, graphical gameplay and campaign completion.

For a faithful edition, preserve wind, traps, puzzles, power supplies, collision ordering, object identities and unusual source behavior. For the reimagining, explicitly authorize new mechanics and content without changing the faithful engine. Share resource/data helpers only where their contracts really match.

If full editors are requested, include named original properties, links, room geometry, import/export, stable identities, unknown-byte preservation, undo/redo and actual open/edit/save/reload in the completion contract. A reduced object palette or raw-byte inspector alone is not a full editor.

**Exit:** every requested deliverable has a concrete runtime or data-roundtrip acceptance check.

### 3. Trace one vertical source path

Follow input -> interaction/environment -> movement/mode transition -> presentation effects through the original callers. Identify shared globals, scalar widths, signedness, narrowing points, enum values, frame indices, last-state fields and reset ordering before translating.

**Initialization clobbering:** Many game constructors re-derive runtime state from a different raw byte than the one a test expects to set. For example, an init routine may call `set_state(obj.initial_field())` where `initial_field()` reads byte N, while the test writes byte N+1 (the live-state byte). The constructor silently overwrites the test's value with the default. When writing runtime/differential fixtures, set the byte the *constructor reads* (the initial/source byte), not only the live-state byte — or set both. Diagnose this class first when a dynamic object shows `active=false` or zero velocity despite the fixture appearing correct.

Preserve initialization fixtures' arbitrary raw bytes when a later visibility fix changes dynamic admission. Test the initialized record independently, then require an optional dynamic only when the original draw-time clipping admits it; initialization alone does not guarantee a runtime entry. Select admitted objects by `(room, slot)`, not slot alone, because source-correct neighbors can share a slot and precede the central object.

Preserve narrowing at the same operation, not only at the final output; narrowing before an overshoot comparison can change the branch. Keep desired-velocity reset timing and source asymmetries, including depletion and held-key behavior. For co-op, retain the original interleaving of both players and shared supplies rather than calling a single-player wrapper twice.

Keep global/room state separate from similarly named entity fields; a room's clipping edge is not the paper's clip rectangle. Compare both immediately after entry and over subsequent frames, because later movement can conceal a wrong alias.

Complete interrupted source transitions before overwriting their mode/frame only where the original caller does so, including source/mask selection from the old frame. Never apply that completion to every transport: a mailbox can deliberately replace a foil-transition mode without settling its sheet or installing another sprite. Compare source/mask rectangles, shared supply and visibility as well as the final mode; preserve each caller's lifecycle rather than normalize it.

Verify each object's admission and exceptional-mode branch order independently; a web containment gate does not establish a duct or other transport's burning-contact gate. Read increments/decrements literally before proposing a larger alignment step, and treat unchanged entry velocities as part of the source contract. Compile the selected bodies before accepting a source-derived RED, because a test based on an incorrect reading can manufacture a false fix.

Read each direction's about-face helper literally: opposite turns can start at opposite sprite-frame endpoints and advance in opposite directions. Keep the logical facing flag unchanged until the original animation changes it, and include a constructor/input-driven boundary crossing as well as seeded facing controls.

Compare swept paper and shadow bounds, including edges the source deliberately retains when motion stops. A generic per-frame union or blanket reset can match the visible destination while changing persistent state. Add chained alignment-to-zero-motion controls and an ordinary-tick witness alongside the complete-state corpus.

Trace overlap-latch ownership per dispatcher arm. Mere intersection may preserve a latch; admission may set it only after full containment; mode completion may reflag all active hotspots while explicitly clearing disabled ones. A blanket latch-on-hit can prevent later entry or conceal recapture. Compare latches before containment, at entry, across room load and at completion through ordinary controls.

When adding an environmental gameplay trace to an empty-world oracle, execute the actual hotspot builder/intersection/dispatch and outer interaction order; do not inherit an empty-world shortcut or feed a helper result each tick. Pin the original sprite-size initializer as well as the builder constants, and prove enabled/disabled plus touching/outside controls from raw constructor inputs. Inspect post-wrap geometry before extending a trace: an upward arrival can lie beyond the closed-floor limit, so open-bottom and closed-floor/death inputs are distinct source behaviors, not grounds to inject immunity or change correct runtime code.

Trace same-room loading policy per caller: a linked transport can guard locale rebuilds, while a natural boundary transfer can rebuild even when a missing target retains the same room. Preserve each source guard or unconditional call rather than adding a blanket identity-based skip or rebuild. Unwanted rebuilding can erase active object/projectile lifetimes and replace latches; inventing arrival-overlap flags can mask that reset while changing recapture behavior. Compare linked same-room, cross-room and retained-room boundary traces separately, and keep mode-completion reflagging distinct from arrival.

Bind helper tests to the actual source caller's tail. If the source mode dispatcher clears collision-ignore flags after movement, keep that tail with the corresponding engine handler rather than normalize test output or rely on an unrelated outer scheduler. Distinguish seeded mode-body rows from constructor/input-driven traces, especially when signed-edge states are valid for a mode but invalid as new-game spawn coordinates.

Resolve downstream identifiers only after the source caller's admission guards. An original record may contain an invalid target that a rejected facing/mode/latch branch never reads; eager validation can turn that harmless overlap into a game abort. Test rejected admission against unchanged source-produced frames and retain refusal for an actually admitted malformed target. Preserve a real ordinary-input witness; never invent bit masks or swallow admitted failures merely because the source file contains an out-of-range identifier.

Trace draw-time callback/index correlation as well as constructor admission before adding neighboring runtime objects. Local master-list membership does not prove a neighboring hotspot or dynamic exists: literal draw code can reuse a central same-slot callback index. Preserve ignored placeholder entries and the original construction-time validity filter whenever collection positions feed a persistent contact latch; removing a noncolliding entry can change the first admitted contact. Prove that ordering through the real constructor and ordinary prize/input path without replacing the hotspot vector or inserting a filler object that masks the index difference. Preserve the actual mapping and shared latch, distinguish safe source aliases from negative/unlinked accesses, and label a compiled recording slice separately from full constructor/handler execution; otherwise an intuitive neighbor projection can introduce a new fidelity bug.

Resolve a mismatching numeric object kind through the pinned constant definitions before diagnosing its admission or handler. Trace the actual rebuild and caller once instead of cycling through fixture-versus-engine guesses; a snapshot containing a neighboring entry does not identify it as a toaster or prove the reference producer used C. Preserve characterization provenance and require source-backed evidence before refreshing it. Never add an empty match arm or placeholder comment as a purported visual implementation: locate the renderer-owned state and prove the exercised behavior, or leave that obligation explicitly open.

Preserve raw object unions and stable room/slot identifiers. Distinguish point versus rectangle field order, empty records, link sentinels and aliasing fields. Do not translate unsupported objects into approximate generic objects merely to make a house load.

Reuse the exact pinned collision-side helper rather than substituting intuitive left-edge or midpoint ordering; unusual width arithmetic can deliberately reverse a shove. Apply mode-specific collision bounds before the caller's inset (for example, exclude a burning sprite's decorative flame before shrinking the paper body). Prove each mismatch RED->GREEN through the real tick/input/movement caller and retain touching-edge, immunity and protective-state controls.

**Exit:** one end-to-end behavior is understood well enough to write its first failing test.

### 4. Translate with executable source proof

Use vertical RED -> GREEN cycles. Prefer a bounded oracle that compiles unedited selected source bodies and compares complete resulting state plus ordered effects. Load [Differential oracles](references/differential-oracles.md) before designing the harness.

Give platform/environment dependencies explicit caller-owned contracts. Preserve their mutations and result semantics, not just notification events. A successful allocation callback that drops recoil or another player-state mutation is not a faithful substitute for the original call.

Represent unsupported runtime behavior explicitly; a mode enum, exhaustive kind match or success-returning stub does not establish implementation. Keep the selected low-level API usable while adding the actual full-engine caller.

**Exit:** the new behavior passes source-backed differential tests and an actual integrated runtime test.

### 5. Keep verification reproducible and scoped

For Rust work, use the user's build parallelism (`CARGO_BUILD_JOBS=44` for this user) and run focused proof before broader checks. Typical verified commands through `terminal`, with the repository as `workdir`, are:

```text
CARGO_BUILD_JOBS=44 cargo test --test <focused-test>
CARGO_BUILD_JOBS=44 cargo test --all-targets
CARGO_BUILD_JOBS=44 cargo clippy --all-targets -- -D warnings
cargo fmt --all -- --check
CARGO_BUILD_JOBS=44 cargo test --release --test <focused-test>
CARGO_BUILD_JOBS=44 cargo doc --no-deps
git diff --check
```

Format only explicitly owned files with `rustfmt --edition <project-edition> <owned-files>`. Check debug and release where overflow/narrowing behavior matters. Regenerate oracle outputs into new evidence and compare them with the retained fixture; do not overwrite expected data to turn a mismatch green.

Inspect complete new/untracked files as well as diffs; an unborn repository can return a clean `git diff --check` while none of its source is included in the diff. Record exact commands, exits, source hashes and the tested set before claiming a checkpoint.

Inspect a receipt runner's environment assignments before selecting a fresh build cache. If it pins `CARGO_TARGET_DIR` internally, a caller-side override is ineffective: adapt or parameterize a private runner copy, retain canonical compiler flags, and verify the resolved target in the new receipt. Preserve earlier attempts; do not delete receipts or clear a shared cache to reuse a label. A fresh-cache pass establishes that execution, not the root cause of earlier compiler/linker crashes.

After observed reboot/interruption instability, flush/fsync newly written source helpers, fixtures and their parent directories before returning control, not only evidence JSON. Batch the write and durability step when frontend interruptions can separate tool calls. A zero-byte Python generator can exit 0 without doing work: require its nonempty compiler/execution receipts and expected case count before crediting a reference run; preserve the empty-producer attempt as missing proof.

On a reboot-prone frozen-source continuation, schedule independently reusable cheap supplemental checks before long compiler or solver checks when their dependencies allow it. Preserve one receipt per completed command and retain the exact argv, source bindings and serial build ownership; reordering protects partial progress but neither qualifies interrupted commands nor reduces the required matrix.

Use a distinct Cargo target directory for each disposable source variant or checkout. Copied packages can share artifact names and relative dep-info; a negative-control build can then replace a candidate's test executable while its older source mtimes appear fresh. Keep source variants out of the live candidate's target, preserve any crossed-cache failure, and rebuild the candidate in a new private target before attributing it to source behavior. Do not clear shared caches or touch source timestamps to force a pass.

Reconcile the normalized testcase catalog with the producer's suite totals before aggregating proof. Recognize libtest's `ignored, REASON` form as ignored, never as a pending or passing test; an exact `... ignored` parser can otherwise lose diagnostic child entries and falsely make an intact suite look ambiguous. With Rust `--nocapture`, diagnostic output can separate `test NAME ...` from a later standalone `ok`, so a single-line parser can omit a genuinely passed case. Recover an identity only from the hash-bound raw log, exact binary/test selector, unique test prefix, framed completion and matching nonempty suite count. Preserve the original receipt and record the catalog repair explicitly; do not invent identities, waive mismatches or rerun valid tests merely to normalize their metadata.

Use a fresh label for every invocation of a create-only receipt runner. A refused repeat can leave an older successful or failed receipt at the expected path; reading that file does not prove the new command ran. Check the wrapper's actual return, the newly created producer identity and its matching result/log before attributing fresh execution. Preserve old attempts and reusable proof explicitly rather than overwriting or relabeling them. For large verification output, run the producer directly into a private log and persist its own return code before filtering that saved log; for example, use `subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)` and record `result.returncode`. Do not accept the exit of a test-to-filter pipeline as the test exit, because a successful filter can hide a failed build or test.

**Exit:** reproducible behavior proof and no unaccounted source changes.

### 6. Connect real assets, editors and persistence

Use original resource IDs, sprite frames, masks, house records and sound priority where fidelity requires them. Distinguish an original sound-slot index from its resource ID: a shared/custom slot can resolve through a loader-owned resource rather than a fixed base-plus-slot filename. Preserve first-successful-load admission, failed-load behavior and reset ownership; capture the resolved raw ID at request time so a later locale load cannot retarget an earlier event. Keep raw resource presence separate from decoded-codec availability, so an unsupported decoder neither silently removes a source hotspot nor falls back to the wrong resource. Bound preload entry and byte budgets independently and prove actual native lookup, not only the emitted request metadata.

Keep source-wiring guards aligned with audio ownership: adding an independent music decoder legitimately changes global factory/borrow counts. Scope assertions per owner while retaining the shared run-long bank, unfiltered source-ordered dispatch, and behavioral stop/locale controls; lexical checks never qualify device playback.

Preserve attribution and distinguish local asset use from verified redistribution rights; community download availability is not a license.

Verify sound beyond successful decoding and game event counters: backend initialization may be asynchronous, stubbed or failed while those counters still advance. For Linux ALSA/PipeWire, follow [Audio playback qualification](references/audio-playback.md); native streams may be absent from PulseAudio sink-inputs, so resolve the owning PipeWire client PID and active links instead of declaring silence from that interface alone.

Trace the actual error producer through the locked audio dependencies before repairing an alleged `Result::Err` path. A fallible signature can have only `Ok` normal returns while decode failures panic or device failures occur on a detached thread. Bind registry sources to lock checksums and consumed dep-info; label injected contract errors separately from reachable defects, decoding proof and actual device/playback qualification.

Trace per-object lighting gates through the original draw dispatcher, validity predicate and saved-background/admission helpers before adding a room-wide visibility gate. Controls, transports and active prizes can deliberately remain visible in darkness while furniture disappears. Keep consumed-object state filtering separate; a non-collectible's false state can select fallen or disabled artwork instead of disappearance. Trace validity per kind, retain dispatcher ordering, and prove both active visibility and inactive absence in actual framebuffer crops. Label native initial-state galleries separately from input-driven transitions or collection playthroughs.

Trace the original empty-record sentinel through editor creation, occupancy, allocation, copying, counts, link checks, deletion, serialization and runtime admission. Zero-filled synthetic editor fixtures can conceal a mismatch with an original `-1` sentinel. Exercise new/edit/delete/save/reopen through the actual engine; preserve unknown record bytes and refuse incompatible kinds rather than weakening the engine gate or silently migrating loaded data.

For editable JSON, retain immutable original bytes and stable record provenance alongside the typed view. Position-based merging or typed equality alone can misattach opaque metadata after copy/delete/reordering. Prove exact no-op bytes, immutable snapshots, undo/redo and atomic rejected edits; budget duplicated opaque payloads before reconstructing output and bound the serialization buffer. Preserve arbitrary-precision numbers and literal opaque map keys through actual JSON syntax: a generic Value parser's private numeric-map protocol can reinterpret user keys. Refuse ambiguous edited data rather than silently selecting or dropping a duplicate key.

Measure a real house's unique required resource IDs and actual decoded resident-byte footprint before changing an admission limit. Keep entry-count, dimensions, decoder-output and resident-byte bounds independent; if only the count cap blocks valid source-distributed content, make a bounded compatibility correction rather than removing caps or inventing a streaming framework. Prove over-count refusal before asset reads, byte-budget refusal with an admitted count, startup cancellation, and actual original-data loading separately; a header-size estimate alone is not a successful loader run.

Keep decoded picture bounds distinct from the original caller's offscreen-port bounds. Before relaxing a color/mask size check, trace the source allocation, native-size drawing and sprite rectangles; a larger port can contain an undrawn row even when the resource is valid. Keep the raw decoder/mask seam strict and implement only a source-justified, resource-and-shape-specific adapter. Preserve drawn pixels without resampling; define any undrawn padding deterministically and disclose where historical initialization remains unproved. Test exact retained pixels, output dimensions and transparent padding, plus unrelated mismatches refusing before color mutation; blanket resizing changes atlas coordinates and can conceal malformed assets.

Exercise real asset-backed gameplay rather than leaving the source-faithful engine behind a headless test while the graphical binary still runs preview physics. Verify room transitions, wind, power, hazards, linked puzzles, death/recovery and victory through the actual runtime.

Verify standalone editor-to-player launches separately from in-process playtests. Trace the selected player's actual CLI contract, forward required original-asset/import arguments, and reject incompatible mode-specific options before graphical startup. Before an independently admitted headless check, trace its exact argument branch to a return before window/audio initialization; a guessed unknown option can be ignored and launch the game. Run the current hash-bound executable with private HOME/XDG/TMPDIR and no display environment, asserting the expected exit and branch-specific output. Environment isolation alone does not prove the branch stayed headless. Use the [production-caller qualification recipe](references/differential-oracles.md#8-qualify-production-headless-callers) for help/refusal and create-only export roundtrips. Keep those claims separate from GUI editor, gameplay and device qualification; a successful in-process editor return does not validate the adjacent executable's launch protocol.

Keep authoritative simulation synchronous and ordered. Move asset decoding, loading and save work off the render path only through bounded jobs with tested backpressure, stale-result cancellation, failure propagation and shutdown; `async` syntax is not that proof.

Trace load/codec, frame-clone and serialization budgets independently before declaring a save refusal unreachable. A document admitted by a larger loader cap can exceed a smaller frame-side snapshot budget. Reproduce through the real load worker and accepted state event, not merely an invalid hand-built game; keep protective limits intact. Route reachable diagnostic or final-save refusals through the required persistence drain, verify already-admitted independent settings complete, and retain the original error alongside any secondary closing refusal. Keep CPU frame/image providers and source-wiring guards explicitly separate from real GUI qualification.

Combine independently reachable closing failures in regression tests. Preserving an initiating capture error does not prove that a synchronous flight refusal survives a later settings-worker refusal: a mutable last-error slot can still erase it. Assert chronological preservation of every reported error, drained idleness and source/competing-target byte preservation, including the three-error case; bound accumulation by actual admitted work.

Trace failure visibility through poll, input handlers and draw: writing a refusal into shared HUD status does not establish that it survives until presentation. Keep any required diagnostic fallback independent of optional tracing, and handle its write failure without adding an early return that can cancel pending work. Call synchronous stderr logging best-effort, not nonblocking or guaranteed delivery. Use the [fresh-process error-visibility recipe](references/differential-oracles.md#7-test-error-visibility-with-a-fresh-process) to prove the production reporter and standard streams while explicitly separating modeled status replacement from real GUI/frame execution.

If graphical setup blocks before application dispatch, preserve that infrastructure HOLD and use a bounded literal-runtime-branch/real-worker proof only for the admitted CPU scope. Declare input, editor, graphics and audio seams; do not promote it to GUI or backend acceptance. Retain its discriminating regression in the repository's maintained checks: a replacement-control test alone can pass with the original editor-entry cancellation bug restored. Pair any structural source guard with the real behavioral proof, require unique extraction boundaries, and show it refuses the original body and accepts the fixed one using a disposable source variant—not by reverting the live dirty checkout. Private evidence can preserve a causal result while still leaving regression maintenance incomplete.

Make the save publication boundary explicit. Prove old-target preservation for pre-commit refusal, but return a typed committed outcome with a durability warning when parent-directory open/sync fails after successful publication; returning an ordinary save error then can make callers falsely claim the old file survived. Exercise normal success, pre-commit refusal and an injected post-publication directory-sync failure through the actual save API. Read back destination bytes/decodability and check the outcome, then propagate warnings through manual save, autosave, options and shutdown callers rather than dropping them. Keep irreversible committed-save acknowledgements distinct from cancellable work: a newer generation cannot undo publication. Bind acknowledgements to the current document's issued revision range and continuations to their triggering revision, so a late save cannot attach an old path/stamp to New/Open or fire a stale close/playtest action. Exercise commit-before-cancel, replacement, newer edits and undo/redo through the maintained editor/worker seams.

Separate intentional editor-save replacement from create-only diagnostic outputs. A derived data-fork/container export must remain create-only even when OUTPUT is lexically INPUT; never reuse the opened source stamp as replacement authorization after dropping its container backing. Prove refusal preserves the entire source envelope and that intentional roundtrip/edit saves still retain their backing. Route screenshots, metrics and exports through the same checked artifact boundary rather than leaving a convenience image-export API on an unchecked path; an output/source alias or followed symlink can truncate the original house. Bound output size, resolve parent directories without following symlinks, write a private exclusive temporary file in the held destination directory, sync it and publish with an atomic no-replace operation where supported; report unsupported secure semantics explicitly. Test successful creation, existing-input preservation, symlinked parents and targets, traversal, special files, competing creators and cleanup after failure. Audit capture-directory creation as well as final-file publication: an unchecked `create_dir_all` can mutate a symlinked destination before a later guard refuses the output. Create missing components through held no-follow parent handles, and validate the entire traversal before the first mkdir; assert that refusal created no redirected directories. Keep screenshot encoding errors separate from persistence errors, and do not treat one metrics-file regression as proof that the screenshot caller or concurrent publication is safe.

**Exit:** both runtime and editor paths operate on real, compatible content with observable error handling.

### 7. Verify GPU presentation without altering simulation

Before restarting heavy builds or graphical/device qualification after kernel-related interruptions, inspect the current boot's kernel diagnostics. Fresh `Bad page state` faults in unrelated processes or kernel workers are host-integrity risk evidence, not a game-code finding. By default preserve the source/evidence checkpoint and pause heavy execution; an earlier focused pass, a quiet process list, or successful reboot does not establish host stability. Keep kernel-versus-hardware causality unresolved without evidence, and obtain explicit approval before reboot, boot/kernel, clock/voltage or shared-process changes.

Honor an explicit task-scoped direction to continue project work/builds on the actively booted kernel while the user retains host recovery. Record that decision, keep diagnostics informational rather than a recurring boot gate, and proceed with bounded project verification without repeatedly requesting a kernel switch. Do not touch the user's concurrent kernel build or widen this exception to other tasks. Actual test failures, source corruption, unresolved writer ownership, unreaped owned processes, independent acceptance and commit/push limits remain real boundaries.

- Where host diagnostic admission is required, query the complete current boot for memory-fault, kernel Oops/general-protection and RCU-stall signatures, not only a short tail or `err` priority window. A later fault reopens that default hold unless the explicit task-scoped active-kernel continuation above applies; preserve completed checks at their historical scope rather than treating them as host clearance. Do not turn informational diagnostics back into a boot gate after the user retained host recovery.
- Classify journal-query outcomes separately from kernel faults and application test exits. On the observed `journalctl --grep` implementation, exit 1 with literal `-- No entries --` and empty stderr means no match; preserve the first admission refusal and correct that narrow classification without waiving real query errors or fault records.

Resolve missing graphical executables from retained qualified-tooling receipts before declaring the capability unavailable; absence from PATH does not prove absence from private tooling. Verify exact executable/dependency paths and scope private driver-library overrides to that driver rather than altering the game's renderer environment.

Persist screenshot bytes and other declared supports with fsync before publishing a successful receipt; sync new output-directory entries too. After interruption, verify their original hashes. Preserve a zero-byte or mismatched capture with an integrity notice and rerun into fresh evidence, rather than treating retained success JSON as reusable visual proof or rewriting its old hash.

For private Xvfb tests, do not use `-displayfd` auto-allocation: it can unlink an existing filesystem-only Xwayland listener when the abstract socket is absent. Choose an explicit high display only when its lock, filesystem socket (including dangling symlinks), and abstract socket are absent. Let Xorg acquire its explicit-display lock, then verify both listeners with `SO_PEERCRED` and the lock PID before any X protocol, capture, focus or input. Use private HOME/XDG/TMPDIR and the same software-rendering environment for server and client. Verify that preexisting display paths retain their identities after cleanup; terminate only owned children. A shared desktop socket repair requires explicit approval, never a retry around a permission denial.

Wait for an actual input/draw or document-ready acknowledgement before sending subsequent graphical workflow controls. A nonzero dark framebuffer can be an async startup-loading screen, not the ready game/editor; a fixed sleep or a pre-render backend log can lose an entire queued editing sequence while the real UI is still initializing. Preserve failed attempts and correct the driver readiness contract without weakening the requested edit/playtest outcome.

Capture a rendered framebuffer before advancing to a newly cleared frame. Bound readback to requested capture points, preserve image orientation, propagate encoding/output failures, and verify actual nonblank pixels rather than accepting process success or asset counts as visual proof. A capture performed after `next_frame` may contain only the cleared backbuffer even while the window displayed correctly.

Make smoothing render-only. Reset render history on teleports, room changes, respawn, restart, pause and editor transitions; interpolation must never alter collision coordinates or original tick ordering.

For this user, GPU rendering and high-refresh operation are acceptance criteria, not optional polish. Measure the actual renderer/backend, workload and frame-time distribution. A GPU-capable library, smooth motion, an average FPS counter or a software-rendered capture does not prove hardware refresh saturation or VRR operation.

Treat a reimagining as its own designed game: distinct taught mechanics, art/audio and a beatable progression, not only a palette change. Replay the campaign through normal controller inputs and actual failure rules; teleporting, injecting score or disabling hazards cannot serve as completion evidence.

**Exit:** exercised graphical/audio gameplay, explicit performance observations, and input-driven campaign proof.

### 8. Multi-checkout convergence (parallel-lane merge)

When the port was built in isolated checkouts (classic, reimagining, editor) and must converge into one primary tree:

1. Record each checkout's base, changed paths, and last passing test set before touching the primary.
2. Diff the primary against each checkout per file; identify which checkout is authoritative for each module (typically the most-evolved branch owns the file).
3. Copy or merge file-by-file; prefer whole-file copy from the authoritative checkout over surgical merge when the files have diverged significantly — partial merges produce compile errors that cascade.
4. Build after each file batch; fix compile errors in the same pass before moving to the next file.
5. Run the full test suite; behavioral failures after convergence are almost always missing *calls* (a `rebuild()` or `tick()` hook not wired into the main loop) or missing *derives/imports* (a trait bound, a `mod` declaration, a `use` statement). Grep for the symbol the failing test references to find the unwired call site.
6. Only after all tests pass, run the headless verification binaries (replay, oracle, asset-extract) as an integration smoke test.

**Exit:** single tree, clean build, all tests green, headless tools functional.

### 9. Integrate, review and report honestly

Integrate only completed or explicitly salvaged owned deltas against their recorded base. Reserve shared export files for parent integration when parallel components add modules. Obtain the required independent review separately from implementer self-review; changing the execution provider does not automatically approve a different review route.

Treat a credit-locked Codex CLI account separately from included GPT subscriber-route availability. When this project's GPT review route is already approved, consult the qualified direct-subscriber procedure in `hermes-agent` before declaring independent review unavailable; retain zero-tool/read-only enforcement, explicit model/effort and no fallback, without changing shared routing or billing.

Map every original acceptance criterion to final evidence. Keep open requirements visible when only a subsystem passes, and call the result a checkpoint rather than a complete port. Report the working artifact and exact proof concisely, not a transcript of orchestration.

## Verification checklist

- Source behavior, not preview behavior, drives the faithful binary.
- Stable records, links, raw unknown data and source ordering survive.
- Differential tests include complete state, effects, negative cases and chained frames.
- Both editors and save/load paths are exercised when requested.
- Campaign completion uses normal runtime inputs.
- Headless verification binaries (replay solver, oracle runner, asset extractor) execute successfully as a final smoke test.
- GPU/high-refresh claims identify actual measurement conditions.
- Partial source proof, local completion and independent acceptance remain distinct.
