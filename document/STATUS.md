# Tiến độ thực tế

Cập nhật: 2026-11-03 (Asia/Saigon). Phiên bản hội thoại: V1.3.3.

V1.3.3: bổ sung/xem ảnh công tơ ngay trên màn Sửa điện; form ảnh riêng không yêu cầu đổi số. Link từ bảng điện và redirect upload về đúng kỳ điện, bỏ form ảnh điện bên phòng (giữ xem lịch sử). Kiểm tra 10 test ảnh và 12 test billing đạt, inventory/diff đạt. Không đổi DB/nén; chưa browser QA/VPS.

V1.3.2: sửa lỗi dev thiếu bảng photo sau khi người dùng nhập DB VPS cũ. Đã backup bản nhập rồi upgrade từ 41eb1b88b816 lên f13a98c52b70. db check/integrity đạt, nội dung mọi bảng cũ khớp backup, GET /electricity/ với phiên đăng nhập trả 200. Không đổi tài khoản/mật khẩu hoặc VPS; không xác nhận tính đầy đủ của bản copy so với VPS/WAL. Kiểm tra inventory/diff; không chạy lại suite vì không đổi code.

V1.3.1: tạo lại .env dev bị xóa bằng mẫu và SECRET_KEY ngẫu nhiên mới; giữ database/tài khoản, COOKIE_SECURE=false để chạy HTTP local. Kiểm tra app load và /login HTTP 200, inventory/diff đạt; không chạy lại suite nghiệp vụ hoặc thao tác VPS. Phiên đăng nhập dev cũ hết hiệu lực do đổi khóa.

V1.3.0: đã hiện thực upload ảnh hợp đồng tùy chọn theo đợt thuê, ảnh điện bắt buộc khi chốt/sửa; dữ liệu cũ giữ nguyên và có thể bổ sung ảnh. Ảnh riêng tư ngoài static, kiểm tra JPEG/PNG/WebP 10 MB/24 MP, request 64 MB. Hàng đợi SQLite + một worker CLI có khóa OS nén WebP 2200 px/quality 82, bỏ metadata, xóa gốc tạm, báo pending/failed và cho tải lại. 57 tests pass với Pillow 13.0.0 trong .venv; Node syntax đạt. Migration f13a98c52b70 đã backup/upgrade local, số dòng nghiệp vụ giữ nguyên/integrity ok/db check không drift. Docs inventory/diff đạt. Có hướng dẫn PHOTOS.md và service worker Ubuntu; chưa cập nhật VPS hoặc chạy worker dev lâu dài, chưa browser QA/đánh giá ảnh chữ thực tế/restore DB+ảnh. Khi deploy cần Nginx 64m và bật worker; backup phải lưu thêm uploads.

V1.2.28: đã dọn 23 mục artifact kiểm tra UI trong instance dev theo yêu cầu. Chỉ còn .gitkeep và chdv.sqlite3; SHA256 database không đổi trước/sau. Không đổi code hoặc thao tác VPS. Inventory/diff đạt, không chạy test nghiệp vụ; các ảnh/HTML kiểm tra cũ không còn, cần tạo lại nếu muốn xem.

V1.2.27: chuyển ngữ cảnh về instance dev theo ảnh IDE; phân biệt database/.gitkeep với artifact kiểm tra giao diện. Chưa dọn file do người dùng chưa yêu cầu cụ thể. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy test nghiệp vụ hoặc thao tác VPS.

V1.2.26: kiểm tra danh sách instance local và giải thích DB/WAL/SHM trên VPS so với HTML/PNG kiểm tra giao diện local. Không xóa hoặc sửa runtime, không xác nhận nội dung VPS ngoài ảnh đã gửi. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy test nghiệp vụ.

V1.2.25: ảnh instance xác nhận DB có WAL/SHM. Làm rõ tải riêng DB hoặc tải tuần tự cả ba khi đang hoạt động không bảo đảm nhất quán; hướng dẫn backup-db rồi tải file kết quả, không dừng web. Chưa nhận bằng chứng backup/restore. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy lệnh VPS hoặc test nghiệp vụ.

V1.2.24: hướng dẫn danh sách cần lưu từ VPS để khôi phục dữ liệu/cấu hình, ưu tiên SQLite Backup API và tải bản backup qua SFTP; không copy riêng DB đang mở. Chưa nhận bằng chứng backup hoặc restore, chưa lập lịch. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy lệnh VPS hoặc test nghiệp vụ.

V1.2.23: ảnh access.log cho thấy nhiều request dò đường dẫn, các dòng hiển thị trả 301/404. Giải thích đây là dấu hiệu quét tự động, chưa có bằng chứng truy cập thành công từ ảnh; hướng dẫn lọc hiển thị gọn qua awk, không thay log gốc hoặc chặn IP. Chỉ sửa tài liệu, kiểm tra inventory/diff; chưa chạy lệnh hiển thị trên VPS.

V1.2.22: log systemctl xác nhận chdv/nginx enabled và active; đoạn journalctl gửi chỉ có startup, chưa thấy lỗi. Giải thích màn theo dõi chờ log mới và hướng dẫn xem access.log Nginx để theo dõi lượt truy cập. Chưa kiểm tra thực tế access.log trên VPS. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy test nghiệp vụ.

V1.2.21: người dùng báo ok và hỏi cách xem terminal/trạng thái web. Hướng dẫn systemctl, journalctl, curl HTTPS và log lỗi Nginx; giải thích systemd chạy nền, không có terminal Flask cần giữ mở. Chưa có log renew dry-run hoặc xác nhận riêng backup/restore/reboot. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy lệnh VPS hoặc test nghiệp vụ.

V1.2.20: log người dùng xác nhận Certbot đã cấp/cài HTTPS chdv.alominh.homes thành công, hạn 2027-02-01 và báo lập lịch gia hạn; UFW thêm rule Nginx Full nhưng chưa rõ active. Chưa có kết quả browser login/đổi mật khẩu, renew dry-run hoặc backup/restore/reboot. Hướng dẫn kiểm tra đăng nhập và gia hạn thử. Chỉ sửa tài liệu, kiểm tra inventory/diff; không tự chạy lệnh VPS hoặc test nghiệp vụ.

V1.2.19: ảnh người dùng xác nhận curl /login qua Nginx với Host chdv.alominh.homes trả HTTP 200. Hướng dẫn cho phép Nginx Full và cấp HTTPS qua Certbot; chưa có kết quả chứng chỉ hoặc kiểm tra HTTPS. Chỉ cập nhật tài liệu, kiểm tra inventory/diff; chưa chạy lệnh VPS hoặc test nghiệp vụ.

V1.2.18: log xác nhận nginx -t thành công nhưng curl qua Nginx /login với Host domain trả 404, chưa đạt proxy. Hướng dẫn đọc site/nginx -T và thử lại; chưa xác định nguyên nhân, chưa cấp HTTPS. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy lệnh VPS hoặc test nghiệp vụ.

V1.2.17: log VPS xác nhận systemd chdv enabled/active và Gunicorn /login trả HTTP 200 trên 127.0.0.1:8000, cookie Secure. Hướng dẫn cấu hình Nginx cho chdv.alominh.homes và kiểm tra proxy; chưa nhận kết quả Nginx, chưa cấp HTTPS. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy lệnh VPS hoặc test nghiệp vụ.

V1.2.16: ảnh vẫn ở shell /opt/chdv sau tạo root. Làm rõ cách mở nano trước khi dán cấu hình INI, chưa có bằng chứng tạo hoặc chạy service. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy test nghiệp vụ.

V1.2.15: người dùng gửi nslookup qua 1.1.1.1 xác nhận chdv.alominh.homes phân giải 103.167.88.214. Hướng dẫn systemd/Gunicorn loopback và curl nội bộ; chưa nhận kết quả. Chưa cấu hình Nginx/HTTPS cho app. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy lệnh VPS hoặc test nghiệp vụ.

V1.2.14: người dùng xác nhận IP VPS 103.167.88.214. Hướng dẫn sửa riêng A record chdv và kiểm tra DNS; chưa có kết quả thay đổi/phân giải. Chưa cấu hình service/HTTPS. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy lệnh VPS hoặc test nghiệp vụ.

V1.2.13: ảnh DNS hiển thị A chdv.alominh.homes về 103.75.183.230, khác IP SSH/eth0 Ubuntu ở ảnh trước (103.167.88.214). Đang yêu cầu xác minh IP Ubuntu và IP public trong bảng quản lý VPS trước khi sửa DNS hoặc cấu hình HTTPS. Chưa kết luận topology/NAT. Chỉ cập nhật tài liệu, kiểm tra inventory/diff; không chạy lệnh VPS.

V1.2.12: log người dùng xác nhận root được tạo trên VPS. Đã chọn domain chdv.alominh.homes và hướng dẫn A record trên Porkbun về IP VPS 103.167.88.214 theo ảnh SSH/eth0 trước. Chưa xác nhận DNS, service hoặc HTTPS; chưa xác nhận xóa mật khẩu khởi tạo. Đối chiếu hướng dẫn Porkbun chính thức, kiểm tra inventory/diff; không chạy test nghiệp vụ.

V1.2.11: log VPS xác nhận database mới đã upgrade đến 41eb1b88b816 (head). Đối chiếu code xác nhận APP_ENV chưa được sử dụng, không bắt buộc trong .env VPS. Chưa xác nhận tạo root/service/HTTPS. Chỉ cập nhật tài liệu, kiểm tra inventory/diff; không chạy lại test nghiệp vụ.

V1.2.10: log người dùng gửi xác nhận 48 tests OK trong 35.304s trên VPS. Đã chọn bắt đầu dữ liệu mới; hướng dẫn tạo .env riêng và chạy migration, chưa nhận kết quả. Chưa tạo root/service/HTTPS. Kiểm tra tài liệu inventory/diff; không tự chạy lệnh VPS hoặc chạy lại suite local.

V1.2.9: ảnh pip xác nhận cài requirements và Gunicorn 26.2.0 thành công trong venv trên VPS. Đã hướng dẫn unittest, chưa nhận kết quả; chờ chọn giữ DB local hay tạo mới. Chưa cấu hình .env/DB/service hoặc mở web. Chỉ sửa tài liệu, kiểm tra inventory/diff; chưa chạy test VPS thay người dùng.

V1.2.8: ảnh xác nhận tạo user chdv; giải thích cảnh báo home chưa tồn tại tại thời điểm adduser và cp -n. Chưa có bằng chứng venv/pip; hướng dẫn kiểm tra file và tiếp tục cài môi trường. Chỉ sửa tài liệu; kiểm tra inventory/diff, không chạy test nghiệp vụ hoặc lệnh VPS.

V1.2.7: ảnh apt hoàn tất về dấu nhắc root, không thấy lỗi trong phần hiển thị. Hướng dẫn chuẩn bị /opt/chdv, user dịch vụ, venv và cài thư viện; chưa nhận kết quả, chưa cấu hình .env/DB/service app. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy test nghiệp vụ.

V1.2.6: ảnh ls xác nhận danh sách code đã upload đúng cấp thư mục /root/chdv-upload, chưa kiểm tra toàn vẹn nội dung. Đang hướng dẫn cài gói hệ thống qua apt, chưa nhận kết quả cài đặt; chưa chuyển DB hoặc chạy web. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy test nghiệp vụ.

V1.2.5: ảnh VPS xác nhận Ubuntu 24.04, chưa có listener cổng 80/443/8000 và đã tạo /root/chdv-upload. Đợt tiếp hướng dẫn upload code, chưa chuyển DB/.env hoặc cài dịch vụ. Chỉ cập nhật tài liệu; kiểm tra inventory/diff, không chạy test nghiệp vụ.

V1.2.4: ảnh người dùng xác nhận đã mở SSH root trên Ubuntu 24.04. Hướng dẫn ngắn đợt đầu: kiểm tra OS/cổng web và tạo thư mục upload; chưa nhận kết quả lệnh, chưa xác nhận cài đặt hoặc triển khai VPS. Chỉ cập nhật tài liệu, kiểm tra inventory/diff; không chạy lại test nghiệp vụ.

V1.2.3: đã phân tích và viết DEPLOY_UBUNTU.md cho Ubuntu 24.04/MobaXterm: danh sách copy, thư mục, cấu hình và chuyển DB bằng backup. Chỉ thay tài liệu; inventory/diff đạt. Chưa triển khai VPS, kiểm thử Python 3.12/HTTPS/restore hoặc chạy lại test nghiệp vụ.

V1.2.2: 47 test suite pass; 12 test_billing pass sau khi th?m test helper. gom reading_cost cho chọn nguồn giá/tính tiền điện ở lịch sử phòng và màn điện. room_query/active_bill_query vào services/queries.py, bỏ import giữa các route. Template lịch sử chỉ trình bày. Thêm test giá snapshot/phiếu 0/thiếu giá/fallback/chưa nhập, ghi quy ước tái sử dụng. Không đổi DB/nghiệp vụ; chưa rà hết template lặp hoặc browser QA.

V1.2.1: 14 test_contracts pass. form thêm/sửa phòng dùng Bootstrap mw-100/w-100 bỏ giới hạn 1000px, nhóm hợp đồng/phí dùng grid 1/2/3 cột theo màn hình, thanh lưu position-static để không phủ nội dung khi cuộn. Ô khách bị khóa khi trạng thái Trống là hành vi hiện có, giữ nguyên. Chưa browser QA; không đổi DB/nghiệp vụ.

V1.2.0: Bootstrap 5.3.8 CSS/bundle CDN có SRI; CSP cho phép jsDelivr. Chuyển nút/form/bảng/alert và tiện ích bố cục sang Bootstrap, bỏ CSS trùng. Sidebar bỏ animation lặp, khôi phục trạng thái lên html trước paint để tránh flash khi tải/chuyển HTMX. 47 test pass, Node syntax và 4 kiểm tra trạng thái trước paint pass. Chưa browser QA/CDN runtime; cần mạng cho Bootstrap. Không đổi DB/nghiệp vụ.

V1.1.24: thêm animation CSS ngắn 140–240ms cho trang/card, sidebar lúc hiện, thông báo/popover và phản hồi hover/nhấn. Không transform nội dung chứa sticky table/form; tôn trọng prefers-reduced-motion. Chỉ CSS/cache asset, không đổi nghiệp vụ/JS/DB. Kiểm tra tài liệu/diff; chưa browser QA hoặc chạy lại test nghiệp vụ.

V1.1.23: lịch sử điện chi tiết phòng thêm đơn giá và tiền điện tự tính; ưu tiên phiếu hiệu lực, sau đó giá snapshot của lần chốt điện. Dữ liệu cũ thiếu giá hiển thị chưa có giá đã lưu, không tự áp giá hiện tại vào lịch sử. Tài khoản chuyển cuối menu sidebar, trên hồ sơ. 11 test billing pass, có test giá snapshot/phiếu/0/thiếu giá; chưa browser QA. Không đổi schema.

V1.1.22: cập nhật AGENTS.md theo yêu cầu: tự tăng patch/minor/major theo mức thay đổi; code gọn, đúng chuẩn, format dễ đọc trong phạm vi sửa. Chỉ sửa tài liệu, không format lại app trong lượt này; không cần chạy test nghiệp vụ. Kiểm tra bằng script tài liệu và diff whitespace.

V1.1.21: bỏ dòng đếm xe trong hai bảng phòng, chỉ giữ biển số từng dòng; không có xe hiển thị dấu —. Xóa CSS vehicle-count không dùng. Kiểm tra render partial với 2 xe/không xe/không khách; không đổi nghiệp vụ/DB, chưa browser QA.

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
