# Bàn giao

Cập nhật: 2026-11-03 (Asia/Saigon).

## Phiên bản hội thoại

- Phiên bản phản hồi gần nhất: V1.2.0.
- Nội dung: Bootstrap CDN, giảm CSS riêng và sửa sidebar nhấp nháy.
- Phản hồi tiếp theo tối thiểu V1.2.1; có thể tăng minor/major theo quy tắc mới trong AGENTS.md.
- Quy tắc đầy đủ ở AGENTS.md, mục “Phiên bản ở cuối phản hồi”.

## Đã làm

- App factory, .env cục bộ có SECRET_KEY ngẫu nhiên, SQLAlchemy, Flask-Login, CSRF và Flask-Migrate.
- instance/chdv.sqlite3 đã upgrade migration 0fecdf9f864b sau backup backups/pre-billing-*.sqlite3; root và dữ liệu hiện có được giữ. Không ghi mật khẩu vào tài liệu/fixtures/repo.
- Root và Admin mới phải đổi pass lần đầu: 8–128 ký tự, khác pass cũ, kiểm tra phía máy chủ.
- Root tạo/khóa/mở/reset Admin; mọi Admin có quyền phòng/điện, không có đăng ký công khai.
- Năm màn hình nghiệp vụ, cùng đổi mật khẩu và quản lý tài khoản root.
- Phòng có đợt thuê/người/xe; chốt điện nối tiếp tháng, không ghi đè dữ liệu cũ.
- HTMX và license lưu nội bộ, CSS riêng; không cần CDN lúc chạy.
- FE V1.1.7: sidebar xanh đậm/điểm nhấn mint, nền sáng, icon SVG nội bộ, trang đăng nhập hai cột có minh họa SVG. Thiết kế dùng chung cho mọi trang; bảng cố định mã phòng/thao tác khi cuộn, form rõ nhóm, responsive, focus bàn phím và reduced-motion. Không đổi route/model/service/JS nghiệp vụ.
- CLI backup nhất quán và bộ test tích hợp.
- Phí nước/người/tháng, dịch vụ/phòng/tháng cho phép 0; NULL của dữ liệu cũ là chưa biết. Hiển thị dự tính phí tháng đủ, chưa phải hóa đơn.
- Chỉ còn ngày bắt đầu hợp đồng (cũng là ngày vào ở), ngày hết hạn/trả thực tế và lịch đóng 1–31. move_in_date chỉ giữ làm cột legacy, không có ô nhập riêng; save/checkout đồng bộ theo contract_start.
- Tiền cọc theo đợt thuê: nguyên VND >=0, NULL legacy là chưa cập nhật. Có trên form/bảng/chi tiết/lịch sử, không cộng vào phí tháng hoặc xác nhận đã thu/hoàn.
- Tiền phòng rent_price theo đợt thuê, nguyên VND >=0, NULL legacy chưa cập nhật. Form/bảng/chi tiết/lịch sử có giá tháng; monthly_total = tiền phòng + nước + dịch vụ, chưa điện, không cọc. Gia hạn giữ giá hiện tại; khách mới nhập giá riêng.
- Gia hạn xem trước/xác nhận, 1–120 tháng, giữ ngày neo, audit Admin/thời điểm/hạn cũ-mới; version chống sửa/gia hạn lặp. Hợp đồng đã gia hạn không sửa trực tiếp ngày bắt đầu/hết hạn qua form.
- Đổi khách/ngừng sử dụng cần ngày trả thực tế và đúng version đợt thuê. Dữ liệu cũ không bị đoán ngày hoặc gán miễn phí.
- V1.1.9: link Sửa điện tại màn hình điện, preview/confirm, lý do bắt buộc, ReadingRevision lưu trước/sau/Admin/thời điểm, đồng bộ đầu kỳ sau khi cần. Chặn sửa nếu có phiếu tiền hiệu lực trong các kỳ bị ảnh hưởng.
- Menu Chốt tiền: chọn kỳ/phòng, nhập giá điện và kiểm tra giá phòng/nước/dịch vụ, số người; preview rồi chốt snapshot MonthlyBill. Phòng và điện cùng kỳ; không tự tính lại phiếu cũ khi đổi giá. Root có thể hủy hiệu lực có lý do, giữ bản cũ, lập lại; chưa theo dõi thực thu.
- Chỉ chốt tiền một đợt thuê xác định đủ tháng; thiếu điện, ngày không rõ, vào/trả giữa tháng hoặc đổi khách cùng kỳ bị chặn. Không có engine lịch giá tự động: giá trên form là gợi ý, Admin xác nhận cho từng kỳ.

## Kiểm tra

- V1.2.0: 47 unittest pass; Node syntax và 4 kiểm tra sidebar true/false/không lưu/storage bị chặn pass. Bootstrap CDN 5.3.8 có SRI/CSP; chưa browser QA/CDN runtime. Bước tiếp kiểm tra trực quan form/bảng/login và HTMX khi sidebar ẩn. Sidebar state lên html trước paint; bỏ animation sidebar. Không migration. Ưu tiên Bootstrap cho các thay đổi tiếp theo.

- V1.1.24: chỉ CSS/cache asset, kiểm tra tài liệu/diff; không chạy lại suite nghiệp vụ, chưa browser QA. Animation opacity cho surface/popover, slide nhẹ lúc sidebar hiện, hover/nhấn; không có hiệu ứng thoát khi sidebar ẩn. Không thêm JS/thư viện. Bước tiếp: kiểm tra chuyển trang HTMX, sticky table, popover và chế độ giảm chuyển động trên browser.

- V1.1.23: 11 test_billing pass, test mới kiểm tra tiền điện lịch sử theo snapshot, không đổi theo giá hiện tại, ưu tiên phiếu hiệu lực, giá 0/thiếu giá. Không đổi DB hoặc quyền root; Tài khoản nằm nav riêng trên profile. Chưa browser QA; bước tiếp kiểm tra vị trí sidebar trên màn thấp/mobile và cuộn ngang bảng lịch sử 6 cột.

- V1.1.21: render partial vehicle_cell với 2 xe/không xe/không khách; bỏ số đếm, không xe dùng dấu —. Chỉ template/CSS, không chạy lại suite nghiệp vụ; chưa browser QA. Tiếp theo kiểm tra trực quan nếu cần.

- V1.1.20: 5 test_receipts và smoke render bảng gọn/đầy đủ/chi tiết pass với DB tạm: 2 xe, nước 2 × 100.000 = 200.000, dịch vụ 150.000. Partial water_cell giữ NULL là chưa có giá, 0 là miễn phí; vehicle_cell dùng chung hai bảng. Không đổi schema/backend/phiếu cũ. Chưa browser QA; bước tiếp kiểm tra bảng nhiều xe, cuộn ngang/mobile và căn cột thực tế.

- V1.1.19: Node syntax và 10 test_billing pass. Sidebar dùng hidden/aria-expanded, localStorage có try/catch, bind trong enhancePage hỗ trợ HTMX. Không đổi DB/backend. Chưa browser QA; bước tiếp: kiểm tra ẩn/mở, điều hướng HTMX/reload, bàn phím/mobile và popover sau đổi độ rộng.

- V1.1.18: thay input month native (lấy ngôn ngữ browser) bằng partial period_select.html hiển thị Tháng x / năm, nhóm Năm. Giữ name period/value YYYY-MM/nút Xem; không cần JS, không đổi backend/DB. Danh sách quanh năm đang chọn +/-3; chọn năm mới rồi Xem để dịch cửa sổ. Kiểm tra test_billing và render ba màn; chưa browser screenshot cho thay đổi này.

- V1.1.17: thay template/CSS, gom badge và nút trong flex một hàng, bỏ nhãn Đã chốt tiền lặp (vẫn giữ Quá hạn), phòng/khách cùng dòng, giảm padding. Kiểm tra test_receipts và test_billing, không đổi DB/route hoặc thêm test mới cho thay đổi trình bày. Chưa chụp browser cho bố cục gọn này.

- V1.1.15: 5 test_receipts pass, node syntax pass. Edge headless trên HTML fixture/DB tạm xác nhận row height trước/sau mở =128px, popover hiện và nằm trong viewport đo; đã xem screenshot instance/payment-layout.png. Không sửa backend/schema/DB; không chạy lại toàn bộ suite cho thay đổi UI này.
- Payment menu/history dùng native Popover API top layer thay details nằm trong ô bảng; CSS fixed, max-height theo viewport, scroll nội bộ. JS neo theo nút, tránh mép, đổi vị trí khi resize/scroll/mở mục hủy. Escape/click ngoài/nút đóng do native popover xử lý. Cần browser hiện đại hỗ trợ Popover API.

- V1.1.14: 46 unittest pass; receive đủ tiền không tin amount gửi từ client, ngày hợp lệ, chống đúp/stale sau hoàn tác, quyền Admin/root, chặn hủy phiếu đã thu, root hoàn tác giữ audit và thu lại, 0 đồng, sort đã thu xuống dưới, bộ lọc phòng theo từng tháng. db check khớp schema, node syntax pass. Chưa browser E2E cho dropdown/compact table mới.
- Migration mới nhất 41eb1b88b816 đã backup/upgrade local (backups/pre-receipts-*.sqlite3). Receipt mới không tự coi phiếu cũ là đã thu; các phiếu cũ vẫn chưa thu đến khi Admin xác nhận.

- V1.1.12: chỉnh template/CSS trang chốt tiền, bỏ max-width 1000px riêng trang này; desktop từ1200px đặt input/preview cạnh nhau, trước preview 3 cột input; mobile giữ một luồng dọc. Không đổi nghiệp vụ/DB. Kiểm tra render qua test_billing.py; chưa chụp browser cho thay đổi bố cục này.

- V1.1.11: 41 unittest pass, kiểm tra thời điểm sửa từ revision, số tiền sau sửa/chốt phiếu, snapshot đơn giá và giá 0. Node smoke test live tiền 445 kWh × 4.000 = 1.780.000 đ, thiếu/0 giá, số sai; node syntax pass. Migration d94f512a37b1 đã backup/upgrade local (backups/pre-reading-dates-money-*.sqlite3), db check khớp. Chưa browser E2E cho bảng mới.

- V1.1.10: 39 unittest pass; sửa giá điện/nước/phòng giữ nguyên tổng phiếu cũ, form mới lấy giá mới, form version cũ bị chặn. Migration c83e4d16b2a0 đã backup/upgrade local (backups/pre-room-electricity-price-*.sqlite3), db check không drift. Chưa browser E2E cho thay đổi này.

- 38 unittest pass: bộ 31 cũ và 7 test sửa điện/ảnh hưởng kỳ sau/audit/stale, snapshot giá độc lập tháng, chống trùng, quyền root hủy, giá 0/âm/thiếu, chặn giữa tháng/thiếu điện và render/quyền trang mới.
- flask db check: không schema drift. node --check app/static/js/app.js: hợp lệ.
- Test client trên app local: /login trả HTTP 200; chưa đổi mật khẩu root thật khi test.
- .env, DB và SQLite sidecars bị Git ignore. Chưa commit/push trong lượt này.
- Đã kiểm tra ảnh tĩnh bằng Edge headless: đăng nhập/bảng phòng/form desktop và bố cục 390px với dữ liệu giả từ DB tạm. Ảnh trong instance/ui-*.png, ngoài Git. Edge có viewport tối thiểu ~492px nên bản 390px giới hạn chiều rộng root trong fixture, cùng breakpoint mobile. Chưa kiểm tra tương tác browser end-to-end trên server thật hoặc thiết bị điện thoại.
- Chưa bật Git hook, hosting hoặc lịch backup tự động.

## Chạy tiếp

    python -m flask --app wsgi run --host 127.0.0.1 --port 5000

Mở http://127.0.0.1:5000, đăng nhập root bằng pass bootstrap đã cung cấp rồi đổi pass. Clone mới làm theo README.md để tạo môi trường, .env, migration, root.

## Việc tiếp theo

- Dropdown Thu tiền trên phiếu: xác nhận nhận đủ bill.total, nhập paid_date/ghi chú. Lưu Receipt gồm amount/ngày/người/thời điểm; chỉ root hoàn tác có lý do. Hoàn tác ghi nhận không thực hiện hoàn tiền thật. Chưa thu một phần.
- Không hủy phiếu đang có receipt hiệu lực; root cần hoàn tác trước, rồi mới hủy/lập lại. Một receipt hiệu lực/phiếu, version lịch sử chặn form thu cũ sau hoàn tác.
- Chốt tiền xếp chưa thu quá hạn → chưa thu còn hạn → đã thu → hủy; cùng nhóm theo mã phòng/id. Bảng Phòng giữ mã phòng, mặc định 10 cột gọn (tiền kỳ từ phiếu, không dự tính), có filter thu và view đầy đủ giữ toàn bộ cột cũ.

- Bảng điện có Ngày chốt = created_at và Cập nhật lần cuối = max ReadingRevision.created_at, UTC hiển thị Asia/Saigon cả giờ/phút/giây. Chưa sửa thì hiện dấu gạch, không đoán ngày.
- Lưu điện mới chụp Tenancy.electricity_price vào reading. Tiền bảng: ưu tiên giá phiếu hiệu lực, sau đó giá lúc lưu điện; legacy thiếu giá dùng giá phòng hiện tại với nhãn tạm tính. Migration chỉ backfill giá từ phiếu hiệu lực cùng kỳ, không đoán giá cũ từ phòng.
- Phiếu lập mới vẫn lấy giá phòng hiện tại theo V1.1.10. Tiền trên bảng trước chốt phiếu là dự tính, không tự lập phiếu/thực thu. Giá phiếu có thể khác giá dự tính lúc lưu điện; khi đã chốt thì bảng ưu tiên giá phiếu.

- Tenancy.electricity_price nhập ở form phòng, có trên bảng/chi tiết/lịch sử. Tất cả giá của phiếu mới lấy từ điều khoản hiện tại; không lấy giá điện phiếu cũ nữa. Phiếu đã chốt giữ snapshot.
- “Sau lúc sửa” tính theo lúc lập phiếu: lập bù/lập lại tháng cũ cũng gợi ý giá hiện tại, Admin kiểm tra giá kỳ trước khi chốt. Chưa có lịch giá theo ngày/tháng.

- Đã triển khai phương án gọn trong BILLING_CORRECTIONS_PROPOSAL.md: cùng kỳ phòng/điện, form preview tạm (không lưu nháp), snapshot chốt, hủy/lập lại khi sai. Phần thực thu, công nợ, điện khác kỳ, chia ngày, lịch giá tự động chưa làm.

- FEES_CONTRACTS_PROPOSAL.md đã được triển khai theo phương án tối giản: chỉ lưu đơn giá/nhắc lịch, không chia ngày hoặc quản lý thực thu. Nếu cần tính phải thu, thiết kế kỳ/snapshot và giao dịch thu tiền riêng trước.

- Người dùng nhập thử phòng/xe/điện trên browser, nhất là điện thoại.
- Người dùng nhập thử hai luồng mới; chưa kiểm tra tương tác browser E2E cho module billing.
- Chốt luồng thay đồng hồ khi cần.
- Trước production: WSGI server, HTTPS/cookie secure, lịch backup ngoài máy, diễn tập restore và rà soát dependencies.

Xem STATUS.md để biết giới hạn chính xác.
