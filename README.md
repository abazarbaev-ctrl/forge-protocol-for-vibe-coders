# The Forge Protocol

**A quality methodology for solo founders and small teams shipping production software with AI coding tools.**

---

## The Problem

AI coding tools (Claude Code, Cursor, Copilot) let non-technical founders build software fast. But speed without structure creates a specific kind of debt:

| Metric | Value | Source |
|--------|-------|--------|
| AI-generated code with critical vulnerabilities | ~40% | Aikido, Wiz |
| Average test coverage in vibe-coded projects | 12% | Beam/Gartner |
| AI-coded projects facing cancellation by 2028 | 40% | Gartner |
| Code duplication vs traditional development | 4x | Beam |
| Code needing refactoring according to developers | 76% | Qodo |

The root cause is the **flow-debt tradeoff** (arXiv 2512.11922): the faster AI generates code, the more technical debt accumulates through architectural inconsistencies, security gaps, duplicate logic, and missing design rationale.

## The Solution

Don't slow down AI generation. Instead, run every output through **adversarial gates** that catch what AI misses — before it reaches users.

```
Gate 0          Gate 1          Gate 2          Gate 3          Gate 4          Gate 5
SPEC            BUILD           REVIEW          TEST            SHIP            LEARN
──────────>──────────>──────────>──────────>──────────>──────────>
                                                                     │
                                                                     │ telemetry
                                                                     │ + AI analysis
                                                                     │ + human approval
                                                                     │
                                                               Back to Gate 0
```

| Gate | What You Do | Time |
|------|------------|------|
| **0. Spec** | AI reviews your idea adversarially — finds dead-end states, missing rules, edge cases | 15-30 min |
| **1. Build** | AI writes code with architectural context (project context file) following validated specs | Normal dev time |
| **2. Review** | Separate AI review focused on duplication, security, architectural drift | 10-20 min |
| **3. Test** | AI writes tests designed to BREAK the code using domain-specific attack patterns | 30-60 min |
| **4. Ship** | Deploy with safety nets — CI, error handlers, health checks, rollback plan | 15-30 min |
| **5. Learn** | Weekly: AI analyzes production telemetry, suggests improvements, you approve/reject | 30 min/week |

## What's Inside

### The Protocol

[`FORGE_PROTOCOL.md`](FORGE_PROTOCOL.md) — the complete methodology:
- 6 gates with prompts you can copy-paste into any AI coding tool
- 10 cognitive rules that prevent known AI failure patterns
- Gate calibration (hotfix vs small vs medium vs large)
- Security tiers (before first user → before paying users → before scale)
- Cost control for AI-powered gates (~$45/project/month cap)
- Protocol rollback procedure (when a gate makes things worse)

### Template Library

Ready-to-use production patterns extracted from real projects rated 5/5:

**FastAPI (Python)** — 11 templates
| Template | What It Does |
|----------|-------------|
| `error_middleware.py` | 3-layer error handling: request context, null byte defense, error classification |
| `structured_logging.py` | JSON logging with ContextVar request/user propagation |
| `auth_dependencies.py` | Composable auth chain: get_user_id → get_current_user → require_active |
| `rate_limiter.py` | Per-user rate limiting via JWT extraction, IP fallback |
| `health_check.py` | /health endpoint with DB, Redis, dependency status |
| `webhook_verification.py` | 4 patterns: HMAC (Stripe), shared secret, Meta, Telegram |
| `retry_client.py` | HTTP client with tenacity retry, token caching, 401 auto-refresh |
| `conftest.py` | Pytest fixtures: auth client, auto-markers, token caching |
| `ci.yml` | 3-stage CI: pytest → smoke test → security scan |
| `Dockerfile` | python:3.12-slim optimized for Cloud Run |
| `docker-compose.yml` | Local dev: app + PostgreSQL + Redis with hot reload |

**Next.js (TypeScript)** — 7 templates
| Template | What It Does |
|----------|-------------|
| `ErrorBoundary.tsx` | React error boundary with JSON logging and recovery UI |
| `GlobalErrorHandler.tsx` | Catches window.onerror + unhandled promise rejections |
| `middleware.ts` | Cookie-based role auth with regex route matching + telemetry |
| `telemetry.ts` | Zero-dependency structured JSON logging |
| `db-mock.ts` | Prisma mock for vitest with per-test override |
| `vitest.config.ts` | Node env, path alias matching tsconfig |
| `ci.yml` | CI: install → lint → test → build + security scan |

**Domain Attack Libraries** — 5 domains, ~20 attacks each
| Domain | Key Attacks |
|--------|------------|
| Healthcare | Medication interactions, prompt injection, HIPAA leakage, cross-tenant access |
| Restaurant/F&B | Negative quantities, webhook spoofing, stop-list races, injection |
| Real Estate | Triage prompt injection, cost manipulation, cross-tenant data leakage |
| Education | XP farming, mastery gaming, answer checker fuzzing, NaN/Infinity edges |
| Banking | Threshold splitting, concurrent balance races, exchange rate drift, KYC bypass |

**Gate 5 CI Enforcement** — 3 GitHub Actions workflows
| Template | What It Does |
|----------|-------------|
| `weekly-review.yml` | Creates review issue every Monday |
| `monthly-audit.yml` | Creates cost audit issue on 1st of month |
| `deploy-gate.yml` | Blocks deploys if reviews are overdue |

## Quick Start

### Claude Code (plugin — recommended)

```
/plugin marketplace add abazarbaev-ctrl/forge-protocol-for-vibe-coders
/plugin install forge-protocol
```

Two commands. Done. Then run:

```
/forge-scan
```

You'll see your project's health instantly:

```
Forge Protocol Scan — your-project
═════════════════════════════════════
  Tests:              No tests found             ✗
  Error handling:     No global handler          ✗
  Auth:               No auth middleware         ✗
  Health check:       Not found                  ✗
  CI pipeline:        Not found                  ✗
  Secrets in code:    2 hardcoded keys           ✗ CRITICAL
  .env protection:    Not in .gitignore          ✗ CRITICAL
  Structured logging: Not found                  ✗
  Input validation:   Pydantic models found      ✓
  Rate limiting:      Not found                  ✗

  Quality score: 1/5

  Run /forge-fix to start fixing — one fix at a time.
```

Then `/forge-fix` applies fixes one by one — each a single commit, highest priority first.

**What the plugin gives you:**

| Command | What it does |
|---------|-------------|
| `/forge-scan` | Instant project health check — shows what's missing |
| `/forge-fix` | Apply the next highest-priority fix (one at a time) |
| `/forge [feature]` | Build a feature with full gate sequence (spec → code → review → tests → ship) |
| `/forge-review` | Weekly review — errors, dead features, improvements |

Plus **automatic behavior**: Claude Code applies quality gates when you build, reviews its own code, writes adversarial tests, and nudges you before deploys. You don't invoke gates — they run around you.

### Any other AI coding tool (manual)

1. Read [`FORGE_PROTOCOL.md`](FORGE_PROTOCOL.md) — takes 15 minutes
2. Create a project context file in your repo root with architecture decisions, module boundaries, and quality score. This is the file your AI tool reads at the start of every session:
   - Claude Code: `CLAUDE.md`
   - Cursor: `.cursorrules`
   - GitHub Copilot: `.github/copilot-instructions.md`
3. Copy relevant templates from `templates/` to your project
4. Use the gate prompts from the protocol — one per gate, copy-paste into your AI tool

### For an existing vibe-coded project

**Claude Code:** Run `/forge-scan` then `/forge-fix` repeatedly until you hit your target score.

**Any tool:** Follow the **Practical Upgrade Path** in the protocol:

| Phase | What | Time |
|-------|------|------|
| 0. Spec Hardening | Write BDD scenarios with MUST NOT sections for core features | 0.5-1 day |
| 1. Safety Net | Global error handlers + structured logging + CI pipeline | 1-2 days |
| 2. Test Foundation | Unit tests + adversarial tests + domain attack patterns | 2-3 days |
| 3. Security Hardening | Auth + input validation + rate limiting + secret scanning | 1-2 days |
| 4. Production Polish | Performance baselines + deploy scripts + rollback testing | 1-2 days |
| 5. Telemetry Loop | Instrument user flows + weekly AI analysis + improvement backlog | 0.5-1 day setup |

**Total: ~8-12 days per project.** Budget 50% contingency for projects with many external integrations.

## The 10 Cognitive Rules

These prevent known AI failure patterns. They apply at every gate:

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

## Who This Is For

- **Solo founders** building SaaS with AI coding tools who want production quality without hiring an engineering team
- **Small teams (1-3 people)** using AI-assisted development who need a structured quality process
- **Technical leaders** looking for a methodology to govern AI-generated code across a portfolio

## Who This Is NOT For

- Teams with established CI/CD, code review, and testing culture — you already have this
- Projects where "move fast and break things" is the correct strategy (pre-PMF prototypes, hackathons)
- Organizations that need compliance-grade audit trails — this is a practitioner methodology, not a compliance framework

## Origin

The Forge Protocol was born from running an AI venture studio — building multiple production products across healthcare, restaurant tech, real estate, and education using AI coding tools.

After watching the same failure patterns repeat across projects (missing error handling, zero tests, duplicate logic, security gaps), it became clear that AI-generated code needed a structured adversarial process — not slower generation, but systematic quality gates after generation.

The protocol was built by combining established methodologies (BDD, TDD, DDD, adversarial ML testing) with practical lessons from shipping real products. It was then adversarially tested through 5 rounds and self-audited through its own 6 gates.

**Tested on a real portfolio:** 6 production projects — upgraded from average 3.2/5 to 3.8/5 quality score, with the two highest-rated projects at 5/5.

## Tool Agnostic

The methodology works with any AI coding tool. The prompts in the protocol are plain English — use them with Claude Code, Cursor, Copilot, Windsurf, or anything else.

The templates are framework-specific (FastAPI, Next.js) but the patterns they implement (error handling, auth, rate limiting, adversarial testing) apply to any stack. Port them to Go, Rust, Flutter, or whatever you're building with.

## Cost

The protocol itself is free. The AI gates (spec review, semantic testing, weekly analysis) consume AI tokens:

| Gate | Monthly Budget Cap | What It Covers |
|------|-------------------|----------------|
| Gate 0 (Spec) | ~$20/project | 2-4 spec reviews |
| Gate 3 (Tests) | ~$10/project | Semantic test evaluation |
| Gate 5 (Learn) | ~$15/project | 4 weekly reviews |
| **Total** | **~$45/project** | Cap, not target |

All other tools (CI, scanning, monitoring) use free tiers.

## Contributing

This is a living methodology. If you apply it to your projects and discover:
- A new domain attack pattern
- A failure mode the protocol doesn't catch
- A template for a framework not yet covered (Go, Rust, Flutter, Django, Rails)
- An improvement to the cognitive rules

Open an issue or PR.

## License

MIT — use it, adapt it, share it.

## Sources

- [Vibe Coding in Practice: Flow, Technical Debt, and Guidelines (arXiv)](https://arxiv.org/abs/2512.11922)
- [AI Code Production Readiness Framework (SoftwareSeni)](https://www.softwareseni.com/ensuring-ai-generated-code-is-production-ready-the-complete-validation-framework/)
- [The AI Technical Debt Crisis (Beam)](https://getbeam.dev/blog/ai-technical-debt-vibe-coding.html)
- [Vibe Coder's Security Checklist (Aikido)](https://www.aikido.dev/blog/vibe-check-the-vibe-coders-security-checklist)
- [State of AI Code Quality 2025 (Qodo)](https://www.qodo.ai/reports/state-of-ai-code-quality/)
- [How AI Redefines Technical Debt (Sonar)](https://www.sonarsource.com/blog/how-ai-is-redefining-technical-debt)
- [Secure Vibe Coding Guide (Cloud Security Alliance)](https://cloudsecurityalliance.org/blog/2025/04/09/secure-vibe-coding-guide)
- [Vibe Coding Security Fundamentals (Wiz)](https://www.wiz.io/academy/ai-security/vibe-coding-security)
