# Kiến trúc hiện tại

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
