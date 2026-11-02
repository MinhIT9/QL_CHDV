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

## Mở rộng đã triển khai — V1.1.4

- Đơn giá nước/người/tháng và dịch vụ/phòng/tháng theo đợt thuê; cho phép 0. Không tự áp giá ví dụ cho dữ liệu cũ.
- Ngày vào thực tế, bắt đầu/hết hạn hợp đồng, trả phòng thực tế; lịch đóng tiền ngày 1–31 hằng tháng, tháng ngắn lấy ngày cuối tháng.
- Gia hạn hợp đồng đang thuê, 1–120 tháng từ hạn cũ; giữ ngày neo, xem trước/xác nhận, lịch sử Admin/thời điểm/hạn cũ-mới; chặn stale form và ghi đồng thời.
- Hợp đồng hết hạn không tự trả phòng. Đổi khách/ngừng sử dụng có khách phải xác nhận ngày trả thực tế.
- Chỉ lưu đơn giá và lịch nhắc; dự tính tháng đủ theo người hiện tại không phải hóa đơn. Chưa chia ngày, chốt số người tính phí, snapshot khoản phải thu hoặc ghi nhận thực thu.

## Điều chỉnh V1.1.5

- Ngày vào ở và ngày bắt đầu gộp thành Ngày bắt đầu hợp đồng; không nhập hai ngày độc lập.
- Tiền cọc theo đợt thuê, cho phép 0; hiển thị trong bảng/form/chi tiết/lịch sử, không tính vào phí tháng và chưa quản lý thực thu/hoàn cọc.

## Điều chỉnh V1.1.6

- Tiền phòng/tháng theo đợt thuê, cho phép 0, hiển thị form/bảng/chi tiết/lịch sử. Tổng dự tính gồm phòng+nước+dịch vụ, không gồm điện/cọc; chưa chia ngày hoặc tạo hóa đơn.
