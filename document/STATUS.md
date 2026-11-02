# Tiến độ thực tế

Cập nhật: 2026-11-02 (Asia/Saigon).

**Giai đoạn: chuẩn bị sườn. Chưa có ứng dụng Flask chạy được.**

| Hạng mục | Trạng thái | Bằng chứng / giới hạn |
| --- | --- | --- |
| Sườn thư mục | Đã có | `app/`, `tests/`, `migrations/`, thư mục runtime |
| Bộ tài liệu và quy tắc bàn giao | Đã có | `document/`, `AGENTS.md` |
| Quy ước phiên bản hội thoại | Đã có | `AGENTS.md`; số gần nhất và số tiếp theo trong `document/HANDOFF.md` |
| Sinh danh mục file | Đã có | `scripts/update_docs.py`; không suy đoán tiến độ |
| Git ignore và cấu hình mẫu | Đã có | `.gitignore`, `.gitattributes`, `.env.example` |
| Khởi tạo Flask / cấu hình / thư viện | Chưa làm | Chưa có entrypoint, app factory hoặc phiên bản thư viện |
| Đăng nhập / phân quyền Admin | Chưa làm | Chưa có model, route, form, session |
| Danh sách phòng | Chưa làm | Chưa có giao diện |
| Thêm / sửa / ngừng sử dụng phòng | Chưa làm | Chưa có xử lý |
| Chốt điện theo tháng | Chưa làm | Chưa có xử lý |
| Chi tiết phòng / lịch sử điện | Chưa làm | Chưa có xử lý |
| Database / migration | Chưa làm | Chưa có schema hoặc file DB |
| Backup / khôi phục | Chưa làm | Chỉ có thư mục dự kiến |
| Kiểm thử nghiệp vụ / triển khai | Chưa làm | Chưa có ứng dụng để kiểm thử |

## Kiểm tra sườn

Chạy `python scripts/update_docs.py --check` để kiểm tra danh mục tài liệu. Kết quả kiểm tra lần tạo sườn được ghi ở `HANDOFF.md`. Git hook chỉ hoạt động sau khi được cài theo `DEVELOPMENT.md`.
