# Process and observer recovery

Use when a control-plane shell stalls, a final API error arrives while owned helpers remain alive, or an interrupted owner must hand its checkout to a successor. This is a recovery procedure, not permission to cancel slow useful work or change host settings.

## 1. Separate the failing observer from the executor

Read the private lane metadata and final-result/exit artifacts through an available file tool. For several recovered lanes, batch their records and compare them with one current boot-ID observation before querying old terminal handles. On a boot mismatch, preserve unknown exit/result fields and proceed to the prior-generation ownership checks in section 4; polling each obsolete handle cannot reconstruct a lost exit. On the same boot, a missing handle is only a lost control-plane reference: inspect the recorded PID/start ticks, descendants, session and checkout before declaring ownership released. Never report a lane as currently running from its saved `state` alone, because a reboot can leave that field unchanged.

If a simple foreground shell command repeatedly times out, classify the failing layer from retained diagnostics before selecting another transport. For an established shell-startup or quoting failure, test a bounded already-authorized direct executable through `execute_code` using Python's `subprocess.run([...], cwd=..., capture_output=True, text=True, timeout=...)`; resolve the executable first, use an argv list rather than `shell=True`, and print only exit and bounded diagnostics. If a pre-execution ownership/admission guard is blocked or ownership remains unresolved, use available file/metadata observations instead of routing the same execution through another shell or subprocess path. A successful permitted direct probe establishes only an alternate control-plane path, not executor completion. Retain the original failures.

When a managed shim reports unrelated tool-resolution or TLS failures, use its observed selected installed CLI path to locate the native executable, record the symlink/wrapper chain, and run bounded native version/auth-metadata checks without changing global configuration, certificates or authentication. Do not guess an installation path or infer that a later native success proves the cause of an earlier hang. Keep native metadata readiness separate from actual provider availability: a subscription-authenticated Opus lane can still be rejected by a five-hour limit after useful reads. Preserve the provider's limit type, reset epoch/timezone, no-overage status, session and completion quorum before transferring ownership; do not retry before the observed reset.

For short CLI preflights, capture stdout/stderr in private regular temporary files and use a separately bounded `Popen.wait`. An inherited PIPE can remain open in a descendant after the direct child exits, so waiting for EOF is not the same as observing top-level completion. Record the preflight PID/generation and actual exit; bound output reads and retain only necessary route metadata, not raw account or credential payloads. Keep a synthetic inherited-descriptor fixture distinct from actual CLI/provider success, and do not infer that a later successful capture establishes the cause of earlier host hangs.

Do not infer that a kernel pseudo-file is empty from `st_size == 0` or an empty generic-file preview. Verify a required `/proc` value through a separately bounded direct read before treating it as absent or corrupt; keep any original viewer limitation visible.

Use direct `/proc` reads for the owned process tree when shell startup itself is suspect. Do not source generated shell snapshots to inspect them, dump environment/snapshot contents, or edit shared shell configuration merely to unblock supervision. Keep execution within the same approval and filesystem boundaries; a direct subprocess is not an approval bypass or a sandbox.

### Permission-probe-to-implementation handoff

Use this recipe when a lane needs a permission probe, not as an extra provider call on every continuation.

1. Prepare the actual task and a separate minimal probe packet before starting. Give the probe the intended cwd and evidence directory, the same Opus-Max environment/flags and normal permission mode as implementation. Ask it to use `Write` for a fixed marker file inside the admitted evidence directory, then `Bash` for a harmless explicit-interpreter assertion of those exact bytes that prints a distinct success marker. A version check alone does not exercise either write or command permission.
2. Capture probe stdout/stderr, session UUID, initialization, tool outcomes and exit under probe-specific filenames. Require exact file-content readback, the command's successful tool result and marker, a non-error final result, observed top-level exit zero and no remaining owned descendants. A marker merely quoted in the prompt or final prose is not command execution.
3. Recheck source ownership, then resume the captured UUID with the prepared real task. Repeat the model, effort, evidence-directory and permission flags; retain all existing billing and source guards. Keep implementation transcript, exit and handoff filenames separate so they cannot overwrite the probe. The invocation shape is:

   ```sh
   export ANTHROPIC_MODEL=opus
   export CLAUDE_CODE_EFFORT_LEVEL=max
   export CLAUDE_CODE_SUBAGENT_MODEL=opus
   # Execute both through the tracked lane runner.
   claude -p --name "$LANE" --add-dir "$EVIDENCE_DIR" \
     --model opus --effort max --permission-mode auto \
     --output-format stream-json --verbose < "$EVIDENCE_DIR/PROBE.md"
   # Only after probe completion quorum and ownership checks:
   claude -p --resume "$SESSION_ID" --add-dir "$EVIDENCE_DIR" \
     --model opus --effort max --permission-mode auto \
     --output-format stream-json --verbose < "$EVIDENCE_DIR/TASK.md"
   ```

4. On denial, preserve the exact blocked operation and classify it before one permitted scope/configuration correction; do not change actors or bypass permissions. Start a different session only when the original is unusable or incompatible under the existing recovery rules. Never reuse an independent review session as an implementation owner.
5. Report the probe only as permission/readiness evidence. Its successful write, model initialization and command do not establish product tests, source acceptance, installation or live behavior; the implementation must produce its own source-bound proof.

## 2. Establish what is still owned

Start with `/proc/PID/stat` and `comm`, identify the tracked generation and PPID descendants, then enrich only relevant owned processes with required PGID, cwd, executable and thread observations. During task-lock stalls, do not read every D-state process's `cmdline` or `maps`: those reads can wait on task memory locks and wedge the observer itself. Classify `stat` and `comm` before opening task-memory-backed files; reading `cmdline` first to decide whether a process is relevant defeats that protection. Add a negative control where an unrelated D-state process raises if its command line is opened. For a parent-released frozen reader snapshot, use retained attempt/session generations and narrowly scoped Claude ownership checks; keep any reader-only adaptation explicitly restricted to Read/Glob/Grep rather than silently reusing it as an implementation guard. Preserve a bounded metadata-only record and leave unavailable identity fields unknown; obtain additional binding data only for an exact owned target through a separately bounded observation when necessary. Exclude the inspector and its known ancestors, not entire process classes. Print only relevant metadata. A tool shell can have a different PGID from Claude, and an inherited stdout descriptor can keep the wrapper waiting after a final result.

During observed procfs/task-lock stalls, avoid host-wide cwd/symlink-resolution walks: even read-only process inspection can block. Prefer retained producer identities and narrowly scoped artifacts. If bounded cwd inspection and even `/proc/locks` reads hang, preserve unreconciled ownership and stop new compiler/native probes rather than accumulating inspectors or assuming the old owner exited. A tool timeout is not an observed child exit or permission to restart shared services.

Keep ordinary remote-model waits RUNNING. A final provider error can classify a lockout without establishing completion quorum; do not transfer source ownership on that result alone. Inspect a particular child command only when needed to explain the wait, with secrets excluded.

## 3. Cancel only when cancellation is justified

For a confirmed hard lockout with a stuck owned helper, an explicit stop, or another established termination condition:

1. Preserve the provider error/result and source checkpoint before signalling.
2. On Linux, acquire `os.pidfd_open(pid)`, then validate the recorded boot, start ticks and executable/command binding. Use `signal.pidfd_send_signal(fd, signal.SIGTERM)` for that exact process, because numerical PID reuse can target unrelated work. Validate and signal separately grouped owned helpers individually; do not assume the leader's PGID covers them.
3. Allow a bounded grace/reap interval. Escalate to SIGKILL only for a still-bound owned process when justified. Never signal a newly reused PID or unrelated user process.
4. Inspect remaining descendants and `/proc/PID/task/*/stat`. Preserve live or unreaped threads as incomplete recovery; do not loop indefinitely or reboot without approval.
5. Obtain the tracked top-level exit receipt and verify the final result independently. A termination exit describes cancellation, not the provider's original error.

## 4. Transfer at a clean boundary

1. Resolve the old process generation before transferring ownership. On the same boot, require the tracked top-level exit, no remaining owned descendants and final-result presence or explicit absence. After a verified boot-ID change, record reboot interruption and any missing exit/result as unknown: the old generation cannot survive, but its termination status cannot be reconstructed. Check for new conflicting owners before launching a successor.
2. Inspect the preserved source and artifacts against their recorded bindings. Separate completed proof, interrupted work and never-attempted obligations; a changed boot invalidates live process identity, not hash-identical source or completed receipts.
   Before assembling a successor, record a generation table for production modules, selected tests, shared fixtures and generated/installed outputs. Prefer a complete source-bound successor archive; otherwise reconstruct the pinned base plus every intervening admitted repair in a new private candidate. Do not seed an older GREEN tree and copy only the newest fix over it, because that can restore defects already repaired in another generation. Keep original snapshots immutable and label the reconstructed composite as a new candidate until its own proof and required review complete.
   Check the maintained test's import, fixture and renderer-input closure before the full matrix. Verify code-only contracts consumed through AST/literal extraction as well as imports: a sibling module can exist while lacking the constant or schema key its generator requires. Record these mismatches, missing modules and absent selected test methods as materialization/discovery errors, not behavioral RED. Restore the provenance-matched support component and its fixture closure in a new private composite; verify every later owned production/test byte remains intact outside that explicit support replacement, and record both origins. Matching a few constants or copying the newest fix onto an older tree is not generation preservation. Run the smallest real generator boundary before the broader matrix, and require each behavioral regression to reach its intended assertion; matching setup refusals do not prove compatibility.
   Recover a zero-byte helper from a retained full tool-write payload when available instead of inventing a plausible replacement. Bind the source session/message, exact tool/path/content and digest; check for later edits before restoring, preserve the damaged preimage, and distinguish source restoration from proof that those bytes executed. Keep successful command/log/runtime bindings reusable independently, and do not blindly rerun a restored producer that overwrites retained receipts or fixtures.
3. Capture a fresh current-boot checkpoint and explicit parent ownership release. If the predecessor is frozen, leave its stale RUNNING/owner/route fields untouched; name them as superseded in the new control record, identifying exactly which ownership or executor decision changed. Do not rewrite the historical outcome.
4. Choose resumption separately for each lane. Locate the exact session UUID under the recorded Claude projects root and verify usable, nonempty session content independently of the supervisor's transcript. Resume a compatible surviving session; for a confirmed absent, zero-byte or malformed session, preserve the damaged artifact and start a fresh session with the same validated source checkpoint and unfinished scope. A surviving transcript preserves partial evidence, not resumability or a terminal verdict.
5. Assign only remaining admitted work to one successor. Carry an exact source-bound failing check as its first obligation, or select the first missing check when the retained proof passed. Require an early draft handoff with that check's actual result and the next maintained execution command before new harness construction or broader discovery. Keep source-only discovery, executed proof and implementation progress separate in status reports; an initialized replacement is not a completed recovery.

### Resume an interrupted verification batch

After the ownership and source checks above:

1. Inventory every expected case as completed-and-bound, interrupted, setup-failed or never dispatched. Record missing/unreadable receipts explicitly while continuing to validate intact sibling results; a wrapper exit or missing receipt is not an observed test-child exit.
2. Reserve a fresh attempt namespace for every retry, covering private HOME/XDG/TMPDIR roots, logs and receipts together. An interrupted runner may have created only its private directory before dispatch, so checking that a receipt or log is absent does not make the old label reusable. Preserve the partial attempt instead of deleting it or enabling overwrite.
3. Run only missing or invalidated checks with the same admitted source and isolation, using fresh labels mapped back to the original case identities. Persist setup failures separately from child command/exit evidence; require the recorded nonempty test population before reporting a pass. Retain valid completed checks without repeating them for a cleaner batch summary.

Compare paired recovery receipts by the recorded argv, selected fully qualified testcase identities and relevant environment, not by lane-specific display labels. Keep raw labels unchanged and build an explicit baseline-to-candidate comparison map; prefixes such as `base-` and `fixed-` describe provenance and otherwise make equivalent checks look absent from both sides. Count distinct cases in code, retain unmatched checks explicitly, and require the expected assertion failure rather than an import error or unknown test name before crediting RED.

Reconcile delayed notifications by attempt/session identity; a notice about the old owner must not restart or disturb its active replacement. Keep task status, ownership and recovery evidence in private durable artifacts. Do not treat a missing in-memory variable, an empty process list, a successful probe or a queued completion callback as a complete handoff.
