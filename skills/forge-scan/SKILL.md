---
name: forge-scan
description: Deep scan of current project for production readiness — analyzes code quality, not just keyword existence. Shows quality score and prioritized fix plan.
tools: [Bash, Read, Grep, Glob, Agent]
---

# Forge Scan — Deep Project Health Check

Analyze the current project's production readiness. Don't just check if things exist — assess their quality.

**IMPORTANT: NEVER output markdown images, shields.io badges, or any `![...]()` syntax. Quality score is text only.**

## Usage

`/forge-scan`

## How To Scan

Use Agent tool to run multiple checks in parallel where possible. Read actual code, not just grep for keywords.

### Category 1: CRITICAL SAFETY (blockers)

**1.1 Secrets in Code**
- Grep ALL source files (exclude .env, node_modules, .git, __pycache__) for:
  - API keys: `sk-`, `AKIA`, `AIza`
  - Hardcoded passwords: `password\s*=\s*["'](?!.*placeholder)`, `secret\s*=\s*["']`
  - Connection strings with credentials: `://\w+:\w+@`
- READ each match to verify it's a real secret (not a template placeholder, not a test fixture, not a comment)
- Result: count of REAL secrets with file:line references

**1.2 .env Protection**
- Check if `.env` exists AND is in `.gitignore`
- Check if `.env` is already tracked in git: `git ls-files .env`
- If tracked: CRITICAL even if in .gitignore (already in history)

**1.3 Dependency Vulnerabilities**
- If Python: run `pip-audit --desc 2>/dev/null` or check requirements.txt for known-bad versions
- If Node: run `npm audit --json 2>/dev/null` and parse severity counts
- Result: `X critical, Y high, Z moderate vulnerabilities` or `Clean`

### Category 2: ERROR VISIBILITY

**2.1 Error Handling — Depth Check**
- Find the main app file (main.py, app.py, index.ts, server.ts, app.ts)
- READ it — check if there's a global exception handler that:
  - Catches unhandled exceptions (not just specific routes)
  - Returns structured error responses (not stack traces to users)
  - Logs errors with context (request_id, user, endpoint)
- Grade: `None` / `Basic (catches errors)` / `Production (structured + logged + no leak)`

**2.2 Structured Logging — Depth Check**
- Don't just grep for `structlog` — READ the logging setup
- Check: Is it JSON format? Does it include request_id? Does it suppress PII?
- Check: Are print() statements used instead of proper logging? Count them.
- Grade: `None` / `print() statements (X found)` / `Basic logging` / `Structured JSON with context`

**2.3 Health Check — Depth Check**
- Find the health endpoint — READ it
- Does it just return 200, or does it actually check dependencies (DB, Redis, external APIs)?
- Grade: `None` / `Shallow (just returns OK)` / `Deep (checks dependencies)`

### Category 3: SECURITY

**3.1 Auth — Coverage Analysis**
- Find ALL route definitions (endpoints, pages, API routes)
- Find which ones have auth middleware/decorators
- Calculate: X of Y routes protected
- Flag unprotected routes that look sensitive (POST/PUT/DELETE, /admin, /api/*)
- Grade: `None` / `Partial (X/Y routes)` / `Full coverage`

**3.2 Input Validation — Coverage Analysis**
- Find ALL endpoints that accept request bodies (POST, PUT, PATCH)
- Check each: does it validate the input (Pydantic, Zod, joi, manual checks)?
- Calculate: X of Y endpoints validated
- Grade: `None` / `Partial (X/Y endpoints)` / `Full coverage`

**3.3 Rate Limiting**
- Check if rate limiting exists on expensive endpoints (AI calls, auth, file upload, webhooks)
- Grade: `None` / `Partial` / `On all expensive endpoints`

**3.4 CORS Configuration**
- Check if CORS is configured. If `allow_origins=["*"]` — flag as wide open.
- Grade: `None` / `Wide open (*)` / `Restricted`

### Category 4: TESTING

**4.1 Test Coverage — Quality Check**
- Count test files AND test functions/methods
- READ 2-3 test files — assess quality:
  - Are they just happy-path? Or do they test edge cases?
  - Do they test error conditions?
  - Are there any adversarial/security tests?
- Try to run tests if possible: `python3 -m pytest --co -q 2>/dev/null` or `npx vitest --list 2>/dev/null`
- Grade: `None` / `Minimal (X tests, happy path only)` / `Moderate (X tests, some edge cases)` / `Strong (X tests, adversarial included)`

**4.2 CI Pipeline — Quality Check**
- Find CI config — READ it
- Check what it actually does: just build? lint? test? security scan?
- Grade: `None` / `Build only` / `Build + test` / `Build + test + security scan`

### Category 5: LLM EFFICIENCY (for projects that call LLMs)

Skip this category if the project doesn't make LLM/AI API calls. If it does, this is a deep analysis.

**5.1 Find All LLM Calls**
- Grep for SDK imports: `anthropic`, `openai`, `google.generativeai`, `cohere`, `together`
- Grep for API endpoints: `api.anthropic.com`, `api.openai.com`, `generativelanguage.googleapis.com`
- Grep for common wrappers: `langchain`, `litellm`, `instructor`, `llamaindex`
- For each call found, READ the surrounding code to understand: what it sends, what model, what it does with the response
- Result: list of LLM calls with file:line, model used, and purpose

**5.2 Cost Controls**
- Does each LLM call have a `max_tokens` / `max_completion_tokens` limit?
- Is there a per-request or per-user cost cap? (middleware, rate limit, or manual check)
- Is there any cost tracking/logging? (token counts logged, cost per call calculated)
- Are token counts visible anywhere? (dashboard, logs, alerts)
- Grade: `None` / `Partial (limits but no tracking)` / `Full (limits + tracking + alerts)`

**5.3 Reliability**
- Does each LLM call have a timeout? (httpx timeout, client timeout, asyncio.wait_for)
- Is there retry with backoff? (tenacity, exponential backoff, manual retry)
- Is there a fallback? (try model A, fall back to model B)
- Are responses validated before use? (check for empty, check for expected format, Pydantic parse)
- Are LLM calls fire-and-forget with no error handling? Count them.
- Grade: `None` / `Basic (timeouts only)` / `Resilient (timeout + retry + validation)` / `Production (+ fallback + error handling)`

**5.4 Prompt Efficiency**
- READ each prompt/system message — is it bloated? (repeating instructions, sending full context when summary would work)
- Is prompt caching used? (Anthropic cache_control, OpenAI cached prompts)
- Are there hardcoded few-shot examples that could be a fine-tuned model or lookup?
- Is the model tier appropriate? (using Opus/GPT-4 for simple extraction/classification that Haiku/GPT-4o-mini handles)
- Grade: `Wasteful` / `Reasonable` / `Optimized (right model + caching + lean prompts)`

**5.5 Migration Candidates — Deterministic Replacement Analysis**
This is the most valuable check. For EACH LLM call, assess:
- **Is the output predictable?** If 90%+ of outputs follow the same pattern, it's a rules engine, not an LLM task.
  - Classification into fixed categories → lookup table / if-else / regex
  - Extracting structured data from structured input → parsing
  - Formatting/templating → string templates
  - Simple Q&A from known data → database query
- **Is the LLM doing work the database could do?** Filtering, sorting, matching on known fields.
- **Is the LLM a glorified if-else?** Decision trees with <10 branches don't need AI.
- Flag each LLM call as: `Keep (genuinely needs LLM)` / `Candidate (could be deterministic)` / `Obvious (should definitely be deterministic)`
- For each candidate/obvious, note what the deterministic replacement would be
- Grade: `No LLM calls` / `All necessary` / `X of Y calls are migration candidates` / `X of Y calls are obvious replacements`

**5.6 Process Leaks**
- Are there background LLM tasks (async, threads, workers) that could hang?
- Is there a timeout on background AI processing?
- Could a stuck LLM call hold a database connection or lock?
- Grade: `No background LLM` / `Background with safeguards` / `Background without safeguards`

### Category 6: ARCHITECTURE

**6.1 Code Duplication**
- Use Agent to check: are there functions/classes that do the same thing in multiple files?
- Look for copy-pasted error handling, repeated API calls, duplicate validation logic
- Grade: `Low` / `Moderate (examples found)` / `High (systematic duplication)`

**6.2 Project Context File**
- Check for CLAUDE.md, .cursorrules, or .github/copilot-instructions.md
- If exists, READ it — does it have architecture decisions, module boundaries, quality score?
- Grade: `None` / `Exists but shallow` / `Comprehensive`

### Scoring

Calculate from grades across all checks:

| Score | Criteria |
|-------|----------|
| **5/5** | Zero criticals, all categories at top grade, adversarial tests exist |
| **4/5** | Zero criticals, most categories covered, moderate+ testing |
| **3/5** | Zero criticals, error handling + CI + basic tests in place |
| **2/5** | No critical secrets exposed, but major gaps in 2+ categories |
| **1/5** | Critical issues exist OR 3+ categories completely missing |

### Output Format

```
Forge Protocol Scan — [project name]
═══════════════════════════════════════════════════════════

CRITICAL SAFETY
  Secrets in code:      None found                          ✓
  .env protection:      In .gitignore, not tracked          ✓
  Dependencies:         2 moderate vulnerabilities          ⚠

ERROR VISIBILITY
  Error handling:       Production (structured + logged)    ✓
  Logging:              Structured JSON with context        ✓
  Health check:         Shallow (just returns OK)           ⚠

SECURITY
  Auth coverage:        12/18 routes protected              ⚠
    Unprotected: POST /api/orders, DELETE /api/sessions, ...
  Input validation:     5/9 POST endpoints validated        ⚠
  Rate limiting:        On AI endpoints only                ⚠
  CORS:                 Restricted to 2 origins             ✓

TESTING
  Tests:                34 tests (happy path + some edges)  ⚠
  CI pipeline:          Build + test + security scan        ✓

LLM EFFICIENCY (if applicable)
  LLM calls found:     8 calls across 4 files               —
  Cost controls:        max_tokens set, no tracking          ⚠
  Reliability:          Timeouts on 5/8, no retry            ⚠
  Prompt efficiency:    Opus used for classification         ⚠
  Migration candidates: 3/8 calls could be deterministic    ⚠
    → classify_urgency(): regex/rules would cover 95%
    → extract_fields(): structured input, use parsing
    → format_response(): string template
  Process leaks:        1 background task without timeout    ⚠

ARCHITECTURE
  Code duplication:     Low                                 ✓
  Project context file: Comprehensive CLAUDE.md             ✓

Quality score: 3/5
═══════════════════════════════════════════════════════════

Fix plan (priority order):
1. [SECURITY] Add auth to 6 unprotected routes
2. [SECURITY] Add input validation to 4 POST endpoints
3. [ERROR] Upgrade health check to verify DB/Redis
4. [LLM] Add cost tracking + timeouts to 3 unprotected calls
5. [LLM] Migrate classify_urgency() to rules engine
6. [TEST] Add adversarial tests for auth bypass, injection
7. [DEPS] Update 2 vulnerable dependencies

Run /forge-fix to execute this plan.
```
