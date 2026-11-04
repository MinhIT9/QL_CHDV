# Thiết kế phiếu gửi khách — bản mẫu V1.4.17

Ngày: 2026-11-04. Người dùng yêu cầu vẽ trước, chưa viết code. Bản mẫu này đã được hiện thực trên dev ở V1.5.0; nội dung dưới ghi lại thiết kế ban đầu.

## Mở phiếu

Bấm Phiếu #ID dưới mã phòng để mở trang riêng, không có sidebar quản trị trong vùng phiếu. Toolbar Quay lại/In phiếu đặt ngoài card để dễ chụp màn hình, không làm rối nội dung gửi khách. Ưu tiên bố cục dọc, vừa màn hình điện thoại, chữ rõ và bảng tiền căn phải.

## Bố cục và màu sắc

Card trắng, nền ngoài xám xanh rất nhạt; tiêu đề navy và điểm nhấn mint/teal, khoảng cách thoáng. Theo thứ tự: thương hiệu/mã phiếu → tên phiếu/kỳ tháng/trạng thái → phòng/khách/ngày lập/hạn → bảng tiền phòng, nước, dịch vụ, điện kèm chỉ số → khối tổng tiền lớn → số tiền bằng chữ → lời cảm ơn/chú thích phiếu nội bộ.

Bản vẽ dùng dữ liệu minh họa: phòng P301, Khách minh họa, kỳ 11/2026; phòng 4.100.000 + nước 200.000 + dịch vụ 150.000 + điện 156 × 3.600 = 561.600; tổng 5.011.600 đ. Không dùng tên/số tài khoản/dữ liệu khách trong ảnh người dùng gửi. Không thêm QR hoặc thông tin ngân hàng giả.

## Trạng thái nghiệp vụ

- Chưa thu: tiêu đề Phiếu tiền phòng, trạng thái Chưa thanh toán, nhãn Tổng cần thanh toán; không hiển thị xác nhận đã nhận tiền.
- Đã thu đủ: khi triển khai có thể dùng Phiếu thu tiền, trạng thái Đã thanh toán và ngày thu thực tế từ Receipt hiệu lực. Đó là ghi nhận thủ công trong app, không tự kiểm chứng ngân hàng.
- Phiếu hủy: phải hiển thị rõ Đã hủy và không trình bày như khoản đang cần thu hoặc biên nhận còn hiệu lực.
- Giá/chỉ số/người và tổng lấy snapshot phiếu, không tính bằng đơn giá phòng hiện tại. Chú thích Phiếu tính tiền nội bộ · Không phải hóa đơn thuế.

## Hiện trạng

Lượt này dùng skill imagegen, built-in image tool, để vẽ một mockup raster xem trước trong hội thoại; không tích hợp asset hoặc sửa code app. Prompt: phiếu dọc nền trắng/mint/navy, typography tiếng Việt dễ đọc, bảng kê bốn khoản, tổng 5.011.600 đ, trạng thái chưa thanh toán, không sidebar và không thông tin khách thật. Thiết kế cần người dùng xem trước khi triển khai.


## Hiện thực V1.5.0

V1.5.0: Đã triển khai trên dev trang phiếu riêng khi bấm ID, tổng tự tính và số thu cuối cùng kèm lý do bắt buộc khi khác tổng gốc; lịch sử phòng có cả phiếu hủy/đã thu. Máy chủ kiểm tra số nguyên không âm, giữ giá 0; Receipt thu theo số cuối cùng đã chốt. Phiếu cũ dùng tổng snapshot, không đổi tiền đã thu. Phiếu đã chốt bất biến, muốn đổi dùng hủy/lập lại theo quyền hiện có. Trang cần đăng nhập, có tiền bằng chữ, responsive và CSS in ẩn toolbar; chưa có link công khai/xuất ảnh tự động. Migration b35e10f97d42 đã áp dụng DEV sau backup backups/pre-bill-final-20261104-v150.sqlite3. Edge headless đạt desktop/390px/in; ảnh giả ở exports/receipt-preview-desktop.png và exports/receipt-preview-mobile.png. Chưa thử máy in giấy/điện thoại thật hoặc cập nhật VPS. Bước tiếp: restart web dev, Ctrl+F5; triển khai VPS cần upgrade DB trước mở web.

## V1.6.0 — QR nhận tiền

Cấu hình /settings/payment dành cho root/Admin; service payment_settings lưu DB và ảnh riêng dưới uploads/payment. Route ảnh yêu cầu đăng nhập. Thay ảnh lưu file mới trước commit, dọn file cũ sau commit; khi lỗi commit xóa file mới. QR PNG lossless để giữ cạnh mã; không qua worker ảnh điện. Phiếu chưa thu hiển thị QR cạnh tài khoản, phiếu đã thu/hủy ẩn chuyển khoản. Không sinh QR hoặc tự xác minh dữ liệu ngân hàng từ ảnh. Backup cả DB và uploads; migration c46f21a08e53.
