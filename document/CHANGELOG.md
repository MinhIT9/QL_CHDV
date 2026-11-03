# Lịch sử thay đổi

## 2026-11-03

- V1.3.3: chuyển form bổ sung ảnh công tơ sang màn điện, hiển thị ngay khi mở Sửa điện; upload giữ nguyên chỉ số và quay lại đúng kỳ, bỏ form ảnh điện khỏi chi tiết phòng.

- V1.3.2: backup và migrate DB VPS cũ vừa nhập vào dev để thêm bảng photo; giữ nguyên nội dung bảng cũ, kiểm tra schema/integrity và màn điện HTTP 200.

- V1.3.1: khôi phục .env dev bị mất từ mẫu với khóa ngẫu nhiên mới, giữ dữ liệu/tài khoản; kiểm tra load app và /login HTTP 200.

- V1.3.0: thêm upload hợp đồng tùy chọn, ảnh chốt/sửa điện bắt buộc, xem ảnh qua đăng nhập và bổ sung ảnh lịch sử. Thêm Photo/migration f13a98c52b70, worker SQLite/CLI nén WebP và xóa gốc tạm, xử lý lỗi/khôi phục sau crash, service Ubuntu và hướng dẫn backup DB+ảnh. Pillow 13.0.0; 57 tests pass. Đã backup/upgrade dev, chưa triển khai VPS hoặc browser QA.

- V1.2.28: dọn 23 mục file/thư mục kiểm tra UI trong instance dev; giữ .gitkeep và database, kiểm tra SHA256 DB không đổi. Không thay ứng dụng hoặc VPS.

- V1.2.27: làm rõ nội dung instance dev theo ảnh IDE; chưa xóa file hoặc đổi cấu hình.

- V1.2.26: giải thích vai trò thư mục instance, bộ file SQLite và các file kiểm tra giao diện local; không thay dữ liệu runtime.

- V1.2.25: giải thích backup SQLite đang chạy có WAL/SHM; hướng dẫn dùng CLI tạo bản nhất quán thay cho copy trực tiếp file runtime.

- V1.2.24: hướng dẫn lưu database nhất quán, .env, code và cấu hình systemd/Nginx từ VPS; phân biệt chứng chỉ có thể cấp lại và runtime không cần lưu.

- V1.2.23: giải thích access.log chứa request dò đường dẫn và hướng dẫn xem gọn các trường chính bằng awk; không thay cấu hình logging.

- V1.2.22: xác nhận trạng thái dịch vụ từ log, giải thích journalctl chờ dữ liệu mới và hướng dẫn theo dõi lượt truy cập qua log Nginx.

- V1.2.21: hướng dẫn theo dõi trạng thái dịch vụ, log ứng dụng trực tiếp và phản hồi HTTPS qua MobaXterm.

- V1.2.20: xác nhận HTTPS đã cấp/cài thành công từ log Certbot; hướng dẫn kiểm tra đăng nhập root, đổi mật khẩu và gia hạn thử, chưa đánh dấu vận hành hoàn tất.

- V1.2.19: xác nhận Nginx proxy trả 200 qua ảnh, hướng dẫn cấp HTTPS và chuyển HTTP sang HTTPS bằng Certbot; chờ kết quả.

- V1.2.18: ghi nhận Nginx syntax pass nhưng proxy trả 404; hướng dẫn thu thập cấu hình đang nạp và kiểm tra lại trước HTTPS.

- V1.2.17: ghi nhận systemd/Gunicorn chạy và /login HTTP 200 từ log; hướng dẫn Nginx reverse proxy cho domain, chờ kiểm tra trước HTTPS.

- V1.2.16: làm rõ thao tác mở nano từ terminal trước khi dán nội dung chdv.service; chờ người dùng mở trình soạn thảo.

- V1.2.15: xác nhận DNS đúng IP từ nslookup người dùng; hướng dẫn tạo/khởi động systemd Gunicorn và kiểm tra nội bộ.

- V1.2.14: chốt IP VPS 103.167.88.214 theo người dùng; hướng dẫn cập nhật riêng DNS chdv và kiểm tra phân giải.

- V1.2.13: phát hiện IP bản ghi chdv khác IP phiên SSH Ubuntu; hướng dẫn xác minh IP VPS trước bước cấu hình dịch vụ và HTTPS.

- V1.2.12: xác nhận tạo root từ log; hướng dẫn cấu hình DNS subdomain chdv.alominh.homes trên Porkbun, chờ kết quả trước cấu hình web/HTTPS.

- V1.2.11: ghi nhận migration VPS đạt head từ log; giải thích APP_ENV hiện chưa có tác dụng trong code và không bắt buộc cấu hình.

- V1.2.10: ghi nhận 48 test pass trên VPS từ log người dùng, chọn DB mới; hướng dẫn tạo .env bí mật riêng và khởi tạo schema qua migration, chờ kết quả.

- V1.2.9: ghi nhận pip cài thành công dependencies và Gunicorn 26.2.0 từ ảnh; hướng dẫn kiểm thử Ubuntu và xác định phương án dữ liệu trước khi cấu hình.

- V1.2.8: giải thích cảnh báo trong bước tạo user/copy code, hướng dẫn kiểm tra thư mục và tiếp tục venv/pip; chưa xác nhận cài thư viện.

- V1.2.7: ghi nhận apt hoàn tất từ ảnh, hướng dẫn tạo tài khoản/thư mục chạy ứng dụng và cài thư viện trong venv, chờ kết quả VPS.

- V1.2.6: xác nhận danh sách upload từ ảnh; hướng dẫn đợt cài gói hệ thống Ubuntu, chờ kết quả trước khi cấu hình thư mục ứng dụng.

- V1.2.5: ghi nhận kết quả kiểm tra VPS từ ảnh; hướng dẫn upload danh sách code cần thiết qua SFTP, chưa chuyển dữ liệu hoặc cài đặt.

- V1.2.4: chuyển sang hướng dẫn triển khai từng đợt ngắn; bắt đầu kiểm tra VPS và tạo thư mục upload, chờ kết quả người dùng trước đợt tiếp theo.

- V1.2.3: phân tích triển khai Ubuntu 24.04 qua MobaXterm; thêm hướng dẫn copy code/backup SQLite, thư mục, Gunicorn/systemd, Nginx/HTTPS và vận hành. Chưa thực thi trên VPS; không đổi app hoặc schema.

- V1.2.2: tái sử dụng reading_cost cho giá/tiền điện; query phòng/phiếu hiệu lực vào service, bỏ phụ thuộc giữa route; thêm test nguồn giá và quy ước tái sử dụng.

- V1.2.1: form phòng rộng theo khung, grid hợp đồng/phí responsive Bootstrap, bỏ sticky thanh lưu gây phủ nội dung.

- V1.2.0: Bootstrap 5.3.8 CSS/bundle CDN có SRI/CSP; nút/form/bảng/alert và tiện ích dùng Bootstrap, bỏ CSS trùng. Sidebar khôi phục trạng thái trước paint và bỏ animation lặp.

- V1.1.24: thêm chuyển động nhẹ khi hiện trang/sidebar/popover/thông báo, phản hồi hover/nhấn; tắt animation khi người dùng chọn giảm chuyển động.

- V1.1.23: lịch sử điện phòng thêm đơn giá/tiền điện tự tính từ giá đã lưu hoặc phiếu hiệu lực; Tài khoản đặt cuối sidebar trên hồ sơ.

- V1.1.22: cho agent tự tăng phiên bản theo mức thay đổi; bổ sung quy ước code ngắn gọn, chuẩn, format nhất quán và giữ phạm vi thay đổi.

- V1.1.21: bỏ dòng số lượng xe trong bảng phòng, giữ từng biển số một dòng; không xe hiển thị dấu —.

- V1.1.20: tách tiền nước/dịch vụ trong chi tiết; bảng phòng thêm số xe/biển số từng dòng, tiền nước tổng theo người, tiền dịch vụ riêng; căn chỉnh số tiền/nhãn xe/dòng bảng. Giữ nguyên phiếu đã chốt.

- V1.1.19: nút ẩn/hiện sidebar và nhớ lựa chọn trên trình duyệt; header tên trang/tài khoản, footer gọn đồng bộ. Không đổi nghiệp vụ.

- V1.1.18: thay bộ chọn month theo ngôn ngữ trình duyệt bằng danh sách Tháng/Năm tiếng Việt dùng chung cho Phòng, Điện và Chốt tiền; giữ YYYY-MM.

- V1.1.17: gom trạng thái/Thông tin thu/Lịch sử thu cùng hàng; bỏ nhãn Đã chốt tiền lặp, giữ Quá hạn; gộp phòng/khách và giảm padding bảng tiền. Chỉ sửa template/CSS.

- V1.1.16: giải thích chọn tháng rồi bấm Xem kỳ, đầu kỳ tự nối cuối kỳ trước và giới hạn chặn lưu tháng tương lai; không đổi chức năng.

- V1.1.15: sửa dropdown thu tiền/history kéo cao dòng và xô cột. Native popover top layer + fixed/JS tự neo, tránh clipping/vượt viewport; Escape/click ngoài/nút đóng. Giữ chức năng thu/hoàn tác/hủy.
- 5 test receipt pass, Node syntax pass; Edge fixture xác nhận dòng128px trước/sau mở, đã xem ảnh. Không thay database.

- V1.1.14: triển khai phân tích V1.1.13 — dropdown ghi nhận thu đủ, ngày/người/số tiền và lịch sử; root hoàn tác có lý do. Chặn hủy phiếu đã thu và gửi lại form cũ sau hoàn tác.
- Phiếu chưa thu ở trên/đã thu ở dưới/hủy cuối; bảng Phòng gọn mặc định, tiền kỳ từ snapshot, bộ lọc thu và chế độ đầy đủ giữ cột cũ.
- Migration 41eb1b88b816 đã backup/upgrade; 46 test pass. Chưa thu một phần/browser E2E cho UI mới.

- V1.1.12: bỏ giới hạn1000px riêng form chốt tiền; dùng chiều ngang còn lại, desktop chia input/preview hai cột, mobile xếp dọc. Không đổi chức năng.

- V1.1.11: thêm ngày giờ chốt, cập nhật lần cuối nếu có revision, đơn giá và tiền điện trong bảng. Nhập chỉ số tự hiện tiền/draft total, xử lý 0 và thiếu giá.
- Snapshot giá khi lưu điện mới; kỳ đã chốt tiền ưu tiên giá phiếu, legacy chưa có giá được ghi rõ tạm tính. Migration d94f512a37b1 đã backup/upgrade; 41 test và Node smoke test pass.

- V1.1.10: thêm giá điện trong thông tin phòng/đợt thuê và bảng/chi tiết/lịch sử. Phiếu mới lấy giá điện/nước/phòng hiện tại, không hồi tố phiếu đã chốt, chặn version cũ.
- Migration c83e4d16b2a0 giữ NULL legacy, đã backup/upgrade local. 39 test pass.

- V1.1.9: sửa điện preview/confirm, audit trước/sau, đồng bộ kỳ kế tiếp và chống ghi đè dữ liệu vừa thay đổi.
- Chốt tiền từng kỳ, snapshot giá/người/điện, chống trùng; root hủy hiệu lực có lý do và giữ bản cũ. Không mở rộng thực thu/công nợ/chia ngày.
- Migration 0fecdf9f864b đã backup/upgrade local; 38 test pass và schema khớp model.

- V1.1.8 (hội thoại): đối chiếu code và phân tích sửa điện có revision, kiểm tra kỳ sau, chốt giá/snapshot theo tháng và xử lý phiếu đã thu; chưa thay đổi chức năng hoặc database.

## 2026-11-02

- V1.1.7 (hội thoại): nâng cấp FE đồng bộ: nền sáng, sidebar navy/mint, icon SVG, login hai cột và minh họa căn hộ nội bộ.
- Bảng phòng có cột mã/thao tác sticky, thanh tóm tắt dữ liệu sẵn có, form và trạng thái dễ đọc, responsive, focus bàn phím/reduced-motion; không đổi nghiệp vụ, database hoặc quyền.
- 31 test hồi quy pass; kiểm tra ảnh Edge headless desktop và bố cục 390px bằng dữ liệu tạm, chưa browser E2E.

- V1.1.6 (hội thoại): thêm tiền phòng/tháng theo đợt thuê, form/bảng/chi tiết/lịch sử và tổng dự tính phòng+nước+dịch vụ, không gồm điện/cọc.
- Giá nguyên VND >=0, legacy NULL; migration b71c430e92ad đã backup/upgrade local. 31 test pass. Bổ sung tiêu đề cột lịch sử khớp dữ liệu tiền cọc/phòng.

- V1.1.5 (hội thoại): gộp ngày vào ở và ngày bắt đầu thành một trường Ngày bắt đầu hợp đồng; checkout/đổi khách dùng mốc này.
- Thêm tiền cọc theo đợt thuê, cho phép 0, hiển thị form/bảng/chi tiết/lịch sử; không cộng vào phí tháng, chưa thực thu/hoàn cọc.
- Migration a65b2f9c018e giữ ngày hợp đồng đã có; dùng ngày vào cũ khi thiếu và không mâu thuẫn; giữ cột legacy và NULL tiền cọc. Đã backup/upgrade local; 30 test pass.

- V1.1.4 (hội thoại): triển khai phí nước/dịch vụ (có 0), ngày vào/hợp đồng/trả phòng và lịch đóng tiền hằng tháng.
- Gia hạn có xem trước/xác nhận, giữ ngày neo cuối tháng, audit lịch sử và version chống ghi đè/đúp; ngày trả phòng bắt buộc khi kết thúc đợt.
- Migration dd7493777e83 giữ NULL legacy và người/xe, CHECK constraint; đã backup và upgrade DB local. 29 test pass, chưa tính hóa đơn/thực thu/chia ngày.

- V1.1.3 (hội thoại): phân tích ràng buộc phí nước/dịch vụ, hợp đồng/gia hạn và lịch đóng tiền; ghi đề xuất riêng, chưa code chức năng.

- V1.1.2 (hội thoại): triển khai V1 Flask/SQLite, migration và `.env` ngoài Git.
- Root bootstrap và quản lý tài khoản; bắt đổi pass lần đầu, hủy phiên cũ khi đổi/reset/khóa.
- Phòng và lịch sử đợt thuê/người/xe; chốt điện nối tiếp tháng, lưu từng phần, không ghi đè.
- HTMX nội bộ, CSS responsive, CSRF, ràng buộc DB, CLI backup; 17 test tích hợp và hướng dẫn chạy.

- V1.1.1 (hội thoại): quy định mọi phản hồi final kết thúc bằng phiên bản và mô tả ngắn; lưu số tiếp nối trong `HANDOFF.md` cho agent sau.

- Khởi tạo sườn dự án CHDV Manager Basic, chưa có code nghiệp vụ.
- Thêm tài liệu phạm vi, kiến trúc, mô hình dự kiến, tiến độ và bàn giao.
- Thêm quy tắc cập nhật tài liệu trong `AGENTS.md`.
- Thêm script sinh danh mục file, hook kiểm tra tùy chọn, Git ignore và cấu hình mẫu.
