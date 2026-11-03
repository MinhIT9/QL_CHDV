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
- Tự chọn mức tăng theo độ phức tạp, phạm vi và ảnh hưởng thực tế của thay đổi, không cần hỏi lại: `Vx.y.z` tăng `z` cho sửa nhỏ, UI, tài liệu hoặc phân tích; tăng `y` và đặt `z=0` cho nhóm tính năng/nâng cấp đáng kể; tăng `x` và đặt `y=1, z=0` cho thay đổi lớn về kiến trúc hoặc nghiệp vụ không tương thích. Ví dụ: `V1.1.22`, `V1.2.0`, `V2.1.0`. Các lượt sau tiếp tục tăng, có thể là `V1.2.1` hoặc `V1.2.34`; không giới hạn số cuối ở 9. Không tăng mức chỉ vì code dài hoặc tốn thời gian.
- Đây là số phiên bản hội thoại, không phải phiên bản phát hành ứng dụng hoặc bằng chứng tính năng đã hoàn thành.
- Trước khi trả lời, đọc mục phiên bản trong `document/HANDOFF.md`, đối chiếu phản hồi gần nhất nếu có, rồi chọn phiên bản tăng phù hợp theo quy tắc trên. Lượt chỉ phân tích/trả lời câu hỏi cũng tăng `z`. Không đặt lại số khi đổi agent hoặc phiên làm việc.
- Ghi lại phiên bản vừa dùng và mô tả trong `document/HANDOFF.md` để agent sau tiếp tục. Nếu không thể ghi file, báo rõ trong phản hồi và vẫn giữ đúng dòng phiên bản cuối cùng.

- Tài liệu dự án dùng tiếng Việt, UTF-8; tên file và mã nguồn dùng tiếng Anh.
- Giữ một project Flask. Không tự thêm React, API riêng hoặc hạ tầng mới khi chưa có nhu cầu.
- Kiểm tra nghiệp vụ và quyền ở máy chủ, kể cả khi giao diện đã kiểm tra.
- Không lưu thông tin khách/mật khẩu vào log hoặc fixture thật.
- Không sửa tay `document/INVENTORY.md`; file này do script sinh.

### Phong cách mã nguồn

- Ưu tiên Bootstrap 5 cho nút/form/bảng/thông báo và tiện ích bố cục; chỉ viết CSS khi Bootstrap không đáp ứng. CDN ghim phiên bản/SRI và cập nhật CSP phù hợp.

- Ưu tiên code cực gọn, ngắn và đúng chuẩn; bỏ lặp, biến/thành phần không cần thiết. Tính đúng, bảo mật và khả năng đọc hiểu được ưu tiên hơn việc giảm số ký tự.
- Khi sửa code, định dạng đẹp và nhất quán trong phần đang chỉnh: thụt lề chuẩn, tên rõ nghĩa, xuống dòng hợp lý. Không nén nhiều câu lệnh hoặc cả template thành một dòng để làm ngắn giả tạo.
- Tái sử dụng helper/partial khi giảm lặp có ý nghĩa; không thêm abstraction, thư viện hoặc cấu trúc phức tạp chỉ cho một thao tác đơn giản.
- Không format toàn repo hoặc chạm file ngoài phạm vi chỉ để làm đẹp; giữ thay đổi tập trung, dễ review và không ghi đè việc của người khác.
