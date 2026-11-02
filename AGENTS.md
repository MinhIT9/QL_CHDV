# Quy tắc làm việc với CHDV Manager Basic

## Trước khi thay đổi

- Đọc `document/STATUS.md`, `document/HANDOFF.md` và tài liệu liên quan.
- Chỉ triển khai trong phạm vi được người dùng yêu cầu. Người dùng đã cho phép triển khai V1 Flask + SQLite và quản lý tài khoản bởi root.
- Không ghi đè thay đổi của người khác. Không đưa bí mật hoặc dữ liệu khách thật vào repo/tài liệu.

## Khi kết thúc mỗi thay đổi

- Cập nhật `document/STATUS.md`: việc đã hoàn thành, chưa làm, bằng chứng kiểm tra và hạn chế.
- Cập nhật `document/HANDOFF.md`: bước tiếp theo, vướng mắc, cách kiểm tra hiện có.
- Ghi thay đổi có ý nghĩa vào `document/CHANGELOG.md` theo ngày.
- Nếu đổi phạm vi, kiến trúc hoặc mô hình dữ liệu, sửa tài liệu tương ứng. Ghi quyết định mới vào `document/DECISIONS.md`.
- Chạy `python scripts/update_docs.py`, sau đó `python scripts/update_docs.py --check`.
- Chỉ đánh dấu hoàn thành khi có hiện thực và kiểm tra phù hợp. Thư mục rỗng, tài liệu và giao diện mẫu không chứng minh chức năng đã hoạt động.
- Báo rõ kiểm tra chưa chạy; không ghi kết quả giả định.

## Quy ước

### Phiên bản ở cuối phản hồi

- Theo yêu cầu người dùng, mọi phản hồi cuối lượt (final) phải kết thúc bằng một dòng theo mẫu `V1.1.1: Mô tả ngắn nội dung vừa xử lý`.
- Bắt đầu từ `V1.1.1`; mỗi phản hồi cuối lượt tiếp theo tăng số cuối lên 1, kể cả lượt chỉ phân tích hoặc trả lời câu hỏi. Chỉ đổi hai số đầu khi người dùng yêu cầu.
- Đây là số phiên bản hội thoại, không phải phiên bản phát hành ứng dụng hoặc bằng chứng tính năng đã hoàn thành.
- Trước khi trả lời, đọc mục phiên bản trong `document/HANDOFF.md`, đối chiếu phản hồi gần nhất nếu có, rồi dùng số kế tiếp. Không đặt lại số khi đổi agent hoặc phiên làm việc.
- Ghi lại phiên bản vừa dùng và mô tả trong `document/HANDOFF.md` để agent sau tiếp tục. Nếu không thể ghi file, báo rõ trong phản hồi và vẫn giữ đúng dòng phiên bản cuối cùng.

- Tài liệu dự án dùng tiếng Việt, UTF-8; tên file và mã nguồn dùng tiếng Anh.
- Giữ một project Flask. Không tự thêm React, API riêng hoặc hạ tầng mới khi chưa có nhu cầu.
- Kiểm tra nghiệp vụ và quyền ở máy chủ, kể cả khi giao diện đã kiểm tra.
- Không lưu thông tin khách/mật khẩu vào log hoặc fixture thật.
- Không sửa tay `document/INVENTORY.md`; file này do script sinh.
