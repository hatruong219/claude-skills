# Claude Code — Dotfiles Harness

## What this repo is
Personal Claude Code configuration: skills, agents, harness settings, and memory.
Designed for AIDD (AI Driven Development) workflows.

## Skill System (`/skill-name`)
Invoke via slash commands. Skills are lazy-loaded — full body only enters context when triggered.

| Skill | When to use |
|---|---|
| `/plan <task>` | Explore + draft plan + critic pass → saves `.claude/<slug>/plan.md` |
| `/implement <slug>` | Execute plan step by step, track in `status.md` |
| `/replan <slug> <feedback>` | Adjust plan mid-flight without losing done steps |
| `/review` | Review current git diff for correctness, security, conventions |
| `/fixbug <description>` | Root-cause diagnosis + fix |
| `/reflect` | Extract learnings → write to memory |

## Agent System (spawned via `Agent` tool)
Agents run in isolated context windows — main context stays clean.

| Agent | Role | Model |
|---|---|---|
| `explore` | Read-only codebase search | sonnet |
| `critic` | Adversarial plan reviewer | sonnet |
| `verify` | Type check + lint + test runner | haiku |
| `dev` | Autonomous full-cycle engineer | sonnet |

## Harness components active
- **Context Loading**: this file + `.claude/<task>/plan.md` when implementing
- **Guardrails**: `settings.json` permissions (allow/deny)
- **Hooks**: Stop → reflect reminder; PreToolUse → audit log
- **Skills**: lazy-loaded via ToolSearch
- **Memory**: `~/.claude/projects/.../memory/` (auto memory system)
- **Observability**: `~/.claude/logs/audit.log`

## Conventions
- Plan files live in `.claude/<task-slug>/plan.md`
- Status files live in `.claude/<task-slug>/status.md`
- Do NOT add explanatory comments to code
- Do NOT add error handling for impossible cases
- Do NOT refactor surrounding code unless it directly blocks the task
- Minimum sufficient context: spawn sub-agents for anything noisy (searches, long outputs)
