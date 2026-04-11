---
name: forge
description: Run the full Forge Protocol gate sequence on a feature — spec review, build, adversarial review, tests, ship checklist
tools: [Bash, Read, Write, Edit, Grep, Glob, Agent]
---

# Forge — Full Gate Sequence

Run the complete Forge Protocol for a feature.

## Usage

`/forge [description of what to build]`

## What This Does

### Gate 0: Spec Validation
Before writing any code:

1. Ask the user naturally (not as a checklist dump):
   - "What should this NOT do?"
   - "What's the worst thing that could happen?"
   - "What edge cases worry you?"

2. Write BDD scenarios (Given/When/Then) with MUST NOT sections.

3. Tag every assumption: SOLID (user said it), INFERRED (implied), GAP (silent — ask about these).

4. Present findings: "Here's what I think this feature needs to handle. Anything I'm missing?"

**Wait for user confirmation before proceeding to Gate 1.**

### Gate 1: Build
1. Read the project context file for architecture constraints
2. Implement following the BDD scenarios
3. Tag assumptions in code: `# INFERRED:` or `# GAP:`

### Gate 2: Adversarial Review
After writing code, review your own work:

1. Check for duplication — does this logic exist elsewhere?
2. Check for security gaps — auth, validation, injection, data exposure
3. Check for architectural drift
4. Rate honestly: "I found [N] issues. [X] I fixed, [Y] need your input."

### Gate 3: Adversarial Tests
Write tests designed to BREAK the code:

1. Happy path tests
2. Edge case tests (empty input, huge input, wrong types)
3. Domain-specific attack tests — check project's attack library if available
4. If no attack library exists, generate one first

Ask: "Tests written. Want me to run them?"

### Gate 4: Ship Checklist
Before deploy, verify:
- [ ] CI pipeline exists and would pass
- [ ] Error handlers catch uncaught exceptions
- [ ] Health check endpoint works
- [ ] No secrets in code
- [ ] Rollback plan exists

Present as: "Ship checklist — [N/5] green. Ready to deploy?"
