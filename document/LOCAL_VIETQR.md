# QR nhận tiền cục bộ

V1.7.0: Đã hiện thực QR chuyển khoản tạo cục bộ bằng qrcode 8.2, TLV NAPAS/QRIBFTTA, CRC16-CCITT. Không gọi dịch vụ bên ngoài hoặc lưu ảnh cho từng phiếu. Dropdown 48 ngân hàng từ snapshot API Banks ngày 2026-11-04 ở app/data/banks.json; không có tác vụ mạng runtime. Admin chọn BIN và điền STK (giữ số 0 đầu, 1–19 ký tự ASCII chữ/số), tên chủ tài khoản, ghi chú. Máy chủ lấy ngân hàng từ allowlist, không tin tên ngân hàng gửi từ form. Ghi chú chỉ hiển thị trên phiếu, nội dung QR tự tạo theo P{id} {room} T{mmyyyy}; tiền dùng bill.total sau điều chỉnh, không nhận override từ query string.

Migration d57032b19f64 thêm bank_bin nullable, không đoán BIN từ tên cũ; admin cấu hình ngân hàng để bật QR mới. Ảnh QR cũ được giữ và dùng fallback khi chưa có BIN, không xóa dữ liệu cũ. QR đã thu/hủy/0 đồng không được phát; tổng trên 13 chữ số không sinh QR nhưng vẫn mở phiếu được. Thông tin nhận tiền là cấu hình chung hiện tại. Tên chủ TK không tự xác minh; không tự ghi nhận đã thu khi tạo/quét QR.

DEV đã backup backups/pre-local-vietqr-v162.sqlite3 và upgrade/db check đạt. QR đối chiếu vector nguồn độc lập và đọc ngược PNG bằng ZXing-C++; Edge kiểm tra QR từng phiếu chứa số cuối cùng 1.234 thay vì query giả 1, STK/nội dung đúng, QR crop trên mobile đọc được, responsive/in và regression ảnh điện đạt. ZXing-C++ chỉ dùng QA, không cần cài trên VPS. Chưa quét bằng app ngân hàng thật hoặc triển khai VPS, không xác nhận tương thích thực tế với mọi ngân hàng. Cần cài requirements mới, migration rồi restart web/worker khi đưa lên VPS; quét thử bằng ngân hàng để đối chiếu người nhận/số tiền/nội dung trước khi dùng gửi khách.

## Cách thử

1. Restart web dev, Ctrl+F5; mở Nhận tiền, chọn ngân hàng và lưu tài khoản.
2. Quét QR tài khoản ở cấu hình (không kèm tiền) để đối chiếu người nhận.
3. Mở phiếu chưa thu qua ID; quét QR có tiền/nội dung theo phiếu, kiểm tra khớp số cuối cùng. Không cần thực hiện chuyển tiền khi chỉ kiểm tra.

QR không chứa tên khách/ghi chú tùy ý. Tên chủ tài khoản chỉ để hiển thị; người nhận được ngân hàng tra cứu theo BIN/STK.

## Nguồn và kiểm tra

- Danh sách ngân hàng: https://www.vietqr.io/api-bank ; snapshot https://api.vietqr.io/v2/banks . Danh sách có thể đổi; cập nhật file có kiểm tra khi cần, không gọi API mỗi lần mở trang.
- Tham chiếu cấu trúc TLV và vector: https://github.com/sunary/vietqr/blob/master/encode.go và https://github.com/sunary/vietqr/blob/master/vietqr_test.go . Không tuyên bố NAPAS chứng nhận triển khai này.
- Thư viện QR: https://pypi.org/project/qrcode/8.2/ . Không chèn logo giữa mã; có quiet zone, PNG đen trắng.
- QA tùy chọn: cài playwright và zxing-cpp, chạy scripts/check_meter_photo_browser.py. Không thêm ZXing vào dependencies vận hành.

## VPS

Gói exports/chdv-v1.7.0.zip gồm code, dependencies, migrations, tests và tài liệu; không chứa .env, SQLite, uploads hay venv. Khi cập nhật: dừng chdv và chdv-photos, backup nhất quán DB/uploads nếu cần, giải nén vào /opt/chdv, cấp lại owner chdv cho code, cài requirements.txt, flask db upgrade và db check, chạy tests, mở lại hai service. Giữ .env và instance trên VPS. Không cài script QA browser trên VPS. Chưa tự chạy các bước này qua SSH.

Kiểm tra V1.7.0: 78 unittest OK (50.165s), DB check/integrity đạt, cột dữ liệu cũ giữ nguyên so với backup. Edge đọc được QR ảnh gốc/crop mobile qua ZXing; không pageerror. Chưa quét app ngân hàng thật.
