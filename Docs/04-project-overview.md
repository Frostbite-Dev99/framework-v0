# Project Overview

The big picture: what this project is, how Git and GitHub fit in, and how a change gets from your PC into the game.
For the step-by-step details, see [02 GitHub workflow](02-github-workflow.md) and [03 CI & releases](03-ci-and-releases.md).

## 1. What this project is

A Unity 6 project with two halves:

- **The framework** (`Assets/_Framework/`): reusable building blocks (saving, health, inventory, menus, audio, input and so on) that any future game can use.
- **The reference game** (`Assets/_Game/`): a small game built only from those blocks. It shows that the framework works.

The framework is split into three layers, and each module belongs to one:

| Layer | What it covers | Modules |
| --- | --- | --- |
| **Core** | Foundations everything else needs | Events, GameConfig, ObjectManager, SaveSystem, SceneLoader |
| **Logic** | Gameplay rules | FiniteStateMachine, Health, Inventory, Loot, Stats |
| **UIX** | What the player sees, hears and touches | Audio, Binding, InputSystem, SafeArea, ScreenManager |

**The one rule:** layers don't reach into each other. Core uses nothing above it, Logic and UIX never use each other, and the framework never uses the game. When modules need to talk, they send events through `FW_Core_Events`. CI checks this on every PR.

```
          _Game  (uses anything below)
        ┌───────┴───────┐
      Logic           UIX        <- never reference each other
        └───────┬───────┘
              Core               <- references nothing above it
```

Each module folder (`FW_<Layer>_<Module>/`) has a `README.md` with its owner and status, a `Runtime/` folder for code that ships in the game, and a `Tests/` folder.

## 2. Git and GitHub

- **Git** is a program on your PC. It saves snapshots of the project, called **commits**, so you can go back, compare and combine everyone's work.
- **GitHub** is the website that holds the shared copy. It's also where we plan work (**issues**), review changes (**pull requests**) and run automatic checks (**CI**).

### Local vs remote

You never edit the shared copy directly. Everyone has their own full copy on their PC (the **local** repo), and GitHub holds the shared one (the **remote**, called `origin`).

```
 Your PC (local)                                        GitHub (remote: origin)
 edit files ──commit──▶ your branch ──push──▶ your branch on GitHub ──PR──▶ main
                        main ◀──────────────pull──────────────────────────── main
```

| Word | Meaning |
| --- | --- |
| **clone** | Download the repo once to get your local copy |
| **commit** | Save a snapshot on your PC. Nobody else sees it yet |
| **push** | Send your commits to GitHub |
| **pull** | Get everyone else's commits from GitHub |
| **branch** | Your own line of work, so unfinished changes don't affect anyone |
| **`main`** | The official version of the project. Only changes from reviewed PRs get in |
| **pull request (PR)** | "Please add my branch to `main`." Where review and checks happen |

## 3. How a change happens

```
 1. Issue      2. Branch           3. Commit + push      4. Pull request       5. Merge
 "what &   ──▶ feat/12-health ──▶  on your branch   ──▶  CI checks +       ──▶ lead merges into main,
  why", #12                                               lead reviews          issue closes
```

1. **Issue first.** Every piece of work starts as a GitHub issue that says what and why, with an assignee. No issue, no work.
2. **Branch.** Make a branch named after the issue, e.g. `feat/12-health-clamp`.
3. **Commit and push** your work to that branch as often as you like.
4. **Open a pull request** into `main`. CI checks it automatically, and a team lead reviews it.
5. **A lead merges it.** The issue closes, and the change is part of `main`.

Nobody pushes straight to `main`, including leads. Every change goes through a PR.

### What happens automatically

- **CI** runs on every PR. It checks the PR title, the issue link, Unity `.meta` files and the layer rule, and runs the tests. A PR can't merge until CI passes.
- **Releases:** merged features and fixes are collected into a new version number and a `CHANGELOG.md` entry by a bot. Nobody edits those files by hand.

## 4. Where things are

**Folders you work in:**

| Folder | What it is |
| --- | --- |
| `Assets/_Framework/` | The framework modules (see section 1) |
| `Assets/_Game/` | The reference game: scenes, settings, game features, shared art and audio |
| `Assets/_Sandbox/<YourName>/` | Your playground. Experiment freely; real code never uses it |
| `Assets/ThirdParty/` | Asset Store imports. Don't edit |
| `Docs/` | These guides |

**Folders you rarely touch:**

| Folder | What it is |
| --- | --- |
| `Packages/` | Which Unity packages the project uses. Unity edits it |
| `ProjectSettings/` | Unity project settings. Change only on purpose |
| `.github/` | CI checks, issue forms, the PR checklist, release automation |
| `.githooks/` | Adds the issue number to your commit messages |
| `Scripts/` | One-time admin setup |

**Created by Unity on your PC, never committed:** `Library/`, `Temp/`, `Logs/`, `UserSettings/`.

Every file Unity knows about has a matching `.meta` file. Always commit them together.
