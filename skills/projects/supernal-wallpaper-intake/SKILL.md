---
name: supernal-wallpaper-intake
description: Use when adding Supernal wallpapers. Audit colour coverage.
version: 0.1.2
author: TyphooN-, Hermes Agent
license: MIT
platforms:
- linux
metadata:
  hermes:
    tags:
    - omarchy
    - wallpaper
    - palette
    - verification
    related_skills:
    - omarchy
    - claude-code
x-local-maintainer: TyphooN (TyphooN-)
---


# Supernal Wallpaper Intake

## Portable scope

This copy preserves a locally developed workflow, not transferable approval. Resolve the current task, repository, active Hermes profile, tools and ownership on this machine first. Historical project choices and TyphooN-specific executor/build policies are context, not permission to start services, run targets, modify security settings or publish. Project-root variables are documented in the collection's `PORTABILITY.md`; unset variables are not usable paths. Installing a skill installs no external tools or plugins.

## When to Use

Use for adding source wallpapers to Supernal or assessing whether a new batch
needs additional palette roles. Do not use for unrelated desktop changes or
assume that a request for assessment authorizes palette edits.

## Scope and truth

Maintain `$SUPERNAL_ROOT` with remote
`https://github.com/TyphooN-/omarchy-supernal-theme.git`; user source images are in
`$SUPERNAL_IMAGES`, and the custom installed theme is
`~/.config/omarchy/themes/supernal`. Load the Omarchy theming guide first.
Use current repository instructions and `docs/palette-assessment.md`, not a
remembered asset count or hardcoded palette, as the task's source of truth.
A source-repository rename does not rename the visible Supernal theme or its
installed `supernal` slug: verify the local installer's prefix/suffix stripping.
Do not validate a Git rename by reinstalling the theme; the native installer
replaces an existing custom theme directory and applies the new clone. Document
that replacement behavior and preserve live customizations during repo-only work.

## Safe asset import

1. Establish sole-writer ownership and capture repository HEAD/dirty state,
   source/installed/active asset inventories and hashes, palette bytes and
   the active background symlink before changes.
2. Compute missing names and byte duplicates. Copy only missing images with
   original bytes/names; refuse same-name/different-content collisions.
   Preserve all originals and unrelated files.
3. Inspect the installed Omarchy background lookup. If the active generated
   theme uses an independent `~/.local/state/omarchy/current/theme/backgrounds`
   copy, add the same new assets there as well. For an asset-only update,
   targeted additive copies can avoid a broad theme reapply and preserve the
   selected wallpaper. Never assume that layout without inspecting it.
4. Verify filename sets, counts, decode success and every copied SHA-256
   against the source; recheck all pre-existing live files and the selection
   symlink before reporting the import complete.

## Palette assessment

- Run the repository's `tools/palette_audit.py` using a separate `--new NAME`
  for each actual addition. Parse `colors.toml`; never substitute a stale
  palette dictionary or synthetic HSV bin-centre colour.
- Use per-image pixel denominators and explicitly equal-image-weighted
  aggregates. Do not label summed image fractions as one-image percentages.
- Separate dark/neutral pixels from chromatic area. Compare chroma and hue
  together, report intentional foreground lightness adaptation separately,
  and exclude selection/surface tokens from usable foreground coverage.
- State thresholds and sensitivity. Heuristic coverage is neither perceptual
  identity nor a rendered accessibility score; nominal contrast on black
  does not prove contrast at terminal opacity over a wallpaper.
- Distinguish a genuinely new family from existing saturation/rose variants.
  Do not remap ANSI roles or add unused keys merely to chase minor shades.
  An optional extra accent needs an actual consumer to change the UI.
- An assessment request alone does not authorize palette edits. Preserve the
  palette and give measured recommendations unless the user assigns changes.

## Proof and integration

Update the asset count and checked-in assessment; preserve creator profile
links and source-post URLs without inventing per-file attribution or rights.
Run the audit's `--check` against the report and the current test suite;
require actual nonempty test execution. Label inherited characterization
separately from new RED-to-GREEN fixes. Stage explicit owned paths, inspect
all outgoing history and normal-push only when the workflow authorizes it;
verify the exact remote branch tip afterward. Keep raw logs/private evidence
outside the repository. Claude remains the primary executor under the
operator's Opus-Max contract; on confirmed lockout preserve its partial work,
prove ownership release and finish through the authorized supervisor route.
