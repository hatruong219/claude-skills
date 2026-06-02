# Team Handoffs

> Log bàn giao công việc giữa các agent.
> Khi một agent xong việc và pass sang agent tiếp theo, ghi vào đây.
> Format: timestamp | from → to | summary | output location

---

## 2026-05-27 | researcher → architect
**Task:** Tạo .claude/team/README.md
**Key findings:**
- Team workspace có 4 shared files: queue.md, memory.md, handoffs.md, agents/*.json
- 5 agent definitions tại `.claude/agents/team/`: coordinator, researcher, architect, implementer, reviewer — mỗi file có frontmatter YAML và full instructions
- `/team` skill được invoke qua dispatcher pattern: parse pipeline → init workspace → spawn coordinator
- Dashboard đọc agents/*.json real-time; approval flow dùng approval.json + approval-response.json
- Memory.md đã có đầy đủ thông tin về roles và pipeline — README cần cross-reference thay vì duplicate
**Patterns tìm được:** `.claude/agents/team/*.md` (frontmatter + body), `.claude/team/agents/*.json` (status schema)
**Tương tự có thể reuse:** Bảng agents trong memory.md có thể adapt cho README
**Gotchas:** agents/*.json bao gồm cả coordinator.json và approval.json — cần phân biệt trong README

## 2026-05-27 | reviewer → coordinator
**Verdict:** APPROVED
**Issues found:** CRITICAL:0 MAJOR:0 MINOR:1
**Minor issues:** Dashboard section chỉ mention CLI — đã fix inline (thêm `/dashboard` skill mention)

## 2026-05-27 | implementer → reviewer
**Task:** Tạo .claude/team/README.md
**Files changed:**
- `.claude/team/README.md`: tạo mới — 5 sections (Mục đích, Workspace Files, Agent Roles, Cách dùng /team, Dashboard)
**Deviations from plan:** Không có — theo đúng plan
**Cần review đặc biệt:** Accuracy của bảng workspace files và agent roles so với thực tế

## 2026-05-27 | architect → implementer
**Task:** Tạo .claude/team/README.md
**Plan file:** .claude/team/plan-team-readme.md
**Key decisions:**
- Reference card format (5 sections), không phải tutorial
- Dùng Markdown tables cho workspace files và agents
- Mỗi section giữ dưới 10 dòng
**Risks cần lưu ý:** Tránh README dài hơn cần thiết — không copy full instructions từ agent definitions
**Không làm:** Không thêm section Installation/Setup, không giải thích status JSON format chi tiết

## 2026-05-27 | Example (template):
<!-- Example:
## 2026-05-27 14:30 | researcher → architect
**Task:** Understand auth module
**Findings summary:** JWT auth, httpOnly cookies, middleware tại src/auth/middleware.ts
**Output:** .claude/team/memory.md#Project Conventions
-->
