# Btrfs / Arch integrity evidence patterns

## Interpretation examples

- A scrub reports `finished` and `no errors found`, while `corruption_errs` is unchanged before and after: report a clean completed scrub with a historical counter, not residual damaged files inferred from that counter.
- A later collector can capture a newer scrub at `running`. Preserve the start time and progress: the older clean result cannot establish that the newer run finished cleanly.
- `/`, `/home`, cache, and logs may share one encrypted Btrfs filesystem; a scrub covers them collectively. Separate FAT `/boot` needs separate assessment. Confirm mappings live.
- `Data,single` with `Metadata,DUP` means one data copy and duplicate metadata on the device; it is not device-failure protection.
- `btrfs check --repair` followed by `exactly 1 argument expected, 0 given` is argument validation failure. `enabling repair mode` alone does not establish a repair. Do not supply the mounted root device to fix this invocation.
- Defragmentation is rewriting, not verification. Leave user-owned processes undisturbed and account for I/O contention.
- SMART can show a cumulative error-entry count while the currently readable detailed log contains no entries. Report both without inventing a media failure.

## Counter and snapshot cleanup decision sequence

1. Capture `btrfs device stats <mountpoint>` before cleanup and preserve the completed scrub report. Do not convert `corruption_errs` into a file count: the same damaged extent may produce multiple events across repeated reads.
2. Check for an existing scrub or repair-script process before starting verification. If the user is already running one, observe its final report rather than adding another filesystem-wide scan. A permission-denied status query means status is unavailable to that caller, not that the scrub stopped.
3. Reconcile the exact saved scrub-path set with deletion receipts and current identity checks. Keep the number of logged paths, successful deletions, already-absent paths, identity changes, and failures distinct. Never count previewed paths as deleted.
4. If a completed scrub still finds damage after live-file cleanup, map its logged root/subvolume IDs to live subvolumes or snapshots. Group checksum records by verified filesystem/device and logical/physical range; the same range reported under several snapshot roots can be one damaged extent with multiple references, not several independent corruptions. Keep extent, root/inode/path, and scrub-error counts separate. Check the exact live path using no-follow identity traversal; an absent live artifact requires no further live-file deletion or invented successful read. Snapshots and reflinks can retain damaged shared extents after a live-path unlink. Do not delete unrelated snapshots just because counters remain nonzero.
5. Preserve useful recovery copies and request the applicable approval for specific snapshot deletion. Removing all references to a damaged extent may allow it to be freed; it does not restore lost content or diagnose the cause of corruption.
6. Wait for authorized deletion cleanup before running one verification scrub. Use `btrfs scrub start -Bdr <mountpoint>` for a foreground read-only verification; preserve its own exit status, final summary and before/after device counters. Check installed documentation for exit semantics: in btrfs-progs, exit 3 denotes uncorrectable errors, not successful repair. Report current uncorrectable errors and the counter delta separately. Withhold replacement baseline snapshots unless verification finishes cleanly without counter increases; do not infer success from removed paths alone.
7. If verification remains unclean, extract the next inventory from that run's bounded kernel journal window rather than immediately repeating the full scrub. Prefer stored journal cursors; if only start/end times survive, verify the boot identity and exact completed-scrub interval before using `journalctl -k -b <verified-boot-id> --since <start> --until <end> --no-pager -o json`. If the boot is not yet identified, collect the bounded interval with `journalctl _TRANSPORT=kernel --since <start> --until <end> --no-pager -o json` and reconcile boot IDs before using records for cleanup; bare `-k` or `-b` selects the current boot and can miss the scrub. Preserve the raw records and pair same-device/logical checksum and regular-file fixup failures. Count unique candidate identities programmatically, restrict deletion to the authorized path class, and preserve absent, rebuilt/readable, replaced and ambiguous files as separate outcomes. Never widen from confirmed generated objects to their entire build tree without authorization.
8. Treat scrub error totals, captured checksum records and unique damaged paths as different quantities. Kernel/journal suppression or incomplete records can leave the path inventory smaller than the error total; deleting every recovered candidate is not filesystem clearance. A subsequent scrub can reveal additional previously unidentified objects without proving they were newly corrupted. Carry the existing cleanup authorization forward within its exact scope, but require new approval for newly implicated source, user data or unrelated snapshots.
9. Preview with the same no-follow identity/read validation used by deletion, save each mutation receipt, and read back exact deleted targets. Confirmation reads can produce more checksum events, so capture the next verification counter baseline only after cleanup and filesystem sync. Compare the completed verification scrub against that baseline, not against the pre-preview counter.
10. Only after saving the evidence, offer `sudo btrfs device stats -z <mountpoint>` as optional bookkeeping. This displays and resets all device-error counters for the filesystem; it does not repair data, metadata, hardware, RAM, or kernel defects.

## Snapper inventory, reset and replacement recipe

1. Inventory both management records and actual Btrfs snapshots: `snapper --jsonout list-configs`, `snapper --jsonout -c <config> list --disable-used-space`, and `btrfs subvolume list -s <mountpoint>`. Also inspect the live root ID, `btrfs subvolume get-default <mountpoint>`, and mounted subvolume sources. Reject active/default or mounted rollback snapshots before deletion. Snapshot number zero represents current state, not a deletable snapshot.
2. Reconcile Snapper numbers with Btrfs IDs and paths. Factory/recovery snapshots may exist outside Snapper; an explicitly authorized all-snapshot reset must account for those without treating every live subvolume as a snapshot. Freeze the inventory and stop if identities or ownership change before mutation.
3. Delete managed snapshots through `snapper -c <config> delete --sync <numbers>` so metadata stays consistent. Preserve explicit approval for those configuration-specific snapshot numbers: removing a home snapshot discards that entire rollback point, not just its damaged artifact. For an explicitly authorized unmanaged snapshot, inspect installed `btrfs subvolume delete --help`; its `--dry-run` and `--subvolid` route can preview and delete by verified ID through an existing filesystem mount without mounting the top-level tree, using `--commit-after`. After either route, wait with `btrfs subvolume sync <mountpoint> <verified-deleted-subvolids...>` and save its own exit and removal receipt; disappearance of the directory alone does not establish that extent cleanup finished.
4. Re-read both inventories to verify exact removals and preservation of live/default subvolumes and unrelated snapshots. Where boot menus expose root snapshots, use the installed integration tool and verify its resulting references; inspect hooks and avoid unrelated initramfs/kernel/reboot work.
5. Complete the cleanup/verification gate before creating repaired-baseline replacements. Kernel scrub root IDs that map to a read-only snapshot explain why live-file cleanup reports skipped paths. Do not make the snapshot writable or redirect those paths into the live tree; seek authorization to remove that contaminated snapshot, verify again, and replace it only if clean.
6. For a separate home subvolume, first inspect existing configs, nested subvolumes and `/home/.snapshots`; preserve existing ownership and never overwrite an existing snapshot tree. If absent, create the managed scope with `snapper -c home create-config --fstype btrfs /home`. Read the installed default template, disable `TIMELINE_CREATE` unless scheduled snapshots were requested, and choose explicit retention consistent with existing policy. Do not grant additional users/groups or alter ACL policy merely to simplify access.
7. Create an explicit read-only single snapshot with `snapper -c <config> create --type single --read-only --print-number --cleanup-algorithm number --description <label>`. Read back the returned number from Snapper, inspect `btrfs subvolume show <snapshot-path>`, verify `btrfs property get -t subvol <snapshot-path> ro` reports `ro=true`, and commit with `btrfs filesystem sync <mountpoint>`.
8. Report each scope, snapshot number and path separately. Root and home snapshots taken separately are not an atomic application-consistent pair, and neither is an independent backup. Leave unchanged workloads running unless stopping/quiescing them is authorized; state the resulting consistency limitation.

## Package-audit anti-patterns

Preserve unfiltered output and exact exit status. A pipeline selecting only checksum/size warnings and printing success for an empty list can conceal missing files, unreadable paths, and operational failures.

Merged stdout/stderr may contain:

```text
cups-filters: 83 total files, 0 alwarning: filesystem: /boot (Permissions mismatch)
```

Anchored matching (`^warning:`) misses that warning. Extract occurrences anywhere in a line, for example `re.findall(r'warning: ([^\n]+)', text)`. Preserve the original log and distinguish backup-file reports from non-backup warnings.

A completed privileged audit with exit 1 may have no content-checksum or size failures: mode, group, timestamp, and file-type differences can account for the result. Classify before repairing:

- SHA256/MD5 or size mismatches outside backup configurations: investigate against trusted package originals.
- Missing files or failed checksum calculations: separate absent paths from verification failures; an unprivileged permission denial is not damaged content.
- Backup configurations: preserve intentional local changes, especially account/authentication/firewall settings.
- `/etc/resolv.conf` symlink to systemd-resolved: verify link metadata/target, not credential contents.
- Icon symlinks to another installed theme: a type substitution, not automatically corruption.
- FAT `/boot` mode differences: inspect mount masks; do not try to normalize modes as if FAT stored Unix permissions.
- Runtime directory groups, setgid helpers, service configuration modes, and modification times: report observed metadata separately; investigate before changing permissions or security settings.

Do not label every metadata difference expected without checking its source and purpose.

## Exact-version package-content repair

Use this recipe after the complete package audit identifies a non-backup content mismatch and package repair is authorized. A clean Btrfs scrub does not establish package-original content: the filesystem may faithfully checksum bytes that differ from the package reference.

1. **Freeze the repair scope.** Preserve the full audit and exact exit. Select packages with confirmed content damage, not every package associated with a warning. Preserve backup/configuration changes and investigate known local binary modifications before overwriting them. Use the existing installed checker when its coverage is sufficient; do not delay a demonstrated repair by commissioning a redundant auditor.
2. **Find a matching source without upgrading.** Capture `pacman -Q "$pkg"` and inspect `pacman -Sp --print-format '%n %v %l' "$pkg"`. The latter reports package selection, not source authenticity. Inspect a candidate cached archive with `bsdtar -xOf "$archive" .PKGINFO` and require the installed name, version and architecture. If only a newer version is available, obtain a trusted exact-version archive or report the source blocker; do not refresh repository databases or introduce a partial upgrade as a repair shortcut.
3. **Check transaction ownership and impact.** Inspect active package-manager processes and `/var/lib/pacman/db.lck`; wait for an existing transaction rather than deleting its lock. Inspect relevant transaction hooks and live consumers of the affected library. Do not stop applications, create extra snapshots, or perform boot maintenance merely to make the reinstall convenient. Reinstalling a library on disk does not prove already-running consumers have loaded the replacement.
4. **Authenticate and validate the reference.** For a cached archive with its adjacent detached signature, run `pacman-key --verify "$archive.sig"` and preserve the exit and verification result. Do not import keys, alter trust, or disable signature checking to bypass failure. Read `.MTREE` with `bsdtar -xOf "$archive" .MTREE`; detect and decompress gzip content before locating the exact member's digest. Stream `bsdtar -xOf "$archive" "$member"` into a bounded-memory SHA-256 calculation and compare it with that manifest. Save the extractor's exit independently: successful hashing of an empty or partial stream is not successful extraction.
5. **Revalidate the live target.** Verify it is the intended regular file, stream its digest using a tool such as Python's `hashlib.file_digest`, and distinguish a mismatch from permission or read failures. Record identity and digests, not file contents. If it already matches the signed reference, skip an unnecessary reinstall. Recheck the installed version before mutation so a concurrent update cannot turn the selected archive into an accidental downgrade.
6. **Perform the bounded reinstall.** Through the existing authorized privilege route, run `pacman -U --noconfirm "$archive"` only for the verified, specifically authorized exact-version package. Keep Pacman's normal dependency, conflict, signature and hook checks. Record its own exit and complete log; do not manually unlink a packaged library first or infer transaction success from the outer wrapper's exit.
7. **Verify both package state and content.** Run `LC_ALL=C pacman -Qkk "$pkg"`, preserve its exit and classify any remaining findings. Reopen and hash each originally damaged file, requiring equality with the signed reference, then run `pacman -Q "$pkg"` to confirm the intended version remains installed. Report the exact package file count and altered-file result only from completed output. Package proof is separate from filesystem scrub completion and application restart proof.
8. **Close with a compact receipt.** Record source archive identity, signature result, before/reference/after digests, exact command exits, preserved configuration differences and unresolved live-consumer limitations. State whether this was a one-off repair or an installed repair-script change; an auxiliary runner does not add automatic repair behavior to the user's script.

## Durable privileged handoff

Use a private persistent evidence directory when reboot/rescue transitions are possible. `/tmp` may be tmpfs; its disappearance does not establish successful completion or a particular cause.

Before the user runs a collector:

1. Read the written script back and verify nonzero size and expected commands.
2. Validate shell syntax with `bash -n`.
3. Confirm device names from current mapping.
4. Print progress before each command, record each exit independently, and announce the final evidence path.
5. Preserve root-only output permissions during collection and make only that dedicated evidence tree readable by the intended user after completion. An EXIT trap can preserve access to partial results; do not change unrelated ownership.

An empty shell script can exit successfully without checking anything. A background wrapper can also exit 0 while its child check recorded exit 1. Inspect the artifacts rather than relying on the notification. Conversely, a recovery wrapper can intentionally exit 1 after a completed unclean scrub and correctly withhold a replacement snapshot; report the deletion outcome, scrub result, and acceptance gate separately rather than labeling the wrapper a crash. On a delayed completion notification, reconcile it with the already-read receipt and do not launch another job. For an 'is it complete?' query, read the saved final state, per-command exits and scrub summary, then check the tracked process; distinguish 'job finished' from 'filesystem clean'.

Keep sudo passwords local. Tool approval does not authenticate sudo. Do not repeatedly probe an established authentication blocker or weaken sudo settings. Check mounted FAT offline rather than launching live fsck merely because `-n` is non-writing.

## Closing the execution gap

Correct explanations can still fail an action request. Begin authorized safe checks, retain ownership through completion, classify results, and distinguish planned/started/running/completed/interrupted/blocked. Repeated user `continue` messages call for actual progress or a concrete blocker, not another promise.

When the user says the collector ran, read its supplied directory immediately. If no results exist, inspect whether the collector has content and whether a process is active before asking them to rerun it. Never claim corruption-free results from empty logs or missing exit markers.
