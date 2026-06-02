---
description: Khởi động Agent Team Dashboard tại http://localhost:5765. Hiển thị real-time status của từng team member, progress bar, và audit log. Chạy song song với /team.
argument-hint: ""
allowed-tools: Bash
---

Khởi động Agent Team Dashboard.

## Bước 1 — Kiểm tra file dashboard

```bash
ls .claude/team/dashboard.py 2>/dev/null || echo "NOT FOUND"
```

Nếu không tìm thấy → báo user: "Chạy lệnh này từ project root có chứa `.claude/team/dashboard.py`"

## Bước 2 — Kiểm tra port 5765 đã bị dùng chưa

```bash
lsof -ti:5765 2>/dev/null && echo "PORT IN USE" || echo "PORT FREE"
```

Nếu port đang dùng → báo: "Dashboard đã chạy tại http://localhost:5765"

## Bước 3 — Khởi động

```bash
mkdir -p .claude/team/agents
python3 .claude/team/dashboard.py &
sleep 1
echo "Dashboard running"
```

Báo user:
```
Dashboard đã khởi động → http://localhost:5765

Mở trình duyệt và truy cập địa chỉ trên.
Dashboard tự cập nhật mỗi 2 giây khi /team đang chạy.

Để dừng: kill $(lsof -ti:5765)
```
