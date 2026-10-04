#!/usr/bin/env bash
# One-time GitHub setup (run by an org admin, after the first commit exists on main):
#   - team: team-leads (maintain, can merge); org base permission = write (members push branches, can't merge)
#   - issue labels (type / layer / priority / needs-owner)
#   - squash-only merges, auto-merge OFF, delete branch after merge
#   - main protection: PR + 1 code-owner (team lead) approval, required CI checks,
#     only team-leads + release bot may merge; release bot skips the review requirement;
#     admins are not enforced, so an admin lead can merge their own PR (admin bypass).
# Usage: RELEASE_BOT_APP_SLUG=<app-slug> bash Scripts/SetupGitHubRepo.sh
set -euo pipefail

readonly ORG="Frostbite-Dev99"
readonly REPO="framework-v0"
readonly BRANCH="main"
readonly LEADS_TEAM="team-leads"
readonly BASE_PERMISSION="write"
readonly APP_SLUG="${RELEASE_BOT_APP_SLUG:?Set RELEASE_BOT_APP_SLUG to the release bot GitHub App slug}"

ensure_team() {
  local team="$1" permission="$2"
  gh api "orgs/$ORG/teams/$team" --silent 2>/dev/null \
    || gh api -X POST "orgs/$ORG/teams" -f name="$team" -f privacy=closed --silent
  gh api -X PUT "orgs/$ORG/teams/$team/repos/$ORG/$REPO" -f permission="$permission" --silent
  echo "team $team -> $permission"
}

configure_org_base_permission() {
  gh api -X PATCH "orgs/$ORG" -f default_repository_permission="$BASE_PERMISSION" --silent
  echo "org base permission -> $BASE_PERMISSION"
}

configure_merge_settings() {
  gh api -X PATCH "repos/$ORG/$REPO" \
    -F allow_squash_merge=true \
    -F allow_merge_commit=false \
    -F allow_rebase_merge=false \
    -F allow_auto_merge=false \
    -F delete_branch_on_merge=true \
    -f squash_merge_commit_title=PR_TITLE \
    -f squash_merge_commit_message=PR_BODY \
    --silent
  echo "merge settings: squash only, auto-merge off"
}

# name|color|description
readonly LABELS=(
  "type: feature|1d76db|New behaviour"
  "type: bug|d73a4a|Something is broken"
  "type: task|c5def5|Docs, refactor, tooling, CI, assets"
  "layer: core|5319e7|FW_Core_*"
  "layer: uix|0e8a16|FW_UIX_*"
  "layer: logic|fbca04|FW_Logic_*"
  "layer: game|bfd4f2|Reference game (_Game)"
  "priority: high|b60205|Do next"
  "priority: low|e4e669|When there is time"
  "needs-owner|ff7619|No assignee yet (bot-managed)"
)

create_labels() {
  local entry name color description
  for entry in "${LABELS[@]}"; do
    IFS='|' read -r name color description <<< "$entry"
    gh label create "$name" --repo "$ORG/$REPO" --color "$color" --description "$description" --force
  done
  echo "labels ready"
}

protect_main() {
  gh api -X PUT "repos/$ORG/$REPO/branches/$BRANCH/protection" --input - --silent <<JSON
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["PR title", "Issue link", "Meta files", "Asmdef layers", "C# format", "C# contract", "Unity tests"]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "require_code_owner_reviews": true,
    "dismiss_stale_reviews": true,
    "require_last_push_approval": true,
    "bypass_pull_request_allowances": { "users": [], "teams": [], "apps": ["$APP_SLUG"] }
  },
  "restrictions": { "users": [], "teams": ["$LEADS_TEAM"], "apps": ["$APP_SLUG"] },
  "required_linear_history": true,
  "required_conversation_resolution": true,
  "allow_force_pushes": false,
  "allow_deletions": false
}
JSON
  echo "branch protection applied to $BRANCH"
}

gh api "repos/$ORG/$REPO/branches/$BRANCH" --silent \
  || { echo "Branch $BRANCH does not exist yet - push the first commit, then rerun." >&2; exit 1; }

ensure_team "$LEADS_TEAM" maintain
configure_org_base_permission
configure_merge_settings
create_labels
protect_main
echo "Done. Add members: https://github.com/orgs/$ORG/teams"
