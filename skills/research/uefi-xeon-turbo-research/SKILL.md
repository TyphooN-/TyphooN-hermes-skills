---
name: uefi-xeon-turbo-research
description: Use when investigating Xeon BIOS turbo unlocks.
version: 0.1.0
author: Hermes Agent
license: MIT
platforms:
- linux
metadata:
  hermes:
    tags:
    - UEFI
    - BIOS
    - Xeon
    - Firmware
    - Research
    related_skills:
    - grounded-citations
    - requesting-code-review
x-local-maintainer: TyphooN (TyphooN-)
---


# UEFI Xeon turbo/multiplier feasibility

## Portable scope

This copy preserves a locally developed workflow, not transferable approval. Resolve the current task, repository, active Hermes profile, tools and ownership on this machine first. Historical project choices and TyphooN-specific executor/build policies are context, not permission to start services, run targets, modify security settings or publish. Project-root variables are documented in the collection's `PORTABILITY.md`; unset variables are not usable paths. Installing a skill installs no external tools or plugins.

Use for static BIOS investigation, not authorization to patch, flash or operate hardware. Load REA and grounded-citations as well.

## When to Use

- Investigating all-core turbo or multiplier-unlock claims against an actual Xeon BIOS image.
- Comparing a known unlock driver with another CPU generation or checking whether hidden menus imply real capabilities.
- Do not use as permission to flash, access hardware or modify firmware.

## Bind identity and acceptance

- Separate maximum existing turbo-bin reuse on every core, arbitrary higher multiplier OC, BCLK changes and sustained permitted-turbo tuning. These require different proof.
- Distinguish production, OEM and ES/QS samples. Record expected CPUID separately from measured sample identity; an “unlocked” software flag is not hardware proof.
- Hash the selected release and record Git HEAD/status. Compare with tracked release copies where useful; preserve user-owned untracked images.
- Treat README tables and historical IFR exports as leads until bound to the actual image. Never supply current NVRAM write offsets from an older unbound IFR.

## Analyze without overstating the tool route

- Inspect the existing REA session/provider state and preserve its pin. Do not bypass validation with npm, a moving-checkout CLI or another persistent registration.
- Report missing native/firmware providers precisely. Do not automatically install Ghidra/JDK/system tools or change shared configuration.
- If admitted, use a supplemental format-aware UEFI parser/decompressor in an isolated evidence environment. Label this supplemental parsing, not REA decompilation. Never execute extracted EFI/firmware or downloaded target utilities.
- Preserve active descriptor bounds, FV/FFS headers, decompression lineage, module GUIDs and section hashes. Decompressed PE offsets are not original flash offsets or observed runtime addresses. Zero parser errors describe that parser's examined coverage only.
- Separate microcode structure/checksum, public-blob identity, cryptographic authentication and runtime loading. Inspect helper argv first and keep every output argument pointed at evidence, never original input images.

## Trace the actual control boundary

- Decode the current HII mode selector before diagnosing ignored ratios. All Core, active-core-count Turbo Ratio, and Per Core modes can select different policy paths; a nonzero global ratio may intentionally replace the table.
- Compare backing VarStore identities for similarly named ratio menus. A hidden reference-code form and a vendor OC form may store independent profiles; shared labels do not prove synchronization or consumer reachability.
- Follow setup policy through CPU policy and power-management modules to capability gates and MSR instruction sites. Raw byte hits are candidates, not control-flow proof. Decode from known boundaries and retain commands plus module hashes.
- Consult primary Intel documentation for the exact CPU model. Haswell-EP and Broadwell-EP turbo override/semaphore details differ; changing a driver's CPUID allowlist is not a new processor exploit.
- Distinguish setup suppression, BIOS OC locks, SPI protection and read-only processor capabilities. A firmware branch patch does not establish CPU acceptance of an otherwise prohibited ratio.
- Inspect original unlock source and admission checks. Distinguish highest allowed turbo-bin reuse from an above-factory multiplier unlock, and built-in microcode from a BIOS/OS update.

## Research and preserve evidence

- Use public Discourse topic JSON when HTML extraction fails. Save raw JSON and readable text; compare fetched post IDs with the returned stream and declared count. Deleted post numbers mean the maximum post number is not the count.
- Read the supplied post specifically. AMITSE reboot/M-Flash fixes and hidden-menu unlocks are not turbo-unlock demonstrations.
- Corroborate reports with independent authors/dates, original implementation and primary register documentation. Keep bounded “no verified method found” separate from physical impossibility or fuse-level proof.
- Mark snippets, blocked bodies and full fetched pages distinctly. Do not turn ES claims, BCLK gains, high-stock-all-core SKUs or peak-frequency screenshots into production all-core unlock evidence.
- Preserve interrupted executor evidence; a reboot/quota stop is not a completed review. Keep the current executor approval and no-paid-fallback boundary.
- Probe in scratch, then retain the final report and selected evidence in a private durable directory outside the read-only checkout; scratch expiry must not erase the source chain.

## Pitfalls

- Do not equate downloaded-file presence with a valid fetch; reject HTML error bodies and preserve retrieval gaps.
- Do not infer whole-firmware or runtime coverage from module names, zero parser errors or immediate-byte searches.
- Do not read a missing exit receipt as successful completion after a reboot; establish process ownership release before resuming.

## Verification

Use `terminal` for exact tool commands and preserve their exit codes. Use `read_file` for bounded source/manual checks and `write_file` for the report. Verify source/repository preservation, extracted-section hashes, topic stream completeness and cited quotations. Retain a manifest binding the final report to its selected evidence. Mark hardware behavior, native-provider coverage and unsupported-sample questions unresolved when not exercised.

## Finish

Deliver a CPU-class feasibility matrix, actual-image findings, sourced mechanism, explicit unknowns, exact check exits and a safe next decision. Do not manufacture a flashable patch for a research request.

Recommend separately admitted read-only target identity, guarded model-valid capability/turbo-table reads and existing limit telemetry first. Future workload or firmware experiments need their own scope. A claimed unlock requires all enabled physical cores, sustained effective rather than requested frequency, workload/AVX context, retained protections, error checks and recovery/reboot proof. This skill authorizes no register writes or flashing.
