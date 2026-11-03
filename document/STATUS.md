# Tiến độ thực tế

Cập nhật: 2026-11-03 (Asia/Saigon). Phiên bản hội thoại: V1.1.20.

V1.1.20: tách dự tính tiền nước/dịch vụ ở chi tiết; bảng phòng gọn và đầy đủ có số xe/biển số từng dòng, tổng tiền nước theo người và tiền dịch vụ riêng. Giá hiện tại không thay phiếu snapshot. Căn phải tiền, căn giữa số người, biển số dạng nhãn, dòng xen kẽ/hover; giữ cuộn ngang và cột sticky. 5 test receipts và 3 render smoke pass (2 xe, nước 200.000, dịch vụ 150.000); chưa browser QA. Không đổi DB/nghiệp vụ.

V1.1.19: nút ẩn/hiện sidebar trên header, nhớ bằng localStorage có xử lý khi storage bị chặn; nội dung mở rộng khi ẩn. Chỉnh header tên trang/tài khoản và footer. Node syntax và 10 test billing pass; chưa browser QA lượt này. Không đổi nghiệp vụ/DB.

V1.1.18 Việt hóa chọn kỳ tháng tại ba màn hình bằng select Tháng/Năm, giữ dữ liệu YYYY-MM và nút Xem. Chỉ thay template/CSS, không DB/route.

V1.1.17 chỉ làm gọn dòng bảng tiền, trạng thái và nút nằm ngang, giữ cảnh báo quá hạn/popover. Không đổi nghiệp vụ/DB; kiểm tra render/luồng billing và receipts, chưa browser QA cho chỉnh sửa này.

V1.1.16 chỉ hướng dẫn sử dụng chuyển kỳ điện, không sửa app/DB, không chạy lại test. Chọn tháng cần bấm Xem kỳ; đầu kỳ lấy cuối tháng trước, chỉ lưu kỳ không ở tương lai.

V1.1.15 sửa UI menu thu tiền/history thành popover nổi không giãn dòng bảng. 5 test receipt pass và kiểm tra Edge row height128px trước/sau; không đổi nghiệp vụ/DB. Bộ46 test phía dưới là kết quả lượt triển khai trước.

V1.1.14 thêm ghi nhận thu đủ/hoàn tác có lịch sử, sort phiếu và bảng Phòng gọn/lọc theo thu từng kỳ. Chưa thu một phần, kết nối ngân hàng hoặc hoàn tiền tự động.

Đã có sửa điện, chốt tiền và xác nhận nhận đủ từng phiếu; phòng/điện cùng tháng, chưa chia ngày hoặc thu một phần.

Đã có đơn giá/hợp đồng/lịch nhắc; thu tiền là xác nhận thủ công bởi Admin, không tự kiểm chứng tiền vào ngân hàng.

**Đã triển khai V1 chạy local bằng Flask + SQLite. Chưa triển khai production.**

| Hạng mục | Trạng thái | Bằng chứng / giới hạn |
| --- | --- | --- |
| Flask factory, cấu hình .env | Đã có | app/__init__.py, wsgi.py; SECRET_KEY bắt buộc |
| Database, migrations | Đã có | Migration 41eb1b88b816 đã áp dụng local sau backup; WAL/FK/busy timeout |
| Root ban đầu | Đã tạo local | init-admin; mật khẩu ngoài Git, phải đổi lần đầu |
| Login/logout/đổi mật khẩu | Đã có | CSRF, scrypt, chặn nghiệp vụ khi chưa đổi pass |
| Quản lý tài khoản | Đã có | Chỉ root tạo/khóa/reset Admin; không khóa/reset root qua danh sách |
| Vô hiệu hóa phiên cũ | Đã có | Xoay token khi đổi/reset pass, khóa/mở tài khoản |
| Khóa tạm đăng nhập | Đã có | 5 lần sai khóa 5 phút; chưa rate limit theo IP ở proxy |
| Danh sách phòng | Đã nâng cấp | Mặc định gọn, giữ mã phòng; lọc đã thu/chưa thu/chưa chốt theo kỳ; tùy chọn đủ cột |
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
| Thu đủ tiền | Đã có | Dropdown, ngày/người/số tiền; chống đúp; root hoàn tác giữ audit; phiếu đã thu xuống dưới |
| Kiểm thử | 46 test pass | unittest nghiệp vụ/permission/filter/sort/migration; Node syntax pass |
| Model/migration khớp nhau | Đã kiểm tra | flask db check không có schema drift |
| Browser/production | Có kiểm tra hình ảnh / chưa production | Edge headless với HTML dữ liệu giả ở desktop và root rộng 390px; chưa kiểm tra tương tác E2E, HTTPS, proxy, job backup |

## Giới hạn nghiệp vụ

- Sửa điện có lịch sử; không xóa lịch sử, chưa hỗ trợ thay đồng hồ. Root cần hủy phiếu tiền hiệu lực bị ảnh hưởng trước khi điều chỉnh điện.
- Không chèn kỳ trước khi đã có kỳ sau. Nếu có lịch sử, chỉ chốt nối tiếp kỳ liền trước.
- Phòng trống vẫn ghi điện. Phòng ngừng sử dụng không có trong bảng nhập.
- Chỉ số nguyên 0–2.147.483.647. Không chia tiền theo đợt thuê giữa tháng.
- Đã ghi nhận thu đủ thủ công; chưa thu một phần, sổ công nợ chi tiết, dashboard, nhiều tòa hoặc tài khoản chỉ xem. Phiếu là bảng tính nội bộ, không phải hóa đơn thuế.
- Phiếu đã chốt giữ snapshot giá/người/chỉ số; giá phiếu mới lấy từ thông tin phòng hiện tại. Form cũ bị chặn khi version đổi. Lập bù/lập lại kỳ cũ cũng gợi ý giá hiện tại; cần kiểm tra giá kỳ. Chưa lịch giá tự động hoặc điện khác tháng tiền phòng.
- Chưa lưu nháp dài hạn: màn hình xem trước rồi chốt trong một phiên. Kỳ vào/trả giữa tháng hoặc đổi khách bị chặn; chưa chia điện theo khách. Root hủy phiếu không có nghĩa hoàn tiền đã thu ngoài hệ thống.
- Gia hạn 1–120 tháng từ hạn cũ; hợp đồng quá hạn cần xác nhận. Hết hạn không tự trả phòng; đợt đã trả không gia hạn. Dữ liệu cũ có thể bổ sung dần; đợt mới cần đủ phí/ngày/lịch đóng.
- HTMX tăng tốc điều hướng; form POST thông thường. Thêm/sửa phòng là trang riêng, chưa popup.

Cách chạy và bằng chứng xem DEVELOPMENT.md, HANDOFF.md.
