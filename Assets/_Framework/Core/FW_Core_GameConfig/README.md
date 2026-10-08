# FW_Core_GameConfig

- **Purpose:** Global variables as ScriptableObjects (tuning, feature flags).
- **Difficulty:** Easy
- **Namespace / asmdef:** `FW.Core.GameConfig`
- **Depends on:** none
- **Owner:** @veyroxie
- **Status:** In progress

## Expectations (v0)
- [x] `ConfigAsset` base: each game builds its own settings assets on it, and bad values show as warnings in the Editor
- [x] `FeatureFlag`: on/off switch asset, one per feature
- [x] Config is read-only at runtime. No singleton, no statics

## How to use
**Your own settings** (game-specific ones live in `_Game`, never here):
```csharp
[CreateAssetMenu(menuName = "Game/Config/Player")]
public sealed class PlayerSettings : ConfigAsset
{
    [SerializeField, Min(0f)] private float _moveSpeed = 5f;
    public float MoveSpeed => _moveSpeed;

    public override IEnumerable<string> GetValidationErrors()
    {
        if (_moveSpeed <= 0f) yield return "Move Speed must be above 0.";
    }
}
```
Create the asset from the Project window (right-click > Create), then drag it into the script that needs it:
```csharp
[SerializeField] private PlayerSettings _settings;
```

**Feature flags:** Create > FW > GameConfig > Feature Flag, tick Is Enabled and write a description. In code:
```csharp
[SerializeField] private FeatureFlag _debugMenu;
if (_debugMenu.IsEnabled) ShowDebugMenu();
```

Never change config values from code at runtime. ScriptableObject changes made during Play mode are saved to the asset.

## Public API
| Type | What it is |
| --- | --- |
| `ConfigAsset` | Abstract ScriptableObject base for settings assets. Override `GetValidationErrors()` to report bad values |
| `FeatureFlag` | On/off switch asset. `IsEnabled`, `Description` |

## TODO (not built yet)
- [ ] Registry to look up config by type, if Inspector references get unwieldy
- [ ] Different flag values per build (debug vs release)
- [ ] Remote config (change values without a new build)
- [ ] Import settings from a spreadsheet / CSV

## Files in this module
| Path | What it's for |
| --- | --- |
| `README.md` | This file: purpose, owner, API, status. Keep it current |
| `Runtime/` | The module's C# code, shipped in builds. `FW.Core.GameConfig.asmdef` lists what it may reference |
| `Tests/` | EditMode tests (`FW.Core.GameConfig.Tests.asmdef`, Editor-only, never shipped) |
| `Editor/` _(add if needed)_ | Inspector/editor tools, with its own Editor-only asmdef |
| `Prefabs/`, `Art/`, `Audio/` _(add if needed)_ | Assets this module ships with |
