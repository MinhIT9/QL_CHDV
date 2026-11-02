# Kiến trúc dự kiến

Một project Flask trả HTML bằng Jinja2. HTMX cập nhật từng phần trang; Bootstrap định dạng giao diện. Chỉ thêm JavaScript/Alpine.js khi có nhu cầu tương tác cụ thể.

Luồng dự kiến: trình duyệt → route/form → service nghiệp vụ → SQLAlchemy → SQLite. Route trả trang đầy đủ hoặc HTML fragment cho HTMX.

## Vai trò thư mục

| Đường dẫn | Vai trò dự kiến |
| --- | --- |
| `app/` | Mã ứng dụng, sau này có app factory và cấu hình |
| `app/auth/` | Route/form đăng nhập và đăng xuất |
| `app/rooms/` | Route/form phòng và chi tiết |
| `app/electricity/` | Route/form nhập và xem điện |
| `app/models/` | Model SQLAlchemy, ràng buộc dữ liệu |
| `app/services/` | Nghiệp vụ dùng chung, giao dịch chốt điện |
| `app/templates/` | Trang Jinja2 theo module |
| `app/templates/partials/` | HTML fragment dùng với HTMX |
| `app/static/` | CSS, JavaScript, ảnh, thư viện frontend nội bộ |
| `migrations/` | Alembic/Flask-Migrate; chưa được khởi tạo |
| `tests/` | Test quyền, nghiệp vụ, ràng buộc khi triển khai |
| `instance/` | DB và cấu hình cục bộ, không commit |
| `logs/`, `backups/` | Dữ liệu vận hành cục bộ, không commit |
| `scripts/` | Công cụ hỗ trợ phát triển/vận hành |
| `.githooks/` | Hook kiểm tra tài liệu, phải bật riêng |
| `document/` | Tài liệu trạng thái và thiết kế |

Các thư mục chỉ có `.gitkeep` hiện chưa phải Python package hay module hoạt động. Chưa tạo route, model, template hoặc cấu hình ứng dụng.

## Nguyên tắc triển khai sau này

- SQLite ở ổ đĩa cục bộ máy chủ, ngoài static; bật foreign keys, cấu hình WAL và thời gian chờ ghi phù hợp.
- Giao dịch ghi ngắn; ràng buộc mã phòng và kỳ chốt ở DB.
- Bảo vệ route phía máy chủ, CSRF, hash mật khẩu và cấu hình session phù hợp môi trường.
- Chỉ số hiện tại lấy từ lịch sử hợp lệ, tránh nhiều nguồn dữ liệu lệch nhau.
- Dùng migration; SQLAlchemy hỗ trợ chuyển DB nhưng không bảo đảm chuyển PostgreSQL tự động.
- Backup nhất quán và kiểm tra khôi phục; thư mục `backups/` chưa phải giải pháp backup ngoài máy chủ.
