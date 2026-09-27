# FW_Logic_Loot

- **Purpose:** Drop tables and weighted rewards that feed Inventory.
- **Difficulty:** Medium
- **Namespace / asmdef:** `FW.Logic.Loot`
- **Depends on:** FW.Core.ObjectManager, FW.Logic.Inventory
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
| `Runtime/` | The module's C# code, shipped in builds. `FW.Logic.Loot.asmdef` lists what it may reference |
| `Tests/` | EditMode tests (`FW.Logic.Loot.Tests.asmdef`, Editor-only, never shipped) |
| `Editor/` _(add if needed)_ | Inspector/editor tools, with its own Editor-only asmdef |
| `Prefabs/`, `Art/`, `Audio/` _(add if needed)_ | Assets this module ships with |
