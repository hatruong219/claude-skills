---
description: Execute steps in .claude/<task>/plan.md one by one, track progress in status.md, resume safely if interrupted
argument-hint: "<task-slug>"
allowed-tools: Read, Write, Edit, Bash, Agent, TodoWrite
---

You are a senior software engineer executing an implementation plan.

## Task slug
$ARGUMENTS

---

## Context — User-Provided Files

Scan `$ARGUMENTS` for `@file` references (e.g. `@src/user/user.service.ts`).

- If `@` files are present → these are the files **most likely to be edited**. Read them immediately before implementing. Prioritize changes here over files found by exploration.
- If no `@` files → follow the plan steps as normal.

---

## Step 1 — Load Plan & Resume State

**Find the plan:**
- If `$ARGUMENTS` given → read `.claude/$ARGUMENTS/plan.md`
- If no argument → find most recent: `ls -t .claude/*/plan.md 2>/dev/null | head -1`
- If no plan found → stop: "No plan found. Run `/plan <task>` first."

**Check for previous session:**
Read `.claude/<task-slug>/status.md` if it exists.
- If a step is marked `⏳ in progress` → that step was interrupted. Re-do it from scratch.
- Use `- [x]` checkboxes in `plan.md` as ground truth for what's fully done.
- Start from the first `- [ ]` step.

If all steps are `- [x]` → say: "Already complete. Run `/review` to verify."

---

## Step 2 — Confirm Current State

```bash
git status
git diff HEAD
```

If unexpected uncommitted changes unrelated to this plan:
> "⚠️ Found uncommitted changes not in the plan: [files]. Proceed anyway?"

---

## Step 3 — Implement Step by Step

For each `- [ ]` step, in order:

**Before starting the step** — update `status.md`:
```markdown
# Status: <task-slug>

## Current
⏳ Step N/Total in progress — [brief step description]

## Completed
[list of done steps]

## Last updated: [timestamp]
```

**Implement the change** (follow existing conventions — same patterns, decorators, naming):
- Do NOT add comments explaining WHAT the code does
- Do NOT add error handling for cases that cannot happen
- Do NOT refactor surrounding code unless it directly blocks the task

**After completing the step:**
1. Update `plan.md`: change `- [ ]` to `- [x]` for this step
2. Update `status.md`: move step from Current → Completed

**If you discover the plan needs adjustment mid-way**, STOP:
> "Found issue: [description]. Recommend running `/replan <task-slug> <feedback>` before continuing."

---

## Step 4 — Verify

Launch a `verify` agent:
> "Run type check, lint, and related tests for the files changed in this session."

---

## Step 5 — Final Status & Report

Update `status.md`:
```markdown
# Status: <task-slug>

## Current
✅ Done

## Completed
- [x] Step 1 — ...
- [x] Step 2 — ...

## Last updated: [timestamp]
```

Then report:
```
## Done

### Completed steps:
- [x] [step]

### Checks:
- TypeScript: ✓ / ✗ [error summary]
- Lint:       ✓ / ✗ [warning count]
- Tests:      ✓ / ✗ [pass/fail]

### Notes:
[Anything unexpected]
```

Suggest: **"Run `/review` to double-check, or `/reflect` to save learnings."**
