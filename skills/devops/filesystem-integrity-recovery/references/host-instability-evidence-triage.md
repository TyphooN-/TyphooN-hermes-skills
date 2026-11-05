# Host-instability evidence triage

Use when an application crash investigation expands into interrupted builds, checksum findings, or changing hardware topology. Keep this as a bounded host-integrity investigation, not a reason to manufacture unrelated repository changes.

## Evidence separation

Trace application assertions from their own logs and source, and investigate compiler failures, reboot interruptions, and filesystem errors separately. Do not infer a shared cause from temporal overlap: an explained application abort neither explains later storage damage nor establishes that storage damage caused the abort.

Maintain separate ledgers:

| Evidence | What it establishes | What it does not establish |
|---|---|---|
| Collector commands exit 0 | Requested diagnostics were collected successfully | Filesystem or device is healthy |
| Scrub running with uncorrectable checksums | Real checksum failures found so far | Final total, full affected-file inventory, or cause |
| Device corruption counter increases during scrub | More failures were counted | New corruption is being created; old damage may be rediscovered |
| SMART PASSED with zero media errors | Controller is not reporting those failure conditions | Filesystem correctness or conclusive exclusion of SSD faults |
| Lifetime unsafe-shutdown count | Device-recorded lifetime history | Which event caused a particular damaged extent |
| Lifetime NVMe error count with an empty readable log | Both observations are available | A fabricated media-failure explanation; log retention/coverage may differ |
| ECC-disabled channel or failed EDAC registration | Limits on reported memory-error evidence | Proven faulty RAM, or proof that RAM is healthy |
| Orderly systemd shutdown/unmount messages | That captured boot entered normal shutdown | Every other interruption was orderly |
| High utilization of allocated metadata chunks with substantial unallocated space | Current allocation proportions | Whole-device exhaustion or a need to balance immediately |

`Data,single` plus `Metadata,DUP` provides duplicate metadata, not duplicate file data. A scrub cannot reconstruct a damaged single-copy data extent merely because metadata is duplicated. Data-checksum errors alone are not a reason to run mounted `btrfs check --repair`.

## Classify damage without overclaiming

1. Read the supplied evidence directory before initiating another check.
2. Verify collection timestamps, per-command exits, and nonempty outputs.
3. Deduplicate kernel checksum path annotations and retain their original spelling. A bounded log or suppressed callbacks can omit affected files. Path annotations can be absent or escaped; absence is not clearance.
4. Classify named paths by restoration source:
   - Generated objects and caches: usually reproducible from verified source, but coordinate with the owning build before regeneration.
   - Stored coredumps: preserve if still needed for diagnosis; they contain private process memory and must not be publicly uploaded.
   - Package-managed files: compare with matching trusted package versions before restoration.
   - Source, configuration, databases, and personal data: preserve dirty work and use trusted backups or content-specific validation.
5. Reconcile the logged inventory against current metadata before recommending cleanup. Map each logged Btrfs root ID to its current mounted subvolume rather than blindly prepending a mountpoint, then classify exact paths as present, absent, replaced/identity-mismatched, or unreadable. Preserve the historical identity separately from the current one; pathname reuse can hide a different file.
6. Report absent paths as absent, not as deletions performed by this session or proof that damaged extents were freed. Snapshots and other references can retain extents after a pathname disappears; metadata-only checks do not verify file contents or filesystem health.
7. Say "the captured log names only build outputs and a coredump" when that is the observation. Do not turn it into "only disposable files are damaged" or "all models/source are intact."

## Git working-tree validation before metadata repair

1. Pin the expected commit and preserve the real index and dirty source. If the real index is damaged, build a **separate** index with `GIT_INDEX_FILE=<private-index> git read-tree <expected-commit>`; do not replace the real index yet.
2. Run `GIT_INDEX_FILE=<private-index> git update-index --refresh`, record its exit, then inspect `GIT_INDEX_FILE=<private-index> git diff-files --name-only`. A freshly populated index lacks checkout stat information, so an initial all-files difference is not evidence that every file is damaged.
3. For remaining differences, inspect `git check-attr text eol filter -- <relative-path>` and the applicable attributes before comparing raw bytes. Git blobs can store LF while a valid checkout contains CRLF. Review any configured clean filter before invoking it; with only reviewed normalization, compare `git hash-object --path=<relative-path> <working-file>` with `git rev-parse <expected-commit>:<relative-path>`.
4. Classify expected conversion separately from unexplained content changes. Repair only task-owned disposable metadata after the intended source is validated; a raw-byte mismatch or refresh failure alone does not authorize overwriting source or deleting a worktree.

## Verification claims under interrupted builds

- `git fsck --connectivity-only` checks connectivity, not every object's contents. `git diff --check` checks whitespace/errors in a diff. A reverse-apply check establishes patch applicability, not full repository or binary integrity.
- Missing process handles after reboot and absent exit markers mean interrupted/unknown, not successful completion. Confirm no old process group, session, or verification child remains before resuming.
- Zero-length lane-created objects are disposable only when ownership and provenance are established. Do not generalize that finding into deleting another owner's target directory or shared cache.
- Numerical tests must actually execute the intended backend. Device discovery and successful build/link steps alone are not GPU execution proof. Distinguish an expected aborting negative-test child from failure of the parent regression.
- An isolated patched graph library can sometimes be tested with an unchanged same-revision backend library, but matching source revision alone is insufficient: check ABI/configuration compatibility, dynamic-loader selection, transitive dependencies, and actual backend execution. Describe it as isolated assembled-library proof, not a completed fresh backend rebuild or deployment. Obtain the required independent review before treating it as ready to ship.
- Record real-model stages separately: loading, warmup/readiness, completion, server survival, and graceful teardown. If a harness fails after readiness, preserve the stage result and exact harness error. Before retrying, prove the owned server and descendants are gone and recheck current resources.

## Privileged read-only collection pattern

When local sudo authentication is required, give one reviewed collector rather than repeatedly attempting `sudo -n` or asking for a password in chat.

Collector requirements:

- Private uniquely created evidence directory and restrictive umask.
- Validate the script with readback and `bash -n` before delivery.
- Discover the physical device mapping first; no stale device guesses and no signature wiping.
- Read existing scrub status, Btrfs device counters/profiles, and device health/logs. `smartctl -x` reads evidence; do not add `-t`, scrub launch, counter resets, balance, defrag, or repair.
- Record each command's exit separately and preserve partial evidence on failure. Do not let the shell's final success mask a failed diagnostic.
- Change ownership only for the uniquely created evidence tree so the user/agent can inspect it; never weaken unrelated permissions.
- Flush completed logs/checkpoints when interruptions are plausible. Evidence on the suspect volume remains a local checkpoint, not an independent backup.
- Distinguish a pre-authentication helper failure from an authentication wait or completed privileged collection. If a newly written helper is empty after an interruption, preserve it and the failed exit; confirm the previous collector/authentication process is gone before one bounded replacement.
- When explicitly authorized local read-only collection cannot safely depend on a pending disk script, pass reviewed, bounded collector source in memory to an isolated system interpreter through an existing authorized local authentication route. Record exact source digests and private source snapshots. Do not use another transport to bypass a policy denial.
- Keep sudo authentication on the user-visible controlling terminal, never in chat, captured stdin, environment variables or model logs. Capture only the sanitized collector stdout with an unprivileged controller; this keeps evidence user-owned without a root ownership change. Save result/exit records by atomic replacement with file and parent-directory fsync.

When the user supplies results, immediately classify them and close the authentication gap. If the scrub is still running, retain its start time and interim counters and request its final status without starting a duplicate. Example, with an already reviewed user-owned evidence directory:

```bash
sudo btrfs scrub status / > /path/to/evidence/scrub-final.log 2>&1
scrub_status_exit=$?
printf '%s\n' "$scrub_status_exit" > /path/to/evidence/scrub-final.exit
```

The status query does not launch a scrub. The directory and device names must come from the current task, not this example.

## Resume gate

Prefer a narrow decision over an open-ended halt:

1. Preserve irreplaceable work on trusted separate storage where authorized.
2. Obtain the existing scrub's final verdict and identify exact restoration candidates.
3. Establish enough host/kernel/memory/storage stability for the intended workload; do not name a root cause without evidence.
4. Restore or regenerate only authorized affected artifacts, serialized with other writers.
5. Reverify the restored content and the application behavior before activation/publication.

No automatic deletion, service termination, driver changes, firmware updates, reboot, or destructive filesystem repair follows from these diagnostics.
