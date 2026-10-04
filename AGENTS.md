# AGENTS.md

Instructions for AI coding assistants (Cursor, Copilot, Codex, Claude via `CLAUDE.md`). Humans: the same rules live in `Docs/`.

## Project
Unity 6000.6.3f1 (URP 2D), C#. Reusable framework in `Assets/_Framework/` (layers Core, Logic, UIX; one folder per module `FW_<Layer>_<Module>/`) plus a reference game in `Assets/_Game/`. Overview: `Docs/04-project-overview.md`.

## Rules
- Follow `Docs/01-csharp-best-practices.md`. Its section 1 (the 10 rules) is the minimum.
- **Layers:** Core references nothing else. Logic and UIX may reference Core but never each other. `_Framework` never references `_Game`. Cross-module communication goes through `FW_Core_Events`, never direct references.
- New code goes in the module's `Runtime/` folder. Editor-only code goes in `Editor/` with its own Editor-only asmdef. Tests go in `Tests/`.
- Anything not in a module's public API is `internal`. Public API gets `/// <summary>` docs.
- No game-specific names in `_Framework`. Config goes through ScriptableObjects or the Inspector.
- When a module's API or status changes, update that module's `README.md`.

## Don't touch
- `CHANGELOG.md`, `version.txt`, `.release-please-manifest.json` (owned by release-please).
- `Assets/ThirdParty/`, `Library/`, `Temp/`, `Logs/`, `UserSettings/`.
- `ProjectSettings/` and `Packages/` unless the task is about them.
- Never create, delete or rename a `.meta` file by hand. Unity generates them; commit them with their asset.

## Git
- Every change belongs to an assigned GitHub issue. Branch: `<type>/<issue#>-<short-name>` (e.g. `feat/12-event-bus`).
- Commits and PR titles use Conventional Commits with the issue number: `feat(core-events): add typed event bus (#12)`. Scope is the module in kebab-case. PR body keeps `Closes #12`.
- Never push to `main`, never force-push a shared branch. Details: `Docs/02-github-workflow.md`.

## Before finishing
Run the local checks from `Docs/03-ci-and-releases.md`:
```bash
bash .github/scripts/CheckMetaFiles.sh
python3 .github/scripts/CheckAsmdefLayers.py
python3 .github/scripts/CheckCSharpContract.py
dotnet format whitespace . --folder --include Assets/_Framework/ Assets/_Game/
```
Which rules CI enforces and which are left to review: `Docs/01-csharp-best-practices.md` section 16.
