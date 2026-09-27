"""Enforces issue-first rules on a PR (Docs/02-github-workflow.md):

1. PR title ends with "(#N)"
2. PR body links the same issue: "Closes|Fixes|Resolves|Refs #N"
3. #N is an open issue (not a PR) with at least one assignee
4. Every non-merge commit in the PR references an issue ("#N")

Env: GITHUB_TOKEN, GITHUB_REPOSITORY, PR_NUMBER, PR_TITLE, PR_BODY
"""
import json
import os
import re
import sys
import urllib.request

API_ROOT = "https://api.github.com"
PAGE_SIZE = 100
TITLE_ISSUE_PATTERN = re.compile(r"\(#(\d+)\)$")
BODY_LINK_TEMPLATE = r"\b(?:closes|fixes|resolves|refs)\s+#{issue}\b"
COMMIT_ISSUE_PATTERN = re.compile(r"#\d+")
MERGE_PARENT_COUNT = 2


def github_get(path: str) -> dict | list:
    request = urllib.request.Request(
        f"{API_ROOT}{path}",
        headers={
            "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
            "Accept": "application/vnd.github+json",
        },
    )
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def list_pr_commits(repo: str, pr_number: str) -> list[dict]:
    commits: list[dict] = []
    page = 1
    while True:
        batch = github_get(f"/repos/{repo}/pulls/{pr_number}/commits?per_page={PAGE_SIZE}&page={page}")
        commits.extend(batch)
        if len(batch) < PAGE_SIZE:
            return commits
        page += 1


def check_title(title: str) -> tuple[str | None, list[str]]:
    match = TITLE_ISSUE_PATTERN.search(title.strip())
    if not match:
        return None, [f"PR title must end with the issue number, e.g. 'feat(core-events): add bus (#12)'. Got: '{title}'"]
    return match.group(1), []


def check_body(body: str, issue: str) -> list[str]:
    if re.search(BODY_LINK_TEMPLATE.format(issue=issue), body, re.IGNORECASE):
        return []
    return [f"PR body must link the issue: add 'Closes #{issue}' (or Fixes/Resolves/Refs)."]


def check_issue(repo: str, issue: str) -> list[str]:
    data = github_get(f"/repos/{repo}/issues/{issue}")
    if "pull_request" in data:
        return [f"#{issue} is a pull request, not an issue. Create an issue first."]
    errors = []
    if data["state"] != "open":
        errors.append(f"Issue #{issue} is closed. Reopen it or link the right issue.")
    if not data["assignees"]:
        errors.append(f"Issue #{issue} has no assignee. Assign yourself (or ask a lead) before opening the PR.")
    return errors


def check_commits(commits: list[dict]) -> list[str]:
    return [
        f"Commit {commit['sha'][:7]} has no issue number: '{commit['commit']['message'].splitlines()[0]}'"
        for commit in commits
        if len(commit["parents"]) < MERGE_PARENT_COUNT
        and not COMMIT_ISSUE_PATTERN.search(commit["commit"]["message"])
    ]


def main() -> int:
    repo = os.environ["GITHUB_REPOSITORY"]
    pr_number = os.environ["PR_NUMBER"]

    issue, errors = check_title(os.environ["PR_TITLE"])
    if issue is not None:
        errors += check_body(os.environ.get("PR_BODY") or "", issue)
        errors += check_issue(repo, issue)
    errors += check_commits(list_pr_commits(repo, pr_number))

    for error in errors:
        print(f"::error::{error}")
    print(f"Issue link: {len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
