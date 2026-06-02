# Agent Team Workspace

Thư mục này là shared workspace của Agent Team — một nhóm AI agents phối hợp để thực hiện các task phức tạp theo pipeline. Dùng khi task cần nhiều bước chuyên biệt (research → design → code → review) hoặc khi muốn context của main session được giữ sạch.

---

## Workspace Files

| File | Mục đích |
|---|---|
| `queue.md` | Task board chia sẻ giữa tất cả agents — coordinator ghi tasks, agents cập nhật trạng thái `[ ]` → `[⏳]` → `[✅]` |
| `memory.md` | Kiến thức tích lũy qua nhiều session — mọi agent đọc khi bắt đầu, ghi khi có phát hiện mới |
| `handoffs.md` | Log bàn giao giữa các agent — ghi context, findings, và quyết định khi pass task sang agent tiếp theo |
| `agents/*.json` | Status files real-time — mỗi agent ghi `{"name","status","step","result"}` để dashboard hiển thị |

---

## Agent Roles

| Agent | Vai trò | Model |
|---|---|---|
| **coordinator** | Nhận task → break down → dispatch → track tiến độ → tổng hợp kết quả | sonnet |
| **researcher** | Khám phá codebase, nhận diện patterns, ghi findings vào memory.md. KHÔNG viết code | sonnet |
| **architect** | Thiết kế giải pháp, ra quyết định kỹ thuật, viết plan chi tiết. KHÔNG viết code production | sonnet |
| **implementer** | Viết code chính xác theo plan của architect. KHÔNG tự thiết kế, KHÔNG refactor ngoài scope | sonnet |
| **reviewer** | Review code cho correctness, security, conventions, plan alignment. Trả verdict: Approved / Needs Revision | sonnet |

Định nghĩa đầy đủ của từng agent: `.claude/agents/team/<name>.md`

---

## Cách dùng `/team` skill

**Cú pháp:**
```
/team <task>                          # Full pipeline: researcher → architect → implementer → reviewer
/team <members> | <task>             # Subset pipeline
```

**Ví dụ:**
```bash
# Full pipeline
/team Thêm endpoint POST /api/users với validation và tests

# Chỉ research + implement (bỏ architect và reviewer)
/team researcher,implementer | Tìm và sửa bug trong auth middleware

# Chỉ review code hiện tại
/team reviewer | Review thay đổi trong PR #42
```

**Pipeline mặc định:**
```
[researcher] → [architect] → [implementer] → [reviewer]
```

---

## Dashboard

Chạy `/dashboard` skill hoặc trực tiếp `dashboard.py` để xem real-time status của từng agent (màu theo role, progress bar, audit log):

```bash
python3 .claude/team/dashboard.py
```

Khi coordinator cần xác nhận từ user trước khi tiếp tục (ví dụ: xóa file, override logic lớn), dashboard hiện popup. User click để chọn — coordinator đọc response và tiếp tục theo lựa chọn.
