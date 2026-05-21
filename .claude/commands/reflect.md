You are a memory architect. After completing a task, extract what was learned and persist it so future sessions start smarter.

---

## Step 1 — Gather Evidence

Look at this conversation and run:
```bash
git diff HEAD~1  # or appropriate range for this task
git log --oneline -5
```

Understand:
- What task was completed
- What approach was chosen (and what was rejected)
- What was discovered during exploration or implementation
- What went wrong and how it was fixed

---

## Step 2 — Extract Learnings

From the evidence, extract:

**Decisions made** — choices that had alternatives:
- "Chose X over Y because Z"
- Only include if the reasoning is non-obvious

**Patterns discovered** — how things work in this codebase:
- "When adding a new GraphQL field, also need to update X"
- Only include if it's not in CLAUDE.md or obvious from code

**Anti-patterns encountered** — things that broke or nearly broke:
- "Don't do X, it causes Y"
- Include even minor ones

Discard anything already documented in CLAUDE.md or obvious from the code structure.

---

## Step 3 — Persist to Memory

For each learning, write to the appropriate memory file in:
`~/.claude/projects/[current-project-hash]/memory/`

Use this format for each memory file:
```markdown
---
name: [short-kebab-slug]
description: [one-line summary of what this memory is about]
metadata:
  type: project
---

[The learning itself]

**Why:** [why this matters / what went wrong if ignored]
**How to apply:** [when future Claude should use this]
```

Then update `MEMORY.md` index with a one-line pointer.

---

## Step 4 — Report

```
## Reflected

### Saved to memory:
- [memory name]: [one-line description]

### Discarded (already known / in CLAUDE.md):
- [thing discarded and why]

### Nothing new this time (if applicable)
```
