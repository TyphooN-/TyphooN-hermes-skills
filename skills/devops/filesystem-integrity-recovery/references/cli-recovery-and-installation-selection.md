# CLI recovery and installation selection

Use for an application command that silently succeeds, an interrupted atomic update, or competing installation methods on a host with crash/integrity evidence. These are diagnostic patterns, not assertions about the current machine or permanent installation paths.

## Bounded sequence

1. Resolve all command candidates (`type -a`), selected symlink target (`readlink -f`), and file metadata (`stat`). Read shell wrappers before running them: a wrapper may reinstall a package or select an old runtime. Do not dump environment variables or credential files.
2. If the command returns no output, check the actual executable content before calling the updater repeatedly. A zero-byte executable shell script may return 0 for help, doctor, and update alike. Establish meaningful expected output, not just exit status.
3. Find a trusted restoration source: installed console-script metadata plus importable module, a verified package, or a retained generation. If copying a launcher across generations, correct and validate its interpreter path; do not copy a stale absolute shebang blindly. Do not reconstruct arbitrary damaged source from guesses.
4. Inspect interrupted-activation metadata and pointer consistency without immediately editing either. Prefer supported recovery. Read what recovery does first: it may re-enter the CLI, refresh managed content, roll back, or delete a refused candidate. Preserve user-modified managed files and do not force replacement merely to make doctor green.
5. Restore only the smallest justified artifact. Verify byte-zero `#!`, executable mode, target interpreter, and imports. For small durable writes use atomic replacement, file fsync, and parent-directory fsync where appropriate; preserve prior valid evidence. These measures improve durability, not filesystem trust.
6. Inspect runtime bootstrap before invoking even a check command on an alternate install. Version/help may be exempt from dependency guards, while update/check or normal launch may run sync and product builds. Use a supported passive readiness probe if available. Do not switch the default to an unready install or bypass guards to conceal incompleteness.
7. Exercise the restored command and record separate exact exits: launcher/help, update preview, actual update if safe, activation consistency, and health checks. Mark unexecuted stages explicitly. Distinguish plugin installation, import/register smoke, and real host load.

## Reboot recovery

- An interrupted process is not completed work. Verify boot identity, original PID/PGID/session death, descendants, and ownership before resuming.
- `/tmp` evidence can disappear on reboot. Use a private persistent directory when interruptions are plausible, but remember that a directory on the affected device is not an independent backup.
- A persisted file may also be empty or malformed after reboot. Validate nonzero size and parseability; preserve invalid evidence and record the former exit as unknown rather than inventing success.
- Resume the existing coding session only when source/base and ownership remain compatible. Provide the new evidence path explicitly. Avoid restarting discovery repeatedly or relaunching an agent merely to obtain missing prose.
- Inspect background child exit and final result, not just wrapper exit 0. A CLI may emit a nominal success result containing a usage-limit message; classify the actual outcome and preserve remaining work without repeated provider probes.

## Installation selection and support warnings

Consult current primary vendor documentation. Do not infer support status from the presence of a package, a historical installer, or a package-manager label.

For an installation-method warning, compare:

- The command chosen in the active shell versus a fresh login shell.
- Package-manager activation/shims versus the user's bin wrapper.
- Installed runtime versus source checkout and managed dependency generation.
- Version/source identity versus normal-launch readiness.

Inspect the relevant package-manager selection and wrapper only. Once the supported runtime is ready, back up and change the minimal selection/launcher, keep the prior binaries until verification, and avoid terminating current sessions. Editing only a low-priority wrapper will not fix a higher-priority activated executable on PATH.

## Integrity gate and reporting

Fresh checksum findings in generated build outputs are evidence about those outputs, not proof that the CLI source is damaged. Repeated reboot interruptions and kernel memory-state faults can independently justify pausing a large rebuild. State the relevant evidence, bounded work still safe, and the exact next diagnostic or resumption condition.

Report in three parts: **artifact actually repaired**, **commands actually verified**, and **remaining blockers**. Do not call a preview an update, an import smoke a runtime load, or a flushed local checkpoint an independent backup.
