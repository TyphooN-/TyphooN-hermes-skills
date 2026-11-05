# Passive native-entry readiness

Use this branch before the first controlled execution of reviewed native artifacts. It establishes source-derived prerequisites and observed metadata only; it is not a provisioning recipe, host-health clearance or native proof.

## Procedure

1. **Trace the real entry path.** Read the entry point, startup importer and every helper that can refuse before useful work. Build a short table of condition, source location, observed evidence and unresolved action. Include loader/protection requirements, argv/environment, inherited descriptors, signals/threads, resource limits and workspace constraints where the actual consumer checks them. Do not infer this contract from a successful compiler receipt or an illustrative CLI command.
2. **Compare existing resources passively.** Read retained manifests and inspect only the named candidate artifacts and relevant mounts. Do not invoke the artifact's `--help`, load its library, or select a real/default backend to find out whether it would refuse; even a preflight-labelled entry can execute code or provision resources.

   | Source requirement | Passive comparison | Common false positive |
   |---|---|---|
   | Protected artifact | Compare recorded identity with `lstat` ownership, type, permission bits, link count and size; trace any required protected ancestor/mount closure separately. | A valid ELF hash or executable bit does not establish the ownership/read-only properties required by the runtime. |
   | Bounded filesystem | Select the relevant filesystem from mount metadata, then compare its total capacity and inode limit using the exact fields and units consumed by the guard. Distinguish `statfs` and `statvfs` field conventions. | Enough free bytes or a small empty directory does not satisfy a cap on the whole filesystem or its inode capacity. |
   | Caller ABI | Compare exact argv, environment, descriptor roles/ownership, signal and threading requirements against the concrete caller. | A correct command string does not prove descriptor transfer, default signals or exclusive wait ownership. |
   | Aggregate resource domain | Trace which owner continuously observes each process, descendant, writer and budget through failure/quarantine. | Monitoring only an outer caller does not account for a separately running inner domain. |

3. **Classify the result without changing it.** Separate a source defect, an existing resource mismatch, missing observation and a missing permission. Preserve exact metadata and its source generation. A passive mismatch can establish that this entry is not ready; it cannot establish how an unexecuted failure or recovery path behaves.
4. **Request only the missing privileged action.** If the actual contract requires ownership/protection changes or a bounded mount, name the private resources, capacity limits, cleanup and unaffected shared services in one focused approval request. General continuation authority does not fill this gap. Keep conditional approval unspent until its acceptance prerequisites hold, and keep parent-only approval out of source/mock worker authority. Do not propose weakening the source guard merely to fit existing artifacts.
5. **Advance the correct stage.** Record source acceptance, provisioning approval, actual provisioning/readback and fresh execution admission separately. Preserve the existing compiled artifacts as historical build evidence rather than relabelling them runtime-ready. Continue independent admitted work only when its actual dependency path does not consume the missing resource.

## Preserve custody during admitted execution

- Inspect the controller's failure/cleanup lifetime, not just its normal phase deadlines, before choosing foreground or background transport. If accepted cleanup intentionally retains ownership until a domain drains, launch the controller as a tracked background process with completion notification; a foreground tool hard cap can kill the custodian while a separately grouped descendant survives. A short build phase does not imply a bounded cleanup lifetime.
- After an actual timeout or cancellation, inspect the operation journal's recorded child groups and owned cgroup membership as well as the controller group. A descendant may have a different PGID and be reparented after the controller exits. Keep the attempt incomplete until the actual domain is empty and closure is observed.
- Treat a process that remains present with SIGKILL pending as an unresolved host/process-release blocker even if its scheduler state is `R` rather than `D`. Signal only the identity-bound owned generation through pidfds and the verified private domain, bound the cancellation wait, preserve incomplete custody, and stop further dependent native attempts. Do not repeat signals indefinitely, remove a populated domain, weaken confinement or change host settings to manufacture cleanup.

## Completion criterion

Every required startup condition has either source-bound passive evidence or an explicit unresolved action. No produced artifact, default backend, privileged operation or live service was invoked by this readiness check. Later provisioning and native proof require their own observed results and cleanup; do not report them as completed from this table.
