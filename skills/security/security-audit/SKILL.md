---
name: security-audit
description: Use when reviewing code for security vulnerabilities.
version: 0.1.0
license: MIT
author: Cloudflare, Inc.
metadata:
  hermes:
    tags:
    - security
    - audit
    - vulnerabilities
    - source-review
platforms:
- linux
- macos
- windows
x-local-maintainer: TyphooN (TyphooN-)
---


# Security Audit

## Portable scope

This copy preserves a locally developed workflow, not transferable approval. Resolve the current task, repository, active Hermes profile, tools and ownership on this machine first. Historical project choices and TyphooN-specific executor/build policies are context, not permission to start services, run targets, modify security settings or publish. Project-root variables are documented in the collection's `PORTABILITY.md`; unset variables are not usable paths. Installing a skill installs no external tools or plugins.

Use Cloudflare's source-first security audit workflow for security questions, focused vulnerability reviews, and explicitly requested codebase audits. This Hermes entry point loads the unmodified upstream package, whose companion documents, schemas, and validators retain their original relative layout.

## When to Use

- Security questions or a focused source-code vulnerability review.
- An explicitly requested security audit or pen test of an authorized codebase.
- Do not start an audit merely because this skill was imported or loaded.

## Load the workflow

Before applying this skill, load its complete instructions:

`skill_view(name="security-audit", file_path="references/upstream/SKILL.md")`

For that workflow, the **skill directory** is the absolute directory containing `references/upstream/SKILL.md`, not this entry point. Load companion documents relative to that directory, or through `skill_view` with the `references/upstream/` prefix. All companion files shipped by the local source package are included there.

## Scope and safety

- Loading or importing this skill does not authorize an audit, target changes, artifact creation, live probing, publication, spending, or additional agent calls.
- Use guidance mode by default. Run the complete six-phase workflow only when the user's request explicitly calls for it, as defined in the upstream instructions.
- Preserve the active task's approval boundaries, model/provider restrictions, and independent-review requirements. This imported workflow does not expand them.
- Do not execute target-controlled code unless every sandbox control required by the upstream workflow is enforced. Otherwise retain the exact needs-validation blocker.
- Node.js is required only when running the bundled JSON validators. Installation does not execute those scripts or install dependencies.

## Provenance and verification

Imported from the user's local `git/security-audit-skill/` checkout. Read `references/import-manifest.json` for the observed revision and per-file SHA-256 hashes. The original instructions and supporting files are preserved under `references/upstream/`, together with the upstream README and MIT license. Confirm installation with `skill_view(name="security-audit")` and load the upstream instructions before use.
