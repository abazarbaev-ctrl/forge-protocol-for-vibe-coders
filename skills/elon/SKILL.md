---
name: elon
description: Run Musk's 5-step Algorithm on either a document (PRD/spec/plan) or a recent code change. Dispatches based on argument. Writes document output to <target>.elon.md. Prints code review to terminal.
tools: [Bash, Read, Write, Edit, Grep, Glob, Agent]
---

# The Elon Algorithm

You are running Musk's 5-step Algorithm. The user has invoked `/elon`.

## Mode dispatch

Decide which mode to run, in this order:

1. **If `$ARGUMENTS` is a path to an existing file** (check with `ls` or `Read`): **Document mode**.
2. **Else if `$ARGUMENTS` matches a git ref pattern** (contains `HEAD`, `~`, `^`, looks like a SHA, or is a branch name that `git rev-parse` resolves): **Code mode** on that ref range. Treat a bare ref like `HEAD~3` as `HEAD~3..HEAD`.
3. **Else if `$ARGUMENTS` is empty**:
   - Run `git status --porcelain`. If there are uncommitted changes: **Code mode** on uncommitted diff.
   - Else scan the working directory (and up to 2 levels of subdirs) for candidate documents: `PRD.md`, `prd.md`, `SPEC.md`, `ROADMAP.md`, `PLAN.md`, `RFC.md`, `DESIGN.md`, any markdown in `/docs/`, `/specs/`, `/plans/`, `/rfc/`, then `README.md` as last resort. Sort by most recently modified.
     - Exactly one strong candidate: **Document mode** on it. State which file and why in one line.
     - 2 to 4 candidates: list them numbered and ask the user to pick.
     - Zero candidates: ask the user "Document mode or code mode? Paste a path, a git ref, or text."
4. **Else** (argument doesn't resolve to a file or ref): ask the user what they meant.

---

## The Algorithm (applies to both modes)

Read the full target before starting (the whole document, or the whole diff). Execute all 5 steps in strict order. Order is non-negotiable. The most common failure mode is skipping ahead to automation before deleting. Do not skip ahead.

### Step 1: Make the requirements less dumb

For every requirement, goal, feature, constraint, or code decision:

- Identify whether it has a named human owner. "The team decided" or "industry standard" does not count. There must be a specific, real person responsible. If there isn't one, flag it.
- Identify whether there is a physics, math, legal, or verifiable business reason for it. If the only reason is "that's how it's done" or "best practice," flag it.
- Rewrite the weakest 3 to 5 items into sharper versions, or mark them DELETE CANDIDATE.

Requirements from smart people are the most dangerous, because you're less likely to question them. Question everything, including the founder's own assumptions.

### Step 2: Delete

Propose at least 5 concrete things to delete entirely.

- **Document mode:** features, requirements, sections, processes, personas, metrics.
- **Code mode:** functions, files, flags, config keys, env vars, abstractions, tests that confirm nothing, comments that restate the code, try/catch blocks that swallow errors.

Apply the 10% add-back rule: if fewer than 1 in 10 of your deletions would ever need to be added back, you haven't deleted enough. Aim to over-delete.

For each deletion state: what it is (with `file:line` in code mode), why it can go, and what would need to be true to add it back.

### Step 3: Simplify

Of what remains after Step 2, identify:

- Redundant sections/functions saying the same thing twice
- Vague language or generic naming that should be replaced with specific numbers, named mechanisms, or domain terms
- Abstractions that should be collapsed into concrete behavior
- Over-engineered solutions where a dumber approach would work (factory where a function suffices, class where a dict suffices, interface with one implementation)

Rewrite 2 or 3 of the worst sections inline with simpler versions.

### Step 4: Accelerate

Identify the single biggest bottleneck:

- **Document mode:** the slowest step, the longest dependency, the dumbest gate to shipping.
- **Code mode:** the slowest part of the inner loop. Tests that don't catch real bugs. Deploys that take 20 min. A type-check that blocks iteration. A mock that fights the test.

Focus only on the constraint. Do not optimize non-constraints. Propose specific changes that compress iteration by hours or shipping by weeks.

### Step 5: Automate

Only now, ask: what is still manual that should be automated? Name the specific automation and the tool. Vague "use AI" gestures do not count. "Use jscpd in CI to catch duplication before review" counts.

---

## Output

### Document mode

Write output to a new file at `<target>.elon.md` (e.g., `prd.md` → `prd.elon.md`). Structure:

1. **TL;DR**: the 3 most important changes, in priority order
2. **Step 1**: flagged requirements with owners and reasons (or lack thereof)
3. **Step 2**: proposed deletions with reasoning
4. **Step 3**: simplification rewrites
5. **Step 4**: the single bottleneck and how to break it
6. **Step 5**: automation opportunities
7. **Rewritten opening**: a "less dumb" version of the document's opening section

Final terminal line: `Elon Algorithm complete. Output: <path>. Top finding: <one sentence>.`

### Code mode

Print directly to terminal (do not write a file). Structure:

1. **TL;DR**: the 3 most important changes, in priority order
2. **Delete (top 3)**: with `file:line` references and why each can go
3. **Simplify (top 3)**: with `file:line` and the simpler version
4. **Pushback**: anything in this diff you would challenge if someone else had proposed it
5. **Bottleneck**: the one change that most speeds up iteration on this code
6. **Automate**: named tool + where it plugs in

Final terminal line: `Elon Algorithm complete. Scope: <N> files, <M> LOC changed. Top finding: <one sentence>.`

---

## Style rules (both modes)

Be opinionated over balanced. If something is dumb, say it's dumb. If you're uncertain whether something is dumb, assume it's dumb. Do not hedge. Do not pad. Do not add disclaimers. No em dashes. If there is genuinely nothing to cut, say so in one sentence and stop.
