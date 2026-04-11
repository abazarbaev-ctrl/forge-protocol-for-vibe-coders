# The Forge Protocol

**Version:** 1.4
**Date:** 2026-04-11
**Purpose:** A complete methodology for small teams and solo founders to systematically upgrade vibe-coded products to production quality — without hiring a dedicated engineering team.
**Origin:** Built through deep research, real-world application across 6 production projects, and adversarial self-review.

---

## Core Thesis

A non-technical founder or small team (1-3 people) using AI coding tools (Claude Code, Cursor, etc.) can build and maintain production-grade software for thousands of users — if they follow a structured protocol that compensates for what AI lacks: architectural context, adversarial thinking, and continuous feedback from real usage.

The Forge Protocol is that structure. Raw vibe code goes in. Production steel comes out.

**The methodology is tool-agnostic.** Prompts work with any capable LLM. Specific tooling (Claude Code features, CI pipelines) are optional accelerators, not requirements. If your AI tool has an outage, the protocol still works — you just move slower.

---

## Quick Reference (1-page cheat sheet)

**6 Gates:** SPEC → BUILD → REVIEW → TEST → SHIP → LEARN (→ back to SPEC)

| Gate | What | Solo founder action | Skip when |
|------|------|-------------------|-----------|
| 0. Spec | Adversarial spec review | "Find dead-end states, missing MUST NOTs, and role conflicts" | Hotfix (<20 lines) |
| 1. Build | Code with project context file | "Implement following BDD scenarios. Tag assumptions INFERRED/GAP" | Never |
| 2. Review | Adversarial code review | "List problems with severity. Don't suggest fixes" | Never |
| 3. Test | Break the code | "Write adversarial tests with [domain] attack patterns" | Never (but scope varies) |
| 4. Ship | Deploy with safety nets | Run CI checklist, verify rollback works | Never |
| 5. Learn | Telemetry → AI analysis → human approval | Weekly review template, monthly cost audit | Never (enforcement automated) |

**10 Rules:** (1) Never invent data — tag SOLID/INFERRED/GAP (2) Information barriers between agents (3) Reviewers: problems only, no solutions (4) 10/10 = red flag (5) Open questions need A/B/C options (6) Every finding has severity (7) Only BLOCKERs are GO/NO-GO (8) Never auto-split large specs (9) False positives expected 30-40% (10) Domain patterns are starting points

**Calibration:** Hotfix = skip Gate 0, existing tests only | Small = 1-round review | Medium = full 2-4 rounds | Large = full + strict mode + load test

**Cost cap:** ~$45/project/month across Gates 0+3+5. Alert if any gate exceeds 2x first-round cost.

**Rollback:** If a phase makes things worse → revert → investigate → adapt → re-apply (see Protocol Rollback section).

---

## The Problem the Forge Protocol Solves

| Metric | Value | Source |
|--------|-------|--------|
| AI-generated code vulnerability rate | ~40% contain critical vulnerabilities | Aikido, Wiz |
| Vibe-coded test coverage | 12% average (vs 68% traditional) | Beam/Gartner |
| Projects facing cancellation by 2028 | 40% of primarily AI-coded projects | Gartner |
| Code duplication increase | 4x without governance | Beam |
| Maintenance cost growth | 300% within first 18 months | Beam |
| AI code needing refactoring | 76% according to developers | Qodo |

**Root cause (academic):** The "flow-debt tradeoff" — the faster AI generates code, the more technical debt accumulates through architectural inconsistencies, security gaps, duplicate logic, and missing design rationale. (arXiv 2512.11922, Dec 2025)

**The 5 failure modes** (diagnostic checklist for existing vibe-coded projects):
1. **No architectural boundaries** — Module A change breaks module B. Fix: project context file with module boundaries.
2. **Test desert** — 12% coverage means 88% untested. Fix: Test-with-code mandate, build coverage gradually.
3. **Security by accident** — AI hardcodes keys, skips auth, trusts all input. Fix: Security checklist as CI gate.
4. **Duplicate logic** — AI generates fresh code for each request. 4x more duplication. Fix: Review focused on "does this already exist?"
5. **No error visibility** — Errors happen and nobody knows. Fix: Global error handlers + structured logging + alerting.

**The Forge Protocol's answer:** Don't slow down AI generation. Instead, run every output through adversarial gates that catch what AI misses — before it reaches users.

---

## The 6 Gates

```
Gate 0          Gate 1          Gate 2          Gate 3          Gate 4          Gate 5
SPEC            BUILD           REVIEW          TEST            SHIP            LEARN
────────────>────────────>────────────>────────────>────────────>────────────>
                                                                      │
                                                                      │ telemetry
                                                                      │ + AI analysis
                                                                      │ + human approval
                                                                      │
                                                            ┌─────────┘
                                                            │
                                                            ▼
                                                      Back to Gate 0
                                                    (next improvement cycle)
```

### Gate 0: Specification Validation

**What:** Adversarial review of requirements BEFORE any code is written.
**Why:** The highest-leverage quality intervention.

**How it works:**

1. **Builder agent** creates BDD scenarios (Given/When/Then), state transition tables, domain glossary, and coverage maps. Tags every item: SOLID (spec says it), INFERRED (spec implies it), GAP (spec is silent).

2. **Mandatory MUST NOT sections** on every scenario — what the system must NOT do. Missing prohibitions block progression.

3. **Validator agent** attacks Builder's artifacts across 7 categories: dead-end states, role conflicts, timing collisions, escalation chain breaks, missing functional areas, scenario gaps, open questions.

4. **Information barrier:** Validator never sees Builder's reasoning — only artifacts. Prevents confirmation bias.

5. **Iterate 2-8 rounds** with delta tracking. Early stop when no new findings emerge.

**Solo founder prompt:**
> "Review this spec adversarially. Find dead-end states, missing MUST NOTs, role conflicts, and timing collisions. Tag every assumption as SOLID, INFERRED, or GAP."

**Output:** BDD scenarios with MUST NOTs, state tables, glossary, coverage map, verdict (READY / NEEDS_WORK / NOT_READY).

**Tooling:** Any AI coding tool that supports multi-turn conversation (Claude Code, Cursor, etc.)

### Gate 1: Implementation

**What:** Code written with full architectural context.
**Why:** AI without context generates random code. AI with a project context file generates code that fits your system.

**How it works:**

1. **Project context file** constrains every AI session: architecture decisions (and WHY), module boundaries, coupling rules, test requirements, security requirements, quality scores. (Claude Code: `CLAUDE.md`, Cursor: `.cursorrules`, GitHub Copilot: `.github/copilot-instructions.md`)

2. **Follow BDD scenarios from Gate 0** — implementation traces directly to validated specs.

3. **Confidence tagging on code:**
   - SOLID: Directly implements a stated requirement with tests
   - INFERRED: Handles an implied case (error handling, edge cases)
   - GAP: AI made assumptions about behavior — needs human review

4. **Module isolation:** Low coupling, high cohesion. Each module can be developed and tested independently. (This enables Gate 1.5 below.)

**Solo founder prompt:**
> "Implement feature X following the BDD scenarios in the spec and the architecture in the project context file. Tag any assumptions as INFERRED. Flag anything where the spec is silent as GAP."

**Gate 1.5: Parallel Agent Development (for complex features)**

For large features, split work across isolated agents — each handles one module with its own project context. A coordinator agent ensures modules integrate correctly.

**Coordinator agent responsibilities:**
1. **Interface contract validation** — Verify that module A's output type matches module B's expected input type
2. **Integration test generation** — Write tests that exercise the boundaries between modules
3. **Dependency conflict detection** — Flag when two modules import conflicting versions or make incompatible assumptions
4. **Merge sequencing** — Determine the order modules should be integrated (leaf modules first, then composites)

This enables parallel development with coordination, not sequential monolith building.

### Gate 2: Code Review

**What:** Adversarial review of the implementation.
**Why:** The same AI that wrote code will approve its own code. You need a separate review perspective.

**How it works:**

1. **Reviewer agent** checks:
   - **Duplication audit** (primary check — vibe code averages 4x duplication): "Does this logic already exist elsewhere? Can it be extracted to a shared module?"
   - Pattern breaks against project context file architecture rules
   - Security gaps (auth, validation, input sanitization)
   - Architectural drift from module boundaries
   - INFERRED/GAP items from Gate 1 that need human decision

2. **Cognitive rules apply:**
   - 10/10 PASS is a red flag — the review wasn't adversarial enough
   - Reviewer never suggests solutions — only identifies problems
   - False positives (30-40%) are expected and acceptable

3. **Structural checks:** Cyclomatic complexity < 15/function, nesting depth < 4, duplication < 3%.

**Solo founder prompt:**
> "Review this code for duplication, security gaps, architectural consistency, and anything tagged INFERRED or GAP. Don't suggest fixes — just list problems with severity."

### Gate 3: Adversarial Testing

**What:** Tests designed to BREAK the code, not confirm it works.
**Why:** Happy-path tests miss the attacks that real users (and real attackers) will attempt.

**How it works:**

1. **Structural tests:** Response format, required fields, status codes.
2. **Adversarial tests:** Domain-specific attack patterns (see attack libraries below).
3. **Semantic tests:** For AI-powered features, use an LLM as evaluator — "Is this output medically accurate?" not just "Does it return 200?"
4. **Performance tests:** Ramping load, sustained load, error recovery.

**Semantic test example (Python/pytest):**
```python
import os

def test_triage_urgency_is_medically_reasonable(client, llm_client):
    """Semantic test: AI evaluates whether triage output makes clinical sense."""
    r = client.post("/api/triage", json={
        "description": "Прорыв трубы горячей воды, затопление квартиры снизу"
    })
    assert r.status_code == 200
    result = r.json()["result"]

    # Structural assertions (traditional)
    assert result["urgency"] in ["Аварийная", "Срочная", "Плановая", "Косметическая"]

    # Semantic assertion (LLM-evaluated — any capable model works)
    evaluation = llm_client.messages.create(
        model=os.environ.get("EVAL_MODEL", "claude-sonnet-4-5-20250514"),
        max_tokens=200,
        messages=[{"role": "user", "content": f"""
            A maintenance triage system classified this request:
            Description: "Burst hot water pipe, flooding apartment below"
            Urgency assigned: {result['urgency']}
            Category: {result['category']}

            Is this classification reasonable? Answer PASS or FAIL with one sentence why.
        """}]
    )
    verdict = evaluation.content[0].text
    assert "PASS" in verdict, f"Semantic check failed: {verdict}"
```

**Key rule:** Run semantic tests minimum 3 times (AI output is non-deterministic). A test passes only if it passes all 3 runs.

**Domain-specific attack libraries:**

| Domain | Key Attacks |
|--------|------------|
| Healthcare | Medication interactions, wrong-patient data, HIPAA-violating logs, diagnosis prompt injection, clinical safety traps |
| Restaurant/F&B | Negative quantities, webhook spoofing (Telegram/WhatsApp/iiko), stop-list manipulation, Telegram markdown injection |
| Real Estate | Triage prompt injection, tenant data cross-contamination, cost estimate manipulation, cross-tenant data leakage in error responses |
| Education | XP farming, mastery gaming, answer checker fuzzing, grade manipulation, NaN/Infinity edge cases |
| Banking | Threshold splitting, KYC interruption, concurrent balance races, exchange rate drift |

**Bootstrapping a new domain's attack library:**

When starting a project in a domain not listed above, generate the attack library first:

> "I'm building [product description] in the [domain] industry. Generate a domain-specific adversarial attack library with 15+ attack vectors grouped by: (1) data integrity attacks, (2) auth/access bypass, (3) injection attacks, (4) business logic abuse, (5) information leakage. For each attack, give: name, description, example payload, and expected safe behavior. Save as `tests/attack_patterns/[domain].md`."

Review the generated library before using it — LLMs may miss domain-specific attacks that require insider knowledge. Add attacks as you discover them in production (Gate 5 feeds back here).

**Solo founder prompt:**
> "Write adversarial tests for this feature. Try to break it with: injection attacks, boundary values, type confusion, race conditions, and [domain]-specific attack patterns. Run minimum 3 times for AI-powered features."

### Gate 4: Ship

**What:** Deployment with safety nets.
**Why:** Code that passes all gates can still fail in production due to infrastructure, configuration, or scale issues.

**Checklist:**
- [ ] CI/CD pipeline runs lint → test → scan → build on every push
- [ ] Secret scanning (GitLeaks) blocks commits with exposed credentials
- [ ] Dependency scanning (npm audit / pip-audit) flags known CVEs
- [ ] Rollback procedure tested — can roll back in < 5 minutes
- [ ] Global error handlers catch uncaught exceptions (frontend + backend)
- [ ] Structured logging routes to aggregation (Cloud Logging, Vercel Logs)
- [ ] Monitoring alerts on error rate spikes
- [ ] Health check endpoint responds correctly
- [ ] Webhook signature verification on all external event receivers
- [ ] Database backup verified before migration (for projects with real databases)

**Verdict before shipping:**

| Verdict | Criteria | Action |
|---------|----------|--------|
| READY | Zero blockers, zero dead-end states, <3 high-severity findings | Ship it |
| NEEDS_WORK | Zero blockers but dead-ends exist or 3+ high findings | Fix and re-review |
| NOT_READY | Any blocker exists | Stop. Fix blockers first. |

### Gate 5: Continuous Intelligence (the Feedback Loop)

**What:** Telemetry from real usage → AI analysis → improvement suggestions → human approval → back to Gate 0.
**Why:** Production-ready code is a snapshot. Production code that gets better is a system.

**How it works:**

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐     ┌──────────────┐
│  TELEMETRY   │────>│  AI ANALYSIS     │────>│  SUGGESTIONS    │────>│  HUMAN       │
│              │     │                  │     │                 │     │  APPROVAL    │
│ Usage events │     │ Pattern detection│     │ Ranked by       │     │              │
│ Error rates  │     │ Drop-off points  │     │ impact + effort │     │ Approve /    │
│ Performance  │     │ Feature adoption │     │ With tradeoffs  │     │ Reject /     │
│ User flows   │     │ Error clustering │     │ (A/B/C options) │     │ Defer        │
│ AI token cost│     │ Cost anomalies   │     │                 │     │              │
└─────────────┘     └──────────────────┘     └─────────────────┘     └──────────────┘
                                                                            │
                                                                    Approved items
                                                                    go to Gate 0
                                                                    (new spec cycle)
```

**What to track:**
- **Usage:** Page views, feature adoption, user flows, session duration, drop-off points
- **Errors:** Error rates by endpoint/component, error clustering, new-vs-recurring
- **Performance:** Response times (p50/p95/p99), AI token consumption, infrastructure costs
- **Business:** Conversion rates, retention, feature engagement

**AI analysis cadence:**
- **Daily:** Error clustering + anomaly detection (automated)
- **Weekly:** Usage pattern analysis + improvement suggestions (AI-generated, human-reviewed)
- **Monthly:** Cost audit + architecture review prompt

**Enforcement mechanism:** Gate 5 is the only gate that can be skipped by inaction. Human willpower against deadline pressure doesn't work. Automate the enforcement:

1. **Automated trigger:** GitHub Action on `schedule: cron: '0 10 * * 1'` creates an issue or commits a review template file. This makes the review visible and trackable.
2. **CI deploy gate:** The deploy pipeline checks for a `FORGE_WEEKLY_REVIEW` artifact/commit dated within the last 14 days. If missing, the deploy step fails with: "Forge Protocol: weekly review overdue. Complete the review before shipping." This removes willpower from the equation — the machine says no.
3. **Monthly cost audit:** Same mechanism — CI checks for `FORGE_MONTHLY_AUDIT` artifact within last 35 days. Block deploys if missing.

**Weekly Review Template:**

> **FORGE WEEKLY REVIEW — [Project Name] — Week of [Date]**
>
> Input data: [paste or link to telemetry dashboard / logs]
>
> Answer these 6 questions:
> 1. **Dead features:** Which features had <5% engagement this week? Should they be removed, redesigned, or promoted?
> 2. **Error clusters:** Group this week's errors by root cause. Which cluster affects the most users?
> 3. **Performance:** Any endpoint where p95 > 2x last week's p95? Any AI token cost increase > 20%?
> 4. **User friction:** Where do users drop off or retry? What's the #1 friction point?
> 5. **Security:** Any new vulnerability scanner findings? Any suspicious access patterns?
> 6. **Top improvement:** What single change would have the highest impact for the lowest effort? Present as A/B/C with tradeoffs.
>
> Format: Table with finding, severity, recommended action, effort estimate.

**Monthly Cost Audit Template:**

> **FORGE MONTHLY AUDIT — [Project Name] — [Month]**
>
> 1. **AI token spend** this month vs last month (absolute + per-user)
> 2. **Infrastructure cost** (hosting, DB, CDN, monitoring)
> 3. **Cost per active user** trend (rising = investigate, flat = healthy)
> 4. **Gate cost breakdown:** How much did Gates 0/3/5 cost in AI tokens this month?
> 5. **Optimization opportunities:** Any AI calls that could be cached, batched, or eliminated?

---

## The 10 Cognitive Rules

These rules prevent known AI failure patterns. They apply at EVERY gate:

1. **Never invent data.** Tag every assumption: SOLID / INFERRED / GAP.
2. **Reasoning doesn't cross barriers.** Only artifacts pass between agents.
3. **Reviewers never suggest solutions.** Only identify problems.
4. **10/10 PASS is a red flag.** Perfect scores mean insufficient adversarial pressure.
5. **Every open question needs options.** A/B/C with tradeoffs, not just "unclear."
6. **Every finding has severity.** BLOCKER / HIGH / MEDIUM / LOW.
7. **Only blockers are GO/NO-GO.** Everything else is prioritization.
8. **Never auto-split large specs.** Cross-sectional findings disappear through fragmentation.
9. **False positives are expected (30-40%).** Missing real bugs > flagging non-issues.
10. **Domain patterns are starting points.** Best findings come from unexpected angles.

---

## The Security Tiers

### Tier 0 — Before first user
- [ ] `.gitignore` excludes `.env`, credentials, keys
- [ ] Secrets in environment variables, not code
- [ ] Authentication via established provider (Firebase, Auth0), not DIY
- [ ] HTTPS everywhere
- [ ] Basic input validation on all endpoints

### Tier 1 — Before paying users
- [ ] CI/CD with SAST scanning (Semgrep)
- [ ] Dependency vulnerability scanning
- [ ] Rate limiting on expensive endpoints (AI, auth, file upload)
- [ ] Content Security Policy headers
- [ ] Error monitoring (Sentry or structured logging)
- [ ] Secret scanning on every commit (GitLeaks)
- [ ] Webhook signature verification on all external receivers
- [ ] Data isolation between tenants/users (no cross-contamination in queries, logs, or error messages)
- [ ] PII exclusion from logs (no phone numbers, emails, names in structured logs unless explicitly needed)

### Tier 2 — Before scale (1000+ users)
- [ ] Container security (non-root, updated base images)
- [ ] Cloud posture management
- [ ] WAF (Web Application Firewall)
- [ ] Penetration testing (manual or automated)
- [ ] LLM-specific testing (prompt injection, data exfiltration)
- [ ] Separate cloud accounts for dev/staging/prod
- [ ] Budget alerts for cloud spend
- [ ] Load testing at 2x expected peak

---

## Mandatory Project Memory

Every project gets a project context file that contains:
1. Architecture decisions and **WHY** they were made
2. Module boundaries and coupling rules
3. Test requirements (what must be tested, what gates apply)
4. Security requirements (auth, validation, rate limits)
5. Deployment checklist
6. Quality scores (current state, tracked over time)
7. Domain-specific attack patterns reference

Your AI coding tool reads this file at the start of every session. It constrains the AI to work within your architecture instead of generating random code.

---

## Cross-Project Pattern Transfer

The Forge Protocol is designed for a portfolio, not a single project. Patterns proven in one project become templates for all:

**Two layers of templates:**

1. **Framework-agnostic patterns** (transfer to ANY stack — Go, Rust, Flutter, etc.):
   - 10 cognitive rules
   - BDD scenario format with MUST NOT sections
   - Domain-specific attack pattern libraries (markdown files)
   - CI pipeline structure (lint → test → scan → build)
   - Gate calibration rules (see below)
   - Weekly/monthly review templates
   - Quality scoring rubric

2. **Framework-specific implementations:**
   - **FastAPI** (Python): Error middleware, auth dependencies, structlog setup, rate limiting, webhook verification, pytest fixtures, CI, Docker
   - **Next.js** (TypeScript): ErrorBoundary, middleware auth, vitest config, Prisma mocking, telemetry module, CI

**Transfer mechanism:** Central template library → adapted copies applied to each project. See `templates/README.md` for the full index.

| Category | Templates | Count |
|----------|-----------|-------|
| FastAPI (Python) | Error middleware, structured logging, auth, rate limiting, health check, webhook verification, retry client, conftest, CI, Dockerfile, docker-compose | 11 |
| Next.js (TypeScript) | ErrorBoundary, GlobalErrorHandler, middleware auth, telemetry, Prisma mock, vitest config, CI | 7 |
| Attack patterns | Healthcare, Restaurant/F&B, Real Estate, Education, Banking | 5 |
| Gate 5 enforcement | Weekly review, monthly audit, deploy gate | 3 |

---

## Origin: How the Forge Protocol Was Built

The Forge Protocol was born from running an AI venture studio — building multiple production products across healthcare, restaurant tech, real estate, and education using AI coding tools.

After watching the same failure patterns repeat across projects (missing error handling, zero tests, duplicate logic, security gaps), it became clear that AI-generated code needed a structured adversarial process — not slower generation, but systematic quality gates after generation.

The protocol combines established software engineering methodologies with practical lessons from shipping real products:

| Foundation | How It's Used in the Forge Protocol |
|-----------|-------------------------------------|
| BDD (Behavior-Driven Development) | Gate 0: BDD as one of four artifacts (scenarios, state tables, glossary, coverage map) |
| Adversarial validation | Gates 0-4: Gate-specific adversarial agents with information barriers and cognitive rules |
| Module isolation (low coupling, high cohesion) | Gate 1: Modular monolith — isolation without microservices operational overhead |
| TDD (Test-Driven Development) | Gate 3: TDD as foundation, expanded with adversarial attacks, semantic tests, domain-specific attack libraries |
| Telemetry feedback loops | Gate 5: Elevated from nice-to-have to enforced core gate with CI automation |

**What makes this different from standard methodologies:**
1. Adversarial thinking at every gate, not just testing
2. 10 cognitive rules preventing known AI failure modes
3. Confidence tagging (SOLID/INFERRED/GAP) making assumption debt visible
4. Domain-specific attack libraries for adversarial testing
5. Cross-project pattern transfer (portfolio thinking)
6. Gate calibration (scale gate depth to change size)
7. Cost control for AI-powered gates
8. Protocol rollback procedure

---

## Practical Upgrade Path (per project)

### Phase 0: Spec Hardening (0.5-1 day)
1. Write BDD scenarios for core features
2. Add MUST NOT sections to each scenario
3. Tag existing assumptions as SOLID / INFERRED / GAP
4. Review state transitions — find dead-end states

### Phase 1: Safety Net (1-2 days)
1. Global error handlers (frontend + backend)
2. Structured logging (JSON → Cloud Logging / Vercel)
3. CI pipeline (lint → test → build on every push)

### Phase 2: Test Foundation (2-3 days)
1. Unit tests for core business logic (pure functions first)
2. Adversarial tests with domain-specific attack patterns
3. Smoke tests for critical user flows
4. Semantic tests for AI-powered features

### Phase 3: Security Hardening (1-2 days)
1. Auth on all protected endpoints
2. Input validation on all inputs
3. Rate limiting on expensive operations
4. Secret scanning + dependency scanning in CI
5. Webhook signature verification

### Phase 4: Production Polish (1-2 days)
1. Performance baselines (load testing at 2x expected peak)
2. Deployment scripts with health checks
3. Rollback procedure tested
4. Monitoring dashboard

### Phase 5: Telemetry Loop (0.5-1 day setup, then ongoing)
1. Instrument key user flows with structured events
2. Set up weekly AI analysis prompt
3. Create improvement backlog from first analysis
4. Establish human approval cadence

**How this maps to the 6 Gates (for existing code):**
The upgrade path IS the 6 gates applied retroactively to code that already exists. Phase 0 = Gate 0 on existing code (spec what you already built). Phase 1 = Gate 4 prerequisites (safety nets). Phase 2 = Gate 3 (testing what already exists). Phase 3 = security items from Gate 4 checklist. Phase 4 = remaining Gate 4 items. Phase 5 = Gate 5 setup. For NEW features on an upgraded project, use the gates forward: Gate 0 → 1 → 2 → 3 → 4 → 5.

**Total: ~8-12 days per project for initial upgrade. Ongoing improvement via Gate 5.**

*Note (INFERRED):* This estimate is based on applying the protocol to multiple real production projects across healthcare, restaurant tech, real estate, and education domains. Actual time depends on codebase size, existing test coverage, number of external integrations, and domain complexity. Budget 50% contingency for projects with more than 10 external API integrations or legacy code without documentation.

---

## Tools Stack (Solo Founder, Free Tier)

| Need | Tool | Cost | When to upgrade |
|------|------|------|-----------------|
| CI/CD | GitHub Actions | Free | Never |
| SAST | Semgrep (open source) | Free | When you have a security team |
| Secret scanning | GitLeaks | Free | Never |
| Error monitoring | Sentry (5K events/mo) or structured logging | Free | When you hit 5K errors/month |
| Dependency scanning | npm audit / pip-audit | Free | When you need deeper analysis |
| Performance testing | k6 (open source) | Free | When you need cloud execution |
| Code quality | SonarQube Community | Free | When you need enterprise features |
| Monitoring | Vercel Analytics / Cloud Logging | Free | When you need custom dashboards |
| Spec validation | AI coding tool (built-in) | AI API cost | N/A |
| Telemetry analysis | Claude Code (manual prompt) | API cost | When you need automated scheduling |

---

## Gate Calibration

Not every change needs every gate at full intensity. Calibrate gate depth to change size:

| Change Size | Example | Gate 0 | Gate 1 | Gate 2 | Gate 3 | Gate 4 | Gate 5 |
|-------------|---------|--------|--------|--------|--------|--------|--------|
| **Hotfix** | Typo fix, CSS tweak, config change | Skip | Normal | Quick review | Run existing tests only | Normal | Weekly cadence (unchanged) |
| **Small feature** | New button, new field, simple endpoint | 1-round BDD review | Normal | Normal | Add tests for new code | Normal | Weekly cadence (unchanged) |
| **Medium feature** | New page, new integration, new API | Full 2-4 round review | Normal | Full review | Full adversarial suite | Normal | Weekly cadence (unchanged) |
| **Large feature** | New module, new service, architectural change | Full 4-8 rounds + strict mode | Gate 1.5 (parallel agents) | Full review + security focus | Full suite + performance tests | Full + load test | Weekly cadence (unchanged) |
| **New project** | Greenfield | Full + domain patterns | Full | Full | Full | Full | Setup from scratch |

**Criteria for sizing:**
- Hotfix: < 20 lines changed, no new logic, no new endpoints
- Small: < 100 lines, 1 new endpoint or component, no architectural impact
- Medium: 100-500 lines, new integration or user flow, touches 2+ modules
- Large: > 500 lines, new module boundary, changes data model, or affects auth/security

---

## Cost Control for AI-Powered Gates

Gates 0, 3, and 5 consume AI tokens. Without guardrails, costs can spike silently.

**Cost estimation pattern:**
1. After the first round of any AI-powered gate, calculate the token cost
2. Estimate remaining rounds: `remaining_cost = first_round_cost × remaining_rounds`
3. **Alert if** remaining cost exceeds 2x the first round cost
4. **Hard stop if** total gate cost exceeds a per-project budget cap

**Recommended budget caps (solo founder, per month):**

| Gate | Budget cap | Rationale |
|------|-----------|-----------|
| Gate 0 (Spec validation) | $20/project | 2-4 specs per month, ~$5-10 each |
| Gate 3 (Semantic tests) | $10/project | 3 runs × ~$1-3 per suite |
| Gate 5 (Weekly analysis) | $15/project | 4 weekly reviews × ~$2-4 each |
| **Total** | **$45/project/month** | Cap, not target — most months should be lower |

**How to track costs per gate:**
- **Anthropic API:** Use the `metadata` field on API calls to tag gate number and project name. Review in the Anthropic Console usage dashboard.
- **Claude Code CLI:** Check `~/.claude/usage/` after each session. Log the session cost with a note on which gate was running.
- **Simple fallback:** Maintain a spreadsheet — one row per gate invocation with date, project, gate, estimated tokens, and cost. Update monthly during the cost audit.

**Cost reduction tactics:**
- Cache Gate 0 results — re-validate only when spec changes, not on every build
- Use cheaper models (Haiku) for semantic test evaluation when Opus isn't needed
- Batch Gate 5 analysis across projects (one weekly review covering all projects)

---

## Protocol Rollback

If applying a phase of the Forge Protocol makes things worse (introduces bugs, blocks legitimate deploys, increases error rates), follow this rollback procedure:

1. **Detect:** Quality score drops after applying a phase, or CI gate blocks a legitimate change, or error rate increases post-deployment
2. **Isolate:** Identify which specific change caused the regression (git bisect or manual review)
3. **Revert:** Undo the phase that caused the regression (git revert, remove middleware, disable CI step)
4. **Investigate:** Understand WHY it regressed — was the template wrong, was the project incompatible, or was the application incorrect?
5. **Adapt:** Fix the template or the application approach, then re-apply with the fix
6. **Document:** Add the failure mode to the project context file so it's not repeated

**Common rollback scenarios:**
- Auth middleware blocks legitimate unauthenticated endpoints → Add exclusion list before re-applying
- CI gate too strict, blocks deploys on non-critical findings → Adjust thresholds (only blockers are GO/NO-GO)
- Error handler catches expected errors as crashes → Filter known-safe error types
- Rate limiter too aggressive for legitimate use patterns → Increase limits based on actual usage data

**Rule:** A rollback is not a failure of the protocol. It's the protocol working as intended — catching problems early and adapting.

---

## Protocol Versioning

The Forge Protocol evolves. Projects that reference it by file path (`FORGE_PROTOCOL.md`) automatically get the latest version. To manage this:

1. **Version tracking:** Each project's context file records the Forge Protocol version it was last audited against:
   ```markdown
   ## Forge Protocol
   Version applied: 1.1
   Last audit: 2026-04-11
   Reference: /path/to/FORGE_PROTOCOL.md
   ```

2. **Migration on version bump:** When the protocol version changes, each project needs a migration check. The changelog at the top of this file lists what changed between versions.

3. **Backwards compatibility:** New cognitive rules and gate additions are always additive. Existing projects don't break — they just gain new checks on next audit.

**Changelog:**
- **v1.0** (2026-04-11): Initial protocol — 6 gates, 10 cognitive rules, security tiers, practical upgrade path
- **v1.1** (2026-04-11): Added gate calibration, cost control, protocol rollback, bootstrap attack library, quick reference, enforcement mechanism for Gate 5, data isolation in Tier 1, semantic test example, framework-agnostic template layer, protocol versioning
- **v1.2** (2026-04-11): Added CI-automated Gate 5 enforcement (deploy block on overdue reviews), cost tracking mechanism, bootstrap prompt for new domain attack libraries, diagnostic failure modes checklist, clarified calibration table, env-var model name in semantic test example
- **v1.3** (2026-04-11): Connected upgrade path to 6 gates (retroactive application explained), added rollback to quick reference, elevated duplication audit as primary Gate 2 check, self-audited with Forge Protocol gates
- **v1.4** (2026-04-11): Template library created (26 files): 11 FastAPI templates, 7 Next.js templates, 5 domain attack libraries, 3 Gate 5 CI enforcement workflows. Extracted from production-rated golden sources. Closes all 3 implementation GAPs from v1.3 self-audit.

---

## Methodology Lineage

The Forge Protocol stands on established foundations:

| Foundation | Origin | Contribution |
|-----------|--------|-------------|
| BDD | Dan North, 2006 | Shared spec language (Given/When/Then) |
| Event Storming | Alberto Brandolini, 2013 | State transitions and domain event discovery |
| DDD | Eric Evans, 2003 | Bounded contexts, ubiquitous language |
| TDD | Kent Beck, 2003 | Test-first development for critical paths |
| Adversarial ML Testing | Industry, 2020s | Attack-based quality validation |
| Adversarial AI review | Industry practice, 2024-2025 | Using AI agents to review AI-generated artifacts |
| Flow-Debt Tradeoff | arXiv 2512.11922, Dec 2025 | Academic framework for AI technical debt |

---

## Sources

- [Vibe Coding in Practice: Flow, Technical Debt, and Guidelines (arXiv)](https://arxiv.org/abs/2512.11922)
- [AI Code Production Readiness Validation Framework (SoftwareSeni)](https://www.softwareseni.com/ensuring-ai-generated-code-is-production-ready-the-complete-validation-framework/)
- [The AI Technical Debt Crisis: 40% Cancellation Rate (Beam)](https://getbeam.dev/blog/ai-technical-debt-vibe-coding.html)
- [Vibe Coder's Security Checklist (Aikido)](https://www.aikido.dev/blog/vibe-check-the-vibe-coders-security-checklist)
- [How to Secure Your Vibe Coded App (Fencer)](https://www.fencer.dev/blog/how-to-secure-your-vibe-coded-app)
- [State of AI Code Quality 2025 (Qodo)](https://www.qodo.ai/reports/state-of-ai-code-quality/)
- [How AI Redefines Technical Debt (Sonar)](https://www.sonarsource.com/blog/how-ai-is-redefining-technical-debt)
- [Vibe Coding Best Practices (Softr)](https://www.softr.io/blog/vibe-coding-best-practices)
- [Secure Vibe Coding Guide (Cloud Security Alliance)](https://cloudsecurityalliance.org/blog/2025/04/09/secure-vibe-coding-guide)
- [Vibe Coding Security Fundamentals (Wiz)](https://www.wiz.io/academy/ai-security/vibe-coding-security)
