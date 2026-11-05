---
name: linux-kernel-boot-integration
description: Verify kernel package hooks, initramfs and boot entries.
version: 0.1.0
author: TyphooN, Hermes Agent
license: MIT
platforms:
- linux
x-local-maintainer: TyphooN (TyphooN-)
---


# Linux Kernel Boot Integration

## Portable scope

This copy preserves a locally developed workflow, not transferable approval. Resolve the current task, repository, active Hermes profile, tools and ownership on this machine first. Historical project choices and TyphooN-specific executor/build policies are context, not permission to start services, run targets, modify security settings or publish. Project-root variables are documented in the collection's `PORTABILITY.md`; unset variables are not usable paths. Installing a skill installs no external tools or plugins.

Trace a custom kernel from package contents through the active package-manager hook, initramfs generator and bootloader. Fix demonstrated gaps, not presumed missing version-specific configuration.

## When to Use

- Requests to add mkinitcpio hooks or presets for custom kernel versions.
- Checking whether a locally built kernel package will generate an initramfs and boot entry on installation.
- Diagnosing missing boot entries after kernel installation or upgrades.
- Selecting an installed kernel as the bootloader default without rebuilding or rebooting.
- Working around an active kernel build without modifying its inputs or output.

This skill covers integration, not kernel development, signing-key management or proving hardware boot compatibility. Load distribution-specific guidance as well when changing live system configuration.

## Procedure

1. **Establish scope and ownership.** Check the actual repository, branch, dirty state and active build/package-manager processes with `terminal`. Record user-owned changes. A running build owns its source, configuration, generated patches and package output: do not edit these underneath it or attribute its new untracked files to your lane. A request for hooks does not automatically authorize kernel installation, reboot, bootloader replacement or removal of a known-good kernel.
2. **Read the effective hooks first.** Use `search_files` and `read_file` on administrator and packaged hook directories, then trace the selected `Exec` program. For Arch, compare `/etc/pacman.d/hooks` with `/usr/share/libalpm/hooks`; same-named administrator hooks can override packaged hooks. Inspect symlinks and configured alternative hook directories where relevant. Do not infer active behavior from the packaged default alone.
3. **Identify the integration contract.** Record trigger type, operations, target patterns, `NeedsTargets`, executable and downstream image/entry handling. Distinguish mkinitcpio's initramfs `HOOKS` array, mkinitcpio presets, pacman transaction hooks and bootloader integration hooks. They are not interchangeable.
4. **Inspect packages without installing.** Discover exact archive names. Through `terminal`, use `bsdtar -tf <archive>` and filter its output to the relevant module-directory metadata and kernel image. Use `bsdtar -xOf <archive> <exact-member>` only for small metadata such as `pkgbase`. Do not extract all modules or run package scripts. Check exit status. Report package name and kernel release separately.
5. **For an unfinished build, trace packaging.** Read the current source version and package recipe. Follow `modules_install` to the kernel's installation rules. Source-derived future contents are weaker evidence than an inspected finished archive; label them accordingly. Do not start another kernel build merely to test hook coverage.
6. **Decide whether a change is needed.** If the effective generic hook matches the actual package contract and its handler supports that package, leave it alone. Do not create duplicate version-specific hooks or presets simply because the user phrased the request as an addition. If a gap exists, stage the smallest change, preserve existing boot conventions and backups, then apply only within the authorized scope.
7. **Verify at the appropriate level.** Start with syntax checks, target matching and isolated tests of relevant handler functions. Never source the whole installed handler if its top-level code generates images, acquires locks or changes boot entries. Isolate only inspected functions and mock side-effecting dependencies. Fail closed if function extraction is ambiguous. Synthetic paths must be explicitly labeled fixtures.
8. **Close with evidence.** State what changed or why nothing was needed, which archive was checked, what source path supports unfinished-build claims, exact checks and exit codes, and whether installation/image generation/boot testing remain pending. Lead with the answer rather than the investigation chronology.

## Changing the Default Kernel

For a default-selection-only request, use this bounded path instead of tracing package hooks or starting a repository lane:

1. **Discover the live boot configuration.** Check `uname -r`, `findmnt /boot`, installed kernel package identities, and the bootloader's actual config location. Load distribution-specific guidance. Treat an inaccessible root-owned boot directory as an access boundary, not evidence that its files are absent. On Limine, `bootctl list` can enumerate existing UKIs while labeling separately reported Limine menu IDs `reported/absent`; that label alone does not establish a missing kernel image. Resolve Limine's own menu and selection precedence rather than treating the BLS default as the active Limine default.
2. **Read installed semantics before choosing a value.** For Limine, consult `/usr/share/doc/limine/CONFIG.md` and inspect the complete menu hierarchy. Prefer a named entry path when the installed bootloader supports it; numeric indexes can drift when entries are added. Inspect `remember_last_entry` and applicable one-shot overrides because they can supersede the configured default.
3. **Verify the target before writing.** Resolve the exact non-snapshot entry and its referenced kernel image or UKI; require that the artifact exists and is nonempty. A package being installed does not prove its boot artifact exists.
4. **Apply only the selection change.** Use the platform's approved privilege flow, preserve a timestamped backup, coordinate with the installed boot-partition lock, and replace exactly one default directive. Preserve timeout, kernel command lines, hashes, snapshots and known-good fallback entries. Do not run regeneration/install helpers merely to change the selection; they can rebuild images or reinstall the bootloader.
5. **Read back the exact config independently.** Confirm the intended default, referenced artifact, and that the backup-to-current diff contains only the authorized change. Report the selected kernel and next-boot effect, explicitly distinguishing configuration verification from an actual boot. Do not reboot unless separately authorized.

See the Limine default-selection recipe in [Arch mkinitcpio and Limine contracts](references/arch-mkinitcpio-limine.md) for concrete probes and privilege handling.

## Verification Levels

Keep these distinct:

- **Static coverage:** installed trigger and handler agree with package contents or packaging rules.
- **Offline behavior:** actual target-selection code accepts tested inputs with side effects isolated.
- **Installation verified:** an authorized package transaction ran and its hook output was inspected.
- **Boot artifacts verified:** expected images and boot entries exist and identify the intended kernel.
- **Boot verified:** the machine actually booted the intended kernel.

A passing static or mocked test is not proof of successful image generation or bootability. When running a real transaction, inspect handler errors and artifacts rather than relying solely on its exit status; some implementations skip failed kernels and still exit successfully.

## Pitfalls

- Empty `/etc/mkinitcpio.d` does not itself prove integration is broken: another handler may invoke mkinitcpio directly.
- Generic path triggers can support new kernel versions without any version-number edit.
- Duplicate hooks may regenerate images twice or mix incompatible boot layouts.
- Do not switch a Limine-managed installation to plain `mkinitcpio -P` as a generic repair without tracing its current integration.
- Do not read entire process command lines for unrelated agents when checking build ownership; prefer scoped PID, process-group, executable and working-directory evidence.
- Treat a Memtest86+ menu entry as a separate task from kernel installation, UKI generation or default selection. Discover the installed EFI image and its architecture, preserve the existing configuration under the installed boot-partition mutex, back up before an atomic addition, and read back the exact entry and referenced image/hash. Do not reboot or execute the diagnostic unless separately authorized.
- Inspect enrollment helpers before invoking them: an installed `limine-enroll-config` can restore/rewrite and sign the Limine EFI binary even when config enrollment is disabled. It is not a read-only validator or an automatic prerequisite for every menu edit. Preserve Secure Boot, enrollment and signing policy; stop for approval if the requested entry requires a trust-policy change.
- Archive inspection and unit tests can establish readiness, but cannot certify firmware, storage, encryption or driver compatibility.

## Reference

See [Arch mkinitcpio and Limine contracts](references/arch-mkinitcpio-limine.md) for concrete source paths, package probes and the offline verification technique. Revalidate installed implementations before relying on those observations.
