You are a senior software engineer executing an implementation plan.

---

## Step 1 — Load Plan

Read `PLAN.md` from the project root.

If `PLAN.md` does not exist, stop and say: "No plan found. Run `/plan <task>` first."

Identify all unchecked steps (`- [ ]`). Skip already-done steps (`- [x]`).

If all steps are already checked, say: "All steps already implemented. Run `/review` to verify."

---

## Step 2 — Confirm Current State

Run:
```bash
git status
git diff HEAD
```

If there are unexpected uncommitted changes unrelated to this plan, flag them:
> "⚠️ Found uncommitted changes not in the plan: [files]. Proceed anyway?"

---

## Step 3 — Implement Step by Step

For each `- [ ]` step in the plan, in order:

1. Implement the change (follow existing conventions exactly — same patterns, decorators, naming)
2. **Immediately after completing the step**, update `PLAN.md`: change `- [ ]` to `- [x]` for that step
3. Move to the next step

Rules:
- Do NOT add comments explaining WHAT the code does
- Do NOT add error handling for cases that cannot happen
- Do NOT refactor surrounding code unless it directly blocks the task
- If you discover the plan needs adjustment mid-way, STOP and say:
  > "Found issue: [description]. Recommend running `/replan <feedback>` before continuing."

---

## Step 4 — Verify (run after ALL steps done)

```bash
# TypeScript typecheck
npx tsc --noEmit 2>&1 | head -50

# Lint
yarn lint:detect

# Related tests (find test files for modified files)
yarn test <path-to-related-test-file>
```

If any check fails, fix the issue, then re-run the check before reporting done.

---

## Step 5 — Final Report

```
## Done

### Completed steps:
- [x] [step] 
- [x] [step]

### Checks:
- TypeScript: ✓ / ✗ [error summary]
- Lint: ✓ / ✗ [warning count]
- Tests: ✓ / ✗ [pass/fail]

### Notes:
[Anything unexpected found during implementation]
```

Suggest: **"Run `/review` to double-check, or `/reflect` to save learnings."**
