# Licensing and provenance

The repository's existing root `LICENSE` is GPL-3.0. It applies to the new collection tooling/documentation and original local material that did not already declare another license. It **does not erase or relicense** the MIT notices on imported skills. The per-skill `license` and `author` fields, the catalog and `skills-manifest.json` identify the applicable declarations.

## Sources retained

- **Hermes Agent** — ten locally modified bundled skills and their companion files, obtained through the local Hermes installation. Source: https://github.com/NousResearch/hermes-agent . The observed source checkout revision is in `coverage.json`; this revision is context, not a claim that the local modifications were upstream at that commit. Original `author` fields, including Teknium, BadTechBandit, and the obra/superpowers and MorAlekss adaptation credits, remain intact. The upstream MIT text and Nous Research copyright notice are in `licenses/hermes-agent-MIT.txt`.
- **LeanREA** — https://github.com/aicodeking/leanrea , commit `09ba4aa0217f82cd880f855a60b877f59f39b22b`. The Fury-specific entry point is a local adaptation. Its pinned original guide, digest and AICodeKing MIT license are included in `skills/research/leanrea/references/`. Private adoption logs were not copied.
- **Cloudflare security-audit-skill** — https://github.com/cloudflare/security-audit-skill , commit `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`. The Hermes wrapper is a local integration, not a claim of authorship of Cloudflare's workflow. All 22 original upstream package files, including the MIT license, validators and tests, remain byte-identical under `skills/security/security-audit/references/upstream/`. The import manifest retains the pin and individual file hashes without the original machine's absolute paths.
- **Other local workflows** — retained with their original MIT declarations where present. Four original local workflows had no declared license; their missing metadata is completed using the repository's GPL-3.0-only license and TyphooN/Hermes attribution. The source null values remain visible in the manifest rather than inventing historical declarations. The exact number and names can be read from `source_license: null` in the manifest.

“Local/custom” describes a workflow or integration's installation provenance; it is not a claim that all its prose was written here. Ordinary upstream bundled skills, the upstream OMH package, the Omarchy symlink targets and plugin-provided REA are dependencies, not redistributed as this project's work.

No wallpaper images, game binaries, firmware, private logs, credentials, profile configuration, session transcripts or user datasets are included. Skills that discuss those artifacts convey no rights to them. Preserve third-party notices when copying individual skills; the package installer copies the skill's own notices and also ships the collection-level license/provenance files alongside its receipt.

This repository is a local packaging checkpoint. Validation and attribution are not legal advice or approval to publish private project information; public publication remains a separate decision.
