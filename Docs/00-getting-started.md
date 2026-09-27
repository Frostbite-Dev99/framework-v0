# Getting Started

From zero to the project running in Unity. One-time setup, about 30 minutes (mostly downloads).

## 1. Install

| Tool | Get it | Notes |
| --- | --- | --- |
| **Unity Hub** | unity.com/download | Sign in with your Unity account (free Personal licence) |
| **Unity 6000.6.3f1** | Unity Hub → *Installs → Install Editor → Archive* | **Must be this exact version.** Add the modules *Windows Build Support* + *Android/iOS* only if you build for them |
| **Git for Windows** | git-scm.com | Includes **Git LFS** |
| **GitHub Desktop** _(optional)_ | desktop.github.com | Easier if you're new to Git |
| **Code editor** | Rider, Visual Studio 2022 (with *Game development with Unity*), or VS Code + C# Dev Kit + Unity extension | |

## 2. Get the project

Accept the invite to **Frostbite-Dev99** on GitHub first, then clone:

```bash
git lfs install
git clone https://github.com/Frostbite-Dev99/framework-v0.git
cd framework-v0
git config core.hooksPath .githooks     # adds (#issue) to your commits
```

GitHub Desktop: *File → Clone repository → framework-v0*, then run the last line in *Repository → Open in Command Prompt*.

> Clone to a normal Windows folder (e.g. `C:\Dev\`). Avoid OneDrive-synced folders and WSL paths, because Unity gets slow and misses file changes.

## 3. Open in Unity

1. **Unity Hub → Projects → Add → Add project from disk →** select the `framework-v0` folder (the one containing `Assets/`).
2. Click the project in the list. If asked for an editor, pick **6000.6.3f1**.
3. **First open takes a few minutes.** Unity builds the `Library/` cache. That's normal, and it's faster after.
4. Set your code editor: *Edit → Preferences → External Tools → External Script Editor*.

### Check it works
- [ ] Console (*Window → General → Console*) has **no red errors**
- [ ] `Assets/_Game/Scenes/SampleScene` opens, press ▶ Play and nothing errors
- [ ] `git status` shows **no changes** (if it shows changed `.meta` or `ProjectSettings` files, ask in Discord before committing)

## 4. Where things are

| In the Project window | What |
| --- | --- |
| `_Framework/Core`, `UIX`, `Logic` | Framework modules (`FW_…`). Each has a README with owner and status |
| `_Game/` | The reference game: scenes, settings, features |
| `_Sandbox/<YourName>/` | Your personal playground. Make your own folder |
| `ThirdParty/` | Asset Store imports |

## 5. Start working

1. Read [01 C# best practices](01-csharp-best-practices.md) and [02 GitHub workflow](02-github-workflow.md).
2. Pick a module in the role sheet, **create an issue and assign yourself**.
3. `git switch -c feat/<issue#>-<short-name>`, code, then open a PR. A team lead reviews and merges.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| Hub says "version not installed" | Install **6000.6.3f1** exactly. Don't upgrade the project |
| "Enter Safe Mode?" on open | Compile errors. Enter Safe Mode, read the Console, and ask in Discord if it's not your code |
| Pink / magenta sprites | Render pipeline missing: *Edit → Project Settings → Graphics* should use `UniversalRP` from `_Game/Settings` |
| Images/audio are tiny text files | LFS wasn't installed before cloning: `git lfs install && git lfs pull` |
| Commit rejected "needs an issue number" | Name your branch `feat/12-thing` or add `(#12)` to the message |
| Lots of changed files after opening | Unity upgraded or reserialised something. Don't commit it, ask a lead |
| Unity is very slow | Project is on OneDrive/WSL/network drive. Clone to `C:\Dev\` |
