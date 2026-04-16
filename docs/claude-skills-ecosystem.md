# Claude Skills Ecosystem — A Reference for Vibe Coders

A curated catalog of Claude Code skills relevant to building production software with AI tools. Companion resource to the [Forge Protocol](../FORGE_PROTOCOL.md).

---

## What Is a Claude Skill?

A skill is a folder containing a `SKILL.md` file that tells Claude exactly how to perform a specific type of work: step-by-step process, constraints, examples, and any helper scripts or templates.

Instead of re-explaining your process every session, you install the process once as a skill and reuse it forever. The Forge Protocol itself ships as a plugin with four skills (`forge`, `forge-scan`, `forge-fix`, `forge-review`).

### Install format

```
npx skills@latest add <author>/<repo>/<skill-name>
```

### Key repositories

| Source | URL |
|--------|-----|
| Official Anthropic skills | https://github.com/anthropics/skills |
| Matt Pocock skills (popular) | https://github.com/mattpocock/skills |
| Superpowers (engineering suite) | https://github.com/obra/superpowers |
| Awesome Claude Skills | https://github.com/ComposioHQ/awesome-claude-skills |
| Community marketplace | https://skillsmp.com |

---

## Catalog by Category

### Meta — Building and Managing Skills

| Skill | Purpose | Source |
|-------|---------|--------|
| Skill Creator | Benchmarks Claude on your task, then drafts and iterates new skills based on real runs | `anthropics/skills/skill-creator` |
| Write a Skill | Guides Claude to write new skills with proper structure and progressive disclosure | `mattpocock/skills/write-a-skill` |
| Find Skills | Searches public marketplaces for matching skills | skillsmp.com |

### Planning and Design

| Skill | Purpose | Source |
|-------|---------|--------|
| Grill Me | Forces relentless clarifying questions, one at a time, until every branch is resolved | `mattpocock/skills/grill-me` |
| Write a PRD | Creates a PRD through interactive interview, codebase exploration, and module design | `mattpocock/skills/write-a-prd` |
| PRD to Plan | Turns a PRD into a multi-phase plan using tracer-bullet vertical slices | `mattpocock/skills/prd-to-plan` |
| PRD to Issues | Breaks a PRD into independently-grabbable GitHub issues with blocking relationships | `mattpocock/skills/prd-to-issues` |
| Design an Interface | Generates 3-5 competing interface designs via parallel sub-agents | `mattpocock/skills/design-an-interface` |
| Request Refactor Plan | Detailed refactor plan with tiny commits via user interview, filed as GitHub issue | `mattpocock/skills/request-refactor-plan` |
| Brainstorming | Turns raw feature ideas into detailed flows using Socratic questioning | `obra/superpowers/skills/brainstorming` |

### Code Development

| Skill | Purpose | Source |
|-------|---------|--------|
| TDD | Strict test-first, red-green-refactor loop for features and bug fixes | `mattpocock/skills/tdd` |
| Triage Issue | Investigates a bug, identifies root cause, files an issue with TDD-based fix plan | `mattpocock/skills/triage-issue` |
| QA | Runs a full QA pass with issue breakdown including blocking relationships | `mattpocock/skills/qa` |
| Improve Codebase Architecture | Surfaces refactor opportunities, focused on deepening shallow modules | `mattpocock/skills/improve-codebase-architecture` |
| Systematic Debugging | 4-phase methodology that forbids "just try changing stuff" edits | `obra/superpowers/skills/systematic-debugging` |
| Code Review | Systematic review for security, performance, error handling, architecture | `anthropics/skills` |
| Auto-Commit Messages | Reads staged diff, generates conventional commit messages | `anthropics/skills/auto-commit` |
| Simplification Cascade | Identifies convoluted logic and rewrites it as smaller, composable pieces | mcpmarket.com |
| React Best Practices | Enforces Vercel/Next.js best practices in React code | `vercel-labs/agent-skills/skills/react-best-practices` |
| File Search | Teaches Claude to use ripgrep and ast-grep to navigate large codebases fast | `massgen/massgen` |
| Context Optimization | Reduces context size and token bills | `muratcankoylan/agent-skills-for-context-engineering` |
| Migrate to Shoehorn | Migrates TypeScript test `as` assertions to `@total-typescript/shoehorn` | `mattpocock/skills/migrate-to-shoehorn` |
| Scaffold Exercises | Creates exercise directory structures for course/onboarding content | `mattpocock/skills/scaffold-exercises` |

### Tooling and Repo Setup

| Skill | Purpose | Source |
|-------|---------|--------|
| Setup Pre-Commit | Husky + lint-staged + Prettier + type checking + tests | `mattpocock/skills/setup-pre-commit` |
| Git Guardrails for Claude Code | Blocks dangerous git commands (push, reset --hard, clean) before they execute | `mattpocock/skills/git-guardrails-claude-code` |
| Dependency Auditor | Scans `package.json` for outdated, vulnerable, or abandoned packages | `ComposioHQ/awesome-claude-skills/dependency-auditor` |
| Git Work Trees | Manages safe feature development on isolated branches | community |

### Project Management

| Skill | Purpose | Source |
|-------|---------|--------|
| GitHub Triage | Triages incoming issues with agent brief + out-of-scope rules | `mattpocock/skills/github-triage` |
| Change Log Generator | Reads commits, produces human or developer-focused change logs | `ComposioHQ/awesome-claude-skills/changelog-generator` |

### Writing and Knowledge

| Skill | Purpose | Source |
|-------|---------|--------|
| Edit Article | Restructures sections, cuts filler, sharpens arguments — not just grammar | `mattpocock/skills/edit-article` |
| Ubiquitous Language | Extracts a DDD-style glossary from the current conversation | `mattpocock/skills/ubiquitous-language` |
| API Documentation Generator | Generates OpenAPI/Swagger docs from your routes with examples and auth requirements | `ComposioHQ/awesome-claude-skills/api-docs-generator` |
| Content Researcher | Learns your style, drafts long-form blogs with real citations | `ComposioHQ/awesome-claude-skills/content-research-writer` |
| Obsidian Vault | Searches, creates, manages notes with wikilinks and index notes | `mattpocock/skills/obsidian-vault` |

### UI / Frontend / Design

| Skill | Purpose | Source |
|-------|---------|--------|
| Frontend Design | Guides Claude to produce modern, clean UI | `anthropics/skills/frontend-design` |
| Theme Factory | Generates complete color palettes from a single text prompt | `anthropics/skills/theme-factory` |
| Canvas Design | Turns text into social media graphics, posters, covers | `anthropics/skills/canvas-design` |
| Web Artifacts Builder | Builds interactive dashboards and calculators from natural language | `anthropics/skills/web-artifacts-builder` |
| Algorithmic Art | p5.js for generative visuals | `anthropics/skills/algorithmic-art` |
| Brand Guidelines | Enforces brand system across new components | `anthropics/skills/brand-guidelines` |
| Awesome Design | Markdown templates inspired by Notion/Figma to structure UI thinking | `VoltAgent/awesome-design-md` |

### Business / Sales / Marketing

| Skill | Purpose | Source |
|-------|---------|--------|
| Stripe Integration | Sets up secure payment flows, webhooks, subscriptions without rookie API mistakes | `wshobson/agents/payment-processing/skills/stripe-integration` |
| Domain Name Brainstormer | Generates product names and checks domain availability | `Microck/ordinary-claude-skills/domain-name-brainstormer` |
| Lead Research Assistant | Finds target companies and decision-makers based on ICP | `ComposioHQ/awesome-claude-skills/lead-research-assistant` |
| Marketing Skills | 20+ skills for CRO, copywriting, email flows | `coreyhaines31/marketingskills` |
| Claude SEO | Full technical SEO audit, schema, on-page optimization | `AgriciDaniel/claude-seo` |
| YouTube Idea Mining | Scrapes comments, competitor videos, niche trends into weekly idea bank | `AgriciDaniel/claude-youtube` |

### Media Generation

| Skill | Purpose | Source |
|-------|---------|--------|
| Nano Banana Pro | Photo-quality image generation | `feedtailor/ccskill-nanobanana` |
| Nano Banana 2 | Photo-quality image generation v2 | `kingbootoshi/nano-banana-2-skill` |
| Local Image Gen | Local Python script for avatars and icons | `jezweb/claude-skills/design-assets` |
| Image Optimizer | Resizes and converts images to WebP | mcpmarket.com |
| Remotion Best Practices | Programmatic video and motion graphics | `remotion-dev/remotion` |
| Video Toolkit | Scripted video animations | `wilwaldon/Claude-Code-Video-Toolkit` |

### Office and Documents

| Skill | Purpose | Source |
|-------|---------|--------|
| PDF Processing | Extracts tables, fills forms, merges PDFs | `anthropics/skills/pdf` |
| DOCX | Edits Word docs with tracked changes | `anthropics/skills/docx` |
| PPTX | Creates and edits slide decks | `anthropics/skills/pptx` |
| XLSX | Writes formulas, pivot tables, charts from plain English | `anthropics/skills/xlsx` |
| Excel MCP Server | Manipulates Excel files via MCP, no desktop Excel required | `haris-musa/excel-mcp-server` |
| Doc Co-Authoring | Real-time collaborative writing | `anthropics/skills/doc-coauthoring` |
| NotebookLM Integration | Bridges Claude with Google's NotebookLM | `PleasePrompto/notebooklm-skill` |
| Google Workspace | Automates Calendar, Drive, Docs | `googleworkspace/cli` |

### Multi-Agent and Web

| Skill | Purpose | Source |
|-------|---------|--------|
| Stochastic Multi-Agent Consensus | Spawns many sub-agents on the same problem, aggregates answers | `hungv47/meta-skills` |
| Model-Chat (Debate) | Puts multiple Claude instances into a debate to stress-test ideas | `tommasinigiovanni/conclave` |
| Playwright CLI | Real browser control for UI regression and funnel walkthroughs | `microsoft/playwright` |
| Firecrawl | Scrapes structured data from hostile or complex sites | `mendableai/firecrawl` |
| Custom YT Search | Searches and analyzes YouTube content autonomously | `ZeroPointRepo/youtube-skills` |

### Engineering Bundle

| Skill | Purpose | Source |
|-------|---------|--------|
| Superpowers | Battle-tested suite for TDD, debugging, refactoring, execution | `obra/superpowers` |

---

## Relevance to the Forge Protocol

The Forge Protocol ships with four skills (`forge`, `forge-scan`, `forge-fix`, `forge-review`). External skills can reinforce each gate. Mapping below.

### Gate 0 — Spec

| External Skill | Why It Helps |
|----------------|--------------|
| **Grill Me** | Same adversarial questioning posture as Gate 0. Use as a drop-in for the "What should this NOT do?" interview. |
| **Write a PRD** | Turns Gate 0 conversation into a durable artifact. Useful for Medium/Large features. |
| **Brainstorming** (Superpowers) | Pre-Gate-0 exploration when the feature isn't crisp yet. |
| **Ubiquitous Language** | Surfaces domain glossary before code is written — directly supports "tag every assumption". |

### Gate 1 — Build

| External Skill | Why It Helps |
|----------------|--------------|
| **TDD** | Aligns with Gate 1 step 3 ("Write the success criteria test(s) from Gate 0 first"). |
| **PRD to Plan** | Converts Gate 0 spec into ordered build steps for Large features. |
| **PRD to Issues** | Useful when Gate 1 needs to fan out across parallel agents (Gate 1.5). |
| **React Best Practices** | Reinforces Next.js templates in `templates/nextjs/`. |
| **File Search** | Speeds up Gate 1 step 1 (reading CLAUDE.md and finding template matches). |

### Gate 2 — Review

| External Skill | Why It Helps |
|----------------|--------------|
| **Code Review** (Anthropic) | Adds structured security/performance/architecture passes alongside Forge's review. |
| **Improve Codebase Architecture** | Catches "shallow modules" — extends the duplication and drift checks. |
| **Simplification Cascade** | Targets convoluted logic. Useful when Gate 2 finds something fixable but ugly. |

### Gate 3 — Test

| External Skill | Why It Helps |
|----------------|--------------|
| **TDD** | Same loop as Gate 3 but enforces red-green-refactor explicitly. |
| **QA** | Adds blocking-relationship breakdown for the issues Gate 3 surfaces. |
| **Systematic Debugging** | When Gate 3 tests fail and the cause isn't obvious, this prevents random-edit debugging. |
| **Triage Issue** | For bugs that surface post-Gate-3 in production. |
| **Playwright CLI** | Adds real-browser regression checks for Next.js features. |

### Gate 4 — Ship

| External Skill | Why It Helps |
|----------------|--------------|
| **Setup Pre-Commit** | Bolts Husky onto the pre-commit shell scripts in `scripts/pre-commit-check.sh`. |
| **Git Guardrails for Claude Code** | Blocks dangerous git commands during any gate — pairs naturally with the existing `PreToolUse` hook for `Bash`. |
| **Dependency Auditor** | Adds outdated/vulnerable package scan to the existing secret scan. |
| **Auto-Commit Messages** | Useful when Gate 4 produces multiple ship commits. |
| **Stripe Integration** | If the project handles payments, this enforces secure webhook + subscription patterns. |

### Gate 5 — Learn

| External Skill | Why It Helps |
|----------------|--------------|
| **Triage Issue** | Routes telemetry-discovered bugs into a TDD fix plan. |
| **GitHub Triage** | Processes the weekly review backlog when issues pile up. |
| **Change Log Generator** | Useful for Gate 5 weekly reviews — summarizes what shipped. |
| **Stochastic Multi-Agent Consensus** | For the "should we keep or kill this feature" decisions in weekly review. |

---

## Recommended Install Order for This Project

If you maintain or contribute to the Forge Protocol repo itself:

1. **Write a Skill** — for evolving the four shipped skills
   ```
   npx skills@latest add mattpocock/skills/write-a-skill
   ```
2. **Edit Article** — `FORGE_PROTOCOL.md` is 37 KB; this skill restructures and tightens
   ```
   npx skills@latest add mattpocock/skills/edit-article
   ```
3. **Auto-Commit Messages** — for the development branch convention
   ```
   npx skills@latest add anthropics/skills/auto-commit
   ```
4. **GitHub Triage** — once the public repo accumulates issues
   ```
   npx skills@latest add mattpocock/skills/github-triage
   ```
5. **Git Guardrails** — repo safety while editing the plugin
   ```
   npx skills@latest add mattpocock/skills/git-guardrails-claude-code
   ```

If you are a vibe coder using Forge Protocol on your own project:

1. **Grill Me** + **Write a PRD** — pre-Gate-0
2. **TDD** — backbone for Gate 1 + Gate 3
3. **Setup Pre-Commit** + **Git Guardrails** — one-time per repo, Gate 4 hardening
4. **Triage Issue** + **Systematic Debugging** — when production breaks
5. **Superpowers** — install last as your default engineering layer

---

## Source

Catalog adapted from a community post on Claude skills (April 2026). Skill descriptions and install commands belong to their original authors and repositories. Verify install paths against each repo's README before use.
