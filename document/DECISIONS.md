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

## 2026-11-02 — Triển khai V1 theo yêu cầu mới

- Người dùng cho phép code V1 và tạo `.env`; root ban đầu theo thông tin đã cung cấp, không ghi mật khẩu vào tài liệu.
- Root quản lý tài khoản; các tài khoản khác là Admin phòng/điện. Bắt đổi pass lần đầu kể cả root bootstrap, tối thiểu 8 ký tự.
- Pass 8–128 ký tự, scrypt, CSRF, xoay token phiên khi đổi/reset/khóa/mở tài khoản.
- Chọn đợt thuê, tự tính số người, chốt điện nguyên kWh và lưu từng phần.
- Chưa sửa điện cũ hoặc thay đồng hồ; phải thiết kế audit và liên kết kỳ trước khi mở chức năng.
- Dùng CSS riêng + HTMX nội bộ; chưa thêm Bootstrap/Alpine. Form phòng là trang riêng; điều hướng HTMX.
- Khóa dependencies trực tiếp theo môi trường kiểm thử; chưa lock toàn bộ phụ thuộc gián tiếp hoặc audit production.
- Backup có CLI thủ công; lịch và đích ngoài máy cấu hình khi vận hành. Các câu hỏi phía trên là bối cảnh tạo sườn; mục này ghi lựa chọn triển khai hiện tại.
