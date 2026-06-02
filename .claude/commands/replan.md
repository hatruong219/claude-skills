---
description: Update .claude/<task>/plan.md based on feedback without losing already-done work
argument-hint: "<task-slug> <feedback>"
allowed-tools: Read, Write, Bash, Agent
---

You are updating an existing plan based on new feedback. Do NOT restart from scratch — work from what already exists.

## Arguments
$ARGUMENTS

Parse: first word = `<task-slug>`, remainder = `<feedback>`.

---

## Context — User-Provided Files

Scan `$ARGUMENTS` for `@file` references.

- If `@` files are present → these are the **specific parts of the plan** the user wants to revisit. Focus the replan and critic pass around these files.
- If no `@` files → apply feedback broadly as normal.

---

## Step 1 — Load Current State

Read `.claude/<task-slug>/plan.md` and `.claude/<task-slug>/status.md` (if exists).

Then run:
```bash
git diff HEAD
git status
```

Cross-reference: steps marked `- [x]` in plan.md are done. Steps in `status.md` as `⏳` were interrupted — treat as NOT done.

---

## Step 2 — Understand the Feedback

Analyze what needs to change:
- Affects approach? (may conflict with done steps)
- Affects a specific step only? (local change)
- Invalidates already-implemented work?

If it conflicts with already-done work, flag explicitly:
> "⚠️ This change conflicts with already-implemented [file]. You may need to revert [specific change]."

Do NOT silently undo done work.

---

## Step 3 — Update the Plan

Apply feedback to `.claude/<task-slug>/plan.md`:
- Keep `- [x]` items intact
- Update `- [ ]` items and Approach/Specs/Decisions sections as needed
- Add new steps if feedback introduces new scope
- Update the footer:

```
---
_Task: [task]_
_Created: [original timestamp]_
_Updated: [new timestamp]_
_Change: [one-line summary of this update]_
_Critic findings: [from original plan]_
```

---

## Step 4 — Quick Critic on the Changes

Launch a `critic` agent:
> "The plan at .claude/<task-slug>/plan.md was just updated with: <feedback>. Focus only on the changed parts — do the remaining steps still cohere? Any new issues introduced?"

Fix any issues found.

---

## Step 5 — Save and Report

Save the updated `.claude/<task-slug>/plan.md`.

Then show:
```
## Plan updated

### Already done (unchanged):
- [x] [step]

### Updated/remaining:
- [ ] [step] ← [what changed]

### Conflicts detected (if any):
- ⚠️ [conflict description]
```

Ask: **"Updated. Run `/implement <task-slug>` to continue."**
