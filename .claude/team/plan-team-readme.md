# Plan: Tạo .claude/team/README.md

## Approach
Viết tài liệu ngắn gọn, dạng reference card — người dùng đọc 1 lần để hiểu cả workspace. Không duplicate thông tin đã có trong memory.md hay agent definitions, thay vào đó chỉ ra nơi tìm chi tiết.

## Reuse
- Bảng agents từ memory.md (đã có role/tools/model/color đầy đủ) — adapt format cho README
- Pipeline diagram từ memory.md
- Workspace files list từ memory.md

## Steps
- [x] **Create `.claude/team/README.md`** — viết full content gồm 5 sections:
  1. **Mục đích** — 2-3 câu giải thích team workspace là gì, dùng khi nào
  2. **Workspace files** — bảng 4 files (queue.md, memory.md, handoffs.md, agents/*.json) với mục đích từng file
  3. **Agent roles** — bảng 5 agents (coordinator, researcher, architect, implementer, reviewer) với vai trò 1 dòng
  4. **Cách dùng /team skill** — quick start 3 bước: cú pháp, ví dụ full pipeline, ví dụ subset pipeline
  5. **Dashboard** — 1 đoạn ngắn về dashboard.py và approval flow

## Không làm
- Không copy toàn bộ instructions từ agent definitions vào README — chỉ tóm tắt
- Không giải thích chi tiết status JSON format — đã có trong memory.md
- Không viết tutorial dài — đây là reference card

## Risks
- README quá dài → mất tính "ngắn gọn": giữ mỗi section dưới 10 dòng
- Thông tin trùng với memory.md: link sang thay vì copy

## Decisions
- Dùng Markdown table cho workspace files và agents — dễ scan hơn list
- Cú pháp `/team` đặt trong code block — dễ copy
- Không thêm section "Installation" hay "Setup" — workspace đã tự tạo khi chạy `/team`
