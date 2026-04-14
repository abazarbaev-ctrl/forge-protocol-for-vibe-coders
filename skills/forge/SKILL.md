---
name: forge
description: Run the full Forge Protocol gate sequence on a feature — spec review, build, adversarial review, tests, ship checklist
tools: [Bash, Read, Write, Edit, Grep, Glob, Agent]
---

# Forge — Full Gate Sequence

Run the complete Forge Protocol for a feature. Use when you want the full rigorous treatment.

## Usage

`/forge [description of what to build]`

Examples:
- `/forge add WiFi QR code to GuestLoop welcome page`
- `/forge implement webhook signature verification for iiko-assistant`
- `/forge new project: invoice generator for construction company`

## What This Does

### Gate 0: Spec Validation
Before writing any code, conduct an adversarial spec review:

1. Ask the user the 3 key questions (naturally, not as a dump):
   - "What should this NOT do?" → surfaces MUST NOTs
   - "What's the worst thing that could happen?" → surfaces security/safety concerns
   - "What edge cases worry you?" → surfaces dead-end states

2. Write BDD scenarios (Given/When/Then) with MUST NOT sections for each.

3. Tag every assumption: SOLID (user said it), INFERRED (implied), GAP (silent — ask about these).

4. If this is a Medium or Large feature, create a state transition table.

5. **State success criteria as a testable outcome.** This is a hard requirement before Gate 1. Examples:
   - "This feature is done when: test `test_wifi_qr_renders_on_welcome_page` passes AND `test_wifi_qr_rejects_expired_token` passes"
   - "This fix is done when: test `test_order_rejects_negative_quantity` passes (currently fails)"
   - For UI/exploration tasks with no testable assertion, state the observable outcome instead:
     - "Done when: user can scan QR at /table/5 and see welcome page in under 2s"
   - User must approve the criteria. If criteria are too vague, push back — "I can't build this without a concrete success test. Help me define one."

6. Present findings: "Here's what I think this feature needs to handle. Success criteria: [...]. Anything I'm missing?"

**Wait for user confirmation before proceeding to Gate 1.**

### Gate 1: Build
1. Read the project's CLAUDE.md for architecture context
2. Check if templates from `/Users/almazbazarbaev/Documents/02_Business_Projects/_Active/AI enabler venture studio/templates/` apply
3. **Write the success criteria test(s) from Gate 0 first.** They should fail. Confirm they fail for the right reason (missing feature, not setup bug).
4. Implement following the BDD scenarios, looping until the Gate 0 tests pass
5. Tag assumptions in code: `# INFERRED:` or `# GAP:`
6. For large features: consider splitting across parallel agents (Gate 1.5)

### Gate 2: Adversarial Review
After writing code, review your own work adversarially:

1. Check for duplication — does this logic exist elsewhere in the project?
2. Check for security gaps — auth, validation, injection, data exposure
3. Check for architectural drift — does this follow CLAUDE.md boundaries?
4. Check INFERRED/GAP tags — anything that needs human decision?
5. Rate honestly: "I found [N] issues. [X] are things I can fix now, [Y] need your input."

Fix what you can. Ask about the rest.

### Gate 3: Adversarial Tests
Write tests designed to BREAK the code:

1. Happy path tests (the obvious ones)
2. Edge case tests (empty input, huge input, wrong types)
3. Domain-specific attack tests — check the project's attack library:
   - Healthcare: `templates/attack-patterns/healthcare.md`
   - Restaurant/F&B: `templates/attack-patterns/restaurant-fb.md`
   - Real Estate: `templates/attack-patterns/real-estate.md`
   - Education: `templates/attack-patterns/education.md`
   - Banking: `templates/attack-patterns/banking.md`
4. If no attack library exists for this domain, generate one first

Ask: "Tests written. Want me to run them?"

### Gate 4: Ship Checklist
Before deploy, verify:
- [ ] CI pipeline exists and would pass
- [ ] Error handlers catch uncaught exceptions
- [ ] Health check endpoint works
- [ ] No secrets in code (check .env, .gitignore)
- [ ] Rollback plan exists (can revert in < 5 min)

Present as: "Ship checklist — [N/5] items green. [issues if any]. Ready to deploy?"

### Output
At the end, update the project's CLAUDE.md quality score if it changed, and note what was built, tested, and any remaining GAPs.
