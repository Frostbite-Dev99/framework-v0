# GitHub Workflow

How we plan, branch, commit, review and merge. **Every change starts with an issue.**

```
Issue (assigned) ──▶ branch feat/12-event-bus ──▶ commits "… (#12)" ──▶ PR "… (#12)" + "Closes #12"
                                                          ──▶ CI green + team lead approves ──▶ lead squash-merges ──▶ issue auto-closes
```

## 0. Roles

| | Developer | Team lead |
| --- | --- | --- |
| Create issues, assign self | ✅ | ✅ |
| Assign issues to others | — | ✅ |
| Push branches, open PRs | ✅ | ✅ |
| Approve PRs | — | ✅ (not their own) |
| Merge to `main` | ❌ | ✅ |
| Push directly to `main` | ❌ | ❌ |

`main` is protected: PR only, 1 code-owner (lead) approval, stale approvals dismissed, CI green, linear history, no force-push.
A lead's own PR needs **another** lead to approve it. There's no admin bypass.

---

## 1. Issues first

**No issue, no work.** Before you write code, docs or assets:

1. **New → Issue** and pick a template: **Feature**, **Bug** or **Task**.
2. Fill in the **acceptance criteria**. These are the spec: how will a reviewer know it's done?
3. **Assign it.** Assign yourself for your own work. Leads assign found bugs and planned work to members.
4. Every issue has **at least one assignee** at all times. Unassigned issues get the `needs-owner` label automatically, and a PR linked to one fails CI.

| Label | Meaning |
| --- | --- |
| `type: feature` / `type: bug` / `type: task` | Set by the template |
| `layer: core` / `layer: uix` / `layer: logic` / `layer: game` | Which part of the codebase |
| `priority: high` / `priority: low` | Set by leads |
| `needs-owner` | No assignee yet (bot-managed) |

Big feature? Split it into smaller issues and link them in a checklist on the parent issue.

---

## 2. Branch

Name: `<type>/<issue#>-<short-description>`

```bash
git switch main && git pull
git switch -c feat/12-event-bus
```

| Prefix | Use |
| --- | --- |
| `feat/` | new feature |
| `fix/` | bug fix |
| `docs/` | docs only |
| `refactor/` · `test/` · `chore/` · `ci/` | as named |

---

## 3. Commit

[Conventional Commits](https://www.conventionalcommits.org/) + the issue number, **every commit**:

```
feat(core-events): add typed event bus (#12)
fix(logic-health): clamp damage at zero (#31)
```

**One-time per clone:** `git config core.hooksPath .githooks`
After that, the `commit-msg` hook adds `(#12)` for you, reading the number from the branch name. It rejects the commit if it can't find one.

Scope = module in kebab-case (`core-events`, `uix-audio`, `logic-inventory`, `game`).

---

## 4. Pull request

```bash
git push -u origin feat/12-event-bus
gh pr create --base main --fill
```

- **Title:** `feat(core-events): add typed event bus (#12)`. It becomes the squash commit and the changelog line.
- **Body:** keep `Closes #12` from the template so the issue closes on merge.
- Fill in the template checklist and ping a lead in Discord when CI is green.
- Stacked on another unmerged PR? Say so: "Stacked on #NN".

## 5. Review & merge (leads)

- Check the PR against the issue's acceptance criteria and the [C# best practices](01-csharp-best-practices.md).
- Use **Request changes** for anything that must be fixed and **Comment** for nice-to-haves. Resolve every conversation before merging.
- **Squash and merge** only. The branch is deleted automatically.
- If the author pushes new commits, the approval is dismissed and you review again.

---

## 6. Keeping your branch up to date (rebase)

When someone else merges into `main`, your branch is **behind**. Rebase it to move your commits on top of the latest `main`:

```
Before:  main: A---B---C---D          After `git rebase main`:  main: A---B---C---D
                    \                                                          \
         yours:      E---F                                          yours:      E'---F'
```

```bash
git switch main && git pull
git switch feat/12-event-bus
git rebase main
git push --force-with-lease     # commit IDs changed, so a normal push is rejected
```

**Conflicts:** Git pauses at each conflict. Open the file and keep the right version between `<<<<<<<`, `=======` and `>>>>>>>`. Delete the marker lines, then run:
```bash
git add <file>
git rebase --continue           # or: git rebase --abort to undo everything
```

**Unity scenes and prefabs** merge badly. Announce in Discord before editing a shared scene or prefab, and keep those edits small.

Rebase **your own** branch only. Never rebase `main` or a branch someone else pushes to.

## 7. Keep working while your PR waits

- **Same feature?** Keep committing on the same branch. Pushing updates the PR.
- **Next piece needs your unmerged code?** Stack a branch on top (keep stacks 1–2 deep):

```bash
git switch feat/12-event-bus
git switch -c feat/15-event-debugger      # needs its own issue (#15)
# …after #12's PR merges:
git switch main && git pull
git switch feat/15-event-debugger
git rebase --onto main feat/12-event-bus
git push --force-with-lease
```

## 8. Tidy your branch into one commit (optional)

```bash
git reset --soft $(git merge-base main HEAD)
git commit -m "feat(core-events): add typed event bus (#12)"
git push --force-with-lease
```

---

## Do / don't

- ✅ Issue first, assigned, with acceptance criteria
- ✅ `git pull` on `main` before branching and rebase when `main` moves
- ✅ `--force-with-lease`, never plain `--force`
- ✅ Commit `.meta` files with their assets
- ❌ Work without an issue, or leave an issue unassigned
- ❌ Rebase or force-push `main` or a shared branch
- ❌ Edit `CHANGELOG.md` / `version.txt` (release-please owns them)

## Cheat sheet

```bash
git config core.hooksPath .githooks            # once per clone
git switch main && git pull
git switch -c feat/12-event-bus                # branch from an assigned issue
git add -p && git commit -m "feat(core-events): add bus"   # hook appends (#12)
git push -u origin feat/12-event-bus
gh pr create --base main --fill                # title "… (#12)", body "Closes #12"

git switch main && git pull && git switch - && git rebase main   # main moved
git push --force-with-lease

gh issue create --assignee @me                 # new issue, assigned to you
gh issue list --assignee @me                   # your work
git stash / git stash pop                      # shelve / restore
```
