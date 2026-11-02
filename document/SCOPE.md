# Phạm vi V1

## Mục tiêu

Quản lý CHDV ban đầu khoảng 7 phòng, một Admin, ưu tiên bảng và thao tác nhập nhanh. Không có dashboard biểu đồ, quản lý tiền hoặc báo cáo trong V1.

## Năm màn hình

1. Đăng nhập Admin bằng tài khoản và mật khẩu.
2. Danh sách phòng: mã, trạng thái, khách chính, số người, người ở cùng, xe và điện theo kỳ.
3. Thêm/sửa phòng: thông tin phòng và khách, danh sách người ở cùng, nhiều biển số.
4. Chốt điện: chọn kỳ, nhập chỉ số cuối, hiển thị đầu kỳ và tiêu thụ.
5. Chi tiết phòng: thông tin hiện tại và lịch sử điện.

## Quy tắc đã nêu

- Mã phòng duy nhất; một phòng có nhiều người ở cùng và nhiều xe.
- Chỉ Admin được thêm/sửa/xóa phòng.
- Phòng có lịch sử được chuyển ngừng sử dụng thay vì xóa vĩnh viễn.
- Tiêu thụ = chỉ số cuối - chỉ số đầu.
- Đầu kỳ lấy từ cuối kỳ trước; lần đầu được nhập thủ công.
- Không chấp nhận cuối kỳ nhỏ hơn đầu kỳ. Thay đồng hồ là trường hợp riêng.
- Giữ lịch sử từng kỳ, không ghi đè lịch sử cũ.

## Quy tắc đã chọn khi triển khai V1 (2026-11-02)

- Ba trạng thái: trống, đang thuê, ngừng sử dụng.
- Số người tự tính từ khách chính và người ở cùng.
- Lưu đợt thuê để không mất khách cũ khi đổi khách.
- Một bản chốt cho mỗi phòng/kỳ; V1 chưa mở sửa/xóa bản chốt, chưa có audit điều chỉnh.
- Cho lưu một phần danh sách phòng; phòng trống vẫn được ghi điện.
- Khi thiếu kỳ trước, yêu cầu xử lý rõ thay vì coi tiêu thụ nhiều tháng là một tháng.
- Thay đồng hồ tạm hoãn trong V1; không chèn lùi khi đã có kỳ sau.
- Chỉ số điện nguyên kWh. Người/xe mỗi dòng; số người tự tính; đợt thuê giữ khách cũ.
- Root quản lý tài khoản; tài khoản mới và root bootstrap bắt đổi pass lần đầu, ít nhất 8 ký tự.

Trạng thái và giới hạn thực tế xem `STATUS.md`; quyết định xem `DECISIONS.md`.
