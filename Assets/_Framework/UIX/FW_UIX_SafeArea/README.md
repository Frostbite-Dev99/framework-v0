# FW_UIX_SafeArea

- **Purpose:** Aspect ratio, notches, static/anchored elements.
- **Difficulty:** Easy
- **Namespace / asmdef:** `FW.UIX.SafeArea`
- **Depends on:** none
- **Owner:** _TBD_
- **Status:** Not started

## Expectations (v0)
- [ ] _Define the minimum this module must do for the reference game_

## Public API
_List the classes/events other modules may use. Everything else is `internal`._

## Long-term plan
_What v1+ adds._

## Files in this module
| Path | What it's for |
| --- | --- |
| `README.md` | This file: purpose, owner, API, status. Keep it current |
| `Runtime/` | The module's C# code, shipped in builds. `FW.UIX.SafeArea.asmdef` lists what it may reference |
| `Tests/` | EditMode tests (`FW.UIX.SafeArea.Tests.asmdef`, Editor-only, never shipped) |
| `Editor/` _(add if needed)_ | Inspector/editor tools, with its own Editor-only asmdef |
| `Prefabs/`, `Art/`, `Audio/` _(add if needed)_ | Assets this module ships with |
