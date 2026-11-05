# Descriptor-backed I/O test design

Use when testing descriptor-relative staging, pathname revalidation, file identity or checked resource handoff. This is a fixture-design procedure, not evidence that real filesystem behavior was exercised.

## 1. Model the actual identity relationships

Keep separate maps:

- `path -> inode`: directory/name resolution.
- `fd -> {inode, generation, access/status flags, descriptor flags}`: the acquired handle.
- `inode -> current metadata and bytes`: identity, mode, owner, link count, size and content.

Resolve `stat(path)` through the pathname map and `fstat(fd)` through the held inode. Do not implement `fstat(fd)` as `stat(path_saved_at_open)`: pathname replacement would then incorrectly change the identity of the open FD. Do not freeze all metadata at open either; changes to the same inode can legitimately affect later `fstat` observations.

Completion: replacing a name changes pathname identity while an existing FD still identifies the old inode; mutations to that old inode remain observable through its FD.

## 2. Isolate each refusal branch

Construct inputs so every check before the target branch passes. A generic HOLD or exception does not prove which invariant rejected the input.

| Case | Keep valid/stable | Change | Required discrimination |
|---|---|---|---|
| Path rebinding | Open FD inode and its expected metadata | Name resolves to a different inode | Path-to-handle relationship check refuses, not an earlier FD-identity check. |
| Exact private mode | Correct identity, owner, type, access and pathname relationship | Private directory has a nonprivate mode | Exact-mode check decides the refusal. |
| Unexpected hard links | Correct bytes, identity, mode, owner and type | Link count violates the contract | Link-count check decides the refusal. |
| Writer/readback continuity | Equal bytes and valid metadata | Readback resolves to a replacement inode | Handoff refuses despite matching content hashes. |
| Acknowledged close and reuse | Old generation conclusively closed | A later open reuses its numeric FD | New generation is distinct and permitted under the ownership contract. |
| Close uncertainty | Failed or unacknowledged close | Another acquisition tries to reuse capacity | Uncertainty stays retained; numeric reuse must not fabricate release. |

Use an otherwise valid positive control for each case. Where authorized, a disposable deliberately broken control can show the test depends on the intended branch; retain its actual result rather than claiming an unexecuted mutation passed or failed.

Completion: each test distinguishes its named invariant from unrelated earlier refusal paths.

## 3. Test read-open safety before accepting a handle

When the production contract requires nonblocking regular-file reads, let the fake inspect the requested open flags before returning a handle. Cover every relevant acquisition path, such as listed inputs, maintained source copies and readback files. Preserve no-follow, close-on-exec, access-mode and post-open type/identity checks; adding a nonblocking flag does not replace them.

Do not open a real FIFO or device merely to prove a flag under mock-only authorization: an open can block or have side effects before the later regular-file check. Extend the common default-effect guard whenever a new injected backend is added, and exercise its refusal before positive fake-backed cases. A guard installed only by that feature's fixture leaves other admitted callers able to reach real OS effects.

When required open capabilities are unavailable, test a documented, caller-catchable refusal rather than an uncaught `AttributeError`; never silently drop a no-follow or other required protection for portability. Preserve the distinction between a nonblocking open flag and an enforceable timeout of regular-file I/O.

Completion: the missing required flag causes the intended behavioral failure through the real consumer without performing the prohibited OS effect.

### Prove reservation-backed underlying reads

Use real temporary regular files only when fixture file I/O is admitted; mock-only authority does not permit live model, FIFO or device access.

1. Write a valid small metadata header followed by a recognizable synthetic trailer. Keep the fixture long enough that buffered opening can read beyond the first reservation; do not use installed weights.
2. Give the real consumer a shared byte budget covering only its first small read. Let that read succeed, then observe `os.lseek(handle.fileno(), 0, os.SEEK_CUR)` immediately before the next reservation should refuse. A buffered handle's logical `tell()` can equal the requested count while the underlying descriptor is already far into the trailer.
3. Require the raw descriptor offset to equal the bytes successfully reserved/read before refusal. Assert the budget counters as a separate property, because correct counters alone do not detect read-ahead. Observe the original implementation fail this offset assertion before changing it; do not hardcode a platform-specific buffer size.
4. Add a successful-header control that observes the descriptor before parsing and after the declared metadata is consumed. Require the final offset to equal that metadata length, not the fixture's trailer-inclusive length.
5. Use unbuffered binary opening, or reserve the complete underlying prefetch before I/O, then require both controls to pass without changing their causal assertions. Label real temporary-file descriptor observations separately from synthetic process mechanics and production-data execution.
6. Cover short reads and failed reads/opening separately. Charge bytes before the attempted read, retain those charges on short/error outcomes, and retain a started-file slot after a failed open when the contract requires it. Pair these negative controls with a successful nonempty metadata parse so a blanket refusal cannot satisfy the suite.

Scope the resulting proof to application-level reads. It does not bound kernel/page-cache readahead, physical device traffic, decoded-object heap expansion or blocked-syscall duration. Keep malformed declarations, observed metadata-change detection and authenticated section boundaries distinct.

## 4. Distinguish current handoff uncertainty from completed ownership

1. Establish a successful return control and record the returned descriptor identities, generations and ownership states.
2. Inject return-object allocation failure before transfer intent. Require retained acquisitions, a latched refusal and no claim that resources were transferred.
3. Inject an exception after intended-transfer bookkeeping but before successful return. Require uncertainty for that invocation's attempted handoff, with every resource still accounted for and no speculative close or retry.
4. After a genuinely successful return, invoke the operation again and require its specified duplicate/refusal behavior without relabeling, closing or revoking the already-returned resources. Retain borrowed-root ownership in every case.

Scope transfer-started and rollback bookkeeping to the current invocation; scanning all historical transferred handles in a generic exception handler can corrupt a prior successful transfer. Use synthetic allocator or state-transition faults under the admitted mock seams, not real signals or live descriptor operations.

## 5. Record the right kind of proof

Observe causal RED before changing production behavior, then require the same failed identities to pass their matching GREEN. Adding discriminating tests for an already-correct production branch is characterization, not a retroactive RED cycle. Keep source-derived review findings, synthetic tests, intentionally broken controls and real-system execution separately labelled.
