# Đề xuất ảnh công tơ tùy chọn và upload trong bảng

Ngày: 2026-11-04. V1.3.13 chỉ phân tích theo yêu cầu, chưa triển khai. Nội dung này thay yêu cầu bắt buộc ảnh ở bản đang chạy khi được triển khai; không phải bằng chứng hành vi đã thay đổi.

Cập nhật V1.4.0: đã triển khai trên dev luồng ảnh tùy chọn, drop/preview, upload XHR, thumbnail/modal và polling như dưới. 61 test Python đạt và kiểm tra Edge với dữ liệu tạm đạt; chưa cập nhật VPS. Chi tiết vận hành hiện tại ở PHOTOS.md; nội dung đề xuất bên dưới giữ làm cơ sở đối chiếu.

## Luồng đề xuất

- Chốt hoặc sửa điện không bắt buộc ảnh, kiểm tra này cần bỏ cả ở service, HTML và JS. Nếu người dùng đã chọn ảnh thì ảnh vẫn phải hợp lệ; dữ liệu cũ/ảnh cũ được giữ.
- Mỗi ô ảnh có vùng kéo thả và nút chọn file. Thả/chọn chỉ tạo preview local kèm nhãn Chưa tải lên, có nút bỏ ảnh đang chọn. Không gửi request upload trước thao tác lưu.
- Phòng chưa chốt: nút Lưu chỉ số gửi chỉ số kèm các ảnh đã chọn trong một request AJAX. Giữ kiểm tra kỳ/chống trùng và tính nguyên tử hiện tại; nếu ảnh đính kèm hoặc nghiệp vụ không hợp lệ thì trả lỗi và không báo đã lưu. Trình duyệt giữ dữ liệu đang nhập để sửa/bỏ ảnh rồi thử lại.
- Phòng đã chốt: thêm nút Lưu ảnh tại ô ảnh để bổ sung trực tiếp, không đi sang trang phòng hoặc bắt sửa số. Nút này hoạt động khi toàn bộ phòng đã chốt và nút Lưu chỉ số bị khóa. Lỗi upload chỉ ảnh hưởng ảnh, không lưu lại chỉ số đã chốt.
- Chọn preview local có thể xem lớn nhưng luôn ghi rõ chưa tải; sau ready thì hiển thị thumbnail từ server thay nút Xem ảnh. Click mở Bootstrap modal dùng chung, hiển thị bản WebP đã nén với object-fit contain, có đóng/Escape và hỗ trợ màn nhỏ. Full là kích thước xem lớn của bản đã nén, không phải khôi phục ảnh gốc đã xóa.

## Tiến độ và hoàn tất

Luồng: Chưa chọn → Chờ lưu → Đang tải 0–100% → Đang xử lý → Ảnh đã lưu; có nhánh lỗi/thử lại. Không dùng 100% truyền dữ liệu để tuyên bố đã nén/lưu xong.

Dùng XMLHttpRequest.upload progress để tính phần trăm byte khi tổng kích thước tính được; nếu không có tổng thì báo đang tải. Request nhiều ảnh có một tiến độ tổng, không hiển thị phần trăm giả cho từng ảnh. Sau phản hồi xác nhận lưu nghiệp vụ/job, dùng một truy vấn trạng thái theo lô khoảng 2 giây/lần để cập nhật các ảnh pending. Khi ready thì cập nhật đúng ô/thumbnail, không reload trang và không làm mất file/chỉ số chưa lưu ở hàng khác.

Polling chỉ chạy khi cần, dừng khi ready/failed, rời trang hoặc hết thời gian chờ hợp lý. Quá thời gian thì báo còn đang xử lý và cho kiểm tra lại; không tự kết luận failed nếu worker còn chờ. Chống gửi trùng; khi mất mạng sau gửi phải kiểm tra trạng thái trước khi thử lại để không tạo bản trùng hoặc chốt lại điện. Khi hết phiên đăng nhập, báo cần đăng nhập thay vì coi HTML login là phản hồi JSON thành công.

## Kéo thả và phạm vi

Nhận file ảnh từ Explorer/Desktop hoặc ứng dụng cung cấp File thực. Ảnh kéo từ website/ứng dụng khác đôi khi chỉ là URL/HTML; không cam kết nhận mọi nguồn. Khi không có file, hướng dẫn lưu ảnh về máy rồi chọn/kéo file, không tự cho server tải URL tùy ý. Điện thoại dùng chọn ảnh/chụp ảnh. Giữ JPEG/PNG/WebP, 10 MB/24 MP và request 64 MB như hiện tại; không mở rộng HEIC/PDF trong đợt này.

Thumbnail ban đầu có thể dùng WebP đã nén, kích thước hiển thị gọn và lazy-loading. Nếu cần giảm băng thông ở bảng nhiều ảnh thì bổ sung bản thumbnail riêng; CSS thu nhỏ không làm giảm byte tải. Không thêm thư viện frontend hay dịch vụ hàng đợi mới. Giữ worker hiện tại và quyền xem ảnh riêng tư.

## Phần cần thay khi triển khai

- services/electricity.py và services/billing.py: stage ảnh chỉ khi có file; service upload riêng vẫn yêu cầu file vì đó là thao tác tải ảnh.
- photos.py và electricity/routes.py: hỗ trợ phản hồi AJAX có trạng thái/id/URL, lỗi validation và truy vấn trạng thái ảnh theo lô với xác thực; giữ form thường nếu tắt JS. Đây là route trong project Flask hiện tại.
- Template ô ảnh/form sửa điện và JS: drop zone, preview, nút lưu ảnh, progress, modal, cập nhật DOM đúng ô, bỏ required ảnh. Tránh form lồng nhau và xử lý đúng listener chống submit lặp hiện có/điều hướng HTMX.
- Chưa cần đổi model hoặc migration vì pending/ready/failed và owner theo lần chốt đã có. Nếu bổ sung cơ chế chống retry trùng bền vững hoặc thumbnail riêng thì đánh giá bổ sung ở bước triển khai.
- Chỉ áp dụng luồng mới cho ảnh điện; ảnh hợp đồng giữ luồng đang có.

## Kiểm tra cần có

Chốt/sửa không ảnh; upload sau không đổi số; thả/chọn chưa gửi request; lưu mới bắt đầu upload; bỏ ảnh chờ không xóa ảnh đã lưu; sai ảnh/413/CSRF/phiên hết hạn; tiến độ phản ánh truyền dữ liệu; worker chậm/lỗi/restart; tự hiện thumbnail/modal không reload; nhiều hàng không mất dữ liệu; mất mạng/retry không tạo bản trùng; giữ quyền ảnh và xóa gốc tạm.

## Tham khảo

- https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest_API/Using_XMLHttpRequest
- https://developer.mozilla.org/en-US/docs/Web/API/DataTransfer/files
