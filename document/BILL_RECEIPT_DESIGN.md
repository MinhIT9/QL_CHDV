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

## V1.7.0 — Tạo QR cục bộ

V1.7.0: Đã hiện thực QR chuyển khoản tạo cục bộ bằng qrcode 8.2, TLV NAPAS/QRIBFTTA, CRC16-CCITT. Không gọi dịch vụ bên ngoài hoặc lưu ảnh cho từng phiếu. Dropdown 48 ngân hàng từ snapshot API Banks ngày 2026-11-04 ở app/data/banks.json; không có tác vụ mạng runtime. Admin chọn BIN và điền STK (giữ số 0 đầu, 1–19 ký tự ASCII chữ/số), tên chủ tài khoản, ghi chú. Máy chủ lấy ngân hàng từ allowlist, không tin tên ngân hàng gửi từ form. Ghi chú chỉ hiển thị trên phiếu, nội dung QR tự tạo theo P{id} {room} T{mmyyyy}; tiền dùng bill.total sau điều chỉnh, không nhận override từ query string.

Migration d57032b19f64 thêm bank_bin nullable, không đoán BIN từ tên cũ; admin cấu hình ngân hàng để bật QR mới. Ảnh QR cũ được giữ và dùng fallback khi chưa có BIN, không xóa dữ liệu cũ. QR đã thu/hủy/0 đồng không được phát; tổng trên 13 chữ số không sinh QR nhưng vẫn mở phiếu được. Thông tin nhận tiền là cấu hình chung hiện tại. Tên chủ TK không tự xác minh; không tự ghi nhận đã thu khi tạo/quét QR.

DEV đã backup backups/pre-local-vietqr-v162.sqlite3 và upgrade/db check đạt. QR đối chiếu vector nguồn độc lập và đọc ngược PNG bằng ZXing-C++; Edge kiểm tra QR từng phiếu chứa số cuối cùng 1.234 thay vì query giả 1, STK/nội dung đúng, QR crop trên mobile đọc được, responsive/in và regression ảnh điện đạt. ZXing-C++ chỉ dùng QA, không cần cài trên VPS. Chưa quét bằng app ngân hàng thật hoặc triển khai VPS, không xác nhận tương thích thực tế với mọi ngân hàng. Cần cài requirements mới, migration rồi restart web/worker khi đưa lên VPS; quét thử bằng ngân hàng để đối chiếu người nhận/số tiền/nội dung trước khi dùng gửi khách.

## V1.10.0 — Xuất PNG tại client

receipt.js dùng html2canvas 1.4.1 nội bộ + Canvas/Blob để chụp .receipt-sheet, rộng 800 CSS px/scale 2; QR dùng pixel ảnh đã decode. Dialog ngoài card chứa preview/download/Web Share theo capability detection. Không upload hoặc lưu ảnh tại máy chủ. Tạo ảnh trước rồi bấm share riêng để đáp ứng transient user activation. Tải PNG là fallback; không hứa tự ghi vào album trên mọi điện thoại. Không thay CSP, quyền, dữ liệu hoặc API. Bỏ bằng chữ trên phiếu, trạng thái nhỏ cạnh kỳ và tổng một dòng.

Nguồn: https://html2canvas.hertzen.com/configuration ; https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share ; https://developer.mozilla.org/en-US/docs/Web/API/Navigator/canShare . Thư viện: app/static/vendor/html2canvas.min.js, MIT tại HTML2CANVAS-LICENSE.txt; SHA256 e87e550794322e574a1fda0c1549a3c70dae5a93d9113417a429016838eab8cb. Chưa thử native album iOS/Android, không tuyên bố đã triển khai VPS.
