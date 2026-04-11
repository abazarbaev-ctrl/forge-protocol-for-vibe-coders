#!/bin/bash
# Forge Protocol: Session start context
# Outputs reminders for Claude to use naturally in conversation.

REMINDERS=""

# Monday = review day
DAY=$(date +%u)
if [ "$DAY" -eq 1 ]; then
  REMINDERS="${REMINDERS}forge-reminder: It's Monday — weekly Forge review day. Offer to run /forge-review.\n"
fi

# Check for TODO.md with pending items
if [ -f "TODO.md" ]; then
  PENDING=$(grep -c "^\- \[ \]" TODO.md 2>/dev/null || echo 0)
  if [ "$PENDING" -gt 0 ]; then
    REMINDERS="${REMINDERS}forge-context: This project has ${PENDING} pending TODO items.\n"
  fi
fi

# Check for recent CI failures
if command -v gh &>/dev/null; then
  REPO=$(git remote get-url origin 2>/dev/null | sed 's/.*github.com[:/]\(.*\)\.git/\1/' | sed 's/.*github.com[:/]\(.*\)/\1/')
  if [ -n "$REPO" ]; then
    LAST_RUN=$(gh run list --repo "$REPO" --limit 1 --json conclusion -q '.[0].conclusion' 2>/dev/null)
    if [ "$LAST_RUN" = "failure" ]; then
      REMINDERS="${REMINDERS}forge-alert: Last CI run FAILED. Check before starting new work.\n"
    fi
  fi
fi

if [ -n "$REMINDERS" ]; then
  printf "$REMINDERS"
fi

exit 0
