# C# in Unity — Team Best Practices

Short rules. Code examples. If a rule makes code harder to read, readability wins, so ask in review.
`.editorconfig` in the repo root enforces the formatting and naming rules in Rider / Visual Studio / VS Code.

---

## 1. The 10 rules

1. **Every field is `private`.** Use `[SerializeField]` to expose it in the Inspector and a property to expose it to code.
2. **Cache references** in `Awake`. Never call `GetComponent` / `Find` in `Update`.
3. **No magic strings or numbers.** Use `const`, `enum`, or ScriptableObject config.
4. **No nested `if`.** Use guard clauses and return early.
5. **Subscribe in `OnEnable`, unsubscribe in `OnDisable`.** Every time.
6. **Don't allocate in hot paths** (`Update`, physics, loops). That means no `new List`, LINQ, string concat or boxing per frame.
7. **Pool, don't `Instantiate`/`Destroy`** anything spawned often (use `FW_Core_ObjectManager`).
8. **Never swallow errors.** Every `catch` logs or rethrows.
9. **One class per file**, and the file name matches the class name.
10. **Respect the layers.** `_Framework` never references `_Game`, and modules talk through `FW_Core_Events`.

---

## 2. Naming

| Thing | Style | Example |
| --- | --- | --- |
| Class, struct, enum, method, property, event | `PascalCase` | `PlayerHealth`, `TakeDamage()`, `IsAlive` |
| Interface | `I` + PascalCase | `IDamageable` |
| Private / protected field | `_camelCase` | `_moveSpeed` |
| Constant | `PascalCase` | `MaxLives` |
| Local variable, parameter | `camelCase` | `damageAmount` |
| Boolean | `Is` / `Has` / `Can` / `Should` | `IsGrounded`, `_hasKey` |
| Event | verb, past/present | `Died`, `HealthChanged` |
| Event handler | `Handle` + event | `HandleDied()` |
| Async method | ends in `Async` | `LoadSceneAsync()` |
| Namespace | matches folder | `FW.Logic.Health`, `Game.Player` |

- Abbreviations: `Id`, `Ui`, `Hp` are fine. `ID` and `UI` in identifiers are not. Avoid cryptic ones like `plyrHlth`.
- `_camelCase` shows fields apart from locals at a glance, and Unity's Inspector hides the `_` (it shows *Move Speed*).

---

## 3. Class layout

Order inside a class, top to bottom:

1. Constants
2. Static fields
3. Serialized fields (`[SerializeField] private`)
4. Private fields
5. Properties
6. Events
7. Unity messages in call order: `Awake`, `OnEnable`, `Start`, `Update`, `FixedUpdate`, `LateUpdate`, `OnDisable`, `OnDestroy`
8. Public methods
9. Protected methods
10. Private methods, event handlers, coroutines

```csharp
using System;
using UnityEngine;

namespace FW.Logic.Health
{
    public sealed class Health : MonoBehaviour, IDamageable
    {
        private const int MinHealth = 0;

        [SerializeField] private int _maxHealth = 100;

        private int _current;

        public int Current => _current;
        public bool IsAlive => _current > MinHealth;

        public event Action<int> HealthChanged;
        public event Action Died;

        private void Awake()
        {
            _current = _maxHealth;
        }

        public void TakeDamage(int amount)
        {
            if (!IsAlive) return;
            if (amount <= 0) return;

            _current = Mathf.Max(MinHealth, _current - amount);
            HealthChanged?.Invoke(_current);

            if (!IsAlive) Died?.Invoke();
        }
    }
}
```

---

## 4. Formatting

- **Allman braces**: `{` goes on its own line. A one-line guard `if (x) return;` is fine without braces.
- 4 spaces, no tabs. One declaration per line.
- Always write the access modifier (`private void Awake()`, not `void Awake()`).
- `var` only when the type is obvious: `var list = new List<Enemy>();` ✅ `var x = GetThing();` ❌
- Blank line between methods and between logical blocks.
- Mark classes `sealed` unless they are designed to be inherited.
- Avoid `#region` by default. If a class needs regions, it's usually too big, so split it instead.

**Size limits:** method ≤ 15 lines · class ≤ 200 lines · file ≤ 300 lines · ≤ 3 parameters (use a struct or options object beyond that).

---

## 5. Unity lifecycle — what goes where

| Method | Use for |
| --- | --- |
| `Awake` | Set up **this** object: cache own components, init fields |
| `OnEnable` | Subscribe to events |
| `Start` | Things that need **other** objects to be ready |
| `Update` | Per-frame input and visuals. Keep it tiny |
| `FixedUpdate` | Physics (`Rigidbody`) only |
| `LateUpdate` | Camera follow, things that run after movement |
| `OnDisable` | Unsubscribe from events |
| `OnDestroy` | Release things you created (native resources, etc.) |

- Don't rely on `Awake` order **between** objects. Cross-module boot order is owned by `FW_Core_Events`.
- Remove empty Unity methods. An empty `Update()` still costs a call every frame.

---

## 6. References & components

```csharp
// ✅ Inspector reference, cached, private
[SerializeField] private Rigidbody _body;

// ✅ Own component, cached once
private Animator _animator;
private void Awake() => _animator = GetComponent<Animator>();

// ✅ Optional component
if (other.TryGetComponent(out IDamageable target)) target.TakeDamage(_damage);

// ❌ Never
GameObject.Find("Player");            // slow, breaks on rename
FindObjectOfType<GameManager>();      // slow, hides dependencies
public float speed;                   // anyone can change it
```

- Use `[RequireComponent]` when a script can't work without another component.
- Use `CompareTag("Enemy")`, not `tag == "Enemy"` (which allocates). Put tag, layer and animator names in constants.

```csharp
private static readonly int SpeedHash = Animator.StringToHash("Speed");
_animator.SetFloat(SpeedHash, speed);
```

---

## 7. The Unity null trap

Destroyed Unity objects are "fake null". `==` knows this, but `?.`, `??` and `is null` **don't**.

```csharp
if (_target != null) _target.Hit();   // ✅
_target?.Hit();                        // ❌ may call into a destroyed object
```

- Don't keep references to objects from a scene that has been unloaded.
- Plain C# classes (not `UnityEngine.Object`) can use `?.` normally.

---

## 8. Performance

- **Allocations → GC spikes → stutter.** In anything per-frame:
  - reuse lists: `_results.Clear()` instead of `new List<>()`
  - no LINQ, no `string` concatenation or `$""` interpolation. Use `StringBuilder` or update text only when the value changes
  - use the `NonAlloc` / list overloads of `Physics.Raycast`, `OverlapSphere`, and similar
- **Fewer `Update` methods.** 1000 objects each with `Update` costs more than one manager looping over 1000. Use events for things that change rarely.
- **Pool** bullets, VFX, enemies and audio sources.
- No C# finalizers (`~MyClass()`). Use `IDisposable` / `OnDestroy`.
- **Profile before optimising.** Use the Unity Profiler on a real device, not guesses.

---

## 9. Data: ScriptableObjects

Config and shared data belong in assets, not in code or in scene objects.

```csharp
[CreateAssetMenu(menuName = "FW/Config/Player")]
public sealed class PlayerConfig : ScriptableObject
{
    [SerializeField, Min(0f)] private float _moveSpeed = 5f;
    public float MoveSpeed => _moveSpeed;
}
```

- Treat config ScriptableObjects as **read-only at runtime**. Changes made in the Editor during Play mode are saved to the asset.
- Use `[Tooltip]`, `[Range]`, `[Min]` and `[Header]` so designers know what they're editing.

---

## 10. Events & communication

```csharp
private void OnEnable()  => _health.Died += HandleDied;
private void OnDisable() => _health.Died -= HandleDied;

private void HandleDied() { /* ... */ }
```

- Use a C# `event Action<T>` in code and `UnityEvent` only for designer-wired Inspector hooks.
- Cross-module or cross-layer communication goes through **`FW_Core_Events`**, never through direct references.
- **Avoid singletons.** If something must be global, register it through the framework boot sequence.

---

## 11. Async & coroutines

- Unity 6: prefer **`Awaitable`** (`await Awaitable.WaitForSecondsAsync(1f, token)`). Coroutines are fine for simple sequences.
- Pass `destroyCancellationToken` so async work stops when the object is destroyed.
- `async void` **only** for event handlers. Everything else returns `Awaitable` or `Task`.
- Never `.Result` or `.Wait()`, because they freeze the game.
- Most Unity APIs are **main-thread only**. Use the Job System for heavy parallel work.

---

## 12. Errors & logging

```csharp
try
{
    _saveService.Write(data);
}
catch (IOException ex)
{
    Debug.LogException(ex);   // ✅ logged, not swallowed
    SaveFailed?.Invoke();
}
```

- `catch { }` is **never** allowed.
- Validate Inspector setup in `OnValidate` or `Awake` and log a clear error with `this` as context: `Debug.LogError("Missing _body", this);`.
- `Debug.Log` runs in builds too. Wrap noisy logs in a `[Conditional("UNITY_EDITOR")]` helper or the framework logger.

---

## 13. Assemblies (asmdef)

- Every FW module has `Runtime/` and `Tests/` asmdefs.
- **Layer rules:** `Core` references nothing else. `UIX` and `Logic` may reference `Core` but not each other. `_Framework` never references `_Game`. CI (**Asmdef layers**) enforces this.
- Only reference what the dependency rules allow. If you need something else, raise it in the PR.
- Use `internal` for anything not in the module's public API.
- Editor-only code goes in an `Editor/` folder with its own Editor-only asmdef. It must never ship in a build.

---

## 14. Framework rules (sellable code)

- **Zero references to `_Game`**, and no game-specific names (`Dragon`, `Level3`) in `_Framework`.
- Public API documented with `/// <summary>` comments. Buyers and teammates read these.
- Everything configurable through ScriptableObjects or the Inspector, not by editing framework source.
- Each module's `README.md` stays current: purpose, API, status.
- New public behaviour needs a test in `Tests/`.

---

## 15. PR checklist

- [ ] Compiles with **zero warnings** and no errors in the Console
- [ ] Naming + layout match this doc
- [ ] No `public` fields, no `Find`/`GetComponent` in `Update`
- [ ] Events unsubscribed in `OnDisable`
- [ ] No magic numbers/strings, no nested `if`, no empty `catch`
- [ ] No per-frame allocations in hot paths
- [ ] `.meta` files committed, no files under `Library/` committed
- [ ] Module README updated
- [ ] Tested in Play mode (and tests pass in Test Runner)

---

## 16. What enforces each rule

A rule nobody checks is a suggestion. Every rule above has an enforcer, from strictest to softest:

| Enforcer | Blocks merge? | Rules |
| --- | --- | --- |
| **CI: C# format** (`dotnet format` + `.editorconfig`) | Yes | Allman braces, 4 spaces, spacing, line endings, trailing whitespace, final newline (§4) |
| **CI: C# contract** (`.github/scripts/CheckCSharpContract.py`) | Yes | One type per file named after the file (§1.9), namespace under the module's asmdef `rootNamespace` (§2), no empty `catch` (§1.8), no `UnityEditor` in `Runtime/` without `#if UNITY_EDITOR` (§13), file ≤ 300 lines (§4) |
| **CI: Asmdef layers** | Yes | Layer rules, `_Framework` never references `_Game` (§1.10, §13) |
| **IDE warnings** (`.editorconfig` in Rider / Visual Studio / VS Code) | No, fix before PR | Naming: `_camelCase` fields, `PascalCase` constants, `I` interfaces (§2); always write access modifiers, `var` only when obvious (§4) |
| **AI review** on the PR | No, advisory | `Find`/`GetComponent` in `Update`, magic numbers, nested `if`, hot-path allocations, `OnEnable`/`OnDisable` pairing, `public` fields, method/class size, `sealed` (§1, §4, §5–§8) |
| **Lead review** | Yes | Design and API shape, whether code belongs in `_Framework`, README and tests updated (§14, §15) |

Adding a rule? Add it to this table too, and push it as far up as it can reliably go.

---

**Sources:** [Unity Manual: programming best practices](https://docs.unity3d.com/6000.5/Documentation/Manual/programming-best-practices.html) · [unity.com/how-to](https://unity.com/how-to#ai) · [SamuelAsherRivello/unity-best-practices](https://github.com/SamuelAsherRivello/unity-best-practices) (SOLID + design patterns with Unity samples) · M. A. Khan, *Unity C# Coding Conventions & Best Practices* (2025).
