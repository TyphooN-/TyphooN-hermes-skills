# Troubleshooting

### `/resume` shows many idle, zero-message sessions

Investigate without deleting or closing history. On a canonical/shared gateway, distinguish TUI frontend processes, registered live routes, currently executing turns, and stored resumable conversations; the picker's `live` count is not a process or active-model count.

- Resolve the active profile, launcher/source chain and running gateway's `code_sha` before tracing source. Do not start another Hermes chat merely to inspect sessions.
- Inspect `state.db` with SQLite `mode=ro` and `PRAGMA query_only=ON`. Collect only IDs, source/created_source, start/end timestamps, message/API/token counters and role counts, never raw messages or frozen policies. Compare stored message counts with actual rows rather than assuming they are interchangeable after compression.
- Correlate blank-session creation timestamps with sanitized `[tui-parent]` attach/start events in `logs/tui_gateway_crash.log`; return timestamps and event categories, not arbitrary log bodies. Groups of blank rows near groups of TUI attaches can be unused startup conversations, not extra model workers.
- Trace `ui-tui/src/app/createGatewayEventHandler.ts::handleReady`, `useSessionLifecycle.ts`, `gateway/session_controls.py`, `hermes_state_local.py`, `gateway/session_local_recovery.py` and `gateway/session_live_listing.py`. In canonical implementations, create can reserve a durable row before the first prompt; ordinary disconnect detaches a viewer without an explicit end reason, and recovery restores receipt-backed routes. Confirm these semantics in the installed revision rather than treating every unended row as a running agent.
- Check explicit close versus ordinary detach and stale-attachment disposal separately. Keeping real conversations alive across disconnects is intentional; do not propose blanket session reaping as a repair for unused drafts.
- Report zero recorded model calls/tokens as an accounting observation, not proof of a billing refund or absolute absence of auxiliary work. A model name on a draft is routing configuration, not evidence of a loaded model instance.
- Treat repeated `Your request was not processed` notices and `[paused: lost in restart]` as failed-turn/admission symptoms, not proof the blank sessions caused them. Inspect admission status separately; do not discard unknown submissions or resend automatically.
- For explicitly approved list cleanup, prefer reversible `session.mutate` metadata (`operation=sidebar`, `payload={hidden:true}`) over deletion or raw SQL. Recheck the approved exact IDs for actual messages, usage, admissions, workers, children, pending-input references and current-view pointers; fence with the current runtime revision/generation, record original flags, and verify both exact hidden flags and the live-list readback. Do not assume current-view pointer files are plain IDs: `HERMES_TUI_ACTIVE_SESSION_FILE` contains JSON with `session_id` in current Ink revisions.
- Use `discover_gateway_endpoint` plus `connect_gateway(endpoint=...)` for maintenance that must never start/restart an owner; the connection helper's default path can start one. An existing `draining/restart_wait` owner permits picker reads but refuses `session.mutate`; preserve the approved cleanup as blocked, do not clear its drain marker, force a restart, or fall back to direct database writes. The switcher's Ctrl+D can only close a subscription held by that view, so it is not a general ownerless-draft cleanup mechanism.
- Freeze each approved pass's exact candidate IDs in a private inventory with its count and SHA-256, then revalidate every target immediately before mutation. Bind the script to that manifest instead of repeatedly patching a stale literal count. Preserve the original approval and failed attempts; a continuation retains its scope but does not justify inventing or backdating approval records. Perform fresh checks and the missing apply stage together when possible, so repeated interruptions do not become an endless preparation loop.
- Run maintenance helpers through the installed dependency owner, not a captured `installs/.../environments/.../venv/bin/python` that dependency GC can remove. In installations exposing it, use `hermes_cli._launchers.runtime_command(repo_root, args=['--apply'], code='import runpy; runpy.run_path(<repr of helper path>, run_name="__main__")', home=profile_home)` and execute the returned argv. This uses the maintained store interpreter and bootstrap-selected dependencies without launching a chat. The `runpy` module's command-line entry expects a module name, not a filesystem path; `--module runpy -- /path/helper.py` is not a file runner. Do not install missing Hermes dependencies into system Python as a workaround.
- Separate exact hidden-record readback from net picker counts. New draft IDs can appear during cleanup even while every previously hidden record remains hidden; a smaller net reduction does not imply that old visibility flags reverted. Permit a bounded, freshly guarded follow-up rather than an endless cleanup loop, and report any continuing draft creation as unresolved. A successful metadata cleanup is not a permanent fix to draft creation.
- Durable helper for repeatable cleanup: `~/hermes-resume-cleanup.py` (self-contained, re-runnable). `--status` (read-only, no gateway) for a quick count, no args = preflight (no changes), `--apply` hides eligible drafts. It auto re-execs under the installed managed runtime via `hermes_cli._launchers.runtime_command` when a bare interpreter lacks deps (ruamel.yaml), uses `session.list limit=200` (larger limits are rejected as invalid_params), re-verifies every candidate immediately before its `session.mutate`, writes `evidence/resume-cleanup-<UTC>/` (report/baseline/undo, 0700), and treats per-item hidden-flag readback as the authoritative gate while recording concurrent live-list drift as advisory. It never starts/restarts the gateway, never writes SQL, and preserves current TUI windows, populated history, pending inputs and usage. Verify gateway `code_sha` matches on-disk HEAD before a pass.

### Sessions seem lost and OMH skills collide after update

- Check the active profile's raw `display.interface` and its pre-update backups before repairing session storage. An OMH display-release migration can remove a previously selected `tui` default; Hermes then starts the classic CLI, whose `/resume` lists only CLI-source history. Read-only `CLISessionMixin._list_recent_sessions` against a backup distinguishes real CLI conversations from zero-message drafts; a small list is not database loss.
- Restore a proven previous TUI preference with `hermes config set display.interface tui`, not by relabeling session rows or widening gateway authorization. The running classic process remains classic until relaunched; do not kill an active turn. Verify `_config_default_interface_early()` and both live/stored `session.list` feeds using an already-discovered endpoint, never a connection that may start an owner. Count and deduplicate picker IDs in code; raw session-row counts include compression segments, internal workers and hidden drafts.
- Collapse stale OMH generation registrations to the stable `~/.local/share/omh/current/skills` entry with `hermes config set skills.external_dirs '<JSON list>'`, retaining every unrelated external directory. Back up config and the database first. Multiple generations can make every OMH skill ambiguous even while `omh doctor` exits 0; inspect `identity_conflicts` and verify all managed manifest labels through native `find_all_skills` and `locate_skill(name, None, skill_search_dirs()[0])`. Never erase old generations or overwrite customized skills to fix registration.
- Validate the shipped TUI receipt using Hermes PM's managed Node, not an unrelated PATH-selected Node version: `freshness.mjs` includes exact Node identity. If current, no application rebuild is needed. Picker tests separately require `npm run build:ink` before Vitest when `packages/hermes-ink/dist/entry-exports.js` is absent; the production TUI bundles Ink source and may be healthy despite that missing test prerequisite. Keep setup failures distinct from executed test results.

### Accidentally deleted conversations

#### Find and preserve the donor

1. **Resolve the actual store and distinguish missing from deleted.** Bind the active profile/home and installed runtime, then check source filters, hidden/archive flags and compression lineage before assuming data loss. Use the known repository/cwd alongside current and former titles; renaming can make a title-only search miss the target. Do not start another chat as a diagnostic.
2. **Batch read-only discovery.** Open candidate databases with `sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)` and set `PRAGMA query_only=ON`. Inspect `PRAGMA table_info(sessions)` once, then query the available ID/title/display-name/cwd fields together. If metadata is absent, check message session IDs for orphaned history before widening to bounded content searches. Emit metadata and counts, not whole conversation bodies.
3. **Search preserved stores before declaring the conversation unrecoverable.** Check the active home's `state-snapshots/` and discovered backups/exports. Compare each matching donor's session ID, cwd, schema version, raw message count, active/compacted counts and maximum message timestamp. Snapshot directory timestamps are not the conversation's coverage endpoint. Check local transcript/request-dump artifacts for newer evidence, but do not import request dumps as canonical history: they are partial model-request projections.
4. **Checkpoint a confirmed candidate immediately.** Save donor path, session ID, title/cwd, counts, coverage timestamp and next missing action in private persistent recovery evidence. Preserve a lossless target-only archive and take an online SQLite backup of the active store before any mutation; a plain copy of a live WAL database can omit committed rows. On continuation, reuse this checkpoint and inspect any existing recovery owner rather than repeating the broad search or launching a competing writer.

Useful content-free count query after the target ID is bound:

```sql
SELECT COUNT(*) AS stored_rows,
       SUM(active = 1) AS active_rows,
       SUM(compacted = 1) AS compacted_rows,
       MIN(timestamp) AS first_message_at,
       MAX(timestamp) AS last_message_at
FROM messages WHERE session_id = ?;
```

Compare these with `sessions.message_count` rather than treating a mismatch as corruption: that counter can describe active context while the table retains compacted and rewound history.

#### Select the recovery route

5. **Read the installed command and deletion contracts before writing.** Check `hermes sessions recover --help`, `hermes sessions import --help` and the installed session portability/deletion implementation. Database salvage, foreign-tool import and restoration of one deleted conversation are different operations; see `references/cli-reference.md`.
   - Check for a durable retired-ID marker. In implementations using `state_meta`, inspect the exact key `gateway.retired_session.v1.<session-id>` and confirm current semantics in `hermes_state_mutation_retirement.py`. A row inserted beside a retirement fence can appear in listings while every turn is refused. Preserve that fence and mint a fresh ID through the installed `new_session_id()` helper when required; keep the human-readable title only if it is unclaimed.
   - Inspect native import size/message limits and export projections before choosing a format. A large trusted snapshot can exceed JSON import limits, and a display-oriented export can omit `display_identity`/`display_order`. Never assume that a successful export is lossless or round-trippable. Do not raise global import limits or drop archived rows merely to make a payload fit.
   - Preserve raw message flags, ordering, stable UIDs, tool calls/results, reasoning and required system-prompt/model-usage records. Keep old admissions, leases, routing, delegations and activity labels out of the new live conversation: transcript recovery must not resurrect execution ownership. Preserve historical runtime records separately only when needed for archival fidelity.

#### Require proof before claiming restoration

6. **Qualify the exact recovery implementation on a disposable database first.** Prefer a supported restoration path where it satisfies fidelity and identity requirements. A custom selective-copy helper is a candidate, not a proven recipe: require schema checks, exact owned-row selection, collision refusal, one atomic transaction, preserved triggers/FKs, duplicate refusal and rollback proof. Never replace the active database or use broad `INSERT OR REPLACE` as a shortcut. Compare all donor/destination message fields with only intentional ID mappings excluded, not just counts. Verify active-context flags, archive visibility, prompt resolution, usage records, keyword search and unchanged unrelated session data.
7. **Apply only after its gates pass, then read back the exact target.** Keep rehearsal completion separate from live application. Verify the recovered ID/title/cwd, raw and active counts, native title lookup, display-history hydration and conversation loading without issuing a model prompt. Report the usable `hermes --resume <recovered-id>` command, private recovery artifact paths and source coverage limit. Call later or missing history unresolved; a located snapshot or launched worker is not a restored session.

### Voice not working
1. Check `stt.enabled: true` in config.yaml
2. Verify provider: `python -c "import pm; pm.sync_venv(['stt-whisper'], explicit=True)"` or set API key
3. In gateway: `/restart`. In CLI: exit and relaunch.

### Tool not available
1. `hermes tools` — check if toolset is enabled for your platform
2. Some tools need env vars (check `.env`)
3. `/reset` after enabling tools

### Model/provider issues
1. `hermes doctor` — check config and dependencies
2. `hermes auth` — re-authenticate OAuth providers (or `hermes auth add <provider>`)
3. Check `.env` has the right API key
4. **Copilot 403**: `gh auth login` tokens do NOT work for Copilot API. You must use the Copilot-specific OAuth device code flow via `hermes model` → GitHub Copilot.

### Codex 429 despite quota on another pooled account

1. **Bind the actual consumer.** Resolve the profile, launcher, installed HEAD and existing gateway's `code_sha` before changing accounts. On recurrence, compare the accepted repair's ancestry and reflog with the selected revision: a later checkout can omit a still-preserved local fix. Missing symbols alone do not prove missing behavior; run its behavioral regression on the current source.
2. **Separate balancing from availability.** Read `hermes config get credential_pool_strategies`. Round-robin advances on credential selection, not every tool call of a cached agent. Treat desktop quota bars as observations, not provider-readiness proof.
3. **Project persisted status without healing it.** Use `read_credential_pool` to emit only entry numbers, allowlisted statuses/error codes, reset timestamps and counters. Never emit tokens, labels, account IDs or whole stores, and never clear a genuine cooldown to manufacture availability. Before using an auth status/list command, inspect whether its current implementation loads or refreshes the pool; loading can seed or heal state.
4. **Inspect each affected route's provenance.** With read-only receipt access, project provider/endpoint classifications and booleans for explicit key or credential-reference presence; do not return frozen prompts or secret references. Legacy adoption can save the ordinary ChatGPT Codex URL as an explicit endpoint without pinning an account. `_resolve_explicit_runtime` / `_explicit_codex` can then return singleton credentials before the pool rung; a runtime without `credential_pool` cannot fail over on 429.
5. **Reproduce the real path offline.** Use synthetic credentials through `legacy_launch_params` → `build_policy` → `route_runtime`. Require a failing assertion for retained pool or account choice before the production change. Cover hard-cap rotation, transient-429 retry, cooldown exclusion, round-robin selection and bounded all-exhausted recovery; preserve explicit keys and foreign/proxy routes.
6. **Guard before side effects.** Reject known ineligible environment/configuration/persisted-row endpoints before loading/healing or selecting their pool. Recheck both the raw stored URL and effective endpoints on the actual loaded rows before `select()`, since metadata and loading can observe different generations. A canonical `HERMES_CODEX_BASE_URL` can mask a foreign stored URL; validating only the effective route misses that boundary. Assert unchanged store bytes and an independent selection-attempt counter on rejected routes; a throwing sentinel alone can be swallowed by production exception handling.
7. **Close each local stage honestly.** Keep focused proof, independent auth-boundary acceptance, installation, fresh native imports and running-process activation distinct. Reuse unchanged source-bound proof after interruption, but never substitute partial reviewer output for a terminal verdict. A green isolated candidate does not repair an old gateway's imported modules; do not edit an immutable PM workspace to activate it.
8. **Preserve the repair across source changes.** Retain a named local ref and verified private bundle before switching to a newer upstream. Check that the new selected source retains the behavior and regression, port/review only changed dependencies, and verify activation again. When checking a local repair ref, validate its full name and use `git for-each-ref` with an exact name/object comparison; do not infer absence from an assumed `show-ref --verify` exit code. A clean checkout or preserved backup does not establish that the running revision still contains the fix.

For OpenAI-style credential replacement, keep the installed SDK client, key, account header, entry identity, route and cached kwargs coherent when reconstruction fails. Stage copied kwargs under the existing client lock, commit identity only after successful replacement, and prove rollback with synthetic constructor failures plus the real recovery caller. Do not report a successful rotation merely because a new pool row was selected.

### OMH greeting absent or startup version looks stale

- Distinguish frontend ownership before repairing plugin registration. Bare `hermes` can launch the stock Ink frontend while OMH tools, hooks and context remain active. In OMH builds with a separate terminal, bare `omh` selects its packaged frontend through `HERMES_TUI_DIR`; confirm `commands/bare_launch.py`, `tui/launch.py` and the OMH banner renderer in the installed package. Use `omh -c` only after confirming the installed continuation flag. Do not change aliases, config or gateway lifecycle merely to change branding.
- Compare the exact `hermes --version` result, checkout HEAD and existing gateway `code_sha` before calling a version stale. Trace the frontend's payload producer as well as its renderer: `tui_gateway/server.py` can send `get_version_info().base_version` while the version command shows `derived_version` with commit provenance. Check whether the displayed date comes from a fixed `hermes_cli.__release_date__` string; it is not necessarily the checkout date or last update time. A matching current commit with an old base/date label is a display/provenance issue, not proof of updater failure.
- Keep Hermes's version separate from OMH's package version. Preview/main OMH archives can change content without bumping the declared release label; inspect active-generation metadata, the recorded source commit and workflow manifest comparison rather than treating an unchanged version-to-version line as a failed update.
- Verify a remedy without creating an unsolicited session: the pure `omh_tui_environment` selection helper and existence of the packaged frontend can establish launcher wiring. Label these as metadata checks, not an observed interactive launch. Keep diagnostic-probe warnings separate from actual plugin visibility in the current conversation.

### Changes not taking effect
- **Tools/skills:** `/reset` starts a new session with updated toolset
- **Config changes:** Startup-cached settings may require a gateway restart or CLI relaunch. Check the actual consumer before recommending it: current auxiliary routing resolves `_get_auxiliary_task_config()` per call through `load_config_readonly()`, whose cache tracks the config-file signature, so those route fields reload without restarting an already updated process.
- **Code changes:** Restart the CLI or gateway process. A new conversation or config reload does not replace Python modules already imported by an old process. Inspect fresh native-launcher import origins separately from the current tool kernel: its editable PM snapshot may differ from the canonical checkout the launcher prepends. When fresh imports already resolve to the changed canonical source and the dependency graph is unchanged, do not rebuild dependencies merely to copy a Python fix. PM repair replays recorded workspace inputs and can reproduce an older source snapshot rather than install the changed source. A gateway child must not restart its own backend; honor the lifecycle guard and use the supported command from a separate shell instead of bypassing it.
- **Local model idle after auxiliary activation:** Verify the alias is resident, task pins/fallback policy and title `enabled`/`model_upgrade_enabled` flags. Already titled sessions normally skip model titling; profile description and the generic text-helper CLI run only when invoked. Auxiliary activation does not automatically route ordinary replies, compression, coding or native delegate calls to the local model. Read-only server counters can confirm earlier use; zero current processing between these brief calls is expected. Do not prescribe restarts as a substitute for a missing supervisor-to-worker dispatch integration.

### Bounded local-worker automatic dispatch

- A text-helper CLI or auxiliary pin does not give the supervisor a callable worker. Use a native plugin to register the bounded worker tool and session-frozen dispatch guidance. Reuse the maintained local protocol and model manager; do not transparently reroute global `delegate_task` or change the supervisor's provider.
- Validate registration with `hermes plugins doctor --ci <plugin-path>`, retain independent source acceptance when required, and enable with `hermes plugins enable <name> --no-allow-tool-override`. Use `hermes plugins list --plain --no-bundled` for compact status. Read back the exact enabled entry, link target and protected routing sections.
- A deferred plugin is correctly exposed as `tool_search`, `tool_describe`, `tool_call`, not necessarily its direct tool name. Honor that native surface in real-supervisor proof, constrain the bridge to the admitted worker, and keep `tool_choice: auto`; disabling deferral or forcing a tool does not prove automatic selection. Verify the registered dispatch policy appears in the actual new session's frozen prompt.
- Read the activation result before prescribing restarts. Supported gateways can reload plugins live but defer new tool/prompt surfaces to new sessions; already-frozen conversations are not retrofitted. Relaunch a standalone CLI that has not reloaded the code; do not kill an active backend merely to demonstrate installation.
- A router `/models/load` success may acknowledge scheduling rather than readiness. Bound metadata-only readiness waiting, keep other resident workloads intact and issue no repeated load attempts. Save stage checkpoints before expensive work so a reboot does not erase whether automatic dispatch, loading or inference was actually reached.
- Preserve interrupted attempts and unknown exits separately. Recheck source hashes against their actual live paths: a review snapshot can contain a transport from the Hermes checkout alongside plugin files owned by another repository; do not assume every manifest name lives beneath the plugin root.
- Keep source acceptance, offline mock contracts, real automatic selection, actual tool-free local inference and host/provenance qualification as separate claims. A loaded alias or zero current processing is not either a capability pass or evidence of broken dispatch.

### web_extract reports a search-only backend (Codex/OpenAI Native)

- Reproduce through the actual `web_extract` tool before changing source. OpenAI Native provides search, not URL extraction; a never-configured profile can autodetect it for both capabilities. Inspect only the relevant web settings and resolved search/extract routes.
- Prefer the supported per-capability configuration when it solves the user's failure. Preserve the existing search route, set `hermes config set web.provider_tier.exa free` before `hermes config set web.extract_backend exa`, and read back both values. The explicit free tier avoids silently using an existing paid API key. This is a settings repair, not evidence that an autodetection source defect was patched.
- Verify with the real tool against the original failing URL, and confirm the resolved search backend did not change. Recover a truncated URL from observed links rather than guessing its suffix. Record source/config repair separately from live extraction success; do not create a repository commit for a config-only remedy.
- Test live config reload before prescribing a restart: the web config loader can observe supported config changes within the already-running process. Do not restart a shared gateway or interrupt unrelated sessions merely to activate these settings.

### web_extract shows a stale page (result caching)
`web_search`/`web_extract` cache results for 20 minutes (PR #94618) — a
repeat fetch of the same URL within the TTL is served from cache, which
can look like "my website changes aren't showing up."

Automatic carveouts (always fetched live, never cached):
- localhost / 127.0.0.1 / `*.local` / `*.localhost` / single-label LAN
  hostnames / private + link-local IP ranges (dev servers, hot-reload
  builds, chat-GUI artifact previews)
- URLs matched by `security.website_blocklist`
- failed responses and keyless-rescue-served responses

Developing a site tested over the PUBLIC internet (Vercel/Netlify
preview, ngrok/cloudflared tunnel, staging domain)? Public DNS isn't
auto-carved-out — list the host in config.yaml:

```yaml
web:
  cache_exempt_hosts:      # always fetched live; effective immediately
    - mysite.vercel.app
    - "*.ngrok-free.app"
    - mysite.dev           # suffix match: also covers preview.mysite.dev
```

Blunt instruments: `web.cache_ttl_minutes: 1` (min) or
`web.cache_enabled: false` disables both caches entirely.

### Skills not showing
1. `hermes skills list` — verify installed
2. `hermes skills config` — check platform enablement
3. Load explicitly: `hermes -s name` (or the skill's own `/<name>` slash command)

### Gateway issues
Check logs first:
```bash
grep -i "failed to send\|error" ~/.hermes/logs/gateway.log | tail -20
```

Common gateway problems:
- **Gateway dies on SSH logout**: Enable linger: `sudo loginctl enable-linger $USER`
- **Gateway dies on WSL2 close**: WSL2 requires `systemd=true` in `/etc/wsl.conf` for systemd services to work. Without it, gateway falls back to `nohup` (dies when session closes).
- **Gateway crash loop**: Reset the failed state: `systemctl --user reset-failed hermes-gateway`

### Platform-specific issues
- **Discord bot silent**: Must enable **Message Content Intent** in Bot → Privileged Gateway Intents.
- **Slack bot only works in DMs**: Must subscribe to `message.channels` event. Without it, the bot ignores public channels.
- **Windows-specific issues** (`Alt+Enter` newline, WinError 10106, UTF-8 BOM config, line endings): see `references/windows-quirks.md`.

### Vision rejects image input on a local endpoint

- Test the actual `vision_analyze` tool in the current session before changing configuration. Use a tiny synthetic image with unannounced text and distinct shapes, then the original failing image. A previous local-endpoint error can coexist with a currently working native route after a model/runtime change; distinguish observed recovery from a repair you performed.
- Inspect `tools/vision_tools.py::_handle_vision_analyze` and `agent/image_routing.py` in the installed revision. Vision-capable main sessions can receive native pixels without any auxiliary model call. An explicit `auxiliary.vision` override can instead force the lossy auxiliary-text route, so do not pin a cloud vision model merely to replace a working native path.
- A llama.cpp `image input is not supported` / missing-mmproj error identifies an image-incompatible serving route, not corrupt wallpaper or missing Python packages. Keep local service/model/projector changes separately approved; never restart the router or enable paid fallback to make the probe pass. A `None does not support vision` diagnostic can reflect an unset requested model, not a server-reported model named None.
- Read back config hashes and record whether anything changed. If current native vision works, report that success and the remaining text-only-local-model limitation honestly rather than claiming a system-wide configuration repair. Adding a dedicated vision backend requires a preview/approval and verification of its real included-versus-paid route.

### Auxiliary models not working
If `auxiliary` tasks (vision, compression, session_search) fail silently, the `auto` provider can't find a backend. Either set `OPENROUTER_API_KEY` or `GOOGLE_API_KEY`, or explicitly configure each auxiliary task's provider:
```bash
hermes config set auxiliary.vision.provider <your_provider>
hermes config set auxiliary.vision.model <model_name>
```

### "Reset permissions" / auto-approving everything
See `references/security-privacy.md` — wipe the "Always allow" stores, don't touch yolo mode.

### Git source-install or update recovery

1. **Capture ownership and preserve work.** Resolve the actual profile, executable/wrapper chain and source repository. Record `git rev-parse HEAD`, `git status --porcelain=v1 -uall`, worktrees and local repair refs. Preserve tracked and untracked edits, local-only commits, installed launchers and update receipts in private persistent evidence before any source replacement; volatile scratch is not a power-loss checkpoint.
2. **Diagnose before cleanup.** Inspect current updater instructions and ownership records, then use bounded read-only Git checks such as `git reflog`, `git config --local --get-regexp 'partialclone|promisor'` and `git fsck --full` through `terminal`. A stash failure or recovery launcher is a symptom, not proof of one particular damaged object.
3. **Honor supported recovery and custody.** Prefer the installed updater's documented recovery path. Do not delete stash refs, update locks, pull markers or recovery directories merely to make startup proceed: they can preserve user work or identify a still-active transaction. Do not reset/restore a dirty checkout or broadly remove empty objects. Any destructive repair requires an exact affected set, preserved preimages and the applicable approval.
4. **Qualify a replacement before swapping.** If a replacement is necessary and authorized, keep the original tree intact, verify the replacement's objects and intended base, then port only the owned local changes. Preserve the installed `.hermes/` launchers or regenerate them through the supported installer; they need not be tracked by Git. Reuse an existing qualified runtime when dependencies are unchanged rather than rebuilding solely to copy a Python source fix.
5. **Verify behavior and activate the right owner.** Run the preserved regression against the selected source, obtain required acceptance, verify fresh native import origins, then use supported gateway lifecycle commands from an allowed context. Read back the running owner's identity and code revision after activation. A source swap, an exit-0 update or an active service alone does not prove that local fixes survived or that the running process imported them.
