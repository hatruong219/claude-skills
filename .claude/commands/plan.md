You are orchestrating a planning pipeline. Your ONLY job is to produce a high-quality implementation plan — do NOT write any code.

## Task
$ARGUMENTS

---

## Step 1 — Explore

Spawn an **Explore subagent** (read-only) to:
- Find all files relevant to this task (entities, services, resolvers, DTOs, migrations, tests)
- Identify existing patterns for similar features
- Note conventions in use (naming, structure, decorators)
- Check if similar logic already exists that can be reused

---

## Step 2 — Generate Plan

Using the exploration output, draft an initial plan in this format:

```
## Plan: [task summary]

### Approach
[1-2 sentences: WHAT and WHY this approach over alternatives]

### Steps
- [ ] **[file path]** — [what to change and why]
- [ ] **[file path]** — [what to change and why]
- [ ] Create **[file path]** — [purpose]
- [ ] Migration: [description]

### Decisions & Risks
- [Non-obvious choices and reasoning]
- [Potential gotchas]
```

Use `- [ ]` checkboxes for every step — these will be checked off during `/implement`.

---

## Step 3 — Critic Pass (REQUIRED)

Spawn a **new subagent** with this adversarial role:

> "You are a senior engineer who must find flaws in this plan before it gets implemented.
> Your job is NOT to validate — your job is to break it.
>
> Check:
> - What files are missing? (tests, resolvers, permission configs, GraphQL schema, etc.)
> - If implemented as-is, what will break?
> - Is the approach too complex? Could it be simpler?
> - Backward compatibility issues (especially DB migrations)?
> - Follows project conventions?
>
> Output a numbered list of issues. If nothing is wrong, explain why — don't just say 'looks good'."

---

## Step 4 — Refine

Fix each valid critic issue. Note any disagreements explicitly.

---

## Step 5 — Save to PLAN.md

Write the final plan to `PLAN.md` in the project root. Append:

```
---
_Created: [timestamp]_
_Critic findings: [one-line summary of what was found and fixed]_
```

---

## Step 6 — Checkpoint

Say "Plan saved to PLAN.md" and summarize what the critic flagged and what was adjusted.

Then: **"Looks good? Confirm to proceed with `/implement`, or run `/replan <feedback>` to adjust."**

Do NOT proceed to implementation.
