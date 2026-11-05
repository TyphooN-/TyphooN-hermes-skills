# Privacy and OS-hardening configurator controls

Use this design and verification recipe for opt-in desktop controls. It does not certify a particular implementation or replace its independent security review.

## 1. Discover the actual recording and policy sources

Use `terminal` for bounded, read-only probes and `read_file`/`search_files` for installed definitions. Do not print recent-file URIs, clipboard contents, shell history or browser profiles as discovery evidence.

- Identify the file manager with `terminal(command="xdg-mime query default inode/directory")`; a GNOME setting is not automatically a control for another file manager.
- Discover supported GSettings schemas/keys before choosing targets. For a supported GNOME recent-files control, compare `gsettings get org.gnome.desktop.privacy remember-recent-files` with `dconf read /org/gnome/desktop/privacy/remember-recent-files` through `terminal`: effective value and explicit/unset state are different restoration inputs.
- Inspect the relevant GTK configuration as configuration, not history. Keep original bytes and originally absent files distinct so Restore does not invent a user override.
- For each discovered dedicated index/history unit, use `systemctl --user show "$unit" --property=Id,LoadState,ActiveState,UnitFileState,FragmentPath,DropInPaths --no-pager` through `terminal`, then read its actual definition. Confirm the exact recording/indexing role and any activation mechanism before proposing changes. Do not infer telemetry from an indexer's name.
- Read candidate kernel controls with `sysctl -n "$key"` through `terminal` and inspect competing persistence files. Unsupported keys and administrator-managed settings need an honest unavailable/conflict state, not a success preset.

Completion criterion: each control has a known source, exact scope, applicability condition, tradeoff and restoration input without exposing history content.

## 2. Define the state transition before implementation

| Operation | Preserve and verify | Pitfall to prevent |
|---|---|---|
| Stop recent recording | Original explicit/unset setting and relevant application configuration; effective readback | Stopping recording does not remove existing recent lists or every app's own history. |
| Stop dedicated indexing | Exact unit identity, original mask/activity and custom-override status | Disabling an enabled unit may not stop D-Bus activation; masking is a distinct, disclosed action, not package removal. |
| Purge recent lists/cache | Allowlisted owned regular files/directories, confirmation and partial-failure reporting | A backup recreates the exposure; disabling an indexer also leaves its existing database intact. |
| Enable a hardening key | Supported semantics, stronger existing policy, runtime value and managed persistence | A larger integer is not universally stronger; irreversible settings and competing configs must not be guessed into a reversible toggle. |
| Restore | The owned original and a match against the installed managed state | Blind restoration can erase intervening user/administrator changes. |

Keep history purges outside configuration journals/backups. Explain application restart or writer-closure requirements rather than silently killing processes. Preserve shared desktop infrastructure such as portals, GVFS and D-Bus; control only a proven dedicated recorder/indexer within the user's authorization.

Treat runtime and persistence as separate outcomes. A successful `sysctl -w` does not prove next-boot policy, and writing a persistence file does not prove the running value changed. Avoid broad policy replay to verify a single selected control.

Pin the rendered allowlisted persistence input at the privileged consumer boundary. A user-owned payload path can be swapped while `sudo` waits; an owned parent, an earlier hash and a post-install readback do not prevent unauthorized bytes from reaching the root-owned target. Exercise a benign source-swap fixture with the real native file-copy semantics and require refusal before unapproved persistence, without running root commands.

## 3. Prove safety and the actual menu path offline

1. Create a disposable HOME with explicit XDG config/data/state/cache/runtime roots and TMPDIR. Strip live display/session/D-Bus variables. Mock GSettings/dconf, systemctl, privilege helpers and desktop commands; make unexpected operations fail instead of falling through to the host.
2. Pin originals and test enable/re-enable/restore/re-restore, unset values, absent files, stronger unmanaged settings, missing schemas/keys/units, custom drop-ins and newer conflicting edits. Derive the entire service tuple from version-matched evidence: a masked systemd unit reports `LoadState=masked`, not `loaded`, but `Id`, `UnitFileState`, `ActiveState`, `FragmentPath` and `DropInPaths` must also remain faithful through mask and owned-unmask transitions. Do not equate a reported fragment pathname with its resolved symlink target. When a mask-path assumption is disputed, compare authorized read-only `systemctl show` properties from an already-masked unit with `systemd-analyze --user unit-files` under disposable HOME/XDG roots; label manager output and offline fragment-map evidence separately, because the map alone does not reproduce the controller's Apply/Restore behavior. Exercise the actual controller with the evidenced tuple before declaring the lead confirmed or the fix accepted.
3. Test exact deletion boundaries, symlinks/FIFOs, journal conflicts, partial command failures and confirmation cancellation. For the concurrency contract in SKILL.md, use deterministic interleaving hooks around the real methods and disposable files: inject a valid configuration edit immediately after the caller's ownership check, and separately between the expected-content read and the first metadata snapshot. Require refusal with newer bytes preserved and the recovery journal retained; exercise both replacement and deletion. These fixtures establish the demonstrated interleavings, not exhaustive race freedom.
4. Drive real category rendering, item selection, per-control confirmation, failure summaries and return navigation through a PTY using only inspected function/data spans. Never launch the live top-level configurator to obtain this proof.
5. Capture exact exits and logs, then run syntax and affected existing menu/configurator regressions. Preserve source/fixture hashes with receipts so another executor can reuse valid proof instead of rerunning a green checkpoint merely for a handoff.
6. Freeze the whole new task delta, including added untracked helpers/tests, against the recorded initial dirty baseline. Give an independent reviewer those artifacts and the authorized live boundary; self-review and mocked privilege commands are not live-safety approval.

Completion criterion: passing scoped tests, an honest tested/untested inventory and the required review; a UI checkbox or success summary is never the acceptance receipt.

## 4. Integrate custom-kernel inspection without a hidden build

- Validate the requested checkout literally. If absent, report that fact and expose an explicit alternate path; do not silently substitute a different checkout or modify it.
- Use demonstrably non-executing Git plumbing for untrusted checkout identity, for example `terminal(command='git --no-optional-locks -c core.fsmonitor=false -C "$checkout" rev-parse --show-toplevel')`. Do not infer that these flags make worktree status safe: `git status` may run checkout-configured clean/process filters through attributes even with fsmonitor and hooks disabled. Remove or independently neutralize that execution surface; prefer an honest unknown dirty state when it cannot be inspected safely. Test with a real benign filter sentinel, not just mocked Git. Preserve an active build's inputs and all user-modified configuration.
- Read the checkout's own README and configuration precedence. Parse only supported literal hints; external configuration and environment overrides can change the result, so mark unresolved effective settings unknown. Never source a PKGBUILD or shell customization file for inspection.
- Inspect local package metadata only, with bounded subprocess time/output and no script execution or directory extraction. Keep running release, installed package identity and source target version distinct.
- Label build commands as previews unless a separately authorized build actually runs. Do not sneak dependency installation or package installation into a preview via build-and-install flags.
- Keep installation, initramfs generation, signing, boot-entry/default changes and reboot outside an inspection menu's authority. Use the kernel-boot integration procedure when those operations are actually requested; package presence and fixture tests do not establish bootability.

Completion criterion: a useful, source-backed inspection/preview surface with no build/config/boot mutation and no claims beyond observed metadata.

## 5. Triage possible upstream security reports

1. Map the finding to its owning shipped component and exact revision before proposing disclosure. Separate new configurator defects, upstream integration defects, dependency defects, functional bugs and privacy preferences; an internal P1 label is not a CVSS rating or bounty qualification.
2. Retrieve the current canonical repository security policy with `web_extract`, follow its official disclosure/program links, and verify the actual program's policy, scope table and rewards. Use `web_search` on the official project site for a newer announcement when the repository policy is incomplete; a credits-only page or an old organization's policy does not establish that no bounty exists.
3. Record eligible assets, required verification branch, exclusions, duplicate handling, AI/manual-verification requirements, safe-harbor conditions and confidentiality terms before selecting a research target. Distinguish the total bounty fund from per-report rewards and label discretionary awards honestly; never carry cached amounts or scope into a later session as current facts.
4. Define what the attacker can do before and after the suspected flaw, then prepare a harmless reproduction in a separately owned disposable checkout or VM. Restrict testing to authorized assets and synthetic data; a source-code program does not authorize probing related production websites or third-party services. Treat semantic observations and speculative AI leads as research inputs, not verified submissions.
5. Reverify the required upstream revision and independently exercise the proof before drafting. If the program requires human verification, leave that requirement explicit rather than equating an autonomous second-model review with it. Prepare one private report per vulnerability unless a demonstrated chain requires otherwise; use the designated private channel, retain patch/publication confidentiality as required, and obtain the user's explicit approval before sending or publishing.

Completion criterion: an evidence-grounded attribution and eligibility decision, or a private report draft with unmet requirements named. Policy research and a prepared draft are not proof of an upstream vulnerability, a submitted report, or a bounty award.
