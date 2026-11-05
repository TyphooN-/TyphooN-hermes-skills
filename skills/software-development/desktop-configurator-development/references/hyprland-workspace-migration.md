# Hyprland workspace migration: reference case

These observations came from a Lua-based Omarchy installation and Hyprland 0.56.2. Re-read installed defaults and API behavior on future versions; this is a comparison recipe, not a permanent compatibility promise.

## Sources to compare

- HyDE checkout: `Configs/.local/share/hypr/lua/key_binds.lua`.
- Installed Omarchy: `default/hypr/bindings/tiling.lua` under the discovered installation root.
- User config: entrypoint and binding modules under the actual Hyprland config directory.
- Read-only live registry: `hyprctl binds -j`.
- Only if needed: version-matched Hyprland selector parsing and bind/unbind implementation.

## Observed behavior

| Action | Dispatcher/selector | Distinction |
|---|---|---|
| HyDE Ctrl+Super+Left/Right | `hl.dsp.focus({ workspace = "r-1" })` / `"r+1"` | Relative workspace numbers on focused monitor; can create an unused workspace and skips numbers assigned/open on other monitors. |
| Omarchy Super+Tab / Super+Shift+Tab | `e+1` / `e-1` | Existing workspaces in numeric order, wraps and can cross monitors. Existing empty/persistent workspaces count; nonexistent numbers do not. |
| Omarchy Ctrl+Super+Left/Right | Group previous/next | Conflicts with the requested workspace shortcut. |
| Omarchy Super+Alt+Tab / Super+Alt+Shift+Tab | Group next/previous | Alternate group navigation remained available in the inspected defaults. |

At the lowest eligible workspace, relative-left behavior can also depend on the workspace back-and-forth setting. Avoid asserting a universal boundary behavior without checking it.

Observed `hl.unbind` matching used the key string, ignoring spaces/case, rather than fully canonicalizing modifier ordering and aliases. Use the original stock spelling for removal and inspect for semantically equivalent duplicate binds. Verify this implementation detail against the installed version before relying on it.

## Managed-block/editor interaction

An editor can regenerate its block at EOF containing `hl.unbind` for the old grouped-window shortcut. If the workspace override is above that block, the editor may remove the workspace binding too. Test both orders, and deliberately keep a conflict-free workspace block after editor edits. If the editor assigns another action onto the reserved combo, surface the conflict rather than silently deleting that action.

## Fixture lessons

- Snapshot original config bytes and compare after enable/disable round trips.
- Reset assertion logs at the start of each isolated assertion scenario. A setup action can add a success entry before the failure entry under test; assuming index zero then creates a false test failure.
- Lua versions can reject assignment to generic-for control variables. Normalize `token` into `local part` instead.
- A mock hyprctl should record reload/configerrors calls and support failures as well as nonempty diagnostic output.
- With an isolated HOME and runtime directory, `Hyprland --verify-config -c <fixture>` accepted generated Lua and rejected an intentionally invalid bind. Verify availability and side-effect behavior before reusing this check.
- Shell harnesses must propagate failure: use fail-fast sequencing or explicitly save and return the test exit. A later successful Git status command can otherwise hide an earlier failed suite.

## Useful read-only acceptance query

For the observed modifier representation, Super+Ctrl is modmask 68:

```bash
hyprctl binds -j | jq -r '.[] | select(.modmask == 68 and ((.key | ascii_upcase) == "LEFT" or (.key | ascii_upcase) == "RIGHT")) | [.key, .description, .dispatcher, .arg] | @tsv'
```

Inspect for exactly the intended action per direction. Registry inspection and offline validation do not substitute for an authorized interactive navigation test; report that distinction.
