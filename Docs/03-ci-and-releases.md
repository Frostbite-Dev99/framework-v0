# CI Checks & Releases

How PRs are checked automatically, and how versions and the changelog are produced.
For the team workflow (issues → branch → PR → review), see [`02-github-workflow.md`](02-github-workflow.md).

## CI checks (all required to merge)

| Check | What it catches | Fix |
| --- | --- | --- |
| **PR title** | Title isn't a Conventional Commit | Edit the PR title |
| **Issue link** | Title doesn't end in `(#N)`, body lacks `Closes #N`, issue has no assignee, or a commit has no `#N` | See [02 · Issues](02-github-workflow.md#1-issues-first) |
| **Meta files** | Asset without `.meta`, or orphan `.meta` | Open Unity, let it generate, commit the `.meta` |
| **Asmdef layers** | Core → UIX/Logic, UIX ↔ Logic, Framework → Game references | Communicate via `FW_Core_Events` instead |
| **C# format** | Braces, indentation, spacing, line endings that don't match `.editorconfig` | Run the `dotnet format` fix command below. Editor format-on-save helps, but CI only trusts `dotnet format` |
| **C# contract** | More than one type per file, type name ≠ file name, namespace not under the module's asmdef, empty `catch`, `UnityEditor` in `Runtime/` without `#if UNITY_EDITOR`, files over 300 lines | Follow the message; rules are in [01 · §16](01-csharp-best-practices.md#16-what-enforces-each-rule) |
| **Unity tests** | Failing EditMode/PlayMode tests, compile errors | Run *Window → General → Test Runner* locally |

Pushes to `main` also run a **Unity build** (smoke test, Linux player) to catch Editor-only code in runtime assemblies.
The release-please PR is exempt from **Issue link**.

Run the fast checks locally before pushing:
```bash
bash .github/scripts/CheckMetaFiles.sh
python3 .github/scripts/CheckAsmdefLayers.py
python3 .github/scripts/CheckCSharpContract.py
dotnet format whitespace . --folder --include Assets/_Framework/ Assets/_Game/   # fixes formatting (needs the .NET 8 SDK)
```

## Releases & changelog (release-please)

```
PRs squash-merged to main ──▶ release-please updates "chore: release x.y.z" PR
                              CI green ──▶ release bot auto-merges ──▶ tag + GitHub Release + CHANGELOG
```

| Title type | Version bump (pre-1.0) | In changelog |
| --- | --- | --- |
| `feat` | minor `0.1.0 → 0.2.0` | Features |
| `fix`, `perf` | patch `0.1.0 → 0.1.1` | Bug Fixes / Performance |
| `refactor`, `docs` | none | Refactors / Documentation |
| `test`, `ci`, `chore` | none | hidden |
| `feat!:` / `BREAKING CHANGE:` | minor pre-1.0, major after | highlighted |

- **Don't edit `CHANGELOG.md`, `version.txt` or `.release-please-manifest.json` by hand.** release-please owns them.
- Only the release PR auto-merges. Every other PR needs a team lead (see 02).
- Every merged `feat` or `fix` becomes a release.

## One-time admin setup

1. **Create the release bot:** go to *Org settings → Developer settings → GitHub Apps → New*, uncheck Webhook, and set these repo permissions: **Contents**, **Pull requests** and **Issues**: Read & write (release-please adds labels through the Issues API). Then install it on `framework-v0` only.
2. **Repo variables and secrets** (*Settings → Secrets and variables → Actions*):
   - variable `RELEASE_BOT_APP_ID`, secret `RELEASE_BOT_PRIVATE_KEY` (the app's generated `.pem`)
   - secrets `UNITY_LICENSE`, `UNITY_EMAIL`, `UNITY_PASSWORD` ([GameCI activation guide](https://game-ci.com/docs/github/activation)). Until these are set, Unity tests are **skipped** with a warning.
3. Push the first commit to `main`, then run:
   `RELEASE_BOT_APP_SLUG=<app-slug> bash Scripts/SetupGitHubRepo.sh`
   This creates the `team-leads` team and the labels, sets org base permission to **Write**, sets the merge settings and turns on protection for `main`.
4. Invite everyone to the org. Members can push branches and open PRs. Add leads to **`team-leads`** (review + merge), including org owners who merge.
5. Admin enforcement is **off**: admins in `team-leads` can merge their own PRs (admin bypass). Leads who aren't admins still need another lead's approval.
