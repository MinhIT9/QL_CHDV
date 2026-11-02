# Mô hình dữ liệu đề xuất

**Chưa có model/schema/migration.** Tên và quan hệ dưới đây phục vụ thảo luận trước triển khai.

| Thực thể | Dữ liệu chính | Quan hệ / ràng buộc dự kiến |
| --- | --- | --- |
| Admin | Tài khoản, password hash, trạng thái | Tài khoản duy nhất; không lưu mật khẩu thô |
| Room | ID, mã phòng, trạng thái sử dụng, ghi chú | Mã duy nhất; không xóa khi có lịch sử |
| Tenancy | Phòng, khách chính, ngày vào/ra | Một đợt thuê đang hoạt động mỗi phòng |
| Occupant | Đợt thuê, tên người ở cùng | Nhiều người mỗi đợt thuê |
| Vehicle | Đợt thuê, biển số | Nhiều xe mỗi đợt thuê |
| ElectricityReading | Phòng, kỳ, ngày ghi, đầu/cuối kỳ | Một bản có hiệu lực mỗi phòng/kỳ |
| ReadingRevision | Bản chốt, giá trị cũ/mới, lý do, Admin, thời điểm | Lưu dấu vết điều chỉnh |

## Cần giải quyết khi thiết kế schema

- Tách trạng thái ngừng sử dụng khỏi trạng thái có khách để tránh hai nguồn thông tin mâu thuẫn.
- Xác định độ chính xác số điện trước khi chọn kiểu dữ liệu; nếu có thập phân, không dùng float cho tính toán cần chính xác.
- Khi sửa kỳ trước, kiểm tra ảnh hưởng tới đầu kỳ sau; giữ lịch sử cũ.
- Mã phòng đổi không làm mất liên kết: quan hệ dùng ID nội bộ.
- Ngày giờ lưu và hiển thị cần quy ước thống nhất; giao diện dùng Asia/Saigon.
- Thay đồng hồ có thể cần thực thể đồng hồ và các đoạn tiêu thụ riêng; chưa chốt trong V1.
- Đổi khách giữa tháng chưa bao gồm tính/chia tiền điện.
