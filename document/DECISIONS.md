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

## 2026-11-02 — Phí và hợp đồng (V1.1.4)

- Người dùng yêu cầu triển khai phân tích V1.1.3. Chọn phương án tối giản đã nêu: lưu hai đơn giá và lịch nhắc, chưa chia ngày/tạo hóa đơn/ghi nhận tiền thực thu.
- Phí là số nguyên VND >=0; dữ liệu cũ giữ NULL để phân biệt chưa biết với miễn phí. Đợt mới bắt buộc đủ ngày, phí và lịch đóng; legacy bổ sung dần, không tự đoán từ timestamp.
- Ngày nghiệp vụ là DATE riêng. Khi kết thúc đợt bắt nhập ngày trả thực tế; không tự lấy hôm nay và không nhận ngày trả tương lai.
- Gia hạn từ hạn cũ 1–120 tháng, giữ ngày neo để không trôi sau tháng ngắn; preview/confirm và xác nhận quá hạn. Lưu audit, dùng Tenancy.version để chống stale/concurrent update. Chưa có sửa sai lịch sử gia hạn.
- Lịch đóng 1–31 là lịch tham chiếu theo điều khoản hiện tại, không phải lịch sử nghĩa vụ thanh toán hoặc chứng từ thu.
- Migration thêm CHECK inline trên SQLite, không rebuild bảng tenancy có FK. Đã kiểm thử giữ legacy người/xe và backup trước upgrade local.

## 2026-11-02 — Ngày bắt đầu thống nhất và tiền cọc (V1.1.5)

- Theo yêu cầu người dùng, gộp ngày vào ở vào ngày bắt đầu hợp đồng. Form/chi tiết/lịch sử dùng contract_start; kiểm tra trả phòng và đổi khách dựa vào mốc này.
- Giữ move_in_date như cột legacy để không xóa dữ liệu đã có; ghi mới đồng bộ theo contract_start. Migration ưu tiên ngày hợp đồng đã có, chỉ fallback từ ngày vào cũ khi thiếu và không mâu thuẫn.
- Thêm deposit_amount theo đợt thuê, cho phép 0, giữ NULL legacy và không cộng vào phí tháng. Đây là số cọc thỏa thuận, chưa phải xác nhận thu/hoàn.
- Đợt thuê mới phải nhập tiền cọc; gia hạn giữ nguyên, khách mới có khoản cọc riêng. Đã backup trước nâng schema local.

## 2026-11-02 — Tiền phòng (V1.1.6)

- Theo yêu cầu người dùng, thêm rent_price/tháng theo đợt thuê; nhập bắt buộc cho đợt mới, cho phép 0, số nguyên VND không âm. Legacy không tự gán giá.
- Gia hạn giữ giá, đổi khách nhập giá riêng. Tổng phòng+nước+dịch vụ chỉ là dự tính tháng đủ, chưa điện/cọc/thực thu.
- Migration b71c430e92ad thêm cột nullable/CHECK; đã backup local trước upgrade.

## 2026-11-02 — Nâng cấp FE (V1.1.7)

- Theo yêu cầu giữ chức năng: chỉ sửa template/CSS và bổ sung SVG nội bộ; không migration hoặc đổi quyền/kiểm tra nghiệp vụ.
- Navy/mint/nền sáng, font hệ thống và icon SVG; không thêm framework hoặc font/ảnh từ CDN.
- Giữ bảng đầy đủ, sticky mã phòng/thao tác và nhãn cuộn ngang. Tóm tắt dùng dữ liệu hiện có của kết quả đang xem.
- QA bằng unittest và ảnh tĩnh Edge headless dữ liệu tạm; chưa browser E2E. Giới hạn viewport 390px được mô tả trong UI_DESIGN.md.
