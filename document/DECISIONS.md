# Quyết định và vấn đề cần chốt

## 2026-11-04 — QR tạo cục bộ V1.7.0

V1.7.0: Đã hiện thực QR chuyển khoản tạo cục bộ bằng qrcode 8.2, TLV NAPAS/QRIBFTTA, CRC16-CCITT. Không gọi dịch vụ bên ngoài hoặc lưu ảnh cho từng phiếu. Dropdown 48 ngân hàng từ snapshot API Banks ngày 2026-11-04 ở app/data/banks.json; không có tác vụ mạng runtime. Admin chọn BIN và điền STK (giữ số 0 đầu, 1–19 ký tự ASCII chữ/số), tên chủ tài khoản, ghi chú. Máy chủ lấy ngân hàng từ allowlist, không tin tên ngân hàng gửi từ form. Ghi chú chỉ hiển thị trên phiếu, nội dung QR tự tạo theo P{id} {room} T{mmyyyy}; tiền dùng bill.total sau điều chỉnh, không nhận override từ query string.

Migration d57032b19f64 thêm bank_bin nullable, không đoán BIN từ tên cũ; admin cấu hình ngân hàng để bật QR mới. Ảnh QR cũ được giữ và dùng fallback khi chưa có BIN, không xóa dữ liệu cũ. QR đã thu/hủy/0 đồng không được phát; tổng trên 13 chữ số không sinh QR nhưng vẫn mở phiếu được. Thông tin nhận tiền là cấu hình chung hiện tại. Tên chủ TK không tự xác minh; không tự ghi nhận đã thu khi tạo/quét QR.

DEV đã backup backups/pre-local-vietqr-v162.sqlite3 và upgrade/db check đạt. QR đối chiếu vector nguồn độc lập và đọc ngược PNG bằng ZXing-C++; Edge kiểm tra QR từng phiếu chứa số cuối cùng 1.234 thay vì query giả 1, STK/nội dung đúng, QR crop trên mobile đọc được, responsive/in và regression ảnh điện đạt. ZXing-C++ chỉ dùng QA, không cần cài trên VPS. Chưa quét bằng app ngân hàng thật hoặc triển khai VPS, không xác nhận tương thích thực tế với mọi ngân hàng. Cần cài requirements mới, migration rồi restart web/worker khi đưa lên VPS; quét thử bằng ngân hàng để đối chiếu người nhận/số tiền/nội dung trước khi dùng gửi khách.


## 2026-11-04 — Nhận tiền và QR V1.6.0

Đã thêm quản trị Nhận tiền cho root/Admin đã đăng nhập: ngân hàng, số tài khoản (giữ số 0 đầu), chủ tài khoản, ghi chú và upload/thay/xóa QR. Kiểm tra CSRF/quyền ở máy chủ. QR PNG/JPEG/WebP tối đa 5 MB/4096 px, đọc kiểm tra và mã hóa PNG lossless bỏ metadata; lưu riêng PHOTO_ROOT/payment bằng token ngẫu nhiên, không lưu ảnh gốc hoặc URL bên ngoài. Ảnh chỉ xem sau đăng nhập. Thông tin dùng chung hiện tại, không snapshot vào phiếu: đổi cấu hình cập nhật mọi phiếu chưa thanh toán. Phiếu đã thu/hủy ẩn phần chuyển khoản. QR do admin lấy từ ứng dụng ngân hàng, không tự sinh/đọc hoặc đổi số tiền trong QR; cần dùng QR không cố định tiền và quét thử đúng tài khoản.

Thu gọn khoảng cách tiêu đề/thông tin/bảng/tổng/footer, đặt QR cạnh thông tin tài khoản. Có responsive 390px và CSS in. Chưa xác minh quét mã bằng điện thoại hoặc in giấy thật. QR trong kiểm tra là ảnh fixture, không phải QR thanh toán thật.

Migration mới c46f21a08e53 thêm payment_settings; DEV đã backup backups/pre-payment-settings-v160.sqlite3 rồi upgrade/db check đạt. Backup vận hành cần cả DB và instance/uploads (gồm payment). Không cập nhật VPS. 75 unittest đạt (48.815s), Edge headless đạt upload cấu hình/hiển thị phiếu desktop và 390px/print cùng regression ảnh điện. Ảnh xem thử exports/receipt-preview-desktop.png và exports/receipt-preview-mobile.png. Bước tiếp restart web dev, Ctrl+F5, mở Nhận tiền và cấu hình tài khoản thật trực tiếp trong app; khi triển khai VPS phải migrate trước mở web.


## 2026-11-04 — Phiếu tiền phòng V1.5.0

V1.5.0: Đã triển khai trên dev trang phiếu riêng khi bấm ID, tổng tự tính và số thu cuối cùng kèm lý do bắt buộc khi khác tổng gốc; lịch sử phòng có cả phiếu hủy/đã thu. Máy chủ kiểm tra số nguyên không âm, giữ giá 0; Receipt thu theo số cuối cùng đã chốt. Phiếu cũ dùng tổng snapshot, không đổi tiền đã thu. Phiếu đã chốt bất biến, muốn đổi dùng hủy/lập lại theo quyền hiện có. Trang cần đăng nhập, có tiền bằng chữ, responsive và CSS in ẩn toolbar; chưa có link công khai/xuất ảnh tự động. Migration b35e10f97d42 đã áp dụng DEV sau backup backups/pre-bill-final-20261104-v150.sqlite3. Edge headless đạt desktop/390px/in; ảnh giả ở exports/receipt-preview-desktop.png và exports/receipt-preview-mobile.png. Chưa thử máy in giấy/điện thoại thật hoặc cập nhật VPS. Bước tiếp: restart web dev, Ctrl+F5; triển khai VPS cần upgrade DB trước mở web.


## 2026-11-04 — Chọn phòng lập phiếu (V1.4.13)

- Theo yêu cầu, dropdown vẫn có đủ mã phòng nhưng phòng đã có phiếu hiệu lực cùng kỳ không được đề xuất/lập mới. Hiện trạng thái Đã lập phiếu và khóa option; phiếu đã hủy không khóa lập lại. Khi tất cả đã có phiếu, khóa nút lập mới.
- Gửi room_id bằng form GET do server xử lý thay cho đổi href của link trong JS; lựa chọn hoạt động cả khi không có JS. Nếu phòng thiếu dữ liệu nghiệp vụ để lập phiếu, giữ phòng đã chọn và báo lý do thay vì tự quay phòng đầu. Không thay quy tắc tính tiền hoặc trạng thái phòng cũ.

## 2026-11-04 — Một ảnh công tơ và khóa theo phiếu (V1.4.2)

- Theo yêu cầu mới, mỗi ElectricityReading có tối đa một Photo ở DB, thay ảnh dùng cùng ID; ảnh hợp đồng không đổi. Thay thế chỉ xóa file cũ khi bản mới nén thành công, lỗi giữ ảnh cũ để không mất chứng cứ hiện tại. File fallback tạm không phải ảnh thứ hai có thể sửa trong UI.
- Phiếu tiền hiệu lực cùng phòng/kỳ khóa thêm/thay ảnh cho mọi vai trò; hủy hiệu lực phiếu theo quyền root hiện có thì có thể sửa lại. Không cần chờ ghi nhận thu đủ mới khóa. Chốt phiếu từ chối trong lúc ảnh pending để tránh nền thay ảnh sau chốt.
- Migration unique reading_id gộp nhóm trùng: ready mới nhất, nếu chưa ready thì job mới nhất. Backup cả DB/uploads trước nâng cấp, giữ file thừa trong backup; worker dọn file không còn tham chiếu sau 1 giờ. Không xóa số điện hoặc phiếu tiền.

## 2026-11-04 — Ảnh điện tùy chọn và upload tại bảng (V1.4.0)

- Theo yêu cầu mới, thay quy tắc V1.3.0: ảnh chốt/sửa điện không bắt buộc, cho bổ sung sau. File đã chọn phải hợp lệ; lưu số kèm ảnh là một giao dịch, upload bổ sung không thay chỉ số.
- Chọn/kéo thả chỉ giữ File và Object URL ở trình duyệt; bấm Lưu chỉ số/Lưu ảnh mới upload. Hiện phần trăm truyền byte riêng với bước nén, polling theo lô hữu hạn cập nhật thumbnail; không reload trang hoặc làm mất hàng khác. Preview hỗ trợ CSP blob:, ảnh server vẫn cần đăng nhập.
- Tái sử dụng Photo.token cho mã retry upload ảnh và BEGIN IMMEDIATE SQLite; không thêm migration/hạ tầng. Chốt điện vẫn unique phòng/kỳ, không tự gửi lại khi kết quả lưu chưa rõ. Bootstrap modal dùng chung xem bản WebP đã nén; thumbnail dùng cùng WebP với lazy-loading, chưa tạo file thumbnail riêng.

## 2026-11-03 — Ảnh hợp đồng/điện và nén nền (V1.3.0)

- Người dùng yêu cầu hợp đồng tùy chọn, ảnh chốt điện bắt buộc, lưu thư mục riêng và chỉ giữ ảnh nén dài hạn. Gắn ảnh hợp đồng theo đợt thuê, ảnh điện theo lần chốt; dữ liệu cũ giữ nguyên và có thể bổ sung. Chốt mới/sửa điện yêu cầu ảnh ở máy chủ, ảnh cũ không bị ghi đè.
- Dùng Pillow 13.0.0 và worker CLI riêng trong cùng project Flask; hàng đợi ở SQLite và OS lock một worker, không thêm Redis/Celery. Upload được xác nhận khi đã kiểm tra/lưu tạm và commit nghiệp vụ, trạng thái ảnh pending đến khi nén xong. Khi lỗi, giữ nghiệp vụ và báo failed để tải lại ảnh.
- Gốc chỉ ở tmp, xóa sau xử lý cả khi lỗi; dọn orphan sau 1 giờ khi worker hoạt động. WebP 2200 px/quality 82 bỏ metadata, chỉ xem qua xác thực. Backup cần DB và uploads tương ứng; VPS phải tăng Nginx lên 64m và chạy chdv-photos.service. Chưa tự triển khai VPS.

## 2026-11-03 — Bootstrap CDN và sidebar (V1.2.0)

- Theo yêu cầu mới, dùng Bootstrap 5.3.8 CSS/bundle từ jsDelivr có SRI; thay quyết định trước đây về giao diện chỉ dùng tài nguyên nội bộ. CSP thêm origin CDN, không thêm unsafe-inline/eval.
- Ưu tiên class Bootstrap, bỏ CSS tương đương; giữ CSS cho theme/sidebar/sticky và bố cục đặc thù. Chưa chuyển popup thu tiền native sang component Bootstrap.
- Bỏ animation sidebar tự chạy; khôi phục trạng thái trên html bằng script head trước paint để HTMX swap body không gây nhấp nháy. Cần mạng cho Bootstrap; chưa browser QA sau chuyển đổi.

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
