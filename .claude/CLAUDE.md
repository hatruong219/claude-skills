# Global Claude Instructions

Đây là instructions áp dụng cho **mọi project**.
Project-specific instructions nằm ở `<project-root>/CLAUDE.md`.

## Skills có sẵn (global)

| Skill | Dùng khi |
|---|---|
| `/plan <task>` | Cần plan trước khi code |
| `/implement <slug>` | Thực thi plan đã có |
| `/replan <slug> <feedback>` | Điều chỉnh plan giữa chừng |
| `/review` | Review git diff hiện tại |
| `/fixbug <description>` | Debug + fix root cause |
| `/reflect` | Lưu learnings vào memory |
| `/team <task>` | Feature lớn cần cả team |

## Agents có sẵn (global)

| Agent | Vai trò |
|---|---|
| `explore` | Khám phá codebase (read-only) |
| `critic` | Review plan adversarially |
| `verify` | Chạy type check + lint + test |
| `dev` | Full-cycle autonomous engineer |
| `coordinator` | Điều phối Agent Team |
| `researcher` | Team: khám phá domain |
| `architect` | Team: thiết kế solution |
| `implementer` | Team: viết code |
| `reviewer` | Team: review code |

## Coding conventions (mọi project)

- KHÔNG add comment giải thích code làm gì
- KHÔNG add error handling cho trường hợp không thể xảy ra
- KHÔNG refactor code ngoài scope của task
- KHÔNG thêm feature không được yêu cầu
- Minimum sufficient context: spawn sub-agent cho việc sinh nhiều noise
