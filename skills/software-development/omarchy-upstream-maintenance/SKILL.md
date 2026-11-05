---
name: omarchy-upstream-maintenance
description: Use when maintaining Omarchy changes across updates.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags:
    - omarchy
    - git
    - upstream
    - maintenance
    related_skills:
    - omarchy
    - claude-code
    - requesting-code-review
platforms:
- linux
x-local-maintainer: TyphooN (TyphooN-)
---


# Omarchy upstream/customization maintenance

## Portable scope

This copy preserves a locally developed workflow, not transferable approval. Resolve the current task, repository, active Hermes profile, tools and ownership on this machine first. Historical project choices and TyphooN-specific executor/build policies are context, not permission to start services, run targets, modify security settings or publish. Project-root variables are documented in the collection's `PORTABILITY.md`; unset variables are not usable paths. Installing a skill installs no external tools or plugins.

## When to Use

Use for planning or executing recurring private-source rebases, preserving normal stock updates, or diagnosing customization drift after an Omarchy update. Reconfirm execution authority before applying a previously saved plan.

## Authority and source ownership

Keep planning separate from implementation, scheduling and live activation. Read the proposed plan at `$OMARCHY_MAINTENANCE_PLAN` when relevant; treat it as a proposal unless subsequent user approval explicitly advances its scope. A plan, timer description or handoff is not evidence that a service or rebase ran.

Use `$OMARCHY_DEV_ROOT` as the user's canonical Omarchy development source and keep `$OMARCHY_PATH` upstream-only for normal running/update use. Reverify roots, selected channel, HEADs, dirty/index/untracked state and process ownership; historical commit tips are not current system facts. a-la-carchy owns its configurator and packaging; verification caches are not permanent source homes.

## Safe refresh

1. Inspect the effective updater and selected upstream ref. A planning-only remote query can use `git ls-remote` without mutating refs.
2. Establish pushed/shared history before rewriting. No tracking branch or cached remote containing HEAD does not prove the branch was never shared. Private rebase authority does not authorize shared-history rewrite or force-push.
3. Preserve the base, exact staged/unstaged/untracked preimages, modes and recovery reference before a rewrite. Never automatically stash, clean, reset or discard user work to make an update succeed.
4. Prepare one isolated candidate from a frozen customization stack and upstream OID. Resolve by feature intent and regenerate derived files; do not pick a conflict side wholesale. Preserve the original until verification and required independent review.
5. Promote only with exact source/index/ownership guards and no competing checkout writer. Release disposable worktrees/processes first; preserve a recovery point. A clean source rebase, installed-byte readback and live health are distinct claims.
6. Prefer tested upstream-equivalent behavior and supported user plugins/configuration. A core patch without an approved delivery adapter remains source-only; never dirty the running checkout to label it installed.

## Dirty updater checkout: classify the bytes first

1. Capture `git status --porcelain=v1 -uall`, `git diff --numstat` and `git diff --cached --name-status` in the effective update checkout before choosing a preservation or recovery action. Do not label changes as customizations from filenames alone; Git reports truncated files as ordinary unstaged edits.
2. For whole-file deletions, inspect each actual path with `lstat` and compare its byte length with `git cat-file -s 'HEAD:<path>'`. Distinguish a missing file from an existing empty regular file, and preserve symlink/type/mode differences. Compare the affected set with `git show --format= --name-only HEAD` when an interrupted checkout is plausible; matching paths or timestamps do not establish what caused truncation.
3. Freeze HEAD, index identity, the exact dirty-path set and original bytes/metadata before assigning recovery. Preserve nonempty user changes separately. Empty files do not authorize automatic stash/reset/clean or wholesale restoration; require admitted recovery scope and stop if content, ownership or the checkpoint changes.
4. Give the recovery executor the already established path set and trusted object identities rather than another open-ended discovery task. Keep unrelated private-source customizations and host repair outside that assignment. Record confirmed empty-file damage separately from suspected causes; use `filesystem-integrity-recovery` for justified integrity investigation rather than treating source recovery as filesystem clearance.

## Zero-byte tracked files blocking an update

A large deletion-only diff is not necessarily customization work. Inspect exact file sizes, index/HEAD blobs, modes, timestamps and the latest commit's changed-path set before proposing a stash, commit or rebase. A clean upstream updater tree can contain truncated checkout files; report confirmed truncation separately from its unproven cause.

For a small known set, make source recovery the first bounded deliverable. Confirm writer/update-lock ownership; freeze HEAD/index/status and exact preimages; verify the trusted blobs and attribute semantics; then restore only admitted regular empty files with compare-before-replace guards. Preserve the empty originals and stop if nonempty or concurrent user content appears. Never blanket-reset, auto-stash, commit deletions, or touch the private customization checkout. Standard Git materialization into private evidence is preferable to inventing maintenance infrastructure; expand pack/journal forensics only when a concrete verification failure warrants it.

Require clean tracked/untracked status, appropriate mode/hash checks, `git diff --check`, and `git fsck --connectivity-only --no-dangling` before returning to the stock updater. Source recovery does not complete the package/migration/boot update or establish filesystem health. Keep evidence private and durable; the same filesystem is not an independent backup.

## Broken cached Git refs during an update

Treat `fatal: bad object refs/remotes/...` as a local-reference integrity failure until verified; it does not by itself prove the server omitted objects or explain why a file became corrupt.

1. Confirm no updater, fetch, or maintenance process owns the checkout. Record clean/dirty state and HEAD, and resolve the actual Git/common directory rather than assuming `.git` is a directory. A maintenance lock file's existence alone does not prove an active holder; inspect advisory lock ownership.
2. Inspect the exact named loose ref and packed counterpart. Inventory other empty/invalid cached remote-tracking refs. Preserve exact preimages before a narrowly scoped repair. Never delete local branches, tags, valid refs, object packs or reflogs to silence this error; never run broad reset/clean or prune objects.
3. Repair only confirmed invalid cached remote-tracking entries, then fetch the configured remote to recreate refs that still exist upstream. Do not claim an empty loose ref has a valid packed replacement without checking it.
4. Run the stock checkout updater under `omarchy-update-lock` with the verified `OMARCHY_PATH`. Verify the fast-forward, clean status, `git diff --check`, `git fsck --connectivity-only --no-dangling` (compatible with promised missing blobs), and the selected upstream tip.
5. Distinguish Git repair/source refresh from the full package/migration/boot update. If sudo interaction is required, launch the normal updater in a visible terminal and let the user enter the password there; never request it in chat or weaken the updater's authentication. Record an attributable final exit, not merely a terminal-launch success. Keep separate start/exit/log receipts for each retry, preserving earlier failures; a source-recovery success or delayed notification must not be mistaken for full-update success. An authentication timeout leaves the update incomplete; retry on the user's explicit continuation with a fresh receipt and no duplicate updater. If the agent lacks display settings but the graphical session is active, read only the necessary display/session keys from the user service manager and pass them to the launch; never dump the whole environment.

## Hook ordering and success evidence

Inspect current `bin/omarchy-update`, `omarchy-update-dev`, `omarchy-hook` and `omarchy-update-lock`. Source-derived ordering takes precedence over blanket hook-guide assertions. Versions can use `pull --ff-only`, skip a branch without upstream, clear the update indicator early, and call `post-update` before later AUR/boot-verification phases.

Make an update hook enqueue only. A hook invocation, cleared indicator or released lock proves neither full success nor reusable sudo authority. Require an attributable success signal plus compatible actual source/runtime identities, or keep live application controlled/pending. Never weaken authentication wrappers or let customization failure obstruct the stock updater.

## Durable operation, only when authorized

Prefer an event trigger plus a low-frequency user timer with observed catch-up behavior. Do not silently enable lingering, install a delivery platform, run real system updates or change privileges/security settings. Keep one writer, one active candidate and one coalesced latest target. No source change means no rebase/model call/backup churn. Preserve unique unfinished work and a compatible last-known-good artifact while bounding successful logs and proven disposable worktrees.

Read back exact owned targets after installation. Preserve shell/provider choices and accounting history. Never use database rollback, inference-service restart, model loading, credential changes or paid fallback as maintenance repair. An unavailable required independent review remains an acceptance gate. A local background timer cannot promise delivery into an inactive TUI.
