# Kiến trúc hiện tại

Một project Flask trả HTML bằng Jinja2. CSS riêng theo thiết kế bảng; HTMX 2.0.4 tăng tốc điều hướng qua hx-boost, form POST vẫn thông thường. JS tính điện khi nhập, khóa ô khách theo trạng thái và chống bấm lặp. Chưa dùng Bootstrap/Alpine.

Luồng: trình duyệt → blueprint → quyền/CSRF → service nghiệp vụ → SQLAlchemy → SQLite → redirect/HTML.

| Đường dẫn | Vai trò |
| --- | --- |
| wsgi.py | Entrypoint create_app |
| app/__init__.py | Factory, config, PRAGMA, middleware đổi pass, headers, CLI |
| app/extensions.py | db, login manager, CSRF, migration |
| app/auth/routes.py | Login/logout/đổi pass, root, tài khoản |
| app/rooms/routes.py | Bảng, form, chi tiết, xóa/ngừng phòng |
| app/electricity/routes.py | Bảng nhập điện theo kỳ |
| app/services/rooms.py | Validate phòng, chuyển đợt thuê |
| app/services/electricity.py | Chuỗi kỳ, validate số, giao dịch |
| app/models/__init__.py | User, Room, Tenancy, Occupant, Vehicle, ElectricityReading |
| app/templates/ | Jinja2; partials/ để mở rộng sau |
| app/static/ | CSS/JS riêng, HTMX và license nội bộ |
| migrations/ | Alembic schema có version control |
| tests/test_v1.py | Tích hợp SQLite tạm và Flask test client |
| instance/ | DB local ngoài Git/static |
| backups/, logs/ | Runtime; chưa có scheduler/log file riêng |
| scripts/update_docs.py | Sinh danh mục file |
| document/, AGENTS.md | Trạng thái và quy tắc dev/agent |

## Quyền và phiên

User.is_root cho phép tạo/khóa/reset tài khoản. Tài khoản khác là Admin quản lý phòng/điện. Không tự đăng ký/nâng quyền, không khóa root từ web.

must_change_password kiểm tra mọi request đã đăng nhập; khi còn bật chỉ được đổi pass/logout/static. Hash Werkzeug scrypt. session_token xoay khi đổi/reset pass hoặc khóa/mở để hủy phiên cũ. CSRF mọi POST; cookie HttpOnly/SameSite Lax, Secure theo môi trường.

## Dữ liệu

- SQLite ổ đĩa cục bộ, WAL, foreign keys, busy timeout 5 giây. URL tương đối dưới instance/.
- Một bản điện/phòng/kỳ, nguyên không âm, DB check cuối >= đầu. Đầu kỳ nối tháng trước; không chèn lùi.
- BEGIN IMMEDIATE khi chốt SQLite để tuần tự hóa ghi và đọc lại lịch sử; sai một dòng rollback cả đợt.
- Unique index tối đa một tenancy mở/phòng.
- Ngừng phòng kết thúc đợt thuê, giữ lịch sử. Xóa hẳn chỉ khi chưa có thuê/điện.
- Backup dùng SQLite Backup API, đích mới. Chưa tự lập lịch hoặc lưu ngoài máy.
- UTC lưu DB, ngày hiển thị UTC+7 (Asia/Saigon). Chưa tính tiền.
