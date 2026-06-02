---
description: Dispatch task cho Agent Team. Mặc định chạy full pipeline (researcher→architect→implementer→reviewer). Có thể chỉ định subset bằng cú pháp "member1,member2 | task". Task nhỏ dùng /plan+/implement hoặc agent dev.
argument-hint: "[member1,member2 | ] <task description>"
allowed-tools: Read, Write, Bash, Agent, TodoWrite
---

Bạn là dispatcher — khởi động Agent Team.

## Input
$ARGUMENTS

---

## Bước 1 — Parse pipeline và task

Kiểm tra `$ARGUMENTS` có dạng `<members> | <task>` không (dấu `|` phân cách):

**Có dấu `|`** → phần trước là pipeline, phần sau là task.
```
Ví dụ: "researcher,implementer | Add login endpoint"
Pipeline: [researcher, implementer]
Task: "Add login endpoint"
```

**Không có dấu `|`** → full pipeline mặc định + toàn bộ là task.
```
Ví dụ: "Add login endpoint"
Pipeline: [researcher, architect, implementer, reviewer]
Task: "Add login endpoint"
```

Members hợp lệ: `researcher`, `architect`, `implementer`, `reviewer`
Thứ tự luôn theo: researcher → architect → implementer → reviewer (bỏ qua member không có trong pipeline).

## Bước 2 — Khởi tạo workspace

```bash
mkdir -p .claude/team
```

Đọc trạng thái hiện tại:
- `.claude/team/queue.md` — có task dở không?
- `.claude/team/memory.md` — team đã biết gì?

Nếu queue có task dở, hỏi user: "Có task dở: [task]. Resume hay bắt đầu task mới?"

## Bước 3 — Spawn coordinator với pipeline đã xác định

```
Agent(coordinator, prompt="
Task: <task>
Pipeline: <danh sách members theo thứ tự, ví dụ: researcher, implementer>

CHỈ spawn các members trong Pipeline — bỏ qua members không có trong danh sách.
Đọc .claude/team/memory.md và .claude/team/queue.md trước.

Workspace:
- .claude/team/queue.md
- .claude/team/memory.md
- .claude/team/handoffs.md
")
```

## Bước 4 — Báo cáo kết quả

```
## Team hoàn thành: <task>

### Pipeline chạy
<member> ✅ → <member> ✅ → ...

### Kết quả
[files changed, verdict nếu có reviewer]

### Team memory cập nhật
[những gì mới ghi vào memory.md]
```

Suggest: "Run `/reflect` để lưu learnings cá nhân."
