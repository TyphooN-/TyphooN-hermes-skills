---
name: git-remote-ref-recovery
description: Use when Git fetch/pull fails on a broken remote ref.
version: 0.1.0
author: TyphooN (TyphooN-), Hermes Agent
license: GPL-3.0-only
platforms:
- linux
- macos
x-local-maintainer: TyphooN (TyphooN-)
---


# Broken Remote-Tracking Ref Recovery

## Portable scope

This copy preserves a locally developed workflow, not transferable approval. Resolve the current task, repository, active Hermes profile, tools and ownership on this machine first. Historical project choices and TyphooN-specific executor/build policies are context, not permission to start services, run targets, modify security settings or publish. Project-root variables are documented in the collection's `PORTABILITY.md`; unset variables are not usable paths. Installing a skill installs no external tools or plugins.

Companion to `omh-git-workflow` for `bad object refs/remotes/...` and `does not point to a valid object` errors. This is local Git recovery, not permission to reset work, rewrite history, or change remotes.

1. Record repository/root, HEAD, branch/upstream, dirty state, worktrees, exact remote/refspec, locks, and competing writers. Inspect the exact loose ref and corresponding packed entry; they may differ. Read advertised tips using `git ls-remote`.
2. Inventory ref OIDs using `git for-each-ref --format` and validate targets using `git cat-file --batch-check`. Preserve errors: missing targets and empty/corrupt loose objects are distinct findings. Never treat local branches, tags, or unique commits as disposable tracking metadata.
3. Back up affected loose/packed refs and reflogs in a private unique evidence directory under the active scratch directory. Record original HEAD/status. A same-filesystem checkpoint is not an independent backup.
4. Remove only the confirmed broken remote-tracking cache entry using `git update-ref --no-deref -d <exact-ref> <observed-old-oid>`. The old-OID check guards unexpected ref changes. Fetch with `git fetch --atomic --no-auto-maintenance origin`, then fast-forward the intended branch only when safe; preserve divergence and user changes.
5. Run `git fsck --full --no-dangling` even after fetch succeeds. If it reports exact zero-byte loose object files, verify regular-file identity/size and absence of competing writers, then quarantine only those empty files outside `.git` and rerun fsck. Do not sweep objects, remove nonempty files, or run GC/prune as a shortcut. Remaining reachable-object failures require a trusted restoration source.
6. Prove a normal fast-forward-only pull succeeds, HEAD matches its tracking ref and a fresh remote-tip observation, the repaired ref resolves, and local work remains intact. Preserve command outputs/exits and recovery paths. Git integrity success does not clear filesystem/device health; do not invent a cause for truncation or missing objects.
