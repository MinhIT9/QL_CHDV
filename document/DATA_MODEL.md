# Mô hình dữ liệu V1

Đã triển khai tại app/models/__init__.py; migration mới nhất f13a98c52b70 (ảnh riêng tư).

## Photo — V1.3.0

- token ngẫu nhiên duy nhất; tenancy_id hoặc reading_id (CHECK đúng một chủ sở hữu), created_by/at, status pending/ready/failed (CHECK). Không lưu blob/đường dẫn từ khách vào DB. FK RESTRICT giữ liên kết lịch sử.
- Byte gốc ở instance/uploads/tmp trong lúc chờ; file dài hạn là WebP ở contracts/electricity. Tên file theo token, không theo tên khách hoặc tên upload. Xem PHOTOS.md về worker, crash recovery và backup.
- V1.4.0: ảnh hợp đồng và ảnh chốt/sửa điện đều tùy chọn. Không backfill, ảnh cũ không bị thay thế khi sửa số. Token có thể do client tạo theo định dạng hex32 để retry upload bổ sung không trùng, máy chủ kiểm tra token/owner/user trước tái sử dụng. Không migration mới. Ảnh có thể bổ sung, chưa có UI xóa ảnh đã lưu.

## Receipt — V1.1.14

- bill_id, amount (BigInteger VND), paid_date, note, created_by/at; reversed_at/by/reason khi root hoàn tác. Không xóa bản ghi.
- Partial unique index một receipt chưa hoàn tác mỗi phiếu. Amount lấy bill.total ở server, không tin client; 0 hợp lệ khi phiếu0đ.
- MonthlyBill.paid_receipt suy ra từ receipt hiệu lực, không có cờ paid ở Room. Thu tháng trước không làm tháng sau thành đã thu.
- Phiếu đã thu không được hủy; root cần hoàn tác receipt trước. Hoàn tác không đồng nghĩa hoàn tiền thật. Chưa hỗ trợ thu một phần/khớp ngân hàng.

ElectricityReading.electricity_price nullable là giá chụp lúc lưu số mới; không thay giá phiếu. Migration backfill từ MonthlyBill hiệu lực cùng phòng/kỳ khi có. Ngày chốt là created_at; cập nhật gần nhất lấy từ max ReadingRevision.created_at nên không cần cột updated_at trùng lặp. Bảng hiển thị tiền theo giá phiếu hiệu lực nếu có, rồi giá đọc lưu, cuối cùng giá phòng hiện tại với nhãn tạm tính khi legacy thiếu giá.

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

## Sửa điện và chốt tiền V1.1.9

- reading_revision: reading_id, old_start/end, new_start/end, reason, created_by/at. Chỉnh kỳ trước làm thay đầu kỳ sau thì ghi revision cho cả hai bản ghi.
- monthly_bill: room/tenancy ID và tên/mã snapshot, period, chỉ số điện, bốn đơn giá, số người tính nước, due_date, created_by/at; cancelled_at/by/reason để hủy hiệu lực nhưng giữ bản cũ.
- Partial unique index một phiếu hiệu lực/phòng/kỳ. Tổng tính từ snapshot, không từ Tenancy hiện tại; không cộng cọc. Chưa có Payment hoặc phân bổ thu tiền.
- Điện và tiền phòng cùng tháng, chỉ một đợt thuê đủ tháng. Xác định khách qua contract_start/move_out_date, không tự lấy khách mới cho tháng cũ.
- Ghi SQLite dùng BEGIN IMMEDIATE; kiểm tra stamp chỉ số liên quan và tenancy ID/version trước khi lưu. Hủy phiếu cần root; phiếu hiệu lực chặn sửa điện các kỳ liên quan.
