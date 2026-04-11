---
name: forge-scan
description: Scan current project for production readiness — tests, error handling, auth, CI, secrets, health check. Shows quality score and top fixes.
tools: [Bash, Read, Grep, Glob]
---

# Forge Scan — Instant Project Health Check

Scan the current project and show what's missing for production readiness.

## Usage

`/forge-scan`

## What To Do

Run ALL checks below against the current project directory. Report results as a scorecard.

### Checks to Run

**1. Tests**
- Look for test directories: `tests/`, `test/`, `__tests__/`, `spec/`
- Count test files: `*.test.*`, `*_test.*`, `test_*.*`, `*_spec.*`
- Result: `X test files found` or `No tests found`

**2. Error Handling**
- Grep for global error handlers: `exception_handler`, `ErrorBoundary`, `window.onerror`, `app.use(err`, `@app.exception_handler`, `process.on('uncaughtException'`
- Result: `Global error handler found` or `No global error handler`

**3. Auth / Access Control**
- Grep for auth patterns: `authenticate`, `authorization`, `Bearer`, `verify_token`, `requireAuth`, `middleware.*auth`, `get_current_user`, `isAuthenticated`
- Result: `Auth middleware found` or `No auth middleware detected`

**4. Health Check**
- Grep for health endpoint: `/health`, `healthcheck`, `health_check`
- Result: `Health check endpoint found` or `No health check endpoint`

**5. CI Pipeline**
- Check for: `.github/workflows/*.yml`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/config.yml`
- Result: `CI pipeline found (GitHub Actions)` or `No CI pipeline`

**6. Secrets in Code (CRITICAL)**
- Grep source files (NOT .env, NOT node_modules, NOT .git) for:
  - `sk-` (OpenAI/Anthropic keys)
  - `AKIA` (AWS keys)
  - Patterns like `password = "`, `secret = "`, `api_key = "`
- Result: `No hardcoded secrets found` or `CRITICAL: X potential hardcoded secrets`

**7. .env Protection**
- Check if `.env` file exists AND is listed in `.gitignore`
- Result: `.env protected by .gitignore` or `CRITICAL: .env not in .gitignore` or `No .env file`

**8. Structured Logging**
- Grep for: `structlog`, `json_logger`, `winston`, `pino`, `logEvent`, `logging.config`
- Result: `Structured logging found` or `No structured logging`

**9. Input Validation**
- Grep for: `Pydantic`, `BaseModel`, `zod`, `joi`, `yup`, `class-validator`, `validate`
- Result: `Input validation found` or `No input validation detected`

**10. Rate Limiting**
- Grep for: `rate_limit`, `rateLimit`, `slowapi`, `express-rate-limit`, `throttle`
- Result: `Rate limiting found` or `No rate limiting`

### Scoring

Count green checks:
- 9-10: **5/5** — Production ready
- 7-8: **4/5** — Almost there
- 5-6: **3/5** — Safety net in place, needs hardening
- 3-4: **2/5** — Basic structure, significant gaps
- 0-2: **1/5** — Vibe coded, needs full upgrade

### Output Format

Present results as a clean scorecard:

```
Forge Protocol Scan — [project name]
═════════════════════════════════════
  Tests:              12 test files              ✓
  Error handling:     Global handler found       ✓
  Auth:               No auth middleware         ✗
  Health check:       /health endpoint found     ✓
  CI pipeline:        GitHub Actions             ✓
  Secrets in code:    None found                 ✓
  .env protection:    In .gitignore              ✓
  Structured logging: Not found                  ✗
  Input validation:   Pydantic models found      ✓
  Rate limiting:      Not found                  ✗

  Quality score: 3/5 (7/10 checks passed)

  Top 3 fixes (highest impact, lowest effort):
  1. Add structured logging — copy templates/fastapi/structured_logging.py
  2. Add auth middleware — copy templates/fastapi/auth_dependencies.py
  3. Add rate limiting — copy templates/fastapi/rate_limiter.py

  Run /forge-fix to apply these fixes one at a time.
```

Also suggest a README badge:
```
![Forge Quality](https://img.shields.io/badge/forge_quality-3%2F5-yellow)
```

Badge colors:
- 5/5: `brightgreen`
- 4/5: `green`
- 3/5: `yellow`
- 2/5: `orange`
- 1/5: `red`
