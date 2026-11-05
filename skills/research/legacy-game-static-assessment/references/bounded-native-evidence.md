# Bounded original-byte native verification

Use this recipe when canonical static tracing already exists and a qualified native provider needs a small, source-bound cross-check. It is not a full-image loader, Windows ABI, protocol or gameplay qualification.

## 1. Recover and admit the missing proof

1. Read the current checkpoint and source classification. Preserve media/evidence directories as non-Git inputs when appropriate.
2. Validate the named input and receipt bindings at the ownership-transfer boundary. Reuse successful parsing, tests and provider runs whose source/command/exit/log bindings still match; do not rebuild the workbench or repeat completed analysis to obtain a fresh summary.
3. Select the first missing comparison. Record a half-open original-VA window, its original file offset, architecture, byte count, raw-byte SHA-256 and scope: a complete selected body, an internal fragment, or a single instruction. Never describe an internal fragment as an established function entry.
4. Extract only exact original bytes into a new private target directory. Add no synthetic return, padding, imports or headers to make the provider happier, because altered bytes cease to be a control for the admitted artifact.

Generate canonical x86 disassembly with explicit boundaries and an unwrapped byte column:

```bash
objdump -d -M intel --insn-width=16 \
  --start-address="$LOW" --stop-address="$HIGH_EXCLUSIVE" "$SOURCE_PE"
```

Retain argv, cwd, stdout, stderr and exit. Verify that rows partition the declared window, each byte column matches the original file, and no row is truncated, `.byte` or `(bad)`. Use predecessor/prologue/return/padding and structural-flow evidence for function extents; the first return or a padding run alone does not define the body.

## 2. Reuse the qualified provider in a private analysis namespace

- Reuse the built runtime, matching Node/JDK/Ghidra toolchain, SDK transport and maintained process recorder. Adapt target paths and request selection rather than creating a second analysis framework.
- Mount the admitted raw targets, qualified runtime and toolchain read-only; expose only the new evidence directory for outputs. Supply private HOME, XDG cache/config/runtime and temporary paths, and set the JVM's `user.home` explicitly.
- Preserve the maintained network/filesystem isolation and choose an explicit per-job memory/CPU/deadline budget. Run one JVM/window at a time; serial analysis makes ownership, cleanup and resource attribution tractable.
- Do not weaken isolation or change host security settings when namespace/tooling admission fails. Preserve the exact failed command and a HOLD while continuing other permitted work.

Caller-supplied raw architecture and entry address are part of the analysis profile. A generic x86/gcc profile must remain labelled as such, even when the source was a Windows PE and the raw window starts at a historically supported entry.

## 3. Query the smallest useful native surface

For each admitted window, use the advertised schemas and this sequence:

1. `open_binary`: pass the raw path, `format=raw-binary`, the admitted architecture, original entry address and selected provider explicitly.
2. `read_function_instructions`: retain the full structured listing, function body ranges and limitations.
3. `inspect_native_instruction`: query the selected receiver/field, branch, call, cleanup and return anchors.
4. `resolve_native_call_targets`: query selected direct calls separately from unresolved computed calls.
5. `close_binary`: close in normal and error cleanup paths, then close the SDK transport.

Use the SDK client with the qualified runtime's package resolution and local stdio transport. Whitelist the admitted operations and refuse unadvertised tools. Persist and fsync each full structured response before advancing, plus per-call request, duration, error state and result path. Save only needed schema sections instead of dumping whole output schemas into supervisor context.

Keep progress advisory: the last progress file can still say `QUERYING` after close, while the final record correctly says complete. Qualification requires the final closed-session artifact, actual process exit, and no remaining owned descendants/threads—not the last progress status or a generic background notification alone.

## 4. Compare saved evidence, not PASS labels

Validate the source digest, architecture, provider/version and raw analysis profile on each compared envelope. Use `structuredContent`; a text presentation may be abbreviated.

For every selected instruction require exact agreement on:

- requested and returned address;
- decoded status;
- original bytes;
- instruction width.

Compare direct-call destinations against the signed displacement in the original canonical instruction. For an admitted five-byte x86 `E8` row:

```python
raw = bytes.fromhex(row['bytes_hex'])
assert len(raw) == 5 and raw[0] == 0xE8
expected = int(row['va'], 16) + 5 + int.from_bytes(raw[1:], 'little', signed=True)
```

Require the call-site address and static target list to match. A resolved static reference is not observed dispatch; do not convert an unresolved indirect call into a known runtime target from a nearby vtable alone.

Compare the complete native instruction-address set with canonical instruction boundaries contained in the provider-reported inclusive body ranges. Count selected byte checks, selected direct-target checks and listing-address matches separately; a large listing count is not proof that every listed byte or semantic interpretation was individually compared.

Preserve any difference between the canonical span and native body. A provider may exclude original no-op/alignment slots while retaining all selected anchors. Record the exact omitted addresses/bytes/instructions and keep the canonical span unchanged rather than trimming it to obtain equality. Do not demand textual mnemonic equivalence across disassemblers.

Test the saved-evidence verifier with explicitly synthetic mutations of source digest, decoded address, bytes, width and direct target. Assert both that validation was attempted and that each mutant was rejected. Retain these fixtures separately from real provider observations.

## 5. Recover completion across interruption or reboot

1. Reconcile managed ownership, saved worker metadata and current process/boot evidence before taking over. A cached running marker is not current liveness, and an owner-exit notification supplies no missing terminal result. Preserve the original worker outcome as unknown when completion proof is absent.
2. Snapshot the inherited relative paths, byte lengths and hashes in separate recovery evidence before changing an owned helper, report or control file. Record which paths the recovering executor may write; original media and frozen predecessor proof remain read-only.
3. Qualify completed suboperations individually. Verify the actual command/stage argv/cwd/exit and every declared log or structured-result hash. For disassembly captures, also verify the declared extent, canonical rows and exact original-byte match. An unknown enclosing worker outcome does not erase independently recorded successful captures. Reuse them instead of rerunning objdump, the provider or its JVM.
4. Inspect the saved helper before running it. If a derived result exists, use its recorded non-writing check command through `terminal`. If the result is missing and an implemented creation mode writes only new owned derived outputs, run that mode once, then its read-only replay. Use only supported flags and retain the actual interpreter, argv, cwd, exits and complete logs; do not silently overwrite a completed trace.
5. Characterize inherited helper behavior with focused positive and negative controls before changing it. Exercise byte mismatch, omitted/noncanonical rows, signed direct-target checks and the check path's mutation guard where relevant. Label these as retrospective characterization or synthetic validation, not prior test-first development or game execution.
6. Compare inherited hashes after recovery, explain every permitted delta, and write a handoff distinguishing reused captures from newly executed parent finalization/tests. Keep independent acceptance pending until a fresh terminal verdict covers the resulting frozen slice.

For a previously completed provider stage, require its retained close/session/exit evidence as well as source bindings. A later comparison replay validates saved responses; it is not new native execution. A changed boot ID proves old processes cannot survive, not that an unfinished stage completed or timed out.

## 6. Freeze a reviewable tranche

1. Finish the assessment, helper/tests, machine-readable trace, handoff and existing verification receipts. Identify code-derived claims, native observations, assumptions, provider limitations and unknowns before assigning a final inventory.
2. Keep reused captures/tests, newly executed recovery commands, comparison replay and synthetic controls separately attributed with exact commands/exits/logs. Validate each receipt's actual schema rather than assuming every check has a stdout/stderr pair.
3. Build both an exact path inventory and the immutable path/size/hash set. Prune only named disposable runtime directories before traversal. List any parent-owned live-control path explicitly, retain its name in the exact inventory, and exclude only its mutable contents from proof hashes. Do not exempt broad filename patterns. State separately the hashed-file count, manifest self-exclusion and total inventory count.
4. Run the supported read-only replay against that finalized inventory, using `terminal` with the recorded interpreter and working directory. Where the helper supports `--check --manifest`, exercise both source regeneration and inventory validation together. Store this invocation's logs/receipt outside the candidate tree so recording the result cannot create an unexpected file or change a hash-bound receipt.
5. Give the independent reviewer the manifest fingerprint, exact admitted check commands, named external receipt bindings and a separate output directory. Require source inspection of hand-written semantic claims: an admitted instruction address or passing byte assertion alone does not prove its receiver, branch condition, argument order or effect.
6. After the terminal verdict, recheck source hashes and preserve the full structured delivered result and completed runtime metadata. Put any new acceptance/correction record outside the frozen pending packet; update only the explicitly mutable parent-control record to link it.
7. Keep acceptance tranche-scoped. A local proof or independent PASS supplies no missing server executable, dependency omission, Linux/Docker compatibility or playable-LAN result.
