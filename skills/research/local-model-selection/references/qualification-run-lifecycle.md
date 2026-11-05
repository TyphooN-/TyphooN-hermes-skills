# Qualification run lifecycle

Use for multi-gate local qualification, maintenance contention, long-running launchers, or recovery after the host or control-plane handle disappears. This recipe establishes execution ownership and evidence attribution; it does not certify a model or guarantee reboot survival.

## 1. Freeze the actual requested scope

Before planning a command, recover the latest approved outcome: formal qualification or explicitly diagnostic-only evaluation. Keep an approved diagnostic exception local to that attempt; do not translate it into a formal admission contract, shared waiver or policy rewrite. Point the executor at retained accepted-source evidence and only the missing runtime obligation, because restarting implementation/review consumes the execution allowance without testing the model.

For a fixed diagnostic pack, pin actual case IDs, serialized messages, role budgets and validators before dispatch. Account for each ID as attempted/pass/fail/inconclusive/not-run with a concrete reason; retain outputs privately and leave formal caches, receipts and routing unchanged. Continue independent remaining cases after a semantic failure only while identity, ownership and safety checks remain valid. A diagnostic report must not imply a maintained gate passed.

1. Enumerate configured aliases mechanically, separating chat/vision from embedding, reranking and FIM roles.
2. Read the maintained supervisor's help and run its read-only plan for every proposed invocation. Validate the actual JSON shape and required coverage fields before deriving totals: defaulting absent keys to zero/empty lists can falsely turn a parser defect into a successful coverage report. A preview need not emit live endpoint/provenance fields.
3. Compare the planned union with the requested gate and alias manifest. Some model selectors intentionally remove non-model gates; split those into separate serialized invocations instead of assuming that an all-gates argument survived parsing.
4. Record expected, scheduled, blocked and deferred scope separately. Map a suspect artifact to all dependent aliases and workflows without calling unaffected tests blocked.
5. Freeze source HEAD, initial dirty state, boot ID, relevant presets/runtime bindings and private evidence paths. Avoid changing qualification inputs during the run; source-backed research can continue in separate evidence artifacts.

### Reconcile artifact availability before allocating runtime

1. Read the preset and artifact-record schemas before projecting fields. Join each selected preset's literal full weight path to recorded file destinations, repository/revision, expected bytes and published digest. If the executable inventory deliberately omits research candidates, inspect their separate transfer manifest and state without adding them to the executable inventory or treating download approval as qualification.
2. Observe current file metadata for the exact primary, complete shard set and relevant companions. Record missing paths, file type, device/inode, byte length and modification time; classify symlinks separately rather than calling an `lstat` result a verified regular target. Similar basenames or same-directory files are provenance leads, not authorized substitutions. Do not read weight contents for this metadata-only stage.
3. Reconcile historical download status against those observations. Preserve a stale `complete` record and report the missing primary or companion explicitly. Decide companion necessity from the exact role/profile: missing MTP blocks an MTP-dependent comparison, and missing projection weights block the corresponding vision path, but neither automatically rejects an independently admitted ordinary-text variant.
4. Save input-metadata hashes, observation time/boot and per-alias outcomes in private planning evidence. State whether writer locks were held; without them, an unchanged before/after metadata snapshot remains an observation, not a serialized integrity verification. Keep publisher digest syntax, observed-size equality, validated reuse of an earlier content-hash receipt and fresh content hashing distinct.
   - Across boots, do not use equality of `st_dev` as persistent file identity: mount generations can change it. Preserve raw snapshots, compare filesystem UUID/subvolume and stable inode/size/timestamps when available, and keep a missing historical persistent identity or content digest explicitly unproved rather than declaring changed content or a full identity pass.
   - Before calling preset differences configuration drift, resolve documented option-name equivalences from the served source, such as `temp`/`temperature`, `embedding`/`embeddings` and `gpu-layers`/`n-gpu-layers`. Preserve literal inputs and values, bind the equivalence source, and correct only the observer projection; do not mutate the live preset to satisfy it.
   - Distinguish a missing weight-file process mapping from a demonstrated artifact mismatch. Preserve a required mapping-based attestation at HOLD when its evidence is absent; a matching API path or file metadata neither replaces that gate nor proves served bytes.
5. Carry availability gaps into the comparison manifest as concrete not-run reasons. Do not download, rename, replace or reconfigure artifacts to conceal them under metadata-only authority; those actions retain their separate approval and admission gates.

### Validate device identity and placement

Use this branch only when execution/hardware inspection is in scope, not for intake-only registration.

1. Join observed runtime devices to physical devices using validated unique PCI/UUID identities, not ordinal positions. Inspect a UUID's actual representation before decoding: a 16-byte HIP value can be 16 ASCII hexadecimal characters matching a KFD serial rather than a binary RFC 4122 UUID. In that case compare the exact serial together with PCI identity; do not guess an endian conversion. A standalone probe's mapping does not establish the serving process's effective device visibility.
2. Read the effective preset's devices, tensor split, context and cache types. A zero split component excludes that device from ordinary layer placement even when physically present. Recompute and exercise placement when a higher-fidelity artifact needs previously unused cards rather than only swapping the weight path.
3. Expand the complete selected shard sequence even when the preset names its first shard. Verify expected presence/count and sum those files, not alternative quantizations, archives or adapters. Budget weights, KV, encoders/projectors, workspaces and display headroom per participating device. Aggregate physical RAM plus VRAM is an impossibility screen, not a placement plan or permission to pool heterogeneous memory.

## 2. Establish exclusion without changing policy

1. Check live ownership through the maintained preflight. An operator-declared available slot authorizes the attempt, not a resource-threshold waiver or an assumption of exclusive router access. Treat zero GPU utilization as quiescent compute, not empty VRAM; inspect resident aliases and active slots before admission. Once that authorized preflight passes, do not repeatedly seek permission merely because an idle model remains resident.
2. Trace maintenance jobs to their actual lock implementation and exact lock path. A low-priority hasher can still compete heavily with inference, and a Python process may escape a name-based conflict classifier.
3. Acquire the same cooperative maintenance lock before starting the native supervisor. For a verified Linux `flock` contract, use a regular non-symlink lock file, `fcntl.flock(fd, LOCK_EX | LOCK_NB)`, and refuse admission if busy. Do not replace this with a racy PID check or invent a different lock that the maintenance job never takes.
4. When a nonblocking flock refuses, trust that refusal rather than an empty `/proc/locks` join. On Btrfs, the device number shown by `/proc/locks` can differ from the lock pathname's `st_dev`; narrow candidates by inode, then confirm the candidate owner's FD with `samefile(lock_path)`. Use `fuser -v "$LOCK_PATH"` to corroborate open-file ownership and the process cgroup or `systemctl --user show "$UNIT" -p MainPID -p ActiveState -p SubState` to identify its service. Treat `fuser` or an open FD alone as evidence of an opener, not proof that it holds the lease; retain the flock refusal and matching lock record. Never infer that the lock is free from a failed device-number match, and never replace/unlink the lock or stop its unrelated owner to obtain admission.
5. Hold the descriptor across the entire batch, including gaps between supervisor invocations. Release it in cleanup and preserve an explicit release/interruption observation.
6. Leave native qualification admission and validators unchanged. These locks coordinate participating jobs only; do not claim they reserve GPUs against arbitrary clients.

### Apply no-wait steering without inventing admission

1. Identify a queued wait by its saved boot, PID/start identity, group and command. Cancel only that owned wait, preserve its state, and confirm no descendant remains before launching a successor; cancelling a handle alone is not ownership release.
2. Attempt required cooperative leases with `LOCK_EX | LOCK_NB`. On a busy result, inspect only enough ownership evidence to name the blocker; do not repeatedly relaunch the same refused command or substitute a blocking flock and timeout for the user's no-wait instruction.
3. Apply an explicitly authorized advisory scheduling exception only to the private diagnostic attempt. Record what exclusion was omitted and the resulting timing/interference limitation; keep actual inference ownership, memory, identity and client-busy checks intact. Do not change formal admission, delete lock files or stop the unrelated owner.
4. Close with exact case IDs, actual dispatch counts, native exits and the verified cleanup result. Cases refused before inference are `not-run`, not wrong answers or passes; distinguish wrapping up execution from completing qualification.

### Load only the authorized alias and verify readiness

For a llama.cpp router whose maintained API documents these endpoints, reduce `GET /models` to each alias and `status.value` before loading. If the selected alias is already loaded and otherwise admitted, proceed without repeating the load or approval. If another alias or inference client owns the slot, preserve it rather than unloading it.

When the slot is empty and the user authorized loading the existing alias, send one `POST /models/load` with the literal body `{"model":"<authorized-alias>"}`. Use a bounded loopback client, JSON content type, explicit request deadline and capped response size; do not invent an async flag or turn autoload on. An HTTP 200 response with `{"success":true}` establishes load acceptance, not readiness: read back `GET /models` until that alias's `status.value` is `loaded` within the attempt's deadline. Save the response and readback under the observed boot. If the client times out, inspect load state before retrying, because the server may still be loading after the socket closes.

Keep preset mutation, artifact download, routing activation and capability evaluation separate from this control operation; a successful load response does not prove any of them.

## 3. Use a bounded owned launcher when needed

Prefer the normal managed execution path. If a long run must remain owned independently of the terminal launcher within the authorized task, an isolated transient user service provides a concrete cgroup and deadline. The exercised command shape is:

```sh
systemd-run --user --wait --unit="$UNIT" \
  --property="WorkingDirectory=$EVIDENCE_DIR" \
  --property="StandardOutput=append:$EVIDENCE_DIR/unit.log" \
  --property="StandardError=append:$EVIDENCE_DIR/unit.log" \
  --property="RuntimeMaxSec=6h" \
  --property="TimeoutStopSec=90s" \
  /usr/bin/python3 "$EVIDENCE_DIR/run_batch.py"
```

Choose a unique owned unit, an observed absolute interpreter, and an appropriate task-sized deadline; the shown deadline is not an admission override. The runner must record each native command, child PID/PGID, exact exit, boot and evidence path, and forward cancellation to its owned children.

Track the waiting launcher with native completion notification, then read back the exact target:

```sh
systemctl --user show "$UNIT.service" \
  --property=ActiveState,SubState,MainPID,ControlGroup,Result,ExecMainStatus
```

An active unit is launch evidence, not a pass. `Result=success` while it is running is not a completed result. A transient service does not automatically resume after reboot. Do not enable persistent startup, alter unrelated units or weaken permissions merely to keep the task alive.

## 4. Preserve progress and classify slow work

- Save run-specific logs and receipt/state snapshots at completed boundaries before another invocation can overwrite the canonical artifacts.
- Prefer completion signals over model-turn polling. At a decision-changing check, inspect only owned PID/cgroup state, CPU-time advancement, log growth and the current native gate.
- Do not call a gate stalled because the supervisor's step timestamp is unchanged: many supervisors update only at dispatch and completion. A running child with meaningful CPU progress and growing kernel-selection or warm-up logs remains active work. Treat transient loader D-state separately from an established host stall; correlate owned process start/CPU/log progress and the actual gate before escalating, because model-loading I/O can briefly be uninterruptible without proving a fault.
- Treat warnings as diagnostic evidence, not the terminal verdict. In particular, workspace-selection warnings alone establish neither a TTS pass nor failure; retain the exact eventual result and exit.
- Keep capability, load, memory recovery and interruption outcomes separate. A failed RAM-recovery check is not automatically a wrong-answer failure.

## 5. Recover after disappearance or reboot

1. Read durable launcher records before retrying. A missing terminal handle is lost control-plane state, not a successful task.
2. Compare `/proc/sys/kernel/random/boot_id` with the saved boot. Across a confirmed reboot, original processes and descriptors are gone; record an unknown interrupted exit unless a genuine final receipt survived.
3. Inspect current managed units and their scopes before launching. Auto-started qualification can replace shared state after login; its results do not complete the interrupted manifest automatically.
4. Diagnose the old run using its unique logs and the journal. Obtain the journal's literal boot identifier from `journalctl --list-boots`, then use it in `journalctl --boot=<journal-boot-id>`; an invalid selector is a failed probe, not evidence that no crash was logged.
5. Keep causation bounded: a reboot during shard loading plus no recorded shutdown or kernel fault does not prove the model or loader caused it.
6. Refresh topology, resource/admission state and router residency. Start a new uniquely recorded run only after ownership is released. Resume unattempted independent gates rather than blindly replaying a repeatedly interrupted stage.

## 6. Close against receipts, not activity

Reconcile actual exits and exact alias/gate identifiers against the frozen manifest. Label fresh passes, validated reuse, failures, inconclusive results, admission refusals, interrupted work and integrity blocks separately. Preserve prior-boot evidence without calling it a current-boot exercise. List still-running work and review/acquisition blockers explicitly; collected source metadata, a launcher notification and an active service never close the qualification goal by themselves.
