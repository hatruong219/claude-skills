---
description: Review code changes — supports commit ID, branch, range, PR, or current diff
allowed-tools: Read, Bash, Agent
---

You are a senior code reviewer. Review the specified changes with a focus on correctness, security, and maintainability.

---

## Step 0 — Choose Review Mode

Before doing anything else, check if `$ARGUMENTS` contains `--parallel <N>` (e.g. `--parallel 3`).

**If `--parallel N` is NOT present**, ask the user this question first:

> **Bạn muốn review với bao nhiêu agent?**
>
> | Lựa chọn | Mô tả |
> |---|---|
> | **1 agent** (mặc định) | Nhanh, đủ dùng cho diff nhỏ hoặc refactor đơn giản |
> | **2 agents** | Hai góc nhìn độc lập — tốt cho feature mới hoặc logic phức tạp |
> | **3 agents** | Ba góc nhìn, consensus rõ hơn — nên dùng cho PR quan trọng |
> | **5 agents** | Tối đa coverage — dành cho security review hoặc diff rất lớn |
>
> _(Mặc định là 1 nếu bạn bỏ qua)_

Wait for the user's answer before continuing. Store the chosen number as **N**.

If `--parallel N` IS present in arguments, extract N from there and skip the question. Strip `--parallel N` from the remaining arguments before continuing to Step 1.

- If N = 1: follow the **Standard Flow** (Steps 1–4 below).
- If N > 1: follow the **Parallel Flow** (Steps 1, 1b, 4b below).

---

## Step 1 — Parse Arguments and Get Diff

Parse `$ARGUMENTS` to determine the review target:

### Argument patterns (check in order):

**1. No arguments** — review current working changes:
```bash
git diff HEAD
git diff --staged
```
If nothing found: `git diff HEAD~1`

**2. `@file` reference(s)** (e.g. `@src/foo.ts`) — review specific files:
```bash
git diff HEAD -- <file>
```
These are the **primary review targets** — focus the review here.

**3. Commit SHA** (7–40 hex chars, e.g. `abc1234`) — review a single commit:
```bash
git show <sha>
git show <sha> --stat
```

**4. Commit range** (e.g. `abc123..def456` or `HEAD~3..HEAD`) — review a range:
```bash
git diff <range>
git diff <range> --stat
```

**5. Branch name** (e.g. `feat/login`, `main`) — review diff against current branch or base:
```bash
# Changes on that branch not yet in current branch:
git diff HEAD..<branch>
git diff HEAD..<branch> --stat
```
If the branch IS the current branch, compare against its merge base with main/master:
```bash
git diff $(git merge-base HEAD main)..<branch>
```

**6. `--pr <number>` or `pr/<number>`** — review a GitHub PR (requires `gh` CLI):
```bash
gh pr diff <number>
gh pr view <number> --json title,body,baseRefName,headRefName
```

After running the diff command, also run `git log` or `git show --stat` to understand the scope.

---

## Step 1b — Parallel Flow (N > 1)

Skip Steps 2–3. Instead:

1. Save the diff output to a temp variable (do not write to disk).
2. Collect the list of changed files from `--stat`.
3. Spawn **N `reviewer` agents in parallel** (single message block). Each agent receives:
   - The full diff text
   - The changed file list
   - The same review checklist from Step 3 below
   - Instruction: "Review independently. Do not coordinate with other agents."
4. When all N agents return, go to **Step 4b — Synthesize**.

> **Resource guard**: if N > 5, warn the user and suggest N=3.

---

## Step 2 — Understand Context _(Standard Flow only)_

Launch an `explore` agent with this task:
> "Read the full content of the changed files (not just the diff). Understand what the surrounding code does and identify the conventions used in the rest of the codebase for similar patterns."

---

## Step 3 — Review _(Standard Flow only)_

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

## Step 4 — Output _(Standard Flow only)_

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

---

## Step 4b — Synthesize _(Parallel Flow only)_

Merge all N result sets into one unified report using these rules:

- **Must Fix**: appears in ≥ 1 agent → include (note "flagged by X/N agents" if < majority)
- **Should Fix**: appears in ≥ 2 agents → include; if only 1 agent → downgrade to Minor
- **Minor**: union of all suggestions, deduplicated
- **Looks Good**: only include if ≥ majority of agents agree

Output the same format as Step 4, with a header line:

```
> Reviewed by N independent agents. Findings below reflect consensus.
```

If there are Must Fix items, offer to fix them: "Want me to fix these now?"
