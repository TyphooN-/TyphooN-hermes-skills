# Hermes CLI Reference

Live sources when anything looks stale: `hermes --help`, `hermes <command> --help`,
https://hermes-agent.nousresearch.com/docs/reference/cli-commands

### Global Flags

```
hermes [flags] [command]        (no subcommand = interactive chat)

  --version, -V             Show version
  -z, --oneshot PROMPT      One-shot: print ONLY the final response (for scripts/pipes)
  -m MODEL  --provider P    Model/provider override for this invocation
  -t, --toolsets LIST       Comma-separated toolsets for this invocation
  --resume, -r SESSION      Resume session by ID or title
  --continue, -c [NAME]     Resume by name, or most recent session
  --worktree, -w            Isolated git worktree mode (parallel agents)
  --skills, -s SKILL        Preload skills (comma-separate or repeat)
  --profile, -p NAME        Use a named profile
  --yolo                    Skip dangerous command approval
  --tui / --cli             Force the Ink TUI / classic REPL
  --ignore-rules            Skip AGENTS.md/SOUL.md/memory/skill injection
  --safe-mode               Disable ALL customizations (troubleshooting)
  --pass-session-id         Include session ID in system prompt
```

### Chat

```
hermes chat [flags]
  -q, --query TEXT          Single query, non-interactive
  --image PATH              Attach a local image to a single query
  -Q, --quiet               Suppress banner, spinner, tool previews
  --checkpoints             Enable filesystem checkpoints (/rollback)
  --max-turns N             Cap tool-calling iterations
  --source TAG              Session source tag (default: cli)
```
(plus the global flags above)

### Configuration

```
hermes setup [section]      Wizard (model|tts|terminal|gateway|tools|agent)
hermes model                Interactive model/provider picker
hermes fallback [add|remove|list]  Fallback provider chain
hermes config [show|edit|get|set|unset|path|env-path|check|migrate]
hermes login / logout       OAuth sign-in / clear stored auth
hermes doctor [--fix]       Check dependencies and config
hermes status [--all]       Component status
```

### Tools & Skills

```
hermes tools [list|enable NAME|disable NAME]   Per-platform toolsets (curses UI with no args)

hermes skills list|browse|search QUERY|inspect ID
hermes skills install ID    Hub identifier OR a direct https://…/SKILL.md URL
hermes skills config        Enable/disable skills per platform
hermes skills check|update|uninstall|publish PATH
hermes skills tap add REPO  Add a GitHub repo as a skill source
hermes bundles              Skill bundles (one /<name> alias loads several skills)
```

### Importing a local skill package

- Honor a requested local checkout; do not silently replace it with a network Hub install. Check live CLI support before treating a filesystem path as an install identifier.
- For a flat third-party package with relative companion documents and helper scripts, create a personal Hermes entry point with `skill_manage` and preserve the complete original package under `references/upstream/`. Direct `skill_view` to that upstream `SKILL.md` and define its containing directory as the workflow's skill directory. This retains relative links without rewriting upstream instructions.
- Preserve the README and license. Record the source revision, dirty state, file inventory and hashes; reject symlinks and verify exact source/copy hashes, file counts and relative links. On interrupted imports, preserve differing existing files rather than overwriting them.
- Installing instructions does not authorize audits, agent fan-out, dependency installation or execution of bundled code. Verify native catalog discovery and an exact supporting-file read; the session's initial skill list and cached linked-file metadata are not installation proof.

### MCP Servers

```
hermes mcp add NAME (--url or --command) | remove | list | test NAME
hermes mcp catalog | install NAME     Curated catalog install
hermes mcp configure NAME             Toggle tool selection
hermes mcp serve                      Run Hermes as an MCP server
```
Details (transport, tool discovery, catalog): `references/native-mcp.md`.

### Gateway (Messaging Platforms)

```
hermes gateway run|install|start|stop|restart|status|setup
```

20+ platforms: Telegram, Discord, Slack, WhatsApp (Baileys + Business Cloud API), iMessage (Photon — `hermes photon setup`), Signal, Email, SMS, Matrix, Mattermost, Teams, LINE, SimpleX, ntfy, Google Chat, Home Assistant, DingTalk, Feishu, WeCom, Weixin, API Server, Webhooks. Open WebUI connects via the API Server adapter. Most adapters ship under `plugins/platforms/`.
Docs: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/

### Sessions

```
hermes sessions list|browse|rename ID TITLE|delete ID|export OUT|prune|stats
hermes sessions recover --source SOURCE --inspect-only
hermes sessions recover --source SOURCE --output NEW_DB --report REPORT
hermes sessions import --from {claude,codex} [PATH]
```

Check installed subcommand help before recovery. `sessions recover` is offline database salvage: it copies the source and sidecars, rebuilds canonical data into a separate output and does not automatically replace the active database. It is not a selective undelete command. The CLI `sessions import` shown here imports foreign Claude Code/Codex conversations; the Python `SessionDB.import_sessions` API has a different contract for native exports, including validation limits, archived-row handling, runtime-state reset and retired-ID refusal. Inspect the installed implementation before relying on a round trip. For one accidentally deleted conversation, follow `references/troubleshooting.md` rather than restoring an entire old database over newer history.

### Cron / Webhooks

```
hermes cron list|create SCHED|edit ID|pause|resume|run ID|remove|status
    Schedules: '30m', 'every 2h', '0 9 * * *', ISO timestamp
hermes webhook subscribe NAME|list|remove NAME|test NAME
```
Webhook payloads/routes: `references/webhooks.md`.

### Profiles

```
hermes profile list|create NAME (--clone|--clone-all|--clone-from)|use|show|delete
hermes profile rename A B | alias NAME | export NAME | import FILE
hermes profile migrate-identity A B   Retry a completed rename's session/routing identity migration
```

### Credentials & Pools

```
hermes auth                 Interactive credential manager
hermes auth add [PROVIDER]  Add OAuth or API-key credential (nous, openai-codex, qwen-oauth, …)
hermes auth list|remove P IDX|reset PROVIDER|status
```
Multiple credentials per provider form a pool that rotates automatically and skips exhausted keys.

### Other

```
hermes desktop / gui        Native desktop app
hermes dashboard            Web admin panel + embedded chat (--stop / --status)
hermes proxy                OpenAI-compatible local proxy backed by an OAuth provider
hermes portal               Quick setup / sign in via Nous Portal
hermes kanban <verb>        Multi-agent work-queue board
hermes project              Named multi-folder workspaces
hermes skin list|use|set    Switch/tweak skins (see references/themes.md)
hermes pets <verb>          Pet mascots (see references/petdex.md)
hermes memory setup|status|off|reset   Memory provider
hermes secrets bitwarden|onepassword   External secret stores
hermes moa                  Mixture-of-Agents slots
hermes hooks / security / backup / import / checkpoints / console
hermes logs [-f] [errors]   View agent/error logs
hermes send                 One-off message through a gateway platform
hermes pairing / plugins / insights / journey / computer-use
hermes acp                  ACP server (IDE integration)
hermes completion bash|zsh|fish
hermes update / uninstall / claw migrate
```

Plugin- and provider-supplied subcommands (e.g. `hermes photon setup`) only appear once their plugin is installed/active.

### Update/migration pitfalls

- `hermes update --check` is not guaranteed to be read-only on a source install: startup can first finish an interrupted source update, sync dependencies, build the TUI/web UI, and run post-update maintenance. Track it as a potentially long mutating operation; do not run concurrent installers/builds against that checkout or treat a short runner timeout as completion.
- When migrating an Omarchy/mise pipx installation, inspect both PATH and `~/.local/bin/hermes`: the Omarchy wrapper may reinstall and execute the retired pipx distribution. Back up the wrapper/config, verify the supported runtime before switching, and use `mise unuse --global --no-prune pipx:hermes-agent` to remove selection while retaining old binaries. Verify fresh-shell resolution as well as an absolute launcher.
- A running old Hermes session can export `PYTHONPATH` pointing at its pipx site-packages. OMH's in-process plugin smoke may then report Hermes 0.19.0 even when the command selects the new Git install. Verify with `env -u PYTHONPATH -u PYTHONHOME omh doctor` and a similarly clean new shell; do not weaken the plugin version gate or reinstall it solely to cure this inherited-environment false failure. The old running session remains old until relaunched.

### Retain a local repair across source updates

1. **Establish what changed before blaming the updater.** Compare the last accepted repair, current checkout and running backend revisions. Correlate Git reflog with native update receipts and their pre/post source identities; reflog establishes a ref movement, not its actor. Validate the receipt's argv type before deciding whether a branch choice was explicit, because iterating a string as if it were an argument list can falsely report no branch flag.
2. **Distinguish retained history from retained behavior.** A switch away from an unmerged repair branch can preserve every commit while removing the repair from the executing source. Do not call the fix durable merely because its commit or branch still exists. Preserve the old accepted patch and its source-bound proof while testing the smallest port on the selected current base.
3. **Inspect the maintained update policy before adding safeguards.** When the selected updater exposes `updates.parked_branch_strategy`, inspect it with `terminal(command="hermes config get updates.parked_branch_strategy")` and trace the current implementation plus its parked-branch tests. If supported and appropriate, preview `hermes config set updates.parked_branch_strategy update_in_place` as the smallest operator option instead of inventing hooks, wrappers, updater modules or a global update disable. Obtain any required configuration approval separately from source-repair authority, then apply through native config commands and read back that exact key.
4. **State the option's limits.** Verify explicit branch-switch precedence and merge-conflict handling in the selected revision. Updating an existing repair branch can preserve local commits but cannot guarantee compatibility with future upstream changes; retained regression tests still need to pass. Do not present an inspected recommendation as applied configuration or an unactivated source change as recovered service.

### Source WebUI verification

1. **Bind the requested proof to the effective install.** Resolve the active profile, launcher, source HEAD and existing dirty state. Distinguish a build-only repair from runtime acceptance before adding supplementary checks.
2. **Read the precise failure, then test current source.** Inspect the resolved Hermes home's `logs/update.log` and update receipts for the actual compiler diagnostic. Check whether the current source already includes the correction; a historical failed update is not proof that the present checkout needs another patch.
3. **Run the supported build before hash archaeology.** Exercise `scripts/build/web.mjs` through the installed PM environment and its Node, retaining the exact invocation, exit and log. If using a verification output, keep it outside the hashed source inputs. Do not put temporary probes inside `scripts/build`, because the probe itself changes the build fingerprint.
4. **Check the product with the maintained validator.** Use `scripts/build/freshness.mjs` against the product and matching inputs. Once the real build succeeds and the maintained validator agrees, stop speculative reimplementations of the hash chain. If comparing bytes is still necessary, use the same hash construction on both sides: `git hash-object` for Git blob IDs, or the same digest of both raw byte sequences. Git object headers and object-format algorithms make blob IDs different from raw-file SHA256.
5. **Keep supplementary checks independent.** Record frontend tests, Python build-contract tests and dashboard runtime proof as separate commands/exits/counts. Preserve real-home guards; setup errors and guard-aborted checks are incomplete proof, not passing compatibility evidence. Diagnose the exact denied path before moving a checkout: a detached worktree can still reference a common `.git` under the protected home. Do not present an unverified relocation as a working isolation fix.
6. **Close the accepted scope and hand back control.** For build-only acceptance, retain optional failures in the handoff rather than continuing an unrelated dashboard QA campaign. State any source changes—or that the current upstream fix needed none—and reconcile the checklist before returning to the original task. A prepared launcher is not a running-server result.

### Where to Find Things

| Looking for... | Location |
|---|---|
| Config options | `hermes config edit` · [Configuration docs](https://hermes-agent.nousresearch.com/docs/user-guide/configuration) |
| Tools / toolsets | `hermes tools list` · [Tools reference](https://hermes-agent.nousresearch.com/docs/reference/tools-reference) |
| Skills catalog | `hermes skills browse` · [Skills catalog](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog) |
| Provider setup | `hermes model` · [Providers guide](https://hermes-agent.nousresearch.com/docs/integrations/providers) |
| Env variables | `hermes config env-path` · [Env vars reference](https://hermes-agent.nousresearch.com/docs/reference/environment-variables) |
| Gateway logs | `~/.hermes/logs/gateway.log` (or `hermes logs`) |
| Sessions | `hermes sessions browse` (reads state.db) |
