# claude-skills

Bộ Claude Code skills cá nhân — workflow hoàn chỉnh từ plan đến reflect, với agent layer tách riêng để tái sử dụng.

## Cài đặt

```bash
git clone git@github.com:hatruong219/claude-skills.git ~/dotfiles
cd ~/dotfiles && ./install.sh
```

Script tạo symlink `~/.claude/commands` và `~/.claude/agents` vào repo. Clone ở đâu cũng hoạt động.

## Skills

| Command | Mô tả |
|---|---|
| `/plan <task>` | Explore codebase → draft plan → critic pass → lưu vào `PLAN.md` |
| `/implement` | Thực thi từng bước trong `PLAN.md`, tick checkbox khi xong, verify cuối |
| `/replan <feedback>` | Cập nhật `PLAN.md` theo feedback, giữ nguyên bước đã làm |
| `/review` | Review git diff hiện tại: correctness, security, conventions |
| `/fixbug <description>` | Diagnose root cause → plan fix → implement → verify |
| `/reflect` | Extract learnings từ task vừa xong, lưu vào project memory |

**Workflow thông thường:**
```
/plan <task> → /implement → /review → /reflect
                    ↓ (nếu cần điều chỉnh)
               /replan <feedback>
```

**Khi có bug:**
```
/fixbug <description> → /review → /reflect
```

## Agents

Skills dùng chung 3 agents — mỗi agent có model và tools phù hợp với vai trò:

| Agent | Model | Tools | Dùng bởi |
|---|---|---|---|
| `explore` | sonnet | read-only | plan, review, fixbug |
| `critic` | sonnet | read-only | plan, replan |
| `verify` | haiku | bash | implement, fixbug |

Agents định nghĩa **model + tools + system prompt** một lần. Skills chỉ gọi bằng tên và truyền task cụ thể.

## Cấu trúc

```
.claude/
  commands/       # Skills (user gọi trực tiếp qua /command)
    plan.md
    implement.md
    replan.md
    review.md
    fixbug.md
    reflect.md
  agents/         # Agent definitions (model, tools, system prompt)
    explore.md
    critic.md
    verify.md
install.sh        # Tạo symlinks vào ~/.claude/
```
