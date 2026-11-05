# Portability and operating boundaries

These are preserved development procedures, not a copy of the original machine's configuration. Installing them does not install Hermes, Claude Code, OMH, REA, Docker, Omarchy, compilers, browsers, model runtimes or recovery utilities. Check prerequisites in the selected skill, and obtain the current task's authority before taking action.

## Resolve paths, do not inherit them

Before using a project-specific skill, identify the actual repository and read its instructions. The following names in prose are **parameters**, not configured defaults. Set them only to paths you have verified, or substitute the verified paths when preparing a task. An unset shell variable can collapse a path to `/`; never execute a command with an unresolved parameter. Use `${NAME:?set NAME to the verified path}` in executable shell commands.

| Parameter | Meaning |
| --- | --- |
| `HERMES_HOME` | Active profile's home; resolve it through the installed Hermes runtime. The install command requires an explicit `--home` and does not select a profile for you. |
| `FURY_ROOT` | Preserved original Fury artifacts; this is not a writable lab directory. |
| `LEANREA_ROOT` | Optional LeanREA source checkout, at the pin recorded in that skill. The referenced upstream guide is included. |
| `OMARCHY_DEV_ROOT` | Private/customization development checkout, distinct from the stock running checkout. |
| `OMARCHY_PATH` | Verified stock/running Omarchy checkout selected by the updater. |
| `OMARCHY_MAINTENANCE_PLAN` | Current accepted maintenance plan, if any. The original private plan is not distributed. |
| `SUPERNAL_ROOT` | Supernal theme repository. |
| `SUPERNAL_IMAGES` | User-chosen source wallpaper directory; the image collection is not distributed. |

Paths such as `~/.config/omarchy`, loopback URLs, container names and sample configuration paths in upstream guides are conventions or examples, not proof of the current host. Inspect live source and configuration before using them. The security-audit import manifest uses repository-relative provenance rather than private absolute paths.

## Profiles, dependencies and platforms

- The collection was packaged and tested on Linux. `platforms` metadata describes the workflow's intended applicability, **not** a claim that it was exercised on every listed operating system. Omarchy, kernel, filesystem and GPU-specific procedures remain Linux-gated where appropriate.
- Pure repository workflows may be useful on other operating systems, but audit shell and tool dependencies first. The packaging helper uses Python 3.10+; installing a Linux-only skill on another OS does not make its commands available.
- `CATALOG.md` lists external related skills. They are intentionally not all vendored: use the original Hermes bundled/optional distribution, the current OMH package, or the relevant Omarchy/REA installation. A missing companion is a prerequisite to resolve, not permission to invent its contract.
- Follow the destination machine's installed Hermes documentation for profile selection and skill discovery. `--home` must identify that profile's actual home; do not assume that the default profile lives under `profiles/default`.
- Hermes recognizes the entry-point `SKILL.md` in each skill directory. A vendored `references/upstream/SKILL.md` belongs to a supporting package and is not an additional top-level skill.

## Policy is not transferable approval

TyphooN's Opus-Max execution policy, no-coauthor preference, 44-thread build preference and project-specific preservation/design choices remain visible because they are useful parts of the custom workflows. Another operator should adopt or adapt them deliberately. They do not override that operator's current instructions or available hardware, and they authorize no spending, credential changes, production activation, firmware writes, transactions or publication.

Fury/UEFI instructions remain static-analysis and preservation workflows unless a separate current task admits execution. The included recovery recipes are **not** run by the installer or test suite.

## Updates and source fidelity

The initial export was made from a stable, hash-checked source snapshot on 2026-11-05. `coverage.json` accounts for the 80 regular/symlink skills in the active profile: 27 included, 49 unchanged bundled, 3 upstream Omarchy links and 1 redacted private project skill. The separately registered OMH package provided 153 skills and is not copied. Plugin-provided skills remain with their original plugins. A second existing local profile was inventoried read-only: 57 origin-matching packages and two 43-byte, header-only `offline` placeholders in its `pdf`/`docx` slots. Those placeholders contain no workflow to export; no additional complete custom skills were found and that profile was not changed.

All 98 selected original payload files were preserved, with explicit portability/frontmatter/provenance adaptations. The missing referenced LeanREA upstream guide was restored from its SHA-256-bound source, bringing the exported payload to 98 files. `skills-manifest.json` records original package digests, per-skill adapted files and the current exported file hashes. Repackaging does not establish that a recipe's external command syntax still matches a future tool version.

The inventory is a dated snapshot, not an automatic synchronization service. To refresh, compare current local skills against their recorded bundled origin using the installed `tools.skills_sync.dir_hash` algorithm, inspect supporting-file-only differences, freeze the selected sources, review privacy/licenses and update the collection deliberately. Never export `.usage`, `.hub`, curator logs, credentials, session history or another profile by recursively copying the entire Hermes home.
