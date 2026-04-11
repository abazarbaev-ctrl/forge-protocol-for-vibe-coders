#!/bin/bash
# Forge Protocol: Pre-commit nudge
# Outputs context for Claude to use as a nudge before git commit/push.

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('input',''))" 2>/dev/null || echo "")

# Only trigger on git commit/push commands
case "$COMMAND" in
  *"git commit"*|*"git push"*)
    ;;
  *)
    exit 0
    ;;
esac

if echo "$COMMAND" | grep -q "git push"; then
  UNCOMMITTED=$(git status --porcelain 2>/dev/null | head -5)
  if [ -n "$UNCOMMITTED" ]; then
    echo "forge-nudge: You have uncommitted changes. Verify nothing is being left behind."
  fi
  exit 0
fi

# Check if tests exist but haven't been run recently
PROJECT_DIR=$(pwd)
TESTS_EXIST=false

for d in tests test __tests__ spec; do
  if [ -d "$PROJECT_DIR/$d" ]; then
    TESTS_EXIST=true
    break
  fi
done

if [ "$TESTS_EXIST" = true ]; then
  TESTS_RAN=false
  for f in .pytest_cache/v/cache/lastfailed node_modules/.cache/vitest; do
    if [ -e "$PROJECT_DIR/$f" ]; then
      AGE=$(( $(date +%s) - $(stat -f %m "$PROJECT_DIR/$f" 2>/dev/null || stat -c %Y "$PROJECT_DIR/$f" 2>/dev/null || echo 0) ))
      if [ "$AGE" -lt 600 ]; then
        TESTS_RAN=true
        break
      fi
    fi
  done
  if [ "$TESTS_RAN" = false ]; then
    echo "forge-nudge: Tests exist but haven't been run recently. Consider running tests before committing."
  fi
fi

exit 0
