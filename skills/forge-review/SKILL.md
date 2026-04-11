---
name: forge-review
description: Forge Protocol weekly review — analyze errors, usage, dead features, and suggest improvements
tools: [Bash, Read, Grep, Glob, Agent]
---

# Forge Weekly Review

Run the Gate 5 weekly review for a project.

## Usage

`/forge-review` — review current project

## What This Does

### 1. Gather Data

- `git log --since="7 days ago" --oneline` — what changed this week
- Check for error logs or monitoring endpoints
- Check CI status — any failing pipelines?
- Read project context file for current quality score

### 2. Answer the 6 Review Questions

| # | Question |
|---|----------|
| 1 | **Dead features** — anything built but unused this week? |
| 2 | **Error clusters** — what's breaking? Group by root cause |
| 3 | **Performance** — anything slow or expensive? |
| 4 | **User friction** — where do users struggle? |
| 5 | **Security** — any new findings from CI scans? |
| 6 | **Top improvement** — single highest-impact change? Present as A/B/C with tradeoffs |

### 3. Suggest Next Actions
- Quick wins (< 1 hour) — do now
- Medium (1-4 hours) — schedule this week
- Large (> 4 hours) — add to backlog

### 4. Update Tracking
- Update quality score in project context file if warranted
- Update TODO.md with suggested actions
- Note the review date
