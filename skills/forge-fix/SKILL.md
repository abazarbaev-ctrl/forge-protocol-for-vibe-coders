---
name: forge-fix
description: Execute the fix plan from /forge-scan — plans all fixes upfront, tracks progress with todo list, doesn't lose context when interrupted
tools: [Bash, Read, Write, Edit, Grep, Glob, Agent, TodoWrite]
---

# Forge Fix — Execute Fix Plan

Apply fixes identified by `/forge-scan`. Plans ALL fixes upfront, tracks them with a todo list, and works through them in priority order.

**IMPORTANT: NEVER output markdown images, shields.io badges, or any `![...]()` syntax. Quality score is text only.**

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

### Priority 4: LLM OPTIMIZATION (cost + reliability + migration)

**CRITICAL RULE: Every LLM fix requires explicit user approval.** These changes affect model behavior and costs. Explain what you're doing and why before each change. No silent fixes.

11. **Cost controls** — add safeguards to unprotected LLM calls
   - For each LLM call without max_tokens: explain what it does, what a reasonable limit is, and why
   - Add cost logging if none exists — show the user: "This logs token counts per call so you can see where money goes"
   - ASK: "These X calls have no token limit. Here's what I'd set for each — adjust?"

12. **Reliability** — add timeouts, retry, validation
   - For each LLM call without timeout: "This call to [model] in [file] has no timeout. If the API hangs, your user waits forever. I'd add a 30s timeout — OK?"
   - For calls without retry: "If this fails, it fails silently. I'd add retry with exponential backoff (3 attempts, 1s/2s/4s). OK?"
   - For calls without response validation: "This passes the LLM response directly to [next step] without checking it. If the model returns empty or malformed output, [consequence]. I'd add validation — OK?"

13. **Model tier optimization** — downgrade where possible
   - For each call using an expensive model on a simple task:
     - Show the user: "This uses [Opus/GPT-4] to [simple task]. Here's what the prompt does: [explain]. Haiku/GPT-4o-mini handles this — it's ~20x cheaper."
     - Show a concrete cost comparison: "Currently ~$X/1K calls → ~$Y/1K calls"
     - ASK: "Want me to switch this to [cheaper model]? We can always revert."
   - NEVER downgrade without showing the user what the call does

14. **Prompt efficiency** — reduce token waste
   - For each bloated prompt: show the user the current prompt length vs what it could be
   - If prompt caching isn't used: "Your system prompt is [X] tokens and sent every call. With prompt caching, repeat calls cost 90% less. Want me to add it?"
   - ASK before changing any prompt — prompt changes affect output quality

15. **Deterministic migration** — replace LLM calls with code
   **This is the highest-impact, highest-risk fix. Full transparency required.**
   For each migration candidate identified in the scan:
   - **Explain the current behavior:** "This function calls [model] to [do X]. It receives [input type] and returns [output type]."
   - **Show why it's a candidate:** "Looking at the code, this is doing [classification/extraction/formatting] which follows a predictable pattern. [Explain the pattern]."
   - **Propose the replacement:** "I'd replace this with [rules engine / parser / lookup table / string template]. Here's what the code would look like: [show pseudocode]."
   - **Explain the risks:** "If input doesn't match expected patterns, the deterministic version will [fail/return default]. The LLM would have handled this gracefully."
   - **Propose the safe migration path:**
     1. "First, I'll write the deterministic version alongside the LLM call"
     2. "Add logging that compares both outputs (shadow mode)"
     3. "After you verify agreement is high enough, we switch over"
     4. "Keep the LLM call as fallback for edge cases"
   - ASK: "Want me to proceed with this migration? We can start with shadow mode so nothing changes in production."
   - ONE migration at a time. Never batch these.

16. **Process leak safeguards** — prevent hanging LLM tasks
   - For each background LLM task without timeout: "This async call to [model] in [file] could hang indefinitely, holding [resource]. I'd add a [timeout]s ceiling."
   - ASK before adding — some background tasks are intentionally long-running

### Priority 5: TESTING (verification)
17. **Tests** — write meaningful tests, not boilerplate
    - Read existing code to understand what the critical paths are
    - Write tests that test REAL scenarios, not just "endpoint returns 200"
    - Include at least 2 adversarial tests per critical endpoint
    - Ask: "Want me to run them?"
18. **CI improvements** — add missing stages

### Priority 6: ARCHITECTURE (long-term)
19. **Code duplication** — extract to shared modules
20. **Project context file** — create or improve

## How to Apply Each Fix

**State the success criteria first.** Before applying a fix, write down the test that will prove it's fixed:
- "This fix is done when: test `test_X` passes (currently fails)"
- For non-testable fixes (docs, config, infra): state the observable check ("fix is done when `curl /health` returns 200 and includes DB status")
- If you can't state a criterion, the fix is probably not well-defined — pause and clarify

**Test-first for bug fixes.** For any SECURITY, ERROR, or bug-class fix:
1. Write the regression test first
2. Run it — confirm it fails for the right reason
3. Apply the fix
4. Re-run — confirm it passes
5. Commit both together

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

## Dependency Rules

These prevent the most common CI failures after forge-fix commits:

1. **When adding a new package:** verify the import works with the PINNED version, not whatever is installed locally. Run: `pip install package==<pinned_version> && python -c "import ..."` or equivalent. Local machine may have a different major version with a different API.

2. **When adding a linter to CI:** run it locally against the FULL codebase before committing the CI config. Fix all errors first, in the same commit. Don't push a linter that will immediately fail.

3. **When making pip-audit/npm-audit hard fail:** run the audit locally first. If there are CVEs, fix them in the same commit that enables hard fail. Don't enable hard fail and leave known vulnerabilities to break the next build.

4. **When pinning version ranges (>=X,<Y):** check that the import API is stable across the entire range. Major versions often break APIs. If the code uses v3+ API, don't allow v2 in the pin.

## Rules

- **Always ask before auth decisions** — don't guess what should be public vs protected
- **Always ask before running tests** — user may not have dependencies installed
- **If user asks unrelated question** — answer it, then offer to continue: "Want to continue with forge-fix? X fixes remaining."
- **Don't bundle fixes** — one fix, one commit, one concern
- **Update the todo list** after each fix so progress is visible
- **If a fix fails or gets complicated** — stop, explain what went wrong, ask how to proceed. Don't hack around it.
