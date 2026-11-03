# Quyết định và vấn đề cần chốt

## 2026-11-03 — Thu tiền và bảng Phòng (V1.1.14)

- Triển khai phân tích V1.1.13: tách chốt phiếu khỏi đã thu. Admin được xác nhận thu đủ; root hoàn tác có lý do/audit, không xóa receipt hoặc tự hoàn tiền.
- Chưa thu một phần. Phiếu0đ có thao tác xác nhận hoàn tất riêng, amount0. Ngày thu không ở tương lai; số tiền luôn từ snapshot bill.total.
- Chặn hủy phiếu có thu hiệu lực. Unique receipt/bill và version lịch sử chặn double-submit/form cũ sau hoàn tác.
- Sort ở màn Chốt tiền, không làm xáo trộn mã phòng. Phòng mặc định gọn, có lọc theo phiếu của tháng và view đầy đủ giữ dữ liệu cũ; không gán “tiền kỳ” từ giá dự tính.

## 2026-11-03 — Ngày và tiền trên bảng điện (V1.1.11)

- Ngày chốt là thời điểm lưu ban đầu (tự động), lần cập nhật lấy audit gần nhất; hiển thị UTC+7 đến giây, không sửa ngày chốt khi sửa chỉ số.
- Tự tính tiền điện = kWh × đơn giá trên server và live JS (BigInt để tránh mất chính xác tiền nguyên). Thiếu giá không coi là0.
- Chụp giá vào bản ghi điện mới; không đổi phiếu đã chốt. Giá phiếu hiệu lực luôn là nguồn hiển thị ưu tiên, còn tiền trước chốt chỉ dự tính. Legacy thiếu giá được đánh dấu tạm tính theo giá hiện tại.

## 2026-11-03 — Giá điện trong thông tin phòng (V1.1.10)

- Lưu Tenancy.electricity_price (VND/kWh nguyên >=0, NULL legacy) cùng các giá khác. Không tự gán từ phiếu cũ khi migration.
- Thay giá điện/nước/phòng chỉ làm thay giá gợi ý cho phiếu lập sau; phiếu đã chốt giữ snapshot. Version chống chốt từ form mở trước khi sửa.
- Mốc áp dụng là lúc lập phiếu, chưa có lịch giá theo ngày/tháng; khi lập bù/lập lại kỳ cũ, Admin đối chiếu và điều chỉnh giá trên form trước khi chốt.

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

## 2026-11-03 — Chốt tiền và sửa điện gọn (V1.1.9)

- Theo yêu cầu ưu tiên code ngắn/tập trung: chỉ revision số điện + snapshot tiền tháng; không thực thu/công nợ/chia ngày/lịch giá tự động.
- Phòng và điện cùng kỳ tháng, thông báo giả định trước triển khai và trên UI. Kỳ khách vào/trả giữa tháng hoặc thay khách chưa được chốt để tránh gán sai điện/tiền.
- Admin được sửa điện chưa bị phiếu hiệu lực khóa; root hủy hiệu lực phiếu có lý do trước khi sửa, rồi lập mới. Giữ nguyên dữ liệu phiếu cũ, không tính là hoàn/cấn tiền thực tế.
- Giá theo từng phiếu; điều khoản hiện tại chỉ gợi ý, Admin xác nhận giá kỳ. Số người tính nước được nhập kiểm tra; tiền cọc không thuộc tổng tháng.
