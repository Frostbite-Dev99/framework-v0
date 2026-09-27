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
| **Unity tests** | Failing EditMode/PlayMode tests, compile errors | Run *Window → General → Test Runner* locally |

Pushes to `main` also run a **Unity build** (smoke test, Linux player) to catch Editor-only code in runtime assemblies.
The release-please PR is exempt from **Issue link**.

Run the fast checks locally before pushing:
```bash
bash .github/scripts/CheckMetaFiles.sh
python3 .github/scripts/CheckAsmdefLayers.py
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
   This creates the teams and labels, sets the merge settings and turns on protection for `main`.
4. Add people to the teams: `team-leads` (review + merge) and `developers` (issues, branches, PRs). Org owners who merge must be in `team-leads` too.
5. You need **at least 2 team leads**, because nobody can approve their own PR.
