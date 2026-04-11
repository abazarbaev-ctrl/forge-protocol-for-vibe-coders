---
name: forge-fix
description: Apply the top fix from /forge-scan — one fix at a time, one commit per fix
tools: [Bash, Read, Write, Edit, Grep, Glob]
---

# Forge Fix — Apply One Fix at a Time

Apply the highest-impact fix identified by `/forge-scan`. Each run fixes ONE thing and commits it.

## Usage

`/forge-fix` — apply the next highest-priority fix
`/forge-fix [specific fix]` — apply a specific fix (e.g., `/forge-fix add health check`)

## Priority Order

Always fix in this order (critical safety issues first):

1. **CRITICAL: Secrets in code** — move to .env, add .env to .gitignore
2. **CRITICAL: .env not in .gitignore** — add it immediately
3. **Error handling** — add global error handler from templates
4. **Health check** — add /health endpoint from templates
5. **CI pipeline** — add GitHub Actions workflow from templates
6. **Structured logging** — add from templates
7. **Tests** — create test directory and initial test file
8. **Input validation** — add Pydantic/Zod models for existing endpoints
9. **Auth middleware** — add from templates (needs user input on auth provider)
10. **Rate limiting** — add from templates

## How to Apply Each Fix

### Fix: Secrets in code
1. Identify the hardcoded secrets
2. Create or update `.env` with the secrets as environment variables
3. Update code to use `os.environ.get()` or `process.env.`
4. Add `.env` to `.gitignore` if not already there
5. WARN the user: "These secrets are now in .env but they were already in git history. If this repo is public, rotate these keys immediately."

### Fix: .env not in .gitignore
1. Add `.env` and `.env.*` to `.gitignore`
2. That's it. One line, one commit.

### Fix: Error handling
1. Detect framework: FastAPI (look for `from fastapi`), Next.js (look for `next.config`), Express (look for `express()`)
2. Copy the matching template:
   - FastAPI: adapt `templates/fastapi/error_middleware.py`
   - Next.js: adapt `templates/nextjs/ErrorBoundary.tsx` + `templates/nextjs/GlobalErrorHandler.tsx`
3. Wire it into the app's main file
4. Adapt PLACEHOLDERs to match the project

### Fix: Health check
1. Detect framework
2. Copy and adapt `templates/fastapi/health_check.py` or equivalent
3. Register the route in the main app file

### Fix: CI pipeline
1. Detect framework and package manager
2. Copy matching template: `templates/fastapi/ci.yml` or `templates/nextjs/ci.yml`
3. Place in `.github/workflows/ci.yml`
4. Adapt: Python version, Node version, test commands

### Fix: Structured logging
1. Detect framework
2. Copy and adapt `templates/fastapi/structured_logging.py` or `templates/nextjs/telemetry.ts`
3. Wire into the app

### Fix: Tests
1. Create test directory (`tests/` for Python, `__tests__/` for JS)
2. Create a conftest/setup file from templates
3. Write 3-5 basic tests for existing routes/endpoints (health, main page, one API endpoint)
4. Ask: "Tests written. Want me to run them?"

### Fix: Input validation
1. For Python: add Pydantic models for request bodies on existing POST/PUT endpoints
2. For JS/TS: add Zod schemas for request validation
3. Wire validation into route handlers

### Fix: Auth middleware
1. Ask the user: "Which auth provider? Firebase / Auth0 / Supabase / custom JWT?"
2. Copy and adapt `templates/fastapi/auth_dependencies.py` or `templates/nextjs/middleware.ts`
3. Wire into the app — but DON'T apply to all routes automatically
4. Ask: "Which routes should require auth?"

### Fix: Rate limiting
1. Copy and adapt `templates/fastapi/rate_limiter.py`
2. Apply to expensive endpoints (AI calls, auth, file upload)
3. Ask: "Default is 10 requests/minute for AI endpoints. Adjust?"

## Rules

- **ONE fix per /forge-fix run.** Don't bundle.
- **ONE commit per fix.** Clean git history.
- **Ask before running tests** — user may not have dependencies installed.
- **Ask before auth decisions** — don't guess the auth provider.
- After applying, show updated score: "Quality score: 2/5 → 3/5. Run /forge-fix again for the next fix."
- Templates are in the plugin directory at `${CLAUDE_PLUGIN_ROOT}/templates/` — read from there.
