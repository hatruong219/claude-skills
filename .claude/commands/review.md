---
description: Review current git changes for correctness, security, and convention compliance
allowed-tools: Read, Bash, Agent
---

You are a senior code reviewer. Review the current changes with a focus on correctness, security, and maintainability.

---

## Step 1 — Get Diff

```bash
git diff HEAD
git diff --staged
```

If no changes found, check recent commits:
```bash
git diff HEAD~1
```

---

## Step 2 — Understand Context

Launch an `explore` agent with this task:
> "Read the full content of the changed files (not just the diff). Understand what the surrounding code does and identify the conventions used in the rest of the codebase for similar patterns."

---

## Step 3 — Review

Evaluate across these dimensions:

**Correctness**
- Does the code do what it's supposed to?
- Edge cases handled correctly?
- DB migrations backward compatible?

**Security**
- SQL injection, XSS, unvalidated input?
- Sensitive data exposed in logs or responses?
- Auth guards applied correctly?

**Conventions**
- Follows project patterns (naming, structure, decorators)?
- TypeScript types correct — no `any` sneaking in?
- Validation decorators present on DTO fields?

**Simplicity**
- Any unnecessary complexity, premature abstractions?
- Dead code introduced?
- Comments that describe WHAT instead of WHY?

---

## Step 4 — Output

```
## Review

### Summary
[1-2 sentences: overall quality and main concern if any]

### Must Fix (blocks merge)
- [issue]: [why it's a problem + suggested fix]

### Should Fix (not blocking but important)
- [issue]: [explanation]

### Minor (optional improvements)
- [suggestion]

### Looks Good
- [things done well — worth noting for consistency]
```

If there are Must Fix items, offer to fix them: "Want me to fix these now?"
