---
description: Explore codebase, draft an implementation plan with adversarial critic pass, save to .claude/<task>/plan.md
argument-hint: "<task description>"
allowed-tools: Read, Write, Bash, Agent, TodoWrite
---

You are orchestrating a planning pipeline. Your ONLY job is to produce a high-quality implementation plan — do NOT write any code.

## Task
$ARGUMENTS

---

## Context — User-Provided Files

Scan `$ARGUMENTS` for `@file` references (e.g. `@src/user/user.service.ts`).

- If `@` files are present → read them **immediately**, treat as PRIMARY context. Tell the `explore` agent to start from these files and expand outward only if needed.
- If no `@` files → explore freely as normal.

---

## Step 0 — Prepare directory

Slugify the task name into a short kebab-case identifier (e.g. "add user auth" → `add-user-auth`). Call it `<task-slug>`.

Run:
```bash
mkdir -p .claude/<task-slug>
```

All output for this task lives in `.claude/<task-slug>/`.

---

## Step 1 — Explore

Launch an `explore` agent with this task:
> "Find all files relevant to: $ARGUMENTS. Identify existing patterns for similar features, conventions in use (naming, structure, decorators), and any similar logic that can be reused."

---

## Step 2 — Generate Plan

Using the exploration output, draft a plan with this structure:

```markdown
# Plan: [task summary]

## Approach
[1-2 sentences: WHAT and WHY this approach over alternatives]

## Specs
[Key behaviors the implementation must satisfy — written as requirements, not steps]

## Steps
- [ ] **[file path]** — [what to change and why]
- [ ] **[file path]** — [what to change and why]
- [ ] Create **[file path]** — [purpose]
- [ ] Migration: [description]

## Decisions & Risks
- [Non-obvious choices and reasoning]
- [Potential gotchas]
```

Use `- [ ]` checkboxes — these will be checked off during `/implement`.

---

## Step 3 — Critic Pass (REQUIRED)

Launch a `critic` agent with this task:
> "Review the plan for: $ARGUMENTS. Read the plan content below and relevant source files. Find every flaw — missing files, things that will break, unnecessary complexity, backward compatibility issues, convention violations.
>
> [paste the draft plan here]"

---

## Step 4 — Refine

Fix each valid critic issue. Note any disagreements explicitly.

---

## Step 5 — Save

Use the **Write tool** to save to `.claude/<task-slug>/plan.md`. Append at the bottom:

```
---
_Task: $ARGUMENTS_
_Created: [timestamp]_
_Critic findings: [one-line summary of what was found and fixed]_
```

Do NOT output the plan only in chat — it MUST be written to disk.

---

## Step 6 — Checkpoint

Say "Plan saved to `.claude/<task-slug>/plan.md`" and summarize what the critic flagged and what was adjusted.

Then: **"Looks good? Run `/implement <task-slug>` to start, or `/replan <task-slug> <feedback>` to adjust."**

Do NOT proceed to implementation.
