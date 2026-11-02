# Bàn giao

Cập nhật: 2026-11-02 (Asia/Saigon).

## Phiên bản hội thoại

- Phiên bản phản hồi gần nhất: V1.1.6.
- Nội dung: thêm tiền phòng/tháng theo đợt thuê và tổng dự tính gồm phòng/nước/dịch vụ.
- Phản hồi tiếp theo dùng V1.1.7. Tăng số cuối sau mỗi final; đây không phải phiên bản phát hành.
- Quy tắc đầy đủ ở AGENTS.md, mục “Phiên bản ở cuối phản hồi”.

## Đã làm

- App factory, .env cục bộ có SECRET_KEY ngẫu nhiên, SQLAlchemy, Flask-Login, CSRF và Flask-Migrate.
- instance/chdv.sqlite3 đã upgrade migration b71c430e92ad sau backup backups/pre-rent-*.sqlite3; root và dữ liệu hiện có được giữ. Không ghi mật khẩu vào tài liệu/fixtures/repo.
- Root và Admin mới phải đổi pass lần đầu: 8–128 ký tự, khác pass cũ, kiểm tra phía máy chủ.
- Root tạo/khóa/mở/reset Admin; mọi Admin có quyền phòng/điện, không có đăng ký công khai.
- Năm màn hình nghiệp vụ, cùng đổi mật khẩu và quản lý tài khoản root.
- Phòng có đợt thuê/người/xe; chốt điện nối tiếp tháng, không ghi đè dữ liệu cũ.
- HTMX và license lưu nội bộ, CSS riêng; không cần CDN lúc chạy.
- CLI backup nhất quán và bộ test tích hợp.
- Phí nước/người/tháng, dịch vụ/phòng/tháng cho phép 0; NULL của dữ liệu cũ là chưa biết. Hiển thị dự tính phí tháng đủ, chưa phải hóa đơn.
- Chỉ còn ngày bắt đầu hợp đồng (cũng là ngày vào ở), ngày hết hạn/trả thực tế và lịch đóng 1–31. move_in_date chỉ giữ làm cột legacy, không có ô nhập riêng; save/checkout đồng bộ theo contract_start.
- Tiền cọc theo đợt thuê: nguyên VND >=0, NULL legacy là chưa cập nhật. Có trên form/bảng/chi tiết/lịch sử, không cộng vào phí tháng hoặc xác nhận đã thu/hoàn.
- Tiền phòng rent_price theo đợt thuê, nguyên VND >=0, NULL legacy chưa cập nhật. Form/bảng/chi tiết/lịch sử có giá tháng; monthly_total = tiền phòng + nước + dịch vụ, chưa điện, không cọc. Gia hạn giữ giá hiện tại; khách mới nhập giá riêng.
- Gia hạn xem trước/xác nhận, 1–120 tháng, giữ ngày neo, audit Admin/thời điểm/hạn cũ-mới; version chống sửa/gia hạn lặp. Hợp đồng đã gia hạn không sửa trực tiếp ngày bắt đầu/hết hạn qua form.
- Đổi khách/ngừng sử dụng cần ngày trả thực tế và đúng version đợt thuê. Dữ liệu cũ không bị đoán ngày hoặc gán miễn phí.

## Kiểm tra

- 31 unittest pass: V1, hợp đồng/phí/cọc và tiền phòng; kiểm tra 0/âm/thập phân/quá giới hạn, tổng dự tính, NULL legacy và migration/ràng buộc DB.
- flask db check: không schema drift. node --check app/static/js/app.js: hợp lệ.
- Test client trên app local: /login trả HTTP 200; chưa đổi mật khẩu root thật khi test.
- .env, DB và SQLite sidecars bị Git ignore. Chưa commit/push trong lượt này.
- Chưa kiểm tra trực quan/JavaScript runtime bằng browser; không có trình duyệt tự động tại môi trường hiện tại.
- Chưa bật Git hook, hosting hoặc lịch backup tự động.

## Chạy tiếp

    python -m flask --app wsgi run --host 127.0.0.1 --port 5000

Mở http://127.0.0.1:5000, đăng nhập root bằng pass bootstrap đã cung cấp rồi đổi pass. Clone mới làm theo README.md để tạo môi trường, .env, migration, root.

## Việc tiếp theo

- FEES_CONTRACTS_PROPOSAL.md đã được triển khai theo phương án tối giản: chỉ lưu đơn giá/nhắc lịch, không chia ngày hoặc quản lý thực thu. Nếu cần tính phải thu, thiết kế kỳ/snapshot và giao dịch thu tiền riêng trước.

- Người dùng nhập thử phòng/xe/điện trên browser, nhất là điện thoại.
- Nếu cần sửa điện: thiết kế audit/revision và kiểm tra chuỗi kỳ sau trước khi mở chức năng; không sửa SQL trực tiếp.
- Chốt luồng thay đồng hồ khi cần.
- Trước production: WSGI server, HTTPS/cookie secure, lịch backup ngoài máy, diễn tập restore và rà soát dependencies.

Xem STATUS.md để biết giới hạn chính xác.
