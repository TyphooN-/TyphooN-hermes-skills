# Differential Oracles for Stateful Legacy Game Code

Use this recipe for an authorized source port. It proves selected source semantics; it does not by itself prove a complete historical platform or game.

## 1. Freeze the reference

1. Pin the original revision and bytes. Record the exact encoding/newline transformation used to create readable source.
2. Verify normalized source against that transformation before extraction; never silently repair source tokens or expected output. If a pinned digest fails, compare the original Git blob at the declared revision and reproduce the exact normalization into fresh evidence. UTF-8 replacement can damage MacRoman comments while leaving visible algorithm tokens intact; do not relax the digest or overwrite older evidence to hide that difference.
3. Extract the selected function bodies without editing their algorithms. Retain body hashes and the original declarations/constants needed by them.
4. Write generated C, compiler logs, inputs, outputs and receipts into a fresh evidence directory. Execute the trusted host-built harness, not the recovered game binary.
5. When extending a selected-body oracle, include each newly required constant-bearing header in the pinned inputs; input constants can live in `Externs.h` rather than the main defines file. Assemble a fresh complete normalized source directory from hash-verified retained bytes instead of mutating older pinned evidence or inventing the missing constants.

## 2. Establish the ABI boundary

Use fixed-width host types and compile-time assertions for byte width, short/Boolean widths, rectangle member offsets and relevant source fields. A host's `long` or struct alignment can differ from the historical platform even when a helper appears to run correctly.

If declaration adapters are necessary, confine them to named declarations and record the adaptation. Do not claim full binary ABI equivalence from a host-side scalar adapter.

Identify the owning object array before doing pointer ordering or index arithmetic in a host seam; relational comparison and subtraction across different C arrays are undefined even when their addresses appear contiguous. For a host with `uintptr_t`, check the address against the candidate array's start/end and element alignment, then derive a bounded slot from the checked integer offset. Refuse pointers outside the declared arrays. Keep this adaptation out of extracted algorithm bodies and reproduce the exact corpus after changing the seam, because host undefined behavior can otherwise masquerade as historical behavior.

When generating host prototypes from extracted signatures, remove trailing `//` comments from the prototype-only copy before appending `;`, or emit the terminator on a new line; otherwise the comment can swallow it and manufacture a harness compile failure. Leave the extracted algorithm bodies unchanged, retain their hashes, and require a successful strict C compile before treating a Rust mismatch as source-backed RED.

For compilers supporting the observed GNU-style options, a suitable harness command through `terminal` is:

```text
cc -std=c11 -O2 -fwrapv -Wall -Wextra -Werror <generated-reference.c> -o <reference-executable>
```

`-fwrapv` does not establish every historical conversion rule. Check the narrowing behavior used by the source and test boundary values in both Rust debug and release builds.

## 3. Specify each external seam

List each platform/environment dependency and classify it:

| Seam | What the harness may supply | What remains unproved |
|---|---|---|
| Key polling | Explicit sampled key states | OS scan-code mapping, bit layout, timing |
| Sound/UI command | Ordered request recording | Actual playback, pause, save or quit behavior |
| Allocation/admission | Explicit capacity or rejection | Object lifetime and later interactions |
| Environment phase | Explicit bounded caller inputs | Real room geometry, wind and collision generation |
| RNG supply | Explicit raw values/seed adapter | Historical generator, timing or seeding |

Do not turn a mutation-bearing function into a request-only success stub. Trace everything the original call reads and writes. If a band/projectile allocation also changes velocity and emits sound, either execute that trusted source body under explicit capacity or reproduce those named immediate effects in the test host and compare them. The later projectile engine remains a separate integration gate.

Extract and pin the original outer scheduler slice before extending an empty-world oracle with an environment interaction. A correct lift/intersection helper in the wrong input, collision or reset order is not native tick proof. Guard each omitted phase by asserting zero participants and refusing nonempty state; distinguish those checked-empty seams from executed original bodies.

Assert source-body identity separately from these seams. Keep unsupported mode/room behavior out of success wrappers rather than filling it with no-ops.

Separate terminal signaling from the outer ending controller. A game-over flag may suppress input and movement while presentation, countdown and final-screen work continue. Label post-terminal selected-phase samples as such; frozen player state, timer initialization and a stopped port API clock do not prove the original timer or ending completed. Test the death controller's own already-ended guard independently of the outer scheduler, and label seeded bypass controls separately from constructor/input-driven life-loss traces.

- Bind each unsupported-seam refusal to the exact first callback, a unique witness and a specific nonzero exit. A SIGABRT alone can come from an earlier compositor callback and falsely appear to prove refusal at room arrival; trace callback order rather than installing a success no-op to reach a later boundary.
- Use deterministic nonreturning exits for unsupported host seams when a fatal signal is not itself the behavior under test. RLIMIT_CORE=0 does not disable a configured core-forwarding pipe, and a minimal abort can block there. Preserve the failed attempt, confirm owned processes are terminal, and avoid changing host core/security settings. When real crash/signal behavior is required, retain an infrastructure HOLD instead of replacing that test.

## 4. Compare observable state, not selected coordinates

Capture all selected state fields, shared resources and ordered effects. Include source/mask/destination/swept/shadow/clip rectangles, desired/current/last velocities, facing/mode/frame fields, held-input latches and reset flags when the routine owns them. Untouched fields should remain unchanged too.

Use three complementary corpora:

1. **Matrix:** valid combinations of facing, mode, simultaneous inputs, resource signs/depletion, capacity rejection and boundary arithmetic.
2. **Chained trace:** feed each resulting state and supply into the next frame; do not reset the player between steps. This catches exhaustion, held-fire retries, turning and frame cadence errors that one-step tests miss.
3. **Shared-state/co-op trace:** interleave both players exactly as the original outer loop does. Verify shared supply consumption and interaction ordering; two sequential single-player ticks are not an equivalent substitute.

For small byte-sized link domains, exhaust all values and distinguish the sentinel from ordinary identifiers. For larger state spaces, bound deterministic sampling and document what was not covered.

Keep synthetic labels explicit. A synthetic environment trace is useful differential proof of its selected routines, not an observed original-house playthrough.

## 5. Diagnose mismatches without weakening the oracle

1. Reproduce the first divergent frame and compare complete state/effect output.
2. **Check initialization clobbering first:** if the divergent object shows a zeroed or inactive state, verify the constructor or rebuild path does not overwrite the field your fixture set. Trace the exact byte the init reads (the "initial" field) versus the byte you wrote (the live-state field). The fixture must set the byte the init reads, or both. This is the most common cause of "object is not active / has zero velocity" failures in ported game tests where the fixture appears correct.
3. Check input-owner clobbering too: a prior injected `tipped`/held flag can be reset by `GetInput` before the routine under test. Drive the actual control combination that produces the state; do not bypass input or change expected source results to make the fixture pass.
   Check static-storage initialization independently of fixture seeding: an uninitialized C scalar starts at zero, not a chosen absent/sentinel value. Test the real engine constructor and room/reset lifetime; a differential host that explicitly seeds `-1` cannot validate that startup contract.
4. Check operation ordering and immediate external mutations before changing arithmetic.
5. Check narrowing before comparisons, signedness, desired-state resets and shared flags.
6. Fix the implementation or an identified inaccurate seam. Do not change the original bodies or normalize away the mismatch.
7. Preserve the failing fixture/log and rerun the matrix, chained traces and integration tests.

When a source-correct downstream effect breaks an older component differential, inspect its declared callback seam before changing production behavior or expected data. An explicitly synthetic always-audible switch callback cannot certify the original invisible-switch arm. Keep the C golden unchanged, make the Rust fixture's synthetic object kind match that declared seam, and retain actual-caller controls for both silent and audible kinds with the same link/state/latch assertions. Label the repaired component claim separately from the real downstream routine; do not weaken a strict effect comparison or promote a stub to full source parity.

## 6. Reproduce before accepting the checkpoint

Regenerate into new evidence and compare exact fixture bytes with the retained corpus. Record compiler command/exit, source/body hashes, ABI assertions, Rust check commands/exits and limitations in the receipt. Report C-produced cases/frames, Rust-compared rows, chained traces and ordinary-input runtime frames separately; a large generated reference corpus is not proof that every generated case was checked by the port.

Collect required receipts from the saved manifest's explicit labels rather than treating every `*.json` as a receipt; evidence directories also contain arrays, corpora, checkpoints and control records. Validate the expected object shape and required fields before indexing. Skip only positively identified non-receipt artifacts during optional discovery, never malformed or missing required receipts; a broad `except: pass` can turn lost proof into an apparently clean checkpoint.

Finalize retained proof in this order:

1. Verify the producer's own terminal exit and complete log hash before interpreting its summary.
2. Compare the full checkout inventory to locate every changed, added or missing path; keep the strict launch/ownership checkpoint separate from check-specific freshness. Distinguish a checkpoint's launch-baseline fingerprint from each command's actual input fingerprint before classifying drift. Reconstruct the recorder's complete path set and exact canonical serialization, then compare the per-path hashes with current bytes; an older baseline digest alone does not invalidate a later source-bound passing command.
3. Validate a C reference against its pinned source/body hashes, generator and ABI/seam inputs, compiler invocation, corpus inputs and exact output bytes. Validate Rust behavior against the implementation and test inputs of the corresponding Rust receipt.
4. Record drift as `changed_since_run` until its relevance is established. Do not call a set `non_runtime_changes` merely because a collector wants to reuse the result; formatting and documentation exceptions require positively identified scope, and engine/test edits need their own current proof.
5. Preserve valid reference results while rerunning only affected runtime checks. If dependencies were not captured or cannot be established, leave freshness unknown or rerun the bounded producer; never remove an assertion simply to complete the handoff.
6. Aggregate overlapping commands by normalized `(test source or binary target, fully qualified test name)` identity within each build profile, not executable hash or summed suite totals. Reconcile each command's catalog with its own nonempty producer totals before taking the union, then compare debug/release identity sets explicitly. Keep ignored diagnostic child entries and separate production-CLI cases out of the passing-test union, and report reused execution separately from fresh runs; rebuilding or selecting the same test twice does not add coverage.

Keep the claim narrow: selected-function state/effect equivalence. Advance to actual engine, asset-backed gameplay, editor roundtrip and campaign gates before claiming a finished source-faithful game.

Pair a real original-data loader/tick run with a small repeatable regression when full local asset packs cannot live in CI. Pin the original BinHex/data/resource forks and the actual consumed asset-input universe; disclose any frozen loader-geometry seam rather than presenting it as another full asset load. Mark Rust-observed characterization snapshots explicitly as non-C proof. Compare fresh-process and debug/release output, but count repeated executions separately from unique trace coverage. Report nonempty-room samples separately from active/moving dynamics and projectile lifecycles; a populated room can execute none of those participants. Do not attribute a death to a dynamic merely because dynamics were present: bind the caller phase and pre-motion collision witness, or leave the cause unproved. Keep private simulation fields private: use public observations in an external probe or an owning-module test, not a widened production API solely for diagnostics.

## 7. Test error visibility with a fresh process

Use this bounded recipe when a real runtime reporter must leave a diagnostic even if a later handler replaces shared HUD text. It establishes reporter/process/stream behavior, not a graphical frame or a real failing worker job.

1. Trace the actual poll-to-input-to-draw order and identify the production reporting call. Exercise that exact reporter from an owning-module test rather than recreating its formatting in a probe.
2. Add a normal parent test and an ignored internal child entry in the same test executable. Spawn `std::env::current_exe()` with `std::process::Command`, selecting the child's fully qualified identity using `--exact`, `--ignored`, `--nocapture` and `--test-threads=1`. Pass a child-only marker with `Command::env`; do not mutate the parent test process's environment or globally redirect its streams.
3. In the child, verify its marker, invoke the real reporter with a unique refusal token and optional tracing disabled, then assert its immediate HUD result. Explicitly model the later handler clearing/replacing that status and emit a distinct completion witness on stdout.
4. In the parent, capture stdout/stderr, require a successful child exit and the completion witness, require the refusal token on stderr, and reject the optional trace token on stdout. Exit success alone can mean the test selector matched nothing; the witness makes that false positive fail.
5. Observe RED with the original missing fallback, then GREEN with the smallest production correction. For a Rust stderr fallback, discard an ordinary `std::io::Write::write_fmt` error deliberately instead of propagating it into runtime shutdown; keep the existing HUD and optional trace behavior intact. A writable-sink regression does not itself exercise a broken sink or prove bounded console latency.
6. Run the same maintained parent identity in debug and release through the source-bound receipt runner with an explicit producer deadline and bounded owned-process cleanup. Preserve any unreaped state rather than assuming timeout means cleanup. For example, use `terminal` in the checkout with `CARGO_BUILD_JOBS=44 cargo test --offline --lib refusal_reporting`, then the matching command with `--release`; replace the example filter with the actual test identity and verify that it ran. Give each invocation a fresh receipt label and retain the failed log.
7. Report the child as an internal entry exercised by the parent, not as an independent coverage increment. Record caller wiring/order as source-derived unless the actual loop ran; label a synthetic refusal and modeled status overwrite explicitly. Keep real worker, keyboard, editor, graphics and audio gates open where unexercised.

Completion criterion: the test invokes the actual production reporter in a fresh executable child, the discriminating parent fails before the correction and passes afterward in both profiles, and the claim does not exceed the executed stream/caller seams.

## 8. Qualify production headless callers

Use this recipe only when the task separately permits these executable checks. It exercises the actual built entrypoint and codec/publication caller without admitting the graphical game, editor or audio backend.

1. **Bind the executable and branch.** Verify the current production artifact's hash against its source-bound build receipt. Inspect `main`, argument parsing and any preparation function to identify exact help, malformed-input or conversion branches that return before window/audio setup. Select a refusal whose earlier guards are satisfied. Do not substitute a guessed unknown option: a permissive parser can ignore it and enter the game.
2. **Isolate and record each process.** Use a fresh private cwd, HOME, XDG directories and TMPDIR, omit DISPLAY/WAYLAND_DISPLAY, and supply no credentials or unrelated inherited environment. Capture raw stdout/stderr, exact argv/cwd, actual and expected exit, binary/source bindings, timeout and reap status in a receipt before evaluating assertions. Require the declared diagnostic or success witness, not merely any nonzero or zero exit. Keep an unreaped child as an execution blocker; environment omission is not a sandbox or proof of no device access.
3. **Establish a real positive conversion before refusals.** Have the actual executable create a new artifact in the owned fixture directory; read and validate it, then retain its complete original bytes and digest. Use flags from the inspected parser. For a runtime declaring `--house` and `--export-house`, the sequence is:

   ```text
   "$PLAYER" --export-house "$FRESH_A"
   "$PLAYER" --export-house "$FRESH_A"
   "$PLAYER" --house "$FRESH_A" --export-house "$FRESH_A"
   "$PLAYER" --house "$FRESH_A" --export-house "$FRESH_B"
   ```

   Require success for the first and last commands and the specific create-only refusals for the middle commands. Use only test-owned files, never user media as a destructive negative-control target.
4. **Verify preservation and the reopened caller.** After each refusal, compare the destination/input with the retained raw preimage. For the new-output reload/export, compare exact bytes where promised and validate decoded semantics separately. Check temporary-file cleanup and read back every declared output before publishing success. An earlier parse/load error is not proof that the no-replace boundary was exercised.
5. **Report separate coverage.** Keep production CLI/conversion cases separate from Rust testcase counts. A typed generated-house roundtrip does not establish arbitrary unknown-field/container preservation, actual editor edits, ordinary-input campaign completion, graphics/audio-device behavior or whole-port acceptance. Retain broader admission and independent-review gates.

Completion criterion: the current production executable reaches the intended pre-window branches, positive conversion/reopen succeeds, collision and literal source/output-alias refusals preserve the complete fixture, and every command has an exact source/binary/output-bound receipt.
