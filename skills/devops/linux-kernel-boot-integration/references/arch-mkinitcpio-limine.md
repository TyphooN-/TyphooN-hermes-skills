# Arch mkinitcpio / Limine integration contracts

These are source-derived observations from an Omarchy host using mkinitcpio 41.1 and limine-mkinitcpio-hook 1.38. Re-read the installed files: paths, triggers and handler details can change. Package versions here identify the observed implementation, not a requirement or current-version claim.

## Two different integration paths

| Surface | Observed behavior |
|---|---|
| Packaged `/usr/share/libalpm/hooks/90-mkinitcpio-install.hook` | Kernel install/upgrade trigger matches `usr/lib/modules/*/vmlinuz`; invokes `/usr/share/libalpm/scripts/mkinitcpio install`. |
| Administrator `/etc/pacman.d/hooks/90-mkinitcpio-install.hook` | Same filename overrides the packaged hook. Kernel trigger instead matches `usr/lib/modules/*/modules.builtin`; invokes `/usr/share/libalpm/scripts/limine-mkinitcpio-install`. |
| Plain mkinitcpio handler | Reads adjacent `pkgbase`, creates presets from its template when needed, installs kernel images and invokes mkinitcpio using presets. |
| Limine handler | Collects module directories from trigger paths; determines kernel package name using `pacman -Qqo .../modules.builtin`; generates an initramfs or UKI and calls `limine-entry-tool`. Does not require a per-kernel mkinitcpio preset for this path. |
| `/usr/bin/limine-mkinitcpio` | Validates optional installed package-name arguments before feeding them to the Limine handler; no arguments requested a rebuild of all kernels in this observed implementation. This is a mutating command, not a discovery probe. |
| Limine removal hooks | Separate pre/post transaction hooks manage removed kernel entries; examine these before adding custom removal logic. |

Read only relevant settings from `/etc/limine-entry-tool.conf` and `/etc/default/limine`, such as `ENABLE_UKI`, fallback behavior and ESP location. Avoid copying machine identifiers, full command lines or unrelated private configuration into reports.

## TKG package contract

The inspected TKG recipe:

1. Obtains the built kernel release from its `version` file.
2. Installs the kernel image to `usr/lib/modules/<release>/vmlinuz`.
3. Writes package identity to adjacent `pkgbase`.
4. Calls `make INSTALL_MOD_PATH=... modules_install`.

For the inspected 7.3 source, `scripts/Makefile.modinst` installed `modules.builtin` and `modules.builtin.modinfo` even with loadable modules disabled. The finished 7.2 archive contained all three relevant paths. These facts established coverage by the existing wildcard trigger; they did not require adding hooks for either version.

## Minimal probes

Use `terminal` for the following, substituting discovered exact filenames and quoting paths:

- `bsdtar -tf <kernel-package.pkg.tar.zst>`: stream/filter the listing for `/modules.builtin`, `/pkgbase` and `/vmlinuz`; require successful process completion.
- `bsdtar -xOf <archive> usr/lib/modules/<actual-release>/pkgbase`: read only the discovered metadata member.
- `bash -n /usr/share/libalpm/scripts/limine-mkinitcpio-install`: syntax only; no handler execution.

Do not run `makepkg`, `modules_install`, the pacman hook handler, `limine-mkinitcpio`, or `mkinitcpio -P` as read-only tests.

## Safe offline target-selection test

The successful technique tested the actual installed `collect_kernels` function without invoking the handler's top-level initialization or `main`:

1. Inspect the function and its dependencies. Extract its exact definition only after checking the boundaries; do not blindly split arbitrary shell source at the first closing brace.
2. In an isolated Bash process, declare an empty `KERNEL_DIRS` array and stub `add_kernel_package` to return failure. This deliberately tests path-input selection, not package-name lookup.
3. Feed the actual archive's `usr/lib/modules/<release>/modules.builtin` path and a clearly labeled synthetic future-kernel path to `collect_kernels` on stdin.
4. Assert that the collected directories equal those paths with a leading slash and the `/modules.builtin` suffix removed.
5. Record the syntax-check and fixture-test exits, plus the exact tested source implementation.

This proves target collection only. It does not test pacman's full matching implementation, ownership lookup, mkinitcpio generation, entry updates, or booting. Inspect those stages separately if the task authorizes them.

## Limine default-selection recipe

1. Probe `uname -r`, `findmnt /boot`, `pacman -Q <discovered-kernel-package>`, and installed Limine documentation. Read `/etc/default/limine` for the ESP location; do not assume it contains the menu's default directive.
2. Discover `limine.conf` on the mounted ESP and check for higher-priority config candidates according to the installed Limine documentation. Root-only mount permissions can hide files from an unprivileged probe. For agent-launched commands without an interactive password terminal, use `pkexec` through the desktop authentication prompt; never collect a password in chat or weaken sudo policy.
3. Inspect the actual hierarchy. On versions documenting entry-path support, a menu headed `/+Omarchy` with child `//<kernel-package>` can use `default_entry: Omarchy/<kernel-package>`. The `+` expands the menu and is not part of the path. Resolve the named entry rather than counting visible rows or including snapshot duplicates.
4. Verify the entry's referenced artifact under the ESP. UKI entries use `protocol: efi` and may point to `/EFI/Linux/<name>.efi`; preserve any hash suffix in the entry. Check the actual file exists and is nonempty without regenerating it.
5. Inspect the installed wrapper's locking convention before mutation. Where it uses `/run/lock/boot-partition.lock`, acquire that same lock around the read/backup/update sequence. Assert exactly one matching default directive, create a unique backup beside the config, and modify only its value. A small inspected Python script staged in the runtime scratch directory and executed with `pkexec /usr/bin/python3 <script>` supports this narrowly scoped privileged change.
6. In a separate privileged readback, verify the resulting default and compare against the exact backup path returned by the write operation. Do not select a backup by globally sorting filenames; another update may create a newer backup. Confirm fallback entries remain unchanged. Report configuration verified, reboot not performed, and boot compatibility unproven.

Do not invoke `limine-update` as a selection setter: inspect its installed implementation, which may call `limine-install` and `limine-mkinitcpio`. Likewise, inspect `limine-entry-tool --help` through its non-mutating implementation or documented help route rather than assuming it provides a default-setting option.

## Honest no-change completion

When generic coverage is established, say so directly. Provide the exact package-install command only if useful, with installation clearly pending. Preserve the active build, all existing repository modifications and the working kernel. Do not manufacture persistent files merely to satisfy the word “add.”
