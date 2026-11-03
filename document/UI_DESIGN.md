# Giao diện V1.1.7

V1.1.21: cột Xe / biển số chỉ hiển thị biển số từng dòng, bỏ dòng đếm xe theo yêu cầu; không có xe dùng dấu —.

V1.1.20: bảng phòng gọn 13 cột, thêm Xe / biển số (đếm xe, mỗi biển một nhãn/dòng), tiền dịch vụ và tổng tiền nước kèm phép tính theo người. Bảng đầy đủ cũng dùng hai partial vehicle_cell/water_cell. Đây là dự tính theo giá phòng hiện tại, không thay snapshot tiền kỳ. Chi tiết tách nước/dịch vụ thay dòng cộng gộp; giữ tổng dự tính cũ. Tiền căn phải, số người căn giữa, màu dòng xen kẽ/hover; màn hẹp cuộn ngang, giữ sticky phòng/thao tác.

V1.1.19: header có nút menu điều khiển sidebar bằng hidden/aria-expanded, nội dung mở rộng khi ẩn. Nhớ lựa chọn localStorage, khôi phục khi điều hướng HTMX; không lưu dữ liệu cá nhân. Mobile giữ điều hướng ngang hiện có khi mở. Header hai cấp tên sản phẩm/trang, tài khoản bên phải; footer biểu tượng và tên sản phẩm cùng mô tả ngắn. Không thêm dependency.

V1.1.18: chọn kỳ tháng dùng partial period_select.html với nhãn Tháng x / năm và optgroup Năm, thay input month có popup phụ thuộc ngôn ngữ browser. Giữ một select name period, value YYYY-MM, +/-3 năm quanh năm chọn; chọn kỳ rồi bấm Xem như trước. Không dùng JS hoặc dependency mới.

V1.1.17: billing-table gọn hơn; bill-payment flex ngang không wrap, popover vẫn top layer, không đổi thao tác. Tên phòng/khách cùng dòng, mã phiếu/ngày ở dòng phụ. Giữ điện hai dòng để đọc chỉ số và phép tính; bảng cuộn ngang trên màn hẹp thay vì ép nút xuống nhiều hàng.

V1.1.15 thay dropdown details/summary ở ô bảng bằng button popovertarget + panel popover=auto trong top layer. Panel fixed, giới hạn chiều rộng/cao theo màn hình, cuộn nội bộ; JS neo nút và chọn phía đủ chỗ, cập nhật resize/scroll/nested details. Không tăng chiều cao row hoặc bị table-scroll cắt. Mục hủy bên trong vẫn dùng details. Edge fixture đã kiểm tra128px trước/sau mở; yêu cầu browser hiện đại có Popover API. Ảnh QA: instance/payment-layout.png (dữ liệu giả, ngoài Git).

V1.1.14: dropdown Thu tiền dùng details/summary, có form xác nhận ngày/số tiền và root hoàn tác. Nhóm đã thu có nền nhạt và tự xuống dưới sau POST. Bảng Phòng mặc định 10 cột gọn, view đầy đủ giữ 18 cột cũ; select lọc thu theo kỳ. Mã phòng giữ ổn định, tiền kỳ/hạn lấy từ phiếu chốt, ghi khách trên phiếu khi khác khách hiện tại. Chưa browser E2E cho UI này.

V1.1.12: form chốt tiền có bill-card full-width thay vì max1000px. Từ1200px input và preview đặt cạnh nhau; chưa preview dùng3 cột input. Dưới breakpoint giữ luồng dọc, form mobile một cột. Các form phòng/đổi mật khẩu vẫn giữ giới hạn riêng.

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
