# Bàn giao

Cập nhật: 2026-11-02 (Asia/Saigon).

## Phiên bản hội thoại

- Phiên bản phản hồi gần nhất: V1.1.2.
- Nội dung: triển khai V1 Flask + SQLite, root quản lý tài khoản, đổi mật khẩu lần đầu.
- Phản hồi tiếp theo dùng V1.1.3. Tăng số cuối sau mỗi final; đây không phải phiên bản phát hành.
- Quy tắc đầy đủ ở AGENTS.md, mục “Phiên bản ở cuối phản hồi”.

## Đã làm

- App factory, .env cục bộ có SECRET_KEY ngẫu nhiên, SQLAlchemy, Flask-Login, CSRF và Flask-Migrate.
- instance/chdv.sqlite3 đã upgrade migration e9329a770fe9; root tạo theo thông tin người dùng. Không ghi mật khẩu vào tài liệu/fixtures/repo.
- Root và Admin mới phải đổi pass lần đầu: 8–128 ký tự, khác pass cũ, kiểm tra phía máy chủ.
- Root tạo/khóa/mở/reset Admin; mọi Admin có quyền phòng/điện, không có đăng ký công khai.
- Năm màn hình nghiệp vụ, cùng đổi mật khẩu và quản lý tài khoản root.
- Phòng có đợt thuê/người/xe; chốt điện nối tiếp tháng, không ghi đè dữ liệu cũ.
- HTMX và license lưu nội bộ, CSS riêng; không cần CDN lúc chạy.
- CLI backup nhất quán và bộ test tích hợp.

## Kiểm tra

- 17 unittest pass: CSRF, quyền root/Admin, đổi pass lần đầu, bootstrap idempotent, hủy phiên, khóa login, phòng/lịch sử, XSS escaping, điện/rollback batch, ràng buộc DB, migration DB rỗng, backup/integrity và HTMX redirect khi hết phiên.
- flask db check: không schema drift. node --check app/static/js/app.js: hợp lệ.
- Test client trên app local: /login trả HTTP 200; chưa đổi mật khẩu root thật khi test.
- .env, DB và SQLite sidecars bị Git ignore. Chưa commit/push trong lượt này.
- Chưa kiểm tra trực quan/JavaScript runtime bằng browser; không có trình duyệt tự động tại môi trường hiện tại.
- Chưa bật Git hook, hosting hoặc lịch backup tự động.

## Chạy tiếp

    python -m flask --app wsgi run --host 127.0.0.1 --port 5000

Mở http://127.0.0.1:5000, đăng nhập root bằng pass bootstrap đã cung cấp rồi đổi pass. Clone mới làm theo README.md để tạo môi trường, .env, migration, root.

## Việc tiếp theo

- Người dùng nhập thử phòng/xe/điện trên browser, nhất là điện thoại.
- Nếu cần sửa điện: thiết kế audit/revision và kiểm tra chuỗi kỳ sau trước khi mở chức năng; không sửa SQL trực tiếp.
- Chốt luồng thay đồng hồ khi cần.
- Trước production: WSGI server, HTTPS/cookie secure, lịch backup ngoài máy, diễn tập restore và rà soát dependencies.

Xem STATUS.md để biết giới hạn chính xác.
