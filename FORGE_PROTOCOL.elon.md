# Forge Protocol: Elon Algorithm Pass

**Target:** `FORGE_PROTOCOL.md` v1.4 (637 lines, ~37KB)
**Verdict:** The protocol is real. The document is bloated, ceremonial, and self-congratulatory. Cut it in half and it gets sharper.

---

## TL;DR

1. **Delete Gate 0's "Builder agent vs Validator agent with information barrier across 2-8 rounds" ceremony.** A solo founder cannot run two-agent adversarial loops eight times before writing code. This is the single dumbest requirement in the document and it is the bottleneck to anyone actually using the protocol. Replace with one prompt, one pass, one verdict.
2. **The document repeats itself 4x.** Quick Reference, then 6 Gates section, then Practical Upgrade Path, then Gate Calibration table all teach the same gates. Pick one. Delete the other three.
3. **Most numeric claims have no owner and no source.** $45/project/month, 30-40% false positives, 2-8 rounds, 14-day review staleness, "minimum 3 runs" for semantic tests, $20/$10/$15 gate caps, "8-12 days per project." None measured. All asserted. Flag every number or measure it.

---

## Step 1: Requirements That Are Dumb

### Owner-less assertions

| Claim | Where | Owner | Verifiable basis |
|---|---|---|---|
| "$45/project/month across Gates 0+3+5" | line 37, 549 | None | None. Where's the spreadsheet? |
| "False positives expected 30-40%" | line 33, 158, 338 | None | No source cited |
| "Iterate 2-8 rounds" Gate 0 | line 100 | None | Why not 1? Why not 20? |
| "Run semantic tests minimum 3 times" | line 210 | None | Why 3? Statistical basis? |
| "Cyclomatic complexity < 15, nesting < 4, duplication < 3%" | line 161 | None | Borrowed from where? |
| "Alert if gate exceeds 2x first-round cost" | line 539 | None | Why 2x? |
| "Deploy fails if review > 14 days old" | line 295 | None | Why 14? |
| "Built through real-world application across 6 production projects" | line 6 | None | Which six? Names? |
| "8-12 days per project for initial upgrade" | line 489 | None | Already tagged INFERRED, but never measured |
| "10 cognitive rules" / "6 gates" / "5 failure modes" | throughout | None | Round numbers are a red flag. Reality rarely lands on 5 or 10. |

The protocol mandates `SOLID/INFERRED/GAP` tagging for the user's code. The protocol itself fails this test. **Audit the protocol against its own Rule #1.**

### Smart-person traps

- "BDD as foundation" (Dan North, 2006). Borrowed from a context (Java/Ruby teams of the late 2000s) that has nothing structurally in common with one founder pair-programming with an LLM. Does Given/When/Then actually catch what AI misses, or does it just feel rigorous? No evidence either way in the document.
- "Reviewers never suggest solutions, only identify problems." Asserted as cognitive rule #3. Why? When a reviewer knows the fix, hiding it costs the founder a round trip. This rule treats AI agents like junior humans whose ego must be protected. AI has no ego.
- "10/10 PASS is a red flag." Maybe. Or the diff was small. Conflating low finding count with low rigor is itself a bias.

### Rewrites for the weakest requirements

- **OLD:** "Iterate 2-8 rounds with delta tracking. Early stop when no new findings emerge."
  **NEW:** "Run one adversarial review pass. If it finds blockers, fix and re-run once. Stop. If you need a third pass your spec is fundamentally wrong, rewrite it."

- **OLD:** "Run semantic tests minimum 3 times (AI output is non-deterministic). A test passes only if it passes all 3 runs."
  **NEW:** "Run semantic tests with `temperature=0` and a fixed seed. Run once. If you must use temperature > 0, run 5 times and require pass rate >= 4/5. Three is an arbitrary number."

- **OLD:** "Total: ~8-12 days per project for initial upgrade."
  **NEW:** DELETE CANDIDATE. Until the studio publishes actual elapsed times from the six projects, this is a guess pretending to be a benchmark.

---

## Step 2: Delete

Apply the 10% add-back rule. If fewer than 1 in 10 of these would ever come back, the document was bloated.

1. **Tier 2 Security ("Before scale, 1000+ users")** lines 363-372. A solo founder at 1000+ users hires a security engineer. WAF, container security, separate cloud accounts, pen testing belong in a different document for a different reader. **What it would take to add back:** the protocol expands its audience to small teams with budget.

2. **Methodology Lineage table** lines 609-622. Lists Dan North 2006, Eric Evans 2003, Kent Beck 2003. Pure provenance theater. Zero behavior changes when the reader learns BDD's birthday. **Add back if:** an academic reviewer ever demands citations.

3. **Origin section** lines 420-444. "The Forge Protocol was born from running an AI venture studio." Self-promotional autobiography. The reader does not care how it was made. They care if it works. **Add back if:** the protocol gets a marketing site that needs founder narrative.

4. **Protocol Versioning section** lines 584-605. Five v1.x bumps all dated 2026-04-11. That is not versioning, that is one editing session. The whole section is aspirational scaffolding. **Add back if:** a real v2.0 ships and breaks compatibility.

5. **Cross-Project Pattern Transfer section** lines 390-417. The reader has one project. Telling them to think like a portfolio manager is wishful. **Add back if:** the document is restructured as a studio playbook, not a single-project protocol.

6. **Sources section** lines 625-636. Ten marketing-blog URLs from vendors selling AI security tools (Wiz, Aikido, Fencer, etc.). Each link makes the document look researched while actually citing ad copy. Keep only arXiv 2512.11922. Delete the rest.

7. **Cognitive Rule #9 ("False positives expected 30-40%")** line 338. This is not a rule. It is a built-in excuse for low precision. The actual number is unknown. Delete.

8. **Cognitive Rule #10 ("Domain patterns are starting points")** line 339. Tautological. Of course they are starting points. Says nothing.

9. **Repeated "Tooling: Any AI coding tool that supports multi-turn conversation"** appears or is implied at the end of every gate. State once at the top. Delete the rest.

10. **Phase 4 "load testing at 2x expected peak"** line 475. A solo founder with no users does not load test. Premature optimization. Move to a separate "post-product-market-fit" appendix.

11. **The 6 Gates ASCII diagram** lines 69-83. Redundant with the Quick Reference table on line 22 which says the same thing in less space.

12. **Tools Stack table** lines 495-509. Almost every row says "Free / Never upgrade." That is one sentence: "Use the free tier of GitHub Actions, Semgrep, GitLeaks, Sentry, k6, SonarQube. Upgrade nothing until you have revenue." Delete the table.

If the reader ever needs even three of these back, I deleted too few. I expect zero come back.

---

## Step 3: Simplify

### Three worst sections, rewritten

**Gate 5 ASCII flow diagram** lines 266-279. Six boxes, four arrows, ten lines. Replace with:

> Telemetry → weekly Claude prompt → ranked suggestions with A/B/C tradeoffs → founder approves, rejects, or defers → approved items become next cycle's specs.

**Cost Control section** lines 532-560. 28 lines to say four things:

> Tag every Claude API call with `metadata.gate` and `metadata.project`. Pull monthly spend from the Anthropic Console. If any gate exceeds last month's spend by 50%, investigate. Cap unknown.

That is the whole section. The Anthropic API supports metadata tagging natively. Stop telling the reader to keep a spreadsheet.

**The Quick Reference + 6 Gates + Practical Upgrade Path + Gate Calibration overlap** spans roughly 250 lines describing the same six gates four times. Collapse to:

> The six gates are: SPEC, BUILD, REVIEW, TEST, SHIP, LEARN. SPEC is adversarial review of requirements before code. BUILD is implementation with a project context file. REVIEW is adversarial code review. TEST is adversarial testing using domain attack patterns. SHIP is deployment with safety nets. LEARN is telemetry-driven feedback. Skip SPEC for hotfixes under 20 lines. Skip nothing else, ever.

Six sentences. The rest of the protocol is calibration knobs and prompt examples for those six.

### Specific vague language to replace

- "Multiple production projects" → name a count or delete the claim
- "Real-world application" → cite which projects, in what domain, with what outcome
- "AI coding tool" mentioned generically 12+ times → name two and stop hedging
- "Established provider" for auth → say "Firebase, Auth0, or Clerk"

---

## Step 4: Accelerate (the one bottleneck)

**The bottleneck is Gate 0 itself.**

Gate 0 is the prerequisite for every other gate. The document prescribes:
- Builder agent creates BDD scenarios + state tables + glossary + coverage map
- Validator agent attacks across 7 categories
- Information barrier between them
- 2-8 rounds of iteration
- Delta tracking

For a solo founder, this is unimplementable in a single day. Even with the `forge-review` skill in this repo, executing two agents with an information barrier and 2-8 rounds takes hours and consumes the AI budget that was supposed to last a month.

**Result:** founders skip Gate 0 entirely. Every subsequent gate then operates on an unvalidated spec, undoing the protocol's premise.

### Specific compressions that save weeks

1. **Single-prompt Gate 0.** Replace the two-agent ceremony with one Claude Code slash command (`/forge-spec`) that takes the spec and returns a verdict + ranked findings in one pass. Solo founder runs it in five minutes. If they want adversarial separation they can run it twice with different system prompts. Compresses Gate 0 from "half a day per spec" to "five minutes per spec." Across a month of typical spec changes (10-15 specs), saves 1-2 weeks.

2. **Default to "small feature" calibration.** The calibration table biases readers toward Medium and Large. Default everything to Small unless proven otherwise. Most changes are small. The protocol currently treats every change like a NASA launch.

3. **Drop the 14-day review enforcement gate.** It blocks deploys for hotfixes when the founder is on vacation. Replace with a soft warning. Saves the panic-deploy disaster the document is currently engineering.

The rest of the protocol can be slow if Gate 0 is fast. Optimize the constraint.

---

## Step 5: Automate

Only AFTER deleting and simplifying. Specific automations with named tools:

| Currently manual | Automate with | Why now |
|---|---|---|
| `SOLID / INFERRED / GAP` tagging in code | Pre-commit hook that greps changed files for `# INFERRED` / `# GAP` markers and fails commit if a function over 20 lines lacks confidence tags | Tagging is mandatory but unenforced. Founders skip it. A hook makes it impossible to skip. |
| Duplication audit (Gate 2 primary check) | `jscpd` for TS/JS, `pylint --disable=all --enable=duplicate-code` or `similarity-py` for Python, run in CI before the AI review | The doc says AI should ask "does this already exist?" Real tools do this in milliseconds. Use them first, send only the suspect blocks to Claude. |
| Gate 5 weekly review | GitHub Action: cron weekly → script pulls last week's logs from Vercel/Cloud Logging via API → POSTs to Claude API with the weekly template → opens GitHub issue with the response. Founder reviews the issue, doesn't generate it. | The doc already says "automate enforcement." Then the actual analysis is left manual. Automate both ends. |
| Gate cost tracking | Anthropic API `metadata` field + a 20-line script that queries the Admin API monthly and writes `cost-by-gate.json` to the repo | The doc suggests a spreadsheet. In 2026. With an Admin API available. |
| Gate 4 deploy verdict (READY / NEEDS_WORK / NOT_READY) | GitHub Action that parses the latest review artifact, counts findings by severity, and posts a status check that gates merge | Currently a human reads the verdict and decides. Trivially automatable. |
| Semantic test stability | Wrap pytest semantic tests with `pytest-rerunfailures` and a fixed-seed Claude call (`temperature=0` where possible) | Removes the "run 3 times" folklore with actual deterministic test behavior. |

Vague "use AI" gestures: none in this section. Each row names the tool.

---

## Rewritten Opening (less dumb version)

> # Forge Protocol
>
> A six-gate process for shipping AI-generated code that does not break in production. Built by a small studio, audited against its own rules, used on real projects. Every claim that follows is tagged SOLID, INFERRED, or GAP.
>
> **Who this is for:** one or two people building a product with Claude Code, Cursor, or equivalent, who have shipped or will soon ship to paying users.
>
> **What it costs:** roughly one extra hour of process per feature in exchange for not getting paged at 3am.
>
> **The six gates:** SPEC (adversarial requirements review), BUILD (code with a project context file), REVIEW (adversarial code review), TEST (adversarial tests with domain attack patterns), SHIP (deploy with safety nets), LEARN (telemetry feedback into next cycle's specs). Skip SPEC for changes under 20 lines. Skip none of the others.
>
> **What this is not:** a substitute for hiring a senior engineer when you can afford one. It is the rigging you use until then.
>
> Read the gates. Use the templates in `/templates`. Run `/forge-spec`, `/forge-review`, `/forge-scan`, `/forge-fix` from `/skills`. Stop reading and start shipping.

That is the whole intro. Six paragraphs. The current opening takes 65 lines to say less.

---

## Final note

The protocol is genuinely good. The document teaching it is doing the protocol a disservice by burying the signal under quick references, lineages, versioning theater, vendor blog citations, and prematurely-built portfolio scaffolding. Cut the document to one third. The protocol itself gets sharper, not weaker.
