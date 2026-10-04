<!--
Title: Conventional Commit + issue number, e.g.  feat(core-events): add typed event bus (#12)
It becomes the squash commit and the changelog line. See Docs/02-github-workflow.md.
-->

Closes #

## What & why


## How to test
1.

## Checklist ([Docs/01-csharp-best-practices.md](../Docs/01-csharp-best-practices.md))
CI already checks formatting, `.meta` files, layers and the C# contract ([§16](../Docs/01-csharp-best-practices.md#16-what-enforces-each-rule)). These are the rest:
- [ ] Linked issue is assigned and its acceptance criteria are met
- [ ] Zero Console errors/warnings, tested in Play mode
- [ ] Naming matches §2; no public fields, `Find`/`GetComponent` in `Update`, magic numbers, or events left subscribed in `OnDisable`
- [ ] Module README updated if the API or status changed
