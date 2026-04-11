---
name: forge-fix
description: Execute the fix plan from /forge-scan — plans all fixes upfront, tracks progress with todo list, doesn't lose context when interrupted
tools: [Bash, Read, Write, Edit, Grep, Glob, Agent, TodoWrite]
---

# Forge Fix — Execute Fix Plan

Apply fixes identified by `/forge-scan`. Plans ALL fixes upfront, tracks them with a todo list, and works through them in priority order.

## Usage

`/forge-fix` — execute the fix plan (run /forge-scan first if no plan exists)
`/forge-fix [specific fix]` — jump to a specific fix

## CRITICAL RULE: Plan First, Then Execute

**Step 1: Check if /forge-scan was run this session.**
- If not, run /forge-scan first to get the fix plan.

**Step 2: Create a todo list with ALL fixes from the scan.**
Use TodoWrite to create the full plan. Example:
```
1. [pending] Fix: Add auth to 6 unprotected routes
2. [pending] Fix: Add input validation to 4 POST endpoints
3. [pending] Fix: Upgrade health check to verify DB/Redis
4. [pending] Fix: Add adversarial tests for auth bypass
5. [pending] Fix: Update 2 vulnerable dependencies
```

**Step 3: Work through fixes in order.**
- Mark current fix as `in_progress`
- Apply it
- Commit it
- Mark as `completed`
- Move to next fix

**Step 4: If the user asks an unrelated question — answer it, then come back.**
The todo list persists. After answering, say: "Back to forge-fix — we have X fixes remaining. Continuing with [next fix]?"

## Priority Order

Always fix in this order:

### Priority 1: CRITICAL (do these immediately)
1. **Secrets in code** — move to .env, update code to use env vars
   - WARN: "These were in git history. If repo is public, rotate keys NOW."
2. **.env not protected** — add to .gitignore, check if tracked
3. **Critical dependency vulnerabilities** — update packages

### Priority 2: ERROR VISIBILITY (safety net)
4. **Error handling** — add/upgrade global exception handler
   - Read the main app file, understand the framework
   - Don't just drop in a template — adapt it to existing code structure
   - Wire it properly (middleware registration, error boundary wrapping)
5. **Health check** — add or upgrade to deep health check
   - Check what dependencies exist (DB? Redis? External APIs?)
   - Health check should verify each one
6. **Structured logging** — add or upgrade
   - Replace print() statements with proper logging
   - Add request_id propagation if middleware exists

### Priority 3: SECURITY (hardening)
7. **Auth on unprotected routes** — ASK the user first
   - Show the list of unprotected routes
   - Ask: "Which of these should require auth? Any intentionally public?"
   - Don't blindly protect everything — some routes ARE public
8. **Input validation** — add to unvalidated endpoints
   - Read each endpoint, understand what it accepts
   - Create proper validation models (Pydantic/Zod) matching actual usage
   - Don't over-constrain — read existing code to understand valid inputs
9. **Rate limiting** — add to expensive endpoints
   - Identify: AI calls, auth endpoints, file uploads, webhooks
   - Ask: "Default is 10/min for AI, 5/min for auth. Adjust?"
10. **CORS** — restrict if wide open
    - Ask: "What origins should be allowed?"

### Priority 4: TESTING (verification)
11. **Tests** — write meaningful tests, not boilerplate
    - Read existing code to understand what the critical paths are
    - Write tests that test REAL scenarios, not just "endpoint returns 200"
    - Include at least 2 adversarial tests per critical endpoint
    - Ask: "Want me to run them?"
12. **CI improvements** — add missing stages

### Priority 5: ARCHITECTURE (long-term)
13. **Code duplication** — extract to shared modules
14. **Project context file** — create or improve

## How to Apply Each Fix

**Read before writing.** Don't just drop templates in. Understand the existing code:
- What framework? What patterns does the codebase already use?
- What dependencies are already installed?
- Where does the main app register middleware/routes?

**Adapt, don't copy-paste.** Templates are starting points. The fix should match the project's existing style, naming conventions, and structure.

**One commit per fix.** Commit message format: `forge: [category] description`
Examples:
- `forge: [security] add auth middleware to 6 unprotected routes`
- `forge: [error] upgrade health check to verify DB and Redis`
- `forge: [test] add adversarial tests for order endpoint`

**After each fix, show progress:**
```
Fix 3/5 complete: Upgraded health check to verify DB + Redis
Remaining:
  4. Add adversarial tests for auth bypass
  5. Update 2 vulnerable dependencies

Quality score: 3/5 → 4/5 (projected after remaining fixes)
Continue? (y/n)
```

## Rules

- **Always ask before auth decisions** — don't guess what should be public vs protected
- **Always ask before running tests** — user may not have dependencies installed
- **If user asks unrelated question** — answer it, then offer to continue: "Want to continue with forge-fix? X fixes remaining."
- **Don't bundle fixes** — one fix, one commit, one concern
- **Update the todo list** after each fix so progress is visible
- **If a fix fails or gets complicated** — stop, explain what went wrong, ask how to proceed. Don't hack around it.
