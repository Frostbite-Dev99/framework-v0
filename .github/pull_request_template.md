<!--
Title: Conventional Commit + issue number, e.g.  feat(core-events): add typed event bus (#12)
It becomes the squash commit and the changelog line. See Docs/02-github-workflow.md.
-->

Closes #

## What & why


## How to test
1.

## Checklist ([Docs/01-csharp-best-practices.md](../Docs/01-csharp-best-practices.md))
- [ ] Linked issue is assigned and its acceptance criteria are met
- [ ] Zero Console errors/warnings, tested in Play mode
- [ ] Naming, layout, no public fields, no `Find`/`GetComponent` in `Update`
- [ ] Events unsubscribed in `OnDisable`; no empty `catch`; no magic numbers
- [ ] `.meta` files committed
- [ ] Module README updated
