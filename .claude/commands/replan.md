You are updating an existing plan based on new feedback. Do NOT restart from scratch — work from what already exists.

## Feedback
$ARGUMENTS

---

## Step 1 — Load Current State

Read `PLAN.md` to understand the current plan.

Then run:
```bash
git diff HEAD
git status
```

Check which steps in the plan are already implemented:
- If a file listed in the plan has been modified in the git diff → mark as `- [x]` (done)
- If not yet touched → keep as `- [ ]` (remaining)

---

## Step 2 — Understand the Feedback

Analyze what the user wants to change:
- Is it about approach? (affects remaining steps, may conflict with done steps)
- Is it about a specific file or step? (local change)
- Does it invalidate anything already implemented?

If the feedback conflicts with already-done work, flag it explicitly:
> "⚠️ This change conflicts with already-implemented [file]. You may need to revert [specific change]."

Do NOT silently undo done work.

---

## Step 3 — Update the Plan

Apply the feedback to `PLAN.md`:
- Keep `- [x]` items intact (already done)
- Update only `- [ ]` items and the Approach/Decisions sections as needed
- Add new steps if the feedback introduces new scope
- Update the footer:

```
---
_Created: [original timestamp]_
_Updated: [new timestamp]_
_Change: [one-line summary of this update]_
_Critic findings: [from original plan]_
```

---

## Step 4 — Quick Critic on the Changes

Run a focused critic only on what changed:

> "The plan was just updated with this change: [feedback summary].
> Does this update introduce any new issues?
> Are the remaining steps still coherent with the new approach?"

Fix any issues found.

---

## Step 5 — Save and Report

Save the updated `PLAN.md`.

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

Ask: **"Updated plan looks good? Run `/implement` to continue."**
