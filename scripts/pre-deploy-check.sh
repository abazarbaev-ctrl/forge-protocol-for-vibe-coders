#!/bin/bash
# Forge Protocol: Pre-deploy Gate 4 check
# Runs before deploy-related bash commands.

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('input',''))" 2>/dev/null || echo "")

# Only trigger on deploy-related commands
case "$COMMAND" in
  *"deploy"*|*"gcloud run deploy"*|*"firebase deploy"*|*"vercel"*|*"npm run deploy"*)
    ;;
  *)
    exit 0
    ;;
esac

CHECKS=""
PROJECT_DIR=$(pwd)

# Check 1: Uncommitted changes
DIRTY=$(git status --porcelain 2>/dev/null | head -3)
if [ -n "$DIRTY" ]; then
  CHECKS="${CHECKS}forge-gate4: WARNING — uncommitted changes exist.\n"
fi

# Check 2: Tests exist
TESTS_EXIST=false
for d in tests test __tests__ spec; do
  if [ -d "$PROJECT_DIR/$d" ]; then
    TESTS_EXIST=true
    break
  fi
done
if [ "$TESTS_EXIST" = false ]; then
  CHECKS="${CHECKS}forge-gate4: No test directory found. Deploying without tests.\n"
fi

# Check 3: Health check endpoint
if ! grep -rq "health" "$PROJECT_DIR/app/" "$PROJECT_DIR/src/" 2>/dev/null; then
  CHECKS="${CHECKS}forge-gate4: No health check endpoint detected.\n"
fi

# Check 4: .env in .gitignore
if [ -f "$PROJECT_DIR/.env" ]; then
  if ! grep -q "^\.env$" "$PROJECT_DIR/.gitignore" 2>/dev/null; then
    CHECKS="${CHECKS}forge-gate4: CRITICAL — .env file exists but may not be in .gitignore!\n"
  fi
fi

# Check 5: Secrets in code (quick scan)
SECRETS=$(grep -rn "sk-\|AKIA\|password.*=.*['\"]" "$PROJECT_DIR/app/" "$PROJECT_DIR/src/" 2>/dev/null | grep -v ".env" | grep -v "node_modules" | head -3)
if [ -n "$SECRETS" ]; then
  CHECKS="${CHECKS}forge-gate4: CRITICAL — possible hardcoded secrets detected!\n"
fi

if [ -n "$CHECKS" ]; then
  printf "$CHECKS"
fi

exit 0
