# Mô hình dữ liệu V1

Đã triển khai tại app/models/__init__.py; migration mới nhất b71c430e92ad (tiền phòng).

| Bảng | Dữ liệu chính | Ràng buộc / quan hệ |
| --- | --- | --- |
| user | username, password_hash, is_root, enabled, must_change_password, session_token, failed_logins, locked_until | Username/token duy nhất; scrypt hash |
| room | code, active, note | Code chữ hoa, duy nhất |
| tenancy | room_id, tenant_name, started_at/ended_at, move_in_date/move_out_date, contract_start/end, contract_anchor_day, water_price, service_price, payment_day, version | Một đợt mở/phòng; CHECK phí >=0, ngày hợp lệ; optimistic version |
| contract_renewal | tenancy_id, old_end, new_end, months, note, created_by/at | Một lần gia hạn/hạn cũ, tháng 1–120, hạn mới > cũ, FK Admin/đợt thuê |
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
- Giá VND nguyên 0–2.147.483.647; NULL là chưa biết ở legacy. Dự tính nước = số người hiện tại x giá, cộng dịch vụ; chưa có hóa đơn hoặc snapshot kỳ.
- Ngày vào/trả thực tế và hợp đồng là DATE; started_at/ended_at vẫn là audit hệ thống. Bản cũ không tự điền ngày/phí.
- Gia hạn giữ ngày neo và đợt thuê; khi đã có gia hạn chặn sửa ngày hợp đồng trực tiếp. Đổi khách cần ngày trả khách cũ <= ngày vào khách mới.
- payment_day 1–31; ngày đến hạn kỳ chọn được tính lịch tham chiếu, không lưu xác nhận đã thanh toán.

## Quy tắc thay thế từ V1.1.5

- contract_start là ngày bắt đầu hợp đồng và cũng là ngày vào ở duy nhất. move_in_date chỉ còn cột legacy để không mất dữ liệu cũ; không có input hay nghiệp vụ riêng. Save/checkout đồng bộ nó theo contract_start để tương thích CHECK cũ.
- Migration ưu tiên contract_start đã có; chỉ điền từ move_in_date khi thiếu và không trái ngày hết hạn/trả phòng. Trường hợp mâu thuẫn vẫn cần Admin bổ sung, không tự chọn một ngày sai.
- deposit_amount là tiền cọc thỏa thuận của đợt thuê, VND nguyên 0–2.147.483.647. NULL là chưa cập nhật; đợt mới cần nhập, 0 khi không cọc. Giữ qua gia hạn và theo lịch sử đợt thuê.
- Tiền cọc không cộng vào monthly_fees; không suy diễn đã thu/hoàn/khấu trừ cọc.

## Tiền phòng V1.1.6

- Tenancy.rent_price: số nguyên VND/tháng từ 0 đến 2.147.483.647. Đợt mới nhập bắt buộc; dữ liệu cũ giữ NULL và hiển thị chưa cập nhật.
- monthly_fees vẫn là nước + dịch vụ; monthly_total thêm tiền phòng, trả None khi thiếu giá thành phần. Không cộng điện hoặc cọc, chưa chia ngày hoặc chốt hóa đơn.
- Gia hạn giữ nguyên rent_price; đổi khách mới nhập giá riêng và giữ giá đợt cũ trong lịch sử.
