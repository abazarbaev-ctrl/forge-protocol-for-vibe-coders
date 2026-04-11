# Forge Protocol — Template Library

Reusable production patterns extracted from real projects rated 5/5 on the Forge Protocol quality scale.
Part of the [Forge Protocol](../FORGE_PROTOCOL.md) cross-project pattern transfer system.

---

## FastAPI Templates (Python)

| Template | What it does |
|----------|-------------|
| [error_middleware.py](fastapi/error_middleware.py) | 3-layer error handling: request context, null byte defense, error classification |
| [structured_logging.py](fastapi/structured_logging.py) | JSON logging with ContextVar request/user propagation |
| [auth_dependencies.py](fastapi/auth_dependencies.py) | Composable auth chain: get_user_id -> get_current_user -> require_active |
| [rate_limiter.py](fastapi/rate_limiter.py) | Per-user rate limiting via JWT extraction, IP fallback |
| [health_check.py](fastapi/health_check.py) | /health endpoint with DB, Redis, dependency status |
| [webhook_verification.py](fastapi/webhook_verification.py) | 4 patterns: HMAC (Stripe), shared secret, Meta verification, Telegram |
| [retry_client.py](fastapi/retry_client.py) | HTTP client with tenacity retry, token caching, 401 auto-refresh |
| [conftest.py](fastapi/conftest.py) | Pytest fixtures: auth client, auto-markers, token caching, TestState |
| [ci.yml](fastapi/ci.yml) | 3-stage CI: pytest -> smoke test -> security scan |
| [Dockerfile](fastapi/Dockerfile) | python:3.12-slim for Cloud Run |
| [docker-compose.yml](fastapi/docker-compose.yml) | Local dev: app + PostgreSQL + Redis with hot reload |

## Next.js Templates (TypeScript)

| Template | What it does |
|----------|-------------|
| [ErrorBoundary.tsx](nextjs/ErrorBoundary.tsx) | React error boundary with JSON logging and recovery UI |
| [GlobalErrorHandler.tsx](nextjs/GlobalErrorHandler.tsx) | Catches window.onerror + unhandled promise rejections |
| [middleware.ts](nextjs/middleware.ts) | Cookie-based role auth with regex route matching + telemetry |
| [telemetry.ts](nextjs/telemetry.ts) | Zero-dependency structured JSON logging for Vercel |
| [db-mock.ts](nextjs/db-mock.ts) | Prisma mock for vitest with per-test override |
| [vitest.config.ts](nextjs/vitest.config.ts) | Node env, path alias matching tsconfig |
| [ci.yml](nextjs/ci.yml) | CI: install -> prisma generate -> lint -> test -> build + security scan |

## Domain Attack Libraries (Framework-Agnostic)

| Domain | File | Key Attacks |
|--------|------|------------|
| Healthcare | [healthcare.md](attack-patterns/healthcare.md) | Medication interactions, prompt injection, HIPAA leakage, cross-tenant access |
| Restaurant/F&B | [restaurant-fb.md](attack-patterns/restaurant-fb.md) | Negative quantities, webhook spoofing, stop-list races, Telegram injection |
| Real Estate | [real-estate.md](attack-patterns/real-estate.md) | Triage prompt injection, cost manipulation, cross-tenant data, 1C integration |
| Education | [education.md](attack-patterns/education.md) | XP farming, mastery gaming, answer checker fuzzing, NaN/Infinity edges |
| Banking | [banking.md](attack-patterns/banking.md) | Threshold splitting, concurrent balance races, exchange rate drift, KYC bypass |

## Gate 5 CI Enforcement

| Template | What it does |
|----------|-------------|
| [weekly-review.yml](gate5/weekly-review.yml) | Creates GitHub issue every Monday with review template |
| [monthly-audit.yml](gate5/monthly-audit.yml) | Creates GitHub issue on 1st of month with cost audit template |
| [deploy-gate.yml](gate5/deploy-gate.yml) | Blocks deploys if review (>14d) or audit (>35d) is overdue |

---

## How to Use

1. **New FastAPI project:** Copy relevant templates to your `app/core/` directory. Adapt placeholders.
2. **New Next.js project:** Copy relevant templates to your `src/` directory. Adapt route patterns.
3. **Gate 3 testing:** Reference the domain attack library for your domain when writing adversarial tests.
4. **Gate 5 enforcement:** Copy all 3 gate5/*.yml files to `.github/workflows/`. Set deploy-gate as required check.
5. **New domain:** Use the Forge Protocol bootstrap prompt to generate a new attack library, then review and save here.

## Template Maintenance

- Templates are **upstream** — changes flow FROM here TO projects (one-way)
- When a project improves a pattern, update the template here for future projects
- Templates should be generic with PLACEHOLDER comments for project-specific adaptation
- Never put secrets, URLs, or project-specific config in templates
