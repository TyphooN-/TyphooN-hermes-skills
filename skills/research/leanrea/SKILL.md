---
name: leanrea
description: Use when inspecting Fury artifacts with local CLI tools.
version: 0.1.0
author: AICodeKing; Fury-specific adaptation by Hermes Agent
license: MIT
platforms:
- linux
metadata:
  hermes:
    tags:
    - fury
    - preservation
    - reverse-engineering
    - static-analysis
    related_skills:
    - legacy-game-static-assessment
x-local-maintainer: TyphooN (TyphooN-)
---


# LeanREA for Fury

## Portable scope

This copy preserves a locally developed workflow, not transferable approval. Resolve the current task, repository, active Hermes profile, tools and ownership on this machine first. Historical project choices and TyphooN-specific executor/build policies are context, not permission to start services, run targets, modify security settings or publish. Project-root variables are documented in the collection's `PORTABILITY.md`; unset variables are not usable paths. Installing a skill installs no external tools or plugins.

Use the direct-tool workflow from `https://github.com/aicodeking/leanrea`, selected by TyphooN for Fury on 2026-10-26 instead of REA. This is a Fury-scoped Linux adaptation, not an MCP server or a claim of tool parity. Other projects' REA registration is unchanged.

## When to use

Use for admitted Fury binaries, script packages and saved evidence. Do not use it as permission to execute recovered code or to alter the original project. Ordinary source-repository architecture work needs no reverse-engineering workbench.

## Source and prerequisites

The selected checkout is `$LEANREA_ROOT/`, commit `09ba4aa0217f82cd880f855a60b877f59f39b22b`. Read [upstream provenance](references/upstream-source.md) for the frozen upstream guide, source digest and license. For another target format, consult that guide as reference, translating its shell recipes to the available Hermes tools and current task limits; do not run its examples verbatim.

Check tool availability; a skill installation does not install or qualify Ghidra, Java, debuggers, packet engines or runtime instrumentation. No npm/MCP server is needed. Never fall back to REA, install dependencies or run setup merely because a preferred tool is absent.

## Procedure

1. Recover the accepted checkpoint, credential exclusions, task-specific permissions and current owner. Retain source-bound accepted findings; switching workbenches does not invalidate earlier evidence or discharge missing independent review.
2. Keep `$FURY_ROOT` and original media immutable. Use only individually admitted, hash-bound copies in new private evidence under the active Hermes cache. Do not initialize Git there. Use the configured scratch directory, never an assumed system temporary directory.
3. Identify format from magic bytes and `file`, then run the cheapest relevant inventory. On Linux, use `objdump -x` for PE and `readelf -hlSW`/`readelf -dW` for ELF; do not apply ELF-only commands to PE. Existing static tools are the fast path, not a new REA service.
4. For an admitted PE copy, use `terminal` to capture `file -b -- <copy>`, `objdump -x -- <copy>` and, only for named half-open address ranges, `objdump -d -M intel --insn-width=16 --start-address=<VA> --stop-address=<end-VA> -- <copy>` into private files. Batch independent probes, recording every exit separately. Keep stdout bounded with Python projections; use `read_file` and `search_files` instead of shell dump/search pipelines.
5. Follow named strings, imports, direct calls and known entrypoints before broad decompilation. Preserve image identity, file offset/RVA/VA, encoded bytes and instruction extent. Use the existing qualified UE/package decoders for nonstandard game formats; a generic skill does not establish their layout or semantics.
6. Preserve exact argv/cwd/tool/input identities, complete private captures and producer exits. Report findings as observed static evidence, inferred interpretation or unknown. A missed search is not absence; a disassembler result is not observed execution or a recovered protocol.

## Fury boundaries and pitfalls

- Do not open, stat, hash, decode or reproduce excluded credential-bearing files. Never contact embedded or historical endpoints. Restrict string projections to the admitted allowlist; do not dump a whole legacy configuration or binary string corpus into model context.
- No game/server/Wine/installer/debugger, prototype or native-provider execution follows from this skill. Recover any later disposable-lab approval and satisfy its actual admission gates separately. A prior policy refusal is not permission to disguise or retry the refused task.
- No destructive extraction cleanup, global installation, permission/security changes, paid usage, public exposure, commits or pushes. Upstream `rm -rf`, `brew`, `npx`, tracing and package-install examples are not authorization.
- Keep the existing preservation and static-evidence discipline in `legacy-game-static-assessment`; this skill changes the analysis route, not the evidence standard. Do not cite upstream benchmark claims as local measurements.
- Treat CLI display labels as version-dependent: `file` may call the same PE32 machine `Intel i386` or `Intel 80386`. Check encoded format/machine and selected original bytes instead of asserting one display spelling.

## Verification

Qualify a newly chosen static CLI on an explicitly synthetic, nonexecuted fixture first. Record the fixture bytes/hash, expected format and selected decoded instructions, command exits, bounded result and absence of target execution. This proves only that narrow static path, not native decompiler readiness or correctness for the full Fury image. Require the existing independent-review gate for new high-risk claims.
