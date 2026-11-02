# Mô hình dữ liệu V1

Đã triển khai tại app/models/__init__.py; migration đầu: e9329a770fe9.

| Bảng | Dữ liệu chính | Ràng buộc / quan hệ |
| --- | --- | --- |
| user | username, password_hash, is_root, enabled, must_change_password, session_token, failed_logins, locked_until | Username/token duy nhất; scrypt hash |
| room | code, active, note | Code chữ hoa, duy nhất |
| tenancy | room_id, tenant_name, started_at, ended_at | Partial unique index: một đợt mở mỗi phòng |
| occupant | tenancy_id, name | Nhiều người/đợt, không gồm khách chính |
| vehicle | tenancy_id, plate | Nhiều xe/đợt |
| electricity_reading | room_id, period, start_value, end_value, created_by, created_at | Unique phòng/kỳ, check 0 <= đầu <= cuối |

## Quy ước

- Quan hệ dùng ID nội bộ; đổi mã phòng không mất lịch sử.
- active=false là ngừng sử dụng. Active + tenancy mở là đang thuê, không có là trống.
- Số người = 1 khách chính + occupant; không lưu số người độc lập.
- Chọn đổi khách mới kết thúc tenancy cũ; sửa chính tả thông thường sửa đợt đang mở.
- Người/xe mỗi dòng; bỏ trống/trùng hoàn toàn, tối đa 30 dòng mỗi danh sách. Biển số chữ hoa, chưa kiểm định pháp lý.
- Kỳ YYYY-MM; chỉ số nguyên kWh trong khoảng 0–2.147.483.647.
- Phòng trống vẫn chốt điện. Đầu kỳ lần đầu nhập tay, sau đó nối tháng liền trước.
- Chưa có bảng revision hoặc meter: không sửa điện cũ/thay đồng hồ.
- Thời gian lưu UTC, ngày giao diện UTC+7. Chưa chia tiền/điện theo đợt thuê.
