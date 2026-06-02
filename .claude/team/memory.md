# Team Shared Memory

> Kiến thức tích lũy của cả team qua nhiều session.
> Mỗi agent ĐỌC file này khi bắt đầu. Mỗi agent GHI vào section của mình khi có phát hiện mới.
> Đây là "long-term memory" của Agent Team — càng dùng càng giàu thông tin.

---

## Project Conventions
<!-- researcher ghi: naming, patterns, decorators, file structure -->

[2026-05-27] Researcher: Agent Team gồm 5 members, mỗi member có file định nghĩa tại `.claude/agents/team/<name>.md` với frontmatter YAML (name, description, tools, model, color).

### Agent Team Members

| Member | Role | Tools | Model | Color |
|---|---|---|---|---|
| **coordinator** | Nhận task lớn, break down thành subtasks, dispatch cho đúng team member theo thứ tự phụ thuộc, track tiến độ qua queue.md, tổng hợp kết quả | Read, Write, Edit, Bash, Agent, TodoWrite | sonnet | purple |
| **researcher** | Khám phá codebase, nhận diện patterns, ghi findings vào memory.md. KHÔNG viết code, chỉ quan sát | Read, Write, Edit, Glob, Grep, LS, Bash | sonnet | yellow |
| **architect** | Thiết kế giải pháp, ra quyết định kỹ thuật, viết plan chi tiết cho implementer. KHÔNG viết code production | Read, Write, Edit, Bash | sonnet | blue |
| **implementer** | Viết code chính xác theo plan của architect. KHÔNG tự thiết kế, KHÔNG refactor ngoài scope | Read, Write, Edit, Bash, Glob, Grep | sonnet | green |
| **reviewer** | Review code changes cho correctness, security, conventions, và plan alignment. Trả verdict: Approved hoặc Needs Revision | Read, Write, Edit, Bash, Glob, Grep | sonnet | red |

### Team Pipeline
```
[RESEARCH] → [ARCHITECT] → [IMPLEMENT] → [REVIEW]
```

### Shared Workspace Files
- `.claude/team/queue.md` — task board (coordinator ghi, team cập nhật)
- `.claude/team/memory.md` — kiến thức tích lũy (mọi agent đọc đầu session)
- `.claude/team/handoffs.md` — log bàn giao giữa các agent
- `.claude/team/agents/*.json` — status files real-time cho dashboard

### Status JSON Format
Mỗi agent ghi real-time vào `.claude/team/agents/<name>.json`:
```json
{"name":"<name>","status":"running|done|blocked","step":"Step X/Y: <mô tả>","result":null|"<tóm tắt>"}
```

## Architecture Decisions
<!-- architect ghi: các quyết định thiết kế quan trọng và lý do -->
[2026-05-27] Architect: README.md cho team workspace nên là reference card (5 sections ngắn), không phải tutorial — lý do: người dùng đã có memory.md và agent definitions cho chi tiết.

## Known Gotchas
<!-- mọi agent ghi: những điều bất ngờ, trap, edge case đã gặp -->
_Chưa có dữ liệu._

## Reusable Patterns
<!-- implementer ghi: code patterns đã dùng, có thể tái sử dụng -->
_Chưa có dữ liệu._

## Review Findings
<!-- reviewer ghi: lỗi thường gặp, security issues, convention violations -->
[2026-05-27] Reviewer: README/docs nên mention cả skill invocation (`/dashboard`) lẫn CLI (`python3 dashboard.py`) — user có thể không biết cả hai cách.
