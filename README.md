# CHDV Manager Basic

Ứng dụng quản lý căn hộ dịch vụ, ưu tiên nhập liệu nhanh và xem thông tin bằng bảng.

**Trạng thái: chỉ có sườn thư mục và tài liệu. Chưa có ứng dụng chạy được, database hay chức năng nghiệp vụ.**

## Đọc nhanh

1. [Tiến độ thực tế](document/STATUS.md)
2. [Phạm vi V1 và quy tắc nghiệp vụ](document/SCOPE.md)
3. [Kiến trúc và cấu trúc thư mục](document/ARCHITECTURE.md)
4. [Hướng dẫn phát triển và cập nhật tài liệu](document/DEVELOPMENT.md)
5. [Bàn giao cho lần làm tiếp](document/HANDOFF.md)

Stack dự kiến: Flask, Jinja2, Bootstrap, HTMX, SQLAlchemy, SQLite, Flask-Login và Flask-Migrate. Chưa cài hoặc khóa phiên bản thư viện.

## Cập nhật tài liệu

```powershell
python scripts/update_docs.py
python scripts/update_docs.py --check
```

Script tự sinh `document/INVENTORY.md` từ các file trong dự án. Tiến độ chức năng trong `STATUS.md` được dev/agent cập nhật theo bằng chứng, theo quy tắc trong `AGENTS.md`. Xem cách bật tự chạy trước commit trong [hướng dẫn phát triển](document/DEVELOPMENT.md).

Không commit mật khẩu, dữ liệu khách, database thật hoặc bản sao lưu. Cấu hình mẫu nằm trong `.env.example`.
