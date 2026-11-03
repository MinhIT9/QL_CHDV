# Lịch sử thay đổi

## 2026-11-03

- V1.1.9: sửa điện preview/confirm, audit trước/sau, đồng bộ kỳ kế tiếp và chống ghi đè dữ liệu vừa thay đổi.
- Chốt tiền từng kỳ, snapshot giá/người/điện, chống trùng; root hủy hiệu lực có lý do và giữ bản cũ. Không mở rộng thực thu/công nợ/chia ngày.
- Migration 0fecdf9f864b đã backup/upgrade local; 38 test pass và schema khớp model.

- V1.1.8 (hội thoại): đối chiếu code và phân tích sửa điện có revision, kiểm tra kỳ sau, chốt giá/snapshot theo tháng và xử lý phiếu đã thu; chưa thay đổi chức năng hoặc database.

## 2026-11-02

- V1.1.7 (hội thoại): nâng cấp FE đồng bộ: nền sáng, sidebar navy/mint, icon SVG, login hai cột và minh họa căn hộ nội bộ.
- Bảng phòng có cột mã/thao tác sticky, thanh tóm tắt dữ liệu sẵn có, form và trạng thái dễ đọc, responsive, focus bàn phím/reduced-motion; không đổi nghiệp vụ, database hoặc quyền.
- 31 test hồi quy pass; kiểm tra ảnh Edge headless desktop và bố cục 390px bằng dữ liệu tạm, chưa browser E2E.

- V1.1.6 (hội thoại): thêm tiền phòng/tháng theo đợt thuê, form/bảng/chi tiết/lịch sử và tổng dự tính phòng+nước+dịch vụ, không gồm điện/cọc.
- Giá nguyên VND >=0, legacy NULL; migration b71c430e92ad đã backup/upgrade local. 31 test pass. Bổ sung tiêu đề cột lịch sử khớp dữ liệu tiền cọc/phòng.

- V1.1.5 (hội thoại): gộp ngày vào ở và ngày bắt đầu thành một trường Ngày bắt đầu hợp đồng; checkout/đổi khách dùng mốc này.
- Thêm tiền cọc theo đợt thuê, cho phép 0, hiển thị form/bảng/chi tiết/lịch sử; không cộng vào phí tháng, chưa thực thu/hoàn cọc.
- Migration a65b2f9c018e giữ ngày hợp đồng đã có; dùng ngày vào cũ khi thiếu và không mâu thuẫn; giữ cột legacy và NULL tiền cọc. Đã backup/upgrade local; 30 test pass.

- V1.1.4 (hội thoại): triển khai phí nước/dịch vụ (có 0), ngày vào/hợp đồng/trả phòng và lịch đóng tiền hằng tháng.
- Gia hạn có xem trước/xác nhận, giữ ngày neo cuối tháng, audit lịch sử và version chống ghi đè/đúp; ngày trả phòng bắt buộc khi kết thúc đợt.
- Migration dd7493777e83 giữ NULL legacy và người/xe, CHECK constraint; đã backup và upgrade DB local. 29 test pass, chưa tính hóa đơn/thực thu/chia ngày.

- V1.1.3 (hội thoại): phân tích ràng buộc phí nước/dịch vụ, hợp đồng/gia hạn và lịch đóng tiền; ghi đề xuất riêng, chưa code chức năng.

- V1.1.2 (hội thoại): triển khai V1 Flask/SQLite, migration và `.env` ngoài Git.
- Root bootstrap và quản lý tài khoản; bắt đổi pass lần đầu, hủy phiên cũ khi đổi/reset/khóa.
- Phòng và lịch sử đợt thuê/người/xe; chốt điện nối tiếp tháng, lưu từng phần, không ghi đè.
- HTMX nội bộ, CSS responsive, CSRF, ràng buộc DB, CLI backup; 17 test tích hợp và hướng dẫn chạy.

- V1.1.1 (hội thoại): quy định mọi phản hồi final kết thúc bằng phiên bản và mô tả ngắn; lưu số tiếp nối trong `HANDOFF.md` cho agent sau.

- Khởi tạo sườn dự án CHDV Manager Basic, chưa có code nghiệp vụ.
- Thêm tài liệu phạm vi, kiến trúc, mô hình dự kiến, tiến độ và bàn giao.
- Thêm quy tắc cập nhật tài liệu trong `AGENTS.md`.
- Thêm script sinh danh mục file, hook kiểm tra tùy chọn, Git ignore và cấu hình mẫu.
