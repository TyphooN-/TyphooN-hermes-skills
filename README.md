# TyphooN Hermes Skills

A portable collection of the custom Hermes skills and bundled-skill adaptations developed in TyphooN's day-to-day engineering work. These are the full working procedures and companion files—not short descriptions or empty templates.

**27 skills:** 17 local workflows/integrations and 10 bundled overrides, with 98 payload files. See [CATALOG.md](CATALOG.md) for every skill, [PORTABILITY.md](PORTABILITY.md) for machine-specific parameters and prerequisites, and [THIRD_PARTY.md](THIRD_PARTY.md) for licenses and upstream attribution.

The collection covers executor orchestration, source-bound code reviews, testing/debugging, filesystem/boot recovery, local-model qualification, Omarchy customization, source ports and static reverse engineering. Project-specific skills are retained with explicit path parameters rather than discarded.

## What is and isn't included

- All selected skill entry points and their references, templates, scripts and licenses.
- Locally modified bundled skills such as `claude-code`, `hermes-agent`, `requesting-code-review`, `systematic-debugging` and `test-driven-development`.
- Local adaptations of LeanREA and Cloudflare's security-audit workflow, with their original provenance and licenses.
- No unrelated unchanged bundled skills, upstream OMH distribution, Omarchy symlink targets or plugin-provided REA. Obtain those through their original distributions.
- No credentials, profile settings, private session history, evidence logs, model weights, firmware, game artifacts or wallpapers.

`coverage.json` records the complete dated selection/exclusion inventory. The export does not automatically follow future changes to the source machine.

## Install from a local clone

Requires an existing Hermes installation and **Python 3.10+**. The packaging helper is standard-library-only, offline, and never executes a skill's commands. Review the selected skill before using it; installation is not operational approval.

Run these commands from this checkout. Choose the destination's actual active profile home; `$HERMES_HOME` is profile-specific when set, while `$HOME/.hermes` is the usual default. No `config.yaml` edits or service restarts are performed.

```bash
# Verify all checked-in packages before copying anything.
python3 -B scripts/skills.py verify
python3 -B scripts/skills.py list

# Preview ALL skills. A plan never creates or changes destination files.
python3 -B scripts/skills.py install --home "${HERMES_HOME:-$HOME/.hermes}"

# Apply after reviewing the plan. Existing skill identities cause a refusal.
python3 -B scripts/skills.py install --home "${HERMES_HOME:-$HOME/.hermes}" --apply
```

To install a single skill or a chosen subset:

```bash
python3 -B scripts/skills.py install --home "${HERMES_HOME:-$HOME/.hermes}" \
  --skill git-remote-ref-recovery --skill rust-workspace-dependency-refresh
# Add --apply only after reviewing the plan.
```

On Windows, use the same Python commands with an explicit `--home "C:\\path\\to\\profile"`; shell-variable syntax above is for POSIX shells. The helper uses `pathlib` and copies files, not shell recipes. No Windows/macOS runtime test is claimed.

### Existing bundled skills and updates

Ten packages intentionally reuse bundled skill identities. The default apply command refuses **before any write** if any selected identity is already present, even under another category. It does not silently merge directories or leave two discoverable copies of a skill.

To deliberately replace existing versions, first review the plan, then use:

```bash
python3 -B scripts/skills.py install --home "${HERMES_HOME:-$HOME/.hermes}" --backup-existing
python3 -B scripts/skills.py install --home "${HERMES_HOME:-$HOME/.hermes}" --backup-existing --apply
```

Each replaced directory is moved intact to `HERMES_HOME/skill-install-receipts/install-*/originals/`, **outside** the discoverable skills tree. The result prints exact backup and receipt paths. All selected source copies are staged and hash-checked before originals move; each completed move is recorded. Collection-level notices are copied into that receipt directory. Unselected installed skills are left alone. Symlinked selected skills/destinations, duplicate identities, unsafe paths, changed source payloads and unknown selected names are rejected.

Run while no other process is writing the destination skills. This helper is not a sandbox or a concurrent multi-user transaction. A filesystem failure during final placement can leave a partial install; it returns nonzero and preserves the receipt, staged files and originals. Do not rerun blindly. Read the receipt and restore affected original directories to their recorded paths only after preserving any newer changes. There is no automatic destructive rollback or backup pruning.

For updates, review the new checkout diff, run verification/tests, inspect the plan and explicitly apply with backups. Do not run `hermes skills reset` on these overrides expecting it to preserve local changes; that command concerns the upstream bundled version. The collection does not modify Hermes' bundled-sync manifest or its security scanner. SHA-256 integrity checks detect changed package bytes; they are not a malware review or trusted signature.

### Confirm discovery

On the destination, use Hermes' native `skills_list` and `skill_view(name="<selected-name>")` tools, or the installed version's `hermes skills list` command. Confirm the expected identities and load a supporting file. Begin a fresh session if the running version retains an old discovery snapshot; do not assume that copying files updated already-loaded model context.

The Linux packaging proof exercised this collection's installer in a disposable home, verified all 27 identities and 98 files, and checked discovery using the installed Hermes discovery utility. It did not execute recovery recipes, install external tools, start services or change the active profile.

## Development and verification

The default verifier checks exact payload/file sets, hashes, identity/frontmatter framing, short descriptions, coverage totals, known private-path leakage and support links. Full YAML parsing is an additional development check:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -B scripts/skills.py verify --yaml
.venv/bin/python -B -m unittest discover -s tests -v
```

On Windows, use `.venv\\Scripts\\python` instead of `.venv/bin/python`.

After deliberately editing a skill, update its corresponding metadata in `skills-manifest.json` if needed, then run:

```bash
python3 -B scripts/update_catalog.py
.venv/bin/python -B scripts/skills.py verify --yaml
.venv/bin/python -B -m unittest discover -s tests -v
```

Regeneration deliberately accepts the current file bytes as a new baseline; it is a maintainer action, not a way to make an unreviewed downloaded package safe. Tests cover every included package and exercise fresh installation, explicit selection, collisions, backup preservation, malformed metadata, missing assets, stale integrity/catalogs and unsafe links/paths. No live provider or target execution is needed.

## Licensing and sharing

The existing repository license is GPL-3.0; imported MIT-licensed material retains its own license and attribution. See [THIRD_PARTY.md](THIRD_PARTY.md), individual frontmatter and shipped license texts. “Custom/local” includes integration work around third-party material; it does not claim ownership of that upstream work.

This is a locally prepared collection. No public push, release or external publication is implied by creating it.
