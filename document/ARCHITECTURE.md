# Kiến trúc hiện tại

V1.5.0: service billing kiểm tra số thu cuối cùng/lý do, giữ tổng tính từ snapshot riêng. JS dùng số nguyên BigInt để xem tổng ngay trên form; máy chủ tính và kiểm tra lại. GET /bills/<id> yêu cầu đăng nhập, trình bày phiếu riêng với CSS in, trạng thái Receipt/hủy và tiền bằng chữ. bill_history_query trả cả phiếu hiệu lực/hủy của phòng; template dùng các subtotal từ model. Không thêm framework/dependency hoặc dịch vụ mới.

V1.4.13: bộ chọn phòng lập phiếu là form GET gửi room_id/period/action về billing.index, máy chủ redirect đúng billing.create; bỏ liên kết mặc định phòng đầu và JS đổi href để tránh phụ thuộc HTMX/JavaScript. Dropdown giữ mọi mã phòng, phiếu hiệu lực trong kỳ được đánh dấu/disabled, đề xuất phòng chưa có phiếu. Lỗi mở form lập phiếu giữ room_id khi quay về danh sách. GET tạo phiếu cũng chặn phòng đã có phiếu hiệu lực; POST vẫn giữ kiểm tra giao dịch hiện có. Không đổi schema.

V1.4.2: Photo có unique reading_id và previous_token. stage_photo dùng lại record điện khi thay ảnh, kiểm tra active MonthlyBill và không thay khi pending. Worker chỉ xóa file cũ sau commit ready, fallback ảnh cũ khi failed; dọn output không còn tham chiếu sau 1 giờ để khôi phục crash. Chốt tiền và upload cùng khóa ghi SQLite; chốt phiếu bị chặn khi ảnh pending. Widget chỉ đọc khi phiếu hiệu lực, AJAX thay toàn bộ wrapper ảnh để không nhân đôi thumbnail. Migration a24d09e86c31 gộp ảnh điện trùng, giữ ảnh hợp đồng.

V1.4.0: ảnh điện tùy chọn tại service chốt/sửa. meter-photos.js quản lý File/preview local, XHR upload tiến độ byte, cập nhật các hàng đã lưu từ HTML trả trong JSON và polling /photos/status theo lô. Form thường vẫn hoạt động. Token upload dùng Photo.token hiện có và khóa ghi SQLite để retry bổ sung ảnh không tạo trùng. Thumbnail dùng WebP đã nén/lazy-loading, modal Bootstrap dùng chung; CSP img-src thêm blob: cho preview. Giữ hàng chưa gửi, không đưa file hàng chưa nhập số vào request. Không đổi schema/worker.

V1.3.3: ảnh công tơ được bổ sung ở màn billing.correct, tách form upload khỏi form sửa số. Route photos.add với electricity redirect về reading tương ứng; bảng điện dẫn tới mục meter-photos. Chi tiết phòng giữ xem ảnh lịch sử nhưng không còn form tải ảnh điện. Không đổi model/hàng đợi hoặc quy tắc bắt buộc ảnh khi xác nhận sửa số.

V1.3.0: bảng Photo gắn Tenancy hoặc ElectricityReading; services/photos.py kiểm tra upload, quản lý ảnh tạm/hàng đợi SQLite và nén bằng Pillow 13.0.0. CLI process-photos chạy một worker riêng, khóa OS chống trùng, ghi WebP nguyên tử rồi xóa gốc tạm. app/photos.py phục vụ ảnh qua xác thực và nhận bổ sung, không public uploads. Migration f13a98c52b70 chỉ thêm bảng. Request tối đa 64 MB; ảnh 10 MB/24 MP; WebP tối đa 2200 px/quality 82, bỏ metadata. Xem PHOTOS.md và deploy/chdv-photos.service về vận hành/backup/failure.

V1.2.2: services/queries.py chứa room_query và active_bill_query, không đặt query dùng chung trong route. services/electricity.py có reading_cost trả price/amount/estimated/current_price; màn điện truyền fallback giá hiện tại rõ ràng, lịch sử phòng không fallback. Route chuẩn bị dữ liệu, template không tính lại tiền điện.

V1.1.15: payment.html dùng native popover top layer; app.js định vị panel theo nút, cập nhật scroll/resize và toggle mục con. Chỉ thay UI để tránh giãn row/overflow clipping, không thay route/model/thu tiền. CSS/JS cache version1.1.15.

V1.1.14: route receive/reverse trong billing_routes.py, cùng transaction BEGIN IMMEDIATE và unique index để chống thu đúp. Receipt tách khỏi snapshot phiếu. Rooms route join phiếu hiệu lực/kỳ + receipt để lọc, giữ thứ tự mã phòng. Template compact_table/full_table chia hai cách xem; payment.html dùng details/summary làm dropdown không cần JS mới.

V1.1.11: electricity/routes.py lấy phiếu hiệu lực và max audit cho kỳ để bổ sung metadata bảng; template electricity/reading_meta.html dùng chung cho mỗi dòng. Live tiền ở app.js, kết quả server theo snapshot. local_datetime filter hiển thị UTC+7. Migration chỉ thêm giá đọc nullable, không thêm updated_at trùng lịch sử.

V1.1.10: đơn giá điện nằm trong Tenancy.electricity_price, được validate/lưu cùng giá phòng/nước, form chốt tiền lấy cùng nguồn điều khoản hiện tại. Không đổi cấu trúc snapshot MonthlyBill; sửa giá không cập nhật phiếu cũ. Dùng tenancy version đã có để chặn form cũ; chưa thêm engine lịch giá.

Một project Flask trả HTML bằng Jinja2. Bootstrap 5.3.8 CSS/bundle JS qua jsDelivr CDN có SRI cung cấp nút/form/bảng/alert và tiện ích; CSS riêng giữ theme/sidebar/sticky/responsive đặc thù. HTMX 2.0.4 nội bộ tăng tốc điều hướng qua hx-boost, form POST vẫn thông thường. JS tính điện khi nhập, khóa ô khách theo trạng thái và chống bấm lặp. Chưa dùng Alpine. CSP cho phép jsDelivr ở style-src/script-src, không bật unsafe-inline/eval. Cần mạng để tải Bootstrap.

Luồng: trình duyệt → blueprint → quyền/CSRF → service nghiệp vụ → SQLAlchemy → SQLite → redirect/HTML.

| Đường dẫn | Vai trò |
| --- | --- |
| wsgi.py | Entrypoint create_app |
| app/__init__.py | Factory, config, PRAGMA, middleware đổi pass, headers, CLI |
| app/extensions.py | db, login manager, CSRF, migration |
| app/auth/routes.py | Login/logout/đổi pass, root, tài khoản |
| app/rooms/routes.py | Bảng, form, chi tiết, xóa/ngừng phòng |
| app/electricity/routes.py | Bảng nhập điện theo kỳ |
| app/services/rooms.py | Validate phòng, chuyển đợt thuê |
| app/services/electricity.py | Chuỗi kỳ, validate số, giao dịch |
| app/services/contracts.py | Validate phí/ngày, trả phòng, lịch nhắc, cộng tháng và gia hạn |
| app/models/__init__.py | User, Room, Tenancy, Occupant, Vehicle, ElectricityReading, ContractRenewal |
| app/templates/ | Jinja2; partials/ để mở rộng sau |
| app/static/ | CSS/JS riêng, HTMX và license nội bộ |
| migrations/ | Alembic schema có version control |
| tests/test_v1.py | Tích hợp SQLite tạm và Flask test client |
| instance/ | DB local ngoài Git/static |
| backups/, logs/ | Runtime; chưa có scheduler/log file riêng |
| scripts/update_docs.py | Sinh danh mục file |
| document/, AGENTS.md | Trạng thái và quy tắc dev/agent |

## Quyền và phiên

User.is_root cho phép tạo/khóa/reset tài khoản. Tài khoản khác là Admin quản lý phòng/điện. Không tự đăng ký/nâng quyền, không khóa root từ web.

must_change_password kiểm tra mọi request đã đăng nhập; khi còn bật chỉ được đổi pass/logout/static. Hash Werkzeug scrypt. session_token xoay khi đổi/reset pass hoặc khóa/mở để hủy phiên cũ. CSRF mọi POST; cookie HttpOnly/SameSite Lax, Secure theo môi trường.

## Dữ liệu

- SQLite ổ đĩa cục bộ, WAL, foreign keys, busy timeout 5 giây. URL tương đối dưới instance/.
- Một bản điện/phòng/kỳ, nguyên không âm, DB check cuối >= đầu. Đầu kỳ nối tháng trước; không chèn lùi.
- BEGIN IMMEDIATE khi chốt SQLite để tuần tự hóa ghi và đọc lại lịch sử; sai một dòng rollback cả đợt.
- Unique index tối đa một tenancy mở/phòng.
- Ngừng phòng kết thúc đợt thuê, giữ lịch sử. Xóa hẳn chỉ khi chưa có thuê/điện.
- Backup dùng SQLite Backup API, đích mới. Chưa tự lập lịch hoặc lưu ngoài máy.
- UTC lưu DB, ngày hiển thị UTC+7 (Asia/Saigon). Chưa tính tiền.
- Phí/ngày nghiệp vụ trong Tenancy nullable để giữ dữ liệu cũ; NULL khác 0. Ngày thực tế dùng DATE, tách khỏi started_at/ended_at ghi nhận hệ thống.
- Tenancy.version là version_id_col SQLAlchemy: form có tenancy ID/version, chống stale edit/checkout/renew; DB update cũng kiểm tra version để chặn ghi đồng thời.
- Gia hạn có preview/confirm và audit ContractRenewal. Giữ contract_anchor_day, cộng tháng lịch 1–120. Không đổi phí hoặc tạo khách mới khi gia hạn.
- Ngày đóng 1–31 là lịch tham chiếu theo điều khoản hiện tại, không phải bảng phải thu hoặc thực thu. Chưa có snapshot phí/số người theo kỳ, dự tính tháng đủ không phải hóa đơn.
- Từ V1.1.5: contract_start là ngày vào ở/bắt đầu thống nhất. move_in_date giữ legacy, không chỉnh riêng; save/checkout đồng bộ theo contract_start. deposit_amount theo đợt thuê, không tham gia tổng phí tháng. Migration a65b2f9c018e không xóa cột ngày cũ.
- V1.1.6 bổ sung rent_price theo đợt thuê và migration b71c430e92ad. Tổng dự tính monthly_total = rent_price + monthly_fees; không tính điện/cọc, không phải hóa đơn.

## Giao diện V1.1.7

Thiết kế chia sẻ nằm trong app/static/css/app.css và shell base.html, icon macro trong partials/icons.html, minh họa SVG nội bộ. Bảng vẫn giữ tất cả dữ liệu, chỉ thay trình bày/sticky. Không đổi JS nghiệp vụ, route hoặc schema; xem UI_DESIGN.md.

## Module chốt tiền V1.1.9

app/services/billing.py xử lý sửa điện và snapshot phiếu; app/electricity/billing_routes.py cung cấp route correction, danh sách/tạo/hủy phiếu. Template billing/ và electricity/correct.html dùng layout hiện có. Không thêm framework/dependency; chỉ thêm 2 bảng. Nháp là form preview, chưa có state nháp dài hạn hoặc engine lịch giá.

## V1.6.0 — QR nhận tiền

Cấu hình /settings/payment dành cho root/Admin; service payment_settings lưu DB và ảnh riêng dưới uploads/payment. Route ảnh yêu cầu đăng nhập. Thay ảnh lưu file mới trước commit, dọn file cũ sau commit; khi lỗi commit xóa file mới. QR PNG lossless để giữ cạnh mã; không qua worker ảnh điện. Phiếu chưa thu hiển thị QR cạnh tài khoản, phiếu đã thu/hủy ẩn chuyển khoản. Không sinh QR hoặc tự xác minh dữ liệu ngân hàng từ ảnh. Backup cả DB và uploads; migration c46f21a08e53.

## V1.7.0 — Tạo QR cục bộ

V1.7.0: Đã hiện thực QR chuyển khoản tạo cục bộ bằng qrcode 8.2, TLV NAPAS/QRIBFTTA, CRC16-CCITT. Không gọi dịch vụ bên ngoài hoặc lưu ảnh cho từng phiếu. Dropdown 48 ngân hàng từ snapshot API Banks ngày 2026-11-04 ở app/data/banks.json; không có tác vụ mạng runtime. Admin chọn BIN và điền STK (giữ số 0 đầu, 1–19 ký tự ASCII chữ/số), tên chủ tài khoản, ghi chú. Máy chủ lấy ngân hàng từ allowlist, không tin tên ngân hàng gửi từ form. Ghi chú chỉ hiển thị trên phiếu, nội dung QR tự tạo theo P{id} {room} T{mmyyyy}; tiền dùng bill.total sau điều chỉnh, không nhận override từ query string.

Migration d57032b19f64 thêm bank_bin nullable, không đoán BIN từ tên cũ; admin cấu hình ngân hàng để bật QR mới. Ảnh QR cũ được giữ và dùng fallback khi chưa có BIN, không xóa dữ liệu cũ. QR đã thu/hủy/0 đồng không được phát; tổng trên 13 chữ số không sinh QR nhưng vẫn mở phiếu được. Thông tin nhận tiền là cấu hình chung hiện tại. Tên chủ TK không tự xác minh; không tự ghi nhận đã thu khi tạo/quét QR.

DEV đã backup backups/pre-local-vietqr-v162.sqlite3 và upgrade/db check đạt. QR đối chiếu vector nguồn độc lập và đọc ngược PNG bằng ZXing-C++; Edge kiểm tra QR từng phiếu chứa số cuối cùng 1.234 thay vì query giả 1, STK/nội dung đúng, QR crop trên mobile đọc được, responsive/in và regression ảnh điện đạt. ZXing-C++ chỉ dùng QA, không cần cài trên VPS. Chưa quét bằng app ngân hàng thật hoặc triển khai VPS, không xác nhận tương thích thực tế với mọi ngân hàng. Cần cài requirements mới, migration rồi restart web/worker khi đưa lên VPS; quét thử bằng ngân hàng để đối chiếu người nhận/số tiền/nội dung trước khi dùng gửi khách.

## V1.7.2 — Nội dung chuyển khoản tùy chọn

Bật/tắt qua PaymentSettings.auto_transfer_content, mặc định bật cho cấu hình cũ. Máy chủ dùng công tắc để quyết định sinh tag 62/08; khi tắt phiếu cũng ẩn dòng nội dung. Bỏ nội dung QR để ngân hàng/người chuyển xử lý mặc định, không ép nội dung trống ở ứng dụng ngân hàng. Tiền và tài khoản giữ nguyên. Migration e68143c20a75; không áp dụng để sửa nội dung ảnh QR legacy do admin upload.

## V1.8.0 — Phiếu thay thế và định dạng chung

Admin được sửa phiếu chưa thu bằng edit_bill: khóa ghi/kiểm tra stamp và trạng thái, tạo bản mới từ snapshot cũ, hủy bản gốc có audit trong cùng transaction. Không cập nhật đè snapshot hoặc đổi hợp đồng. Chỉ root được hủy riêng/hoàn tác thu. app/utils/formatting.py tập trung parse/format tiền và ngày, UTC+7 cho hiển thị/đồng hồ nghiệp vụ; formats.js xử lý input và app.js dùng helper này để tính trước. Chuỗi đẹp gửi về máy chủ được kiểm tra lại, tiền vẫn số nguyên, timestamp lưu UTC. ISO chỉ giữ ở giao thức/URL và dữ liệu máy; giao diện dùng dd/mm/yyyy và mm/yyyy. Không thêm dependency/schema. Xem LOCALIZATION.md.

## V1.9.0 — Nhật ký sửa giá

Chỉ dùng adjustment_reason trên form. Chỉ yêu cầu khi đơn giá hoặc tổng tiền thu thay đổi; thay ngày đến hạn không bắt lý do. Lý do điều chỉnh cũ được giữ trên snapshot khi sửa thông tin không liên quan đến giá. BillChange liên kết bản trước/sau, reason mới và actor/time, ghi nguyên tử cùng thao tác thay phiếu. bill_change_query đọc theo room/kỳ; change_history_rows tạo diff có định dạng, template chỉ trình bày. Nhật ký hiển thị dưới form và trong phòng, không nằm trong phiếu gửi khách. Chưa có log chi tiết trước migration f79254d31b86; không suy diễn từ chuỗi cancel_reason cũ.

## V1.9.2 — Quyền sửa điện và ảnh công tơ

Admin và root được hủy phiếu chưa thu với lý do để mở khóa sửa điện/ảnh. Phiếu đã thu vẫn chặn hủy; chỉ root có quyền hoàn tác ghi nhận thu. Các mô tả trước đây yêu cầu root hủy cả phiếu chưa thu được thay bằng quy tắc này. Link sửa điện và ô chọn/thay ảnh luôn hiện; còn phiếu hiệu lực thì service từ chối lưu với thông báo cần hủy trước. Bảo toàn kiểm tra kỳ sau, serializing ghi SQLite và snapshot phiếu cũ. Không thay schema.
