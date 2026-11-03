# Giao diện V1.1.7

Yêu cầu: nâng cấp hình thức, giữ nguyên chức năng. Không có migration, thay đổi route/service/model hoặc thêm tính năng nghiệp vụ trong đợt này.

## Định hướng

- Nền sáng, sidebar navy (#102a36), nút chính xanh (#295de0), điểm nhấn mint (#72dbbd).
- Font hệ thống Segoe UI/Arial, không cần Google Fonts/CDN.
- Các bề mặt có border mảnh, góc bo và bóng nhẹ; label/phân cấp chữ nhất quán; số liệu căn phải/tabular khi thích hợp.
- Không dashboard biểu đồ. Dải tóm tắt phòng trình bày dữ liệu đã có của kết quả đang xem, không tạo KPI hoặc số mẫu trong sản phẩm.

## File chính

- app/static/css/app.css: toàn bộ design tokens, shell, bảng, form, login và responsive, có chú thích theo nhóm.
- app/templates/partials/icons.html: macro icon SVG inline; chỉ dùng hình trang trí, aria-hidden.
- app/templates/base.html: sidebar, breadcrumb, tài khoản, skip-link và CSS cache version.
- app/templates/auth/login.html: layout hai cột, minh họa; giữ nguyên tên trường, POST và CSRF.
- app/static/images/residence.svg, favicon.svg: hình vector nội bộ, không fetch asset ngoài khi chạy.
- app/templates/rooms/index.html: thanh tóm tắt, bảng giữ đủ 17 cột và dữ liệu hiện có; sticky mã phòng/thao tác.

## Quy tắc giữ chức năng

- Không thay tên input, form action/method, CSRF, ID mà app.js sử dụng hoặc điều kiện quyền.
- Không ẩn thao tác đổi mật khẩu/logout trên mobile. Nav tài khoản vẫn chỉ hiện với root.
- Bảng cuộn trong container riêng; vùng cuộn có thể focus bằng bàn phím. Tiêu đề/mã phòng/thao tác sticky giúp đọc bảng rộng.
- Chỉ số tóm tắt theo danh sách đã lọc, điện theo kỳ hiện có. Không suy diễn số liệu nợ/thực thu.
- Giữ nguyên mọi cảnh báo nghiệp vụ: tổng dự tính, chưa thực thu, hạn hợp đồng, gia hạn và điện đã chốt.
- [hidden] được ưu tiên để phần ngày trả phòng do JS ẩn không bị CSS grid làm hiện lại.

## Responsive và kiểm tra

- Các breakpoint 1250/900/680px; form một cột ở mobile, summary 2 cột, sidebar thành nav ngang.
- Hỗ trợ focus-visible, skip-link, aria-current, icon trang trí không đọc bởi screen reader và prefers-reduced-motion.
- 31 unittest hiện có pass sau thay đổi template; node --check cho JS hiện tại pass. Không thêm test nghiệp vụ cho thay đổi trình bày này.
- Đã xem ảnh desktop 1440px: login, bảng phòng, form. Đã xem bố cục root 390px: login và bảng.
- Edge headless có viewport tối thiểu khoảng 492px; fixture 390px giới hạn root ở 390 để xem layout trong breakpoint mobile. Chưa phải mô phỏng đầy đủ thiết bị hoặc browser E2E.
- Fixture/screenshot nằm trong instance/ui-*.html/png, dùng DB tạm và dữ liệu giả; không thay dữ liệu vận hành, không commit. Profile browser QA cũng nằm dưới instance/ và bị ignore.

Khi đổi CSS tiếp, tăng query version trong base.html nếu cần làm mới cache. Có thể Ctrl+F5 trên browser đang mở.
