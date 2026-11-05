# Skill catalog

Generated from `skills-manifest.json` by `scripts/update_catalog.py`.

| Skill | Kind | Platforms | License | Purpose |
| --- | --- | --- | --- | --- |
| [blocked-page-recovery](skills/web/blocked-page-recovery/SKILL.md) | Bundled override | linux, macos, windows | MIT | Use when a fetch fails: 403/429, paywall, WAF, bot wall. |
| [claude-code](skills/autonomous-ai-agents/claude-code/SKILL.md) | Bundled override | linux, macos, windows | MIT | Delegate coding to Claude Code CLI (features, PRs). |
| [claude-design](skills/creative/claude-design/SKILL.md) | Bundled override | linux, macos, windows | MIT | Design one-off HTML artifacts (landing, deck, prototype). |
| [codebase-inspection](skills/software-development/codebase-inspection/SKILL.md) | Bundled override | linux, macos, windows | MIT | Inspect codebases w/ pygount: LOC, languages, ratios. |
| [codex](skills/autonomous-ai-agents/codex/SKILL.md) | Bundled override | linux, macos, windows | MIT | Delegate coding to OpenAI Codex CLI (features, PRs). |
| [desktop-configurator-development](skills/software-development/desktop-configurator-development/SKILL.md) | Local/custom integration | linux | GPL-3.0-only | Use when developing desktop configurators or bar widgets. |
| [filesystem-integrity-recovery](skills/devops/filesystem-integrity-recovery/SKILL.md) | Local/custom integration | linux | GPL-3.0-only | Use when checking or repairing filesystem corruption. |
| [git-remote-ref-recovery](skills/software-development/git-remote-ref-recovery/SKILL.md) | Local/custom integration | linux, macos | GPL-3.0-only | Use when Git fetch/pull fails on a broken remote ref. |
| [hermes-agent](skills/autonomous-ai-agents/hermes-agent/SKILL.md) | Bundled override | linux, macos, windows | MIT | Use, configure, theme, extend, and orchestrate Hermes Agent. |
| [hermes-agent-skill-authoring](skills/software-development/hermes-agent-skill-authoring/SKILL.md) | Bundled override | linux, macos, windows | MIT | Author in-repo SKILL.md files: frontmatter and structure. |
| [hermes-session-recovery](skills/software-development/hermes-session-recovery/SKILL.md) | Local/custom integration | linux, macos, windows | MIT | Use when recovering deleted Hermes chats. Preserve history. |
| [leanrea](skills/research/leanrea/SKILL.md) | Local/custom integration | linux | MIT | Use when inspecting Fury artifacts with local CLI tools. |
| [legacy-game-static-assessment](skills/research/legacy-game-static-assessment/SKILL.md) | Local/custom integration | linux | MIT | Use when tracing recovered legacy game binaries. |
| [linux-kernel-boot-integration](skills/devops/linux-kernel-boot-integration/SKILL.md) | Local/custom integration | linux | MIT | Verify kernel package hooks, initramfs and boot entries. |
| [llama-cpp-upstream-refresh](skills/software-development/llama-cpp-upstream-refresh/SKILL.md) | Local/custom integration | linux | MIT | Use when updating llama.cpp to upstream master. |
| [local-model-selection](skills/research/local-model-selection/SKILL.md) | Local/custom integration | linux | MIT | Use when selecting or qualifying local AI models. |
| [omarchy-upstream-maintenance](skills/software-development/omarchy-upstream-maintenance/SKILL.md) | Local/custom integration | linux | MIT | Use when maintaining Omarchy changes across updates. |
| [omh-handoff-scan-notes](skills/handoff-guide/omh-handoff-scan-notes/SKILL.md) | Local/custom integration | linux, macos | MIT | Use when handoff scans fail. Diagnose and retry safely. |
| [pinned-offline-port-proof](skills/software-development/pinned-offline-port-proof/SKILL.md) | Local/custom integration | linux, macos | MIT | Use when finishing a pinned offline source port. |
| [requesting-code-review](skills/software-development/requesting-code-review/SKILL.md) | Bundled override | linux, macos, windows | MIT | Use when reviewing code or verification evidence. |
| [rust-workspace-dependency-refresh](skills/software-development/rust-workspace-dependency-refresh/SKILL.md) | Local/custom integration | linux, macos | GPL-3.0-only | Use when refreshing Rust workspace dependencies. |
| [security-audit](skills/security/security-audit/SKILL.md) | Local/custom integration | linux, macos, windows | MIT | Use when reviewing code for security vulnerabilities. |
| [source-faithful-game-ports](skills/software-development/source-faithful-game-ports/SKILL.md) | Local/custom integration | linux, macos | MIT | Use when porting games from source. Prove playable parity. |
| [supernal-wallpaper-intake](skills/projects/supernal-wallpaper-intake/SKILL.md) | Local/custom integration | linux | MIT | Use when adding Supernal wallpapers. Audit colour coverage. |
| [systematic-debugging](skills/software-development/systematic-debugging/SKILL.md) | Bundled override | linux, macos, windows | MIT | 4-phase root cause debugging: understand bugs before fixing. |
| [test-driven-development](skills/software-development/test-driven-development/SKILL.md) | Bundled override | linux, macos, windows | MIT | TDD: enforce RED-GREEN-REFACTOR, tests before code. |
| [uefi-xeon-turbo-research](skills/research/uefi-xeon-turbo-research/SKILL.md) | Local/custom integration | linux | MIT | Use when investigating Xeon BIOS turbo unlocks. |

Total: **27 skills**, **98 payload files**.

“Local/custom integration” includes original workflows and local wrappers around attributed upstream packages; it does not mean every line was authored here.

External related skills (install separately through their original distribution):

- `blocked-page-recovery`: `grounded-citations`
- `claude-code`: `opencode`
- `claude-design`: `architecture-diagram`, `design-md`, `excalidraw`, `popular-web-designs`
- `codebase-inspection`: `github`
- `hermes-agent`: `opencode`
- `local-model-selection`: `grounded-citations`, `omh-inference-serving`, `omh-model-optimization`
- `omarchy-upstream-maintenance`: `omarchy`
- `omh-handoff-scan-notes`: `ulw-maestro`, `ulw-work`
- `requesting-code-review`: `github`, `subagent-driven-development`
- `supernal-wallpaper-intake`: `omarchy`
- `systematic-debugging`: `subagent-driven-development`
- `test-driven-development`: `subagent-driven-development`
- `uefi-xeon-turbo-research`: `grounded-citations`
