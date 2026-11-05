---
name: omh-handoff-scan-notes
description: Use when handoff scans fail. Diagnose and retry safely.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags:
    - handoff
    - omh
    - verification
    related_skills:
    - ulw-work
    - ulw-maestro
    - claude-code
platforms:
- linux
- macos
x-local-maintainer: TyphooN (TyphooN-)
---


# OMH handoff scan troubleshooting

## Portable scope

This copy preserves a locally developed workflow, not transferable approval. Resolve the current task, repository, active Hermes profile, tools and ownership on this machine first. Historical project choices and TyphooN-specific executor/build policies are context, not permission to start services, run targets, modify security settings or publish. Project-root variables are documented in the collection's `PORTABILITY.md`; unset variables are not usable paths. Installing a skill installs no external tools or plugins.

## When to Use

Use when `omh handoff-risk-scan` returns an input or parsing error, including `repository_invalid` or `command_syntax_invalid`. Classify the failed input, repair only that input and rescan the final brief. This is scanner troubleshooting, not approval to alter actual commands, substitute a different execution target or bypass risk findings.

Companion to `ulw-work` and `ulw-maestro`; load their main contracts for handoff policy. This note does not change approval, ownership or dispatch authority.

- Resolve the writer source and scan root before Git-dependent preflight. For a declared Git workspace, run `git -C "$SCAN_ROOT" rev-parse --show-toplevel` once. For an intentional non-Git snapshot, verify its complete file manifest, explicit baseline diff and ownership instead; do not continue Git queries or initialize a repository merely to satisfy the scanner.
- Classify `repository_invalid` as an incomplete scan of the supplied target, then inspect `omh handoff-risk-scan --help`. When `--repo` is optional, rescan the unchanged final brief with `omh handoff-risk-scan --brief-file "$BRIEF" --strict --json`, omitting only the inapplicable Git-root argument. Preserve the failed receipt and label the new result brief-only: it does not inspect the snapshot's dirty inventory or replace candidate-specific safety/proof checks. If separately requested provenance-repository context is supplied, record both roots and their different roles; never substitute that repository for the authorized writer or report its scan as candidate acceptance.
- Treat `scan_error` with `command_syntax_invalid` as an incomplete scan, not a safe verdict or necessarily a malformed CLI invocation. The scanner tokenizes each actionable brief line with shell-style quoting; a trailing plural possessive in ordinary prose can be interpreted as an unterminated quote.
- Locate the malformed prose line with bounded, nonexecuting lexical inspection. Rephrase only natural-language prose (for example, change `other sessions' projects` to `work from other sessions`). Preserve literal identifiers, real shell commands and every safety constraint. Never remove a real risk or disable the scanner to obtain a pass.
- Preserve the failed receipt and rescan the complete final brief through the documented CLI. A known dirty isolated overlay can remain a medium advisory; record its preserved preimages and ownership rather than calling an advisory result completely clear.
- Respect a curator lock reported by the skill manager: stop editing that target and report the suggested change, rather than recreating or shadowing the locked skill under another name. Classify other edit refusals by their actual cause; installed or generated provenance alone is not a blanket prohibition on an otherwise authorized skill update.
