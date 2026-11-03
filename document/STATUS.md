# Tiến độ thực tế

Cập nhật: 2026-11-03 (Asia/Saigon). Phiên bản hội thoại: V1.1.12.

V1.1.12 chỉ chỉnh layout chốt tiền full-width và preview hai cột desktop; không đổi nghiệp vụ/DB. Kiểm tra render module billing, chưa browser QA cho layout mới.

Đã triển khai sửa điện có audit và chốt tiền từng kỳ theo phương án gọn: phòng/điện cùng tháng, không thực thu/công nợ/chia ngày.

Đã triển khai phần phí/hợp đồng theo FEES_CONTRACTS_PROPOSAL.md: lưu đơn giá, ngày và lịch nhắc; chưa chia phí giữa tháng hoặc ghi nhận thực thu.

**Đã triển khai V1 chạy local bằng Flask + SQLite. Chưa triển khai production.**

| Hạng mục | Trạng thái | Bằng chứng / giới hạn |
| --- | --- | --- |
| Flask factory, cấu hình .env | Đã có | app/__init__.py, wsgi.py; SECRET_KEY bắt buộc |
| Database, migrations | Đã có | Migration d94f512a37b1 đã áp dụng local sau backup; WAL/FK/busy timeout |
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
| Giao diện | Đã nâng cấp V1.1.7 | Jinja2 + CSS riêng + SVG nội bộ; sidebar, login hai cột, bảng sticky, responsive; giữ nguyên chức năng |
| Backup | Có CLI thủ công | SQLite Backup API, đích mới; chưa lịch hoặc lưu ngoài máy |
| Phí nước/dịch vụ | Đã có | Theo đợt thuê, nguyên VND >=0, NULL legacy không phải miễn phí |
| Ngày hợp đồng/trả phòng | Đã có | DATE riêng; không dùng ngày tạo record để suy diễn |
| Gia hạn hợp đồng | Đã có | Xem trước/xác nhận; audit, giữ ngày neo, optimistic lock |
| Ngày đóng tiền | Có lịch nhắc | Ngày 1–31, tháng ngắn lấy cuối tháng; chưa ghi nhận đã đóng/còn nợ |
| Ngày bắt đầu thống nhất | Đã có | Gộp ngày vào ở vào contract_start; không còn ô nhập ngày vào riêng |
| Tiền cọc | Đã có | Theo đợt thuê, cho phép 0; chưa ghi nhận thu/hoàn cọc |
| Tiền phòng | Đã có | Theo tháng/đợt thuê, cho phép 0; giá cũ thiếu giữ NULL; tổng dự tính phòng+nước+dịch vụ chưa điện/cọc |
| Sửa số điện | Đã có | Preview, lý do, audit, cập nhật đầu kỳ sau; chặn nếu phiếu hiệu lực bị ảnh hưởng |
| Chốt tiền tháng | Đã có | Snapshot phòng/nước/dịch vụ/điện/người/hạn; chống trùng; root hủy có lý do và giữ lịch sử |
| Giá điện theo phòng | Đã có | Theo đợt thuê, cho phép 0; phiếu mới lấy giá hiện tại, phiếu cũ giữ snapshot |
| Ngày chốt/cập nhật điện | Đã có | Thời điểm tạo và revision gần nhất, hiển thị ngày giờ UTC+7 |
| Tiền điện ngay trên bảng | Đã có | Tính khi nhập; lưu snapshot giá; ưu tiên giá phiếu đã chốt; legacy thiếu giá có nhãn tạm tính |
| Kiểm thử | 41 test pass | unittest, migration và Node smoke test tính tiền live |
| Model/migration khớp nhau | Đã kiểm tra | flask db check không có schema drift |
| Browser/production | Có kiểm tra hình ảnh / chưa production | Edge headless với HTML dữ liệu giả ở desktop và root rộng 390px; chưa kiểm tra tương tác E2E, HTTPS, proxy, job backup |

## Giới hạn nghiệp vụ

- Sửa điện có lịch sử; không xóa lịch sử, chưa hỗ trợ thay đồng hồ. Root cần hủy phiếu tiền hiệu lực bị ảnh hưởng trước khi điều chỉnh điện.
- Không chèn kỳ trước khi đã có kỳ sau. Nếu có lịch sử, chỉ chốt nối tiếp kỳ liền trước.
- Phòng trống vẫn ghi điện. Phòng ngừng sử dụng không có trong bảng nhập.
- Chỉ số nguyên 0–2.147.483.647. Không chia tiền theo đợt thuê giữa tháng.
- Chưa dashboard, thực thu/công nợ, nhiều tòa hoặc tài khoản chỉ xem. Phiếu tiền là bảng tính nội bộ, không phải hóa đơn thuế.
- Phiếu đã chốt giữ snapshot giá/người/chỉ số; giá phiếu mới lấy từ thông tin phòng hiện tại. Form cũ bị chặn khi version đổi. Lập bù/lập lại kỳ cũ cũng gợi ý giá hiện tại; cần kiểm tra giá kỳ. Chưa lịch giá tự động hoặc điện khác tháng tiền phòng.
- Chưa lưu nháp dài hạn: màn hình xem trước rồi chốt trong một phiên. Kỳ vào/trả giữa tháng hoặc đổi khách bị chặn; chưa chia điện theo khách. Root hủy phiếu không có nghĩa hoàn tiền đã thu ngoài hệ thống.
- Gia hạn 1–120 tháng từ hạn cũ; hợp đồng quá hạn cần xác nhận. Hết hạn không tự trả phòng; đợt đã trả không gia hạn. Dữ liệu cũ có thể bổ sung dần; đợt mới cần đủ phí/ngày/lịch đóng.
- HTMX tăng tốc điều hướng; form POST thông thường. Thêm/sửa phòng là trang riêng, chưa popup.

Cách chạy và bằng chứng xem DEVELOPMENT.md, HANDOFF.md.
