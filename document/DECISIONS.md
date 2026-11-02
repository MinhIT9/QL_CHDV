# Quyết định và vấn đề cần chốt

## 2026-11-02 — Sườn dự án

- Yêu cầu hiện tại: chỉ dựng folder, tài liệu và file cấu hình nền; chưa code chính.
- Định hướng công nghệ theo trao đổi: một project Flask, giao diện Jinja2 + Bootstrap + HTMX, SQLAlchemy + SQLite. Chưa khóa phiên bản hoặc cài dependencies.
- Chưa đưa Alpine.js thành dependency bắt buộc.
- Tài liệu tập trung trong `document/`; `STATUS.md` là nguồn thông tin tiến độ.
- Script tự sinh danh mục; dev/agent chịu trách nhiệm xác minh và cập nhật chức năng. Có hook tùy chọn, chưa bật cấu hình Git.

## Cần chốt trước hoặc trong bước thiết kế chi tiết

- Chấp nhận mô hình đợt thuê và số người tự tính hay không.
- Chỉ số điện là số nguyên hay có thập phân.
- Quy trình sửa kỳ cũ, thiếu kỳ, lưu từng phần và thay đồng hồ.
- Tiêu chí prototype được duyệt trước khi triển khai backend.
- Môi trường triển khai, HTTPS, lịch backup và nơi lưu ngoài máy chủ.

Không cần giải quyết các mục trên chỉ để tạo sườn.
