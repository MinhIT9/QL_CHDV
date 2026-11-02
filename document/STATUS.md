# Tiến độ thực tế

Cập nhật: 2026-11-02 (Asia/Saigon). Phiên bản hội thoại: V1.1.6.

Đã triển khai phần phí/hợp đồng theo FEES_CONTRACTS_PROPOSAL.md: lưu đơn giá, ngày và lịch nhắc; chưa chia phí giữa tháng hoặc ghi nhận thực thu.

**Đã triển khai V1 chạy local bằng Flask + SQLite. Chưa triển khai production.**

| Hạng mục | Trạng thái | Bằng chứng / giới hạn |
| --- | --- | --- |
| Flask factory, cấu hình .env | Đã có | app/__init__.py, wsgi.py; SECRET_KEY bắt buộc |
| Database, migrations | Đã có | Migration b71c430e92ad đã áp dụng local sau backup; WAL/FK/busy timeout |
| Root ban đầu | Đã tạo local | init-admin; mật khẩu ngoài Git, phải đổi lần đầu |
| Login/logout/đổi mật khẩu | Đã có | CSRF, scrypt, chặn nghiệp vụ khi chưa đổi pass |
| Quản lý tài khoản | Đã có | Chỉ root tạo/khóa/reset Admin; không khóa/reset root qua danh sách |
| Vô hiệu hóa phiên cũ | Đã có | Xoay token khi đổi/reset pass, khóa/mở tài khoản |
| Khóa tạm đăng nhập | Đã có | 5 lần sai khóa 5 phút; chưa rate limit theo IP ở proxy |
| Danh sách phòng | Đã có | Tìm mã/tên khách, xem điện theo kỳ, bảng cuộn ngang |
| Thêm/sửa phòng | Đã có | Mã duy nhất, nhiều người/xe mỗi dòng, đếm người tự động |
| Lịch sử khách thuê | Đã có | Chọn đổi khách mới để giữ đợt thuê cũ |
| Xóa/ngừng sử dụng phòng | Đã có | Có đợt thuê/điện thì ngừng sử dụng, giữ lịch sử |
| Chốt điện theo tháng | Đã có | Số nguyên, lưu từng phần, chống trùng kỳ, giao dịch nguyên tử |
| Chi tiết phòng | Đã có | Khách hiện tại, lịch sử thuê và điện |
| Giao diện | Đã có | Jinja2 + CSS riêng + HTMX 2.0.4 nội bộ; chưa Bootstrap/Alpine |
| Backup | Có CLI thủ công | SQLite Backup API, đích mới; chưa lịch hoặc lưu ngoài máy |
| Phí nước/dịch vụ | Đã có | Theo đợt thuê, nguyên VND >=0, NULL legacy không phải miễn phí |
| Ngày hợp đồng/trả phòng | Đã có | DATE riêng; không dùng ngày tạo record để suy diễn |
| Gia hạn hợp đồng | Đã có | Xem trước/xác nhận; audit, giữ ngày neo, optimistic lock |
| Ngày đóng tiền | Có lịch nhắc | Ngày 1–31, tháng ngắn lấy cuối tháng; chưa ghi nhận đã đóng/còn nợ |
| Ngày bắt đầu thống nhất | Đã có | Gộp ngày vào ở vào contract_start; không còn ô nhập ngày vào riêng |
| Tiền cọc | Đã có | Theo đợt thuê, cho phép 0; chưa ghi nhận thu/hoàn cọc |
| Tiền phòng | Đã có | Theo tháng/đợt thuê, cho phép 0; giá cũ thiếu giữ NULL; tổng dự tính phòng+nước+dịch vụ chưa điện/cọc |
| Kiểm thử | 31 test pass | unittest, CSRF thật, migration rỗng và có dữ liệu cũ |
| Model/migration khớp nhau | Đã kiểm tra | flask db check không có schema drift |
| Browser/production | Chưa kiểm tra / triển khai | Chưa browser QA, HTTPS, reverse proxy, job backup |

## Giới hạn nghiệp vụ

- Không sửa/xóa điện đã chốt; chưa có audit điều chỉnh hoặc thay đồng hồ.
- Không chèn kỳ trước khi đã có kỳ sau. Nếu có lịch sử, chỉ chốt nối tiếp kỳ liền trước.
- Phòng trống vẫn ghi điện. Phòng ngừng sử dụng không có trong bảng nhập.
- Chỉ số nguyên 0–2.147.483.647. Không chia tiền theo đợt thuê giữa tháng.
- Chưa dashboard, hóa đơn/thực thu, nhiều tòa hoặc tài khoản chỉ xem.
- Đã có đơn giá nước/dịch vụ và ước tính tháng đủ theo số người hiện tại; chưa có hóa đơn, chốt số người tính phí/snapshot từng kỳ hoặc thực thu. Đổi giá không được hiểu là tính lại hóa đơn cũ.
- Gia hạn 1–120 tháng từ hạn cũ; hợp đồng quá hạn cần xác nhận. Hết hạn không tự trả phòng; đợt đã trả không gia hạn. Dữ liệu cũ có thể bổ sung dần; đợt mới cần đủ phí/ngày/lịch đóng.
- HTMX tăng tốc điều hướng; form POST thông thường. Thêm/sửa phòng là trang riêng, chưa popup.

Cách chạy và bằng chứng xem DEVELOPMENT.md, HANDOFF.md.
