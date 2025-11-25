# API Summary

This file summarizes the main APIs in the project. Each section below contains a properly formatted Markdown table with: Path | Method | Parameters | Auth required | Response format | Short description.

---

## 1️⃣ Authentication API

| Path | Method | Parameters | Auth required | Response format | Description |
|---|---:|---|:---:|---|---|
| /api/login | POST | body: {"username", "password"} | Yes | JSON {"token": "...", "role": "..."} | Đăng nhập (username, password). Trả về token + role |
| /api/logout | POST | headers/session | Yes | JSON {"success": true} | Đăng xuất, hủy token hiện tại |
| /api/change-password | POST | body: {"old_password","new_password"} | Yes | JSON {"success": true} | Đổi mật khẩu cho tài khoản hiện tại |
| /api/change-pin | POST | body: {"old_pin","new_pin"} | Yes | JSON {"success": true} | Đổi mã PIN cho tài khoản |

---

## 2️⃣ User Management API (Admin)

| Path | Method | Parameters | Auth required | Response format | Description |
|---|---:|---|:---:|---|---|
| /api/users | GET | query: ?query, ?status, ?shift, ?page, ?page_size | Yes (admin) | JSON {"nguoi_list": [...], "total": N} | Lấy danh sách nhân viên |
| /api/users/{id} | GET | path: id | Yes (admin or self) | JSON {"id", "username", "full_name", ...} | Xem thông tin chi tiết nhân viên |
| /api/add-users | POST | form/multipart: {full_name, age, phone, shift, address, gender, role, pin, avatar} | Yes (admin) | JSON {"success": true, "id": new_id} | Thêm mới nhân viên |
| /api/edit-users/{id} | PUT | path: id, body: {fields...} | Yes (admin) | JSON {"success": true} | Cập nhật thông tin nhân viên |
| /api/edit-users/{id}/shift | PUT | path: id, body: {"new_shift", "admin_pin"} | Yes (admin + PIN) | JSON {"success": true} | Thay đổi ca làm nhân viên |
| /api/edit-users/{id}/reset-password | POST | path: id, body: {"admin_pin"} | Yes (admin + PIN) | JSON {"success": true} | Reset mật khẩu nhân viên |
| /api/edit-users/{id}/resign | PUT | path: id, body: {"admin_pin","note"} | Yes (admin + PIN) | JSON {"success": true} | Đánh dấu nghỉ việc (status="resigned") |
| /api/edit-users/{id}/avatar | POST | path: id, file: avatar image | Yes (admin) | JSON {"success": true} | Cập nhật ảnh đại diện (BLOB) |

---

## 4️⃣ Face & Emotion API (RPI + Admin)

| Path | Method | Parameters | Auth required | Response format | Description |
|---|---:|---|:---:|---|---|
| /api/faces | POST | form/multipart: {user_id, file:image} | No (RPI public) | JSON {"success": true, "image_id": id} | RPI gửi ảnh khuôn mặt để thêm/cập nhật |
| /api/faces/{user_id} | GET | path: user_id, query: include_image_base64 | No | JSON {"khuonmats": [...]} | Lấy danh sách khuôn mặt của nhân viên |
| /api/add-emotion | POST | form/multipart: {user_id, camera_id, emotion_type, confidence, image, note} | No (RPI public) | JSON {"success": true, "id": new_id} | Gửi log cảm xúc (ảnh + metadata) |
| /api/emotion | GET | query: user_id, emotion_type, start_ts, end_ts, limit, offset | Yes (or public) | JSON {"emotion_logs": [...]} | Truy vấn danh sách emotion log |
| /api/delete-emotion/{id} | DELETE | path: id, body: {"admin_pin"} | Yes (admin + PIN) | JSON {"success": true} | Xóa một bản ghi emotion log |

---

## 5️⃣ Check-in / Check-out API

| Path | Method | Parameters | Auth required | Response format | Description |
|---|---:|---|:---:|---|---|
| /api/checkin/{id} | POST | path: id or form: {user_id}, note optional | No (RPI public) | JSON {"success": true, "id": rowid, "status": "on_time"} | Tạo check-in cho nhân viên |
| /api/checkout/{id} | POST | path: id or form: {user_id}, note optional | No (RPI public) | JSON {"success": true, "id": rowid, "status": "early|on_time|late"} | Tạo check-out cho nhân viên |
| /api/checklog | GET | query: date, date_from, date_to, full_name, status, limit, offset | Yes (admin/staff) | JSON {"checklogs": [...]} | Xem danh sách chấm công |
| /api/edit-checklog/{id} | PUT | path: id, body: {"status","note","admin_pin"} | Yes (admin + PIN) | JSON {"success": true} | Sửa trạng thái chấm công |
| /api/edit-checklog | PUT | body: {"user_id","date","status","note","admin_pin"} | Yes (admin + PIN) | JSON {"success": true} | Sửa chấm công theo user+date |

---

## 6️⃣ KPI Report API

| Path | Method | Parameters | Auth required | Response format | Description |
|---|---:|---|:---:|---|---|
| /api/kpi | GET | query: date (YYYY-MM-DD), month (YYYY-MM), full_name, limit, offset | No | JSON {"success": true, "kpis": [...]} | Xem danh sách KPI |
| /api/kpi/{user_id} | GET | path: user_id, query: date, month, limit, offset | No | JSON {"success": true, "kpis": [...]} | Xem chi tiết KPI của nhân viên |
| /api/kpi/calculate | POST | body: {"date"} | Yes (admin) | JSON {"success": true} | Tính KPI hằng ngày |

---

## System / Support APIs

| Path | Method | Parameters | Auth required | Response format | Description |
|---|---:|---|:---:|---|---|
| /api/system/pin-verify | POST | body: {"user_id" or "username", "pin"} | No (public) | JSON {"success": true} | Kiểm tra mã PIN hợp lệ trước thao tác nhạy cảm |

---

