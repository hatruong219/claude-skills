---
description: Diagnose and fix a bug at root cause, not just the symptom
argument-hint: "<bug description>"
allowed-tools: Read, Edit, Bash, Agent
---

You are a senior software engineer debugging and fixing a bug. Fix the root cause — not just the symptom.

## Bug Description
$ARGUMENTS

---

## Step 1 — Explore

Launch an `explore` agent with this task:
> "Find the code path related to this bug: $ARGUMENTS. Trace from entry point to where the issue likely originates. Also check git log for recent changes to those files — could be a regression."

---

## Step 2 — Diagnose

Before writing any fix, state clearly:

```
## Diagnosis

**Symptom**: [what the user sees / what error occurs]
**Root cause**: [why it happens — the actual code logic that's wrong]
**Location**: [file:line where the bug lives]
**Trigger**: [what conditions cause it]
**NOT the cause**: [what it's NOT, if there's an obvious false lead]
```

If you cannot determine root cause from static analysis alone, say so and suggest how to reproduce it.

---

## Step 3 — Plan Fix

Describe the fix in 2-3 lines before implementing:
- What exactly will change
- Why this fixes the root cause (not just the symptom)
- Any risk of side effects

If the fix touches more than 3 files or requires a DB migration, stop and recommend running `/plan` instead.

---

## Step 4 — Implement

Apply the minimal fix:
- Change only what's needed to fix the root cause
- Do NOT refactor surrounding code
- Do NOT add defensive checks for cases unrelated to this bug

Then check for the same pattern elsewhere:
```bash
grep -r "[key pattern from the bug]" src/ --include="*.ts" -l
```

If found, fix those too and list them.

---

## Step 5 — Verify

Launch a `verify` agent with this task:
> "Run type check, lint, and tests related to the files changed in this bug fix."

---

## Step 6 — Report

```
## Fixed

**Root cause**: [one line]
**Fix**: [what changed and where]
**Also fixed**: [other files with same bug, if any]

### Checks:
- TypeScript: ✓ / ✗
- Lint:       ✓ / ✗
- Tests:      ✓ / ✗

### No test coverage (if applicable):
- [describe the untested case]
```

Suggest: **"Run `/review` to double-check the fix, or `/reflect` to save learnings."**
