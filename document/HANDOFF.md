# Bàn giao

## 2026-11-04 — Lưu ảnh phiếu tại client

V1.10.0: Thêm nút Lưu ảnh phiếu trên trang phiếu. Dùng html2canvas 1.4.1 vendored (MIT, kèm LICENSE) tạo PNG rộng 1600 px hoàn toàn trong trình duyệt; chỉ chụp card, không toolbar/modal/nhật ký. Chờ font và ảnh QR decode, đưa pixel QR đã tải vào bản clone để tránh lấy lại QR khác với tài khoản đang hiển thị. Không thêm endpoint upload, không lưu file trên server/localStorage. Blob URL được thu hồi khi tạo ảnh mới/rời trang.

Mở dialog ảnh xem trước, có tải PNG; nếu navigator.canShare({files}) hỗ trợ thì hiện Chia sẻ / Lưu ảnh để người dùng chọn đích lưu. Tách bước tạo ảnh và chia sẻ để giữ user activation của lần bấm chia sẻ. Hủy share không báo lỗi; share không được có tải ảnh dự phòng; thiếu QR/không tạo ảnh được thì báo lỗi và giữ In phiếu. Không thể tự ghi vào album trên mọi trình duyệt; cần người dùng chọn lưu/chia sẻ/nhấn giữ ảnh. Chưa kiểm tra menu album trên iPhone/Android thật.

Thu nhỏ trạng thái nằm cạnh tháng, bỏ tiền bằng chữ khỏi phiếu và bỏ tính amount_words trong route; tổng tiền là một dòng lớn, co cỡ chữ khi màn hình hẹp/số dài. Giữ rõ trạng thái đã thu/hủy, QR và quy tắc tính tiền. Không đổi schema/dependencies Python hoặc thao tác VPS. Restart web dev/Ctrl+F5 để thử; các ZIP triển khai cũ không có tính năng này.

Kiểm tra hiện có: 88 unittest OK (49.117s); Node syntax đạt. Edge đã tạo/tải PNG desktop và mobile viewport, kích thước 1600 px, ZXing đọc được QR/số tiền; theo dõi request không có POST/upload trong export. Mock Web Share kiểm tra file và nhánh hủy; không coi mock là xác minh menu hệ điều hành. Ảnh fixture: exports/receipt-export-desktop.png, exports/receipt-export-mobile.png. QA dùng cache đúng Bootstrap 5.3.8 từ exports/browser-assets nếu có; không nới CSP và không cài thư viện QA lên VPS.


V1.9.13: Theo yêu cầu đã xóa toàn bộ mục tmux khỏi document/Lệnh Hay Dùng.md, giữ các hướng dẫn screen. Đã kiểm tra file không còn chuỗi tmux; chỉ sửa tài liệu, không gỡ phần mềm hoặc thao tác VPS.

V1.9.12: Người dùng xác nhận muốn screen quản lý phiên giữ chính pipeline log Nginx rút gọn trong ảnh. Hướng dẫn tạo shell screen -S chdv-web rồi chạy pipeline bên trong, detach Ctrl+A d, screen -ls/-r, -d -r khi Attached, chuyển phiên bằng detach/attach; đóng hẳn bằng Ctrl+C rồi exit. Phân biệt giữ phiên qua SSH với reboot. Không thay cấu hình/code/VPS; ghi lệnh vào Lệnh Hay Dùng.md.

V1.9.11: Người dùng xác nhận ảnh tail access.log vẫn không phải màn hình mong muốn. Dừng suy đoán và hỏi phân biệt terminal Python/Flask, log truy cập rút gọn hay chia ô terminal. Chưa đổi Gunicorn/systemd hoặc chạy web thứ hai; chờ người dùng xác định loại terminal. Không thao tác VPS/code.

V1.9.10: Ảnh người dùng có [screen is terminating], prompt root rồi tail chạy trực tiếp và ^Ad in ra, chứng tỏ không còn ở screen. Hướng dẫn Ctrl+C về shell, tạo screen -dmS chdv-log bash -c với tail access.log và exec bash, attach rồi Ctrl+A thả tay nhấn d để detach. Không thay VPS/code; Ctrl+C chỉ dừng tail.

V1.9.9: Ảnh screen của người dùng đang xem journalctl (startup/stop Gunicorn), không phải request. Hướng dẫn Ctrl+C rồi tail -F access.log Nginx có awk rút gọn ngay trong screen hiện tại; giữ attach/detach cũ. Ảnh có log Started chdv/chdv-photos lúc 14:19:21, nhưng chưa có kiểm tra HTTPS/upload sau deploy. Không sửa code/cấu hình/VPS.

V1.9.8: Người dùng muốn GNU screen theo lệnh nhớ dạng -m -d. Hướng dẫn screen -dmS chdv-log bash -c với journalctl web/worker, screen -r, Ctrl+A d và screen -ls; phân biệt phiên nền với chia ô. Chỉ bổ sung tài liệu, không cài/chạy trên VPS.

V1.9.7: Hướng dẫn tmux chia hai ô terminal, một ô journalctl theo dõi chdv/chdv-photos, ô còn lại thao tác hoặc tail access.log. Có detach/attach giữ phiên SSH và phân biệt với service systemd; không chạy thêm web thủ công. Ghi lệnh vào Lệnh Hay Dùng.md. Chưa cài/chạy tmux trên VPS; vẫn chưa có log người dùng xác nhận start/status/HTTPS sau cập nhật.

V1.9.6: Người dùng gửi kết quả VPS 88 tests OK trong 65.208s sau khối cập nhật. Chưa gửi riêng db current/check nên không xác nhận trực tiếp head từ log mới. Backup giữ tại /root/chdv-before-v193-Vh5xOts7. Bước tiếp start chdv/chdv-photos, kiểm tra status và HTTPS /login; chưa có bằng chứng dịch vụ đã mở lại hoặc kiểm tra trình duyệt. Không thao tác SSH hoặc sửa code.

V1.9.5: Người dùng xác nhận VPS kiểm tra ZIP Done testing, backup-db thành công và tar -tzf đạt. Backup thực tế /root/chdv-before-v193-Vh5xOts7 gồm database.sqlite3 104K, project.tar.gz 410K, chdv.service/chdv-photos.service/nginx-chdv.conf. Hai service đã được dừng bởi khối backup. Bước tiếp: giải nén /opt/chdv/chdv-v1.9.3.zip vào /opt/chdv, cấp owner/quyền code, pip install, db upgrade/check/current và unittest. Chưa có kết quả thay code/migrate/test/start VPS; không tự thao tác SSH. Head cần đạt f79254d31b86.

V1.9.4: Chuẩn bị triển khai bản code V1.9.3 lên VPS theo yêu cầu có backup. Thống nhất upload /opt/chdv/chdv-v1.9.3.zip, app /opt/chdv, VPS 103.167.88.214/domain chdv.alominh.homes. Ghi DEPLOY_V193.md đủ bước CRC, dừng chdv/chdv-photos, backup-db + tar code/.env/instance/uploads + cấu hình, thay code/cài requirements/migrate đến f79254d31b86/test/start/HTTPS. Full suite local 88 tests OK (55.539s). Chưa thao tác SSH hoặc xác nhận VPS đã backup/cập nhật; bước tiếp người dùng upload đúng đường dẫn, kiểm tra ZIP và gửi kết quả backup. Không đổi code/DB local trong lượt đóng gói.

V1.9.3: Bỏ cảnh báo lặp trên trang sửa điện. GET giữ một banner hướng dẫn hủy phiếu; khi có flash danger thì không render banner vàng. Widget ảnh không lặp hướng dẫn trên billing.correct, vẫn hiện nhắc khóa ở bảng điện. Không ẩn lỗi máy chủ hoặc đổi quyền/guard. Kiểm tra fixture: GET một cảnh báo, POST bị chặn một lỗi đỏ/không cảnh báo vàng; 16 photo tests OK (9.347s). Không đổi DB/VPS.

## 2026-11-04 — Admin hủy phiếu chưa thu để sửa điện

V1.9.2: Admin được hủy phiếu chưa thu với lý do; route cancel dùng login_required và vẫn khóa ghi/kiểm tra lại paid_receipt, lưu cancelled_by/at/reason. Admin không được hoàn tác thu; phiếu đã thu không hủy trực tiếp. Root vẫn xử lý hoàn tác thu có lý do trước khi hủy.

Luôn giữ link Sửa điện và widget chọn/kéo/thay ảnh kể cả khi có phiếu hiệu lực. UI báo cần hủy trước; thử sửa số hoặc lưu ảnh bị máy chủ từ chối khi phiếu còn hiệu lực. Không bỏ guard giao dịch ở correction/stage_photo. Sửa số ảnh hưởng đầu kỳ sau vẫn kiểm tra phiếu khóa tại mọi kỳ bị ảnh hưởng. Sau Admin hủy phiếu chưa thu, Admin sửa số/ảnh được; snapshot phiếu đã hủy giữ nguyên. Fallback upload không JavaScript cũng giữ sẵn và kiểm tra máy chủ.

Không đổi schema/DB runtime/dependencies hoặc cập nhật VPS. Bước tiếp restart web dev/Ctrl+F5. Gói ZIP V1.7.0 cũ không chứa thay đổi này.


## 2026-11-04 — Một lý do sửa giá và nhật ký phiếu

V1.9.0: Form sửa phiếu chỉ còn một ô Lý do sửa giá (adjustment_reason), bỏ edit_reason. Client hiện/bắt buộc ô này khi đơn giá hoặc tiền thu cuối cùng khác bản gốc; máy chủ kiểm tra lại độc lập. Đổi ngày đến hạn không bắt lý do, giữ lý do làm tròn/điều chỉnh đã có trên snapshot khi không nhập lý do mới. Không tự điền lại lý do cũ vào ô nhập để tránh dùng nhầm làm lý do cho lần sửa mới. Giá đổi nhưng tổng được giữ nguyên vẫn cần lý do.

Thêm BillChange với FK old_bill_id/new_bill_id duy nhất, reason tối đa 500, created_by/created_at; ghi cùng transaction thay phiếu, rollback không để lại log/bản mới. Nhật ký dưới form và chi tiết phòng có các trường trước → sau, ID phiếu/kỳ, người sửa và giờ Việt Nam. Lưu xong chuyển về form bản mới để thấy nhật ký ngay. Nhật ký quản trị không đưa vào phiếu gửi khách. Không suy đoán/backfill nhật ký cho các lần sửa trước nâng cấp; lịch sử snapshot cũ vẫn giữ.

DEV đã backup backups/pre-bill-change-log-v190.sqlite3 và migrate e68143c20a75 → f79254d31b86; db check đạt. Chưa cập nhật VPS. Bước tiếp restart web dev/Ctrl+F5; khi triển khai VPS phải chạy migration mới. ZIP V1.7.0 cũ không chứa sửa này.


## 2026-11-04 — Sửa phiếu và định dạng Việt Nam

V1.8.0: Thêm nút Sửa tại bảng chốt tiền cho phiếu chưa thu/còn hiệu lực. Root/Admin xem trước rồi xác nhận, bắt buộc lý do tối đa 450 ký tự. Sửa tạo bản thay thế trong cùng giao dịch, đánh dấu bản cũ hủy và ghi ID bản mới/người sửa/thời điểm/lý do; giữ giá, người thuê và chỉ số từ snapshot cũ, không lấy lại giá hợp đồng hiện tại. Chặn phiếu đã thu/đã hủy, dữ liệu form cũ và gửi lặp; rollback khôi phục bản cũ nếu commit lỗi. Hủy riêng và hoàn tác thu vẫn chỉ root. Không đổi schema.

Dùng app/utils/formatting.py cho tiền nguyên VND, ngày dd/mm/yyyy, kỳ mm/yyyy, timestamp Việt Nam UTC+7; app/static/js/formats.js dùng chung cho mọi ô tiền/ngày, có HTMX enhancement và giữ vị trí gõ. Ô tiền hiển thị dấu chấm và đ ngay lúc nhập; máy chủ nhận cả số nguyên canonical và chuỗi nhóm hợp lệ, giữ phân biệt 0/thiếu. Không áp định dạng tiền cho STK hoặc chỉ số kWh. Ngày nhập hiển thị cố định dd/mm/yyyy bằng text input, kiểm tra ngày lịch/max cả client và server; vẫn nhận ISO khi gửi trực tiếp để tương thích dữ liệu/giao thức cũ. Không đổi UTC lưu trữ, không đổi timezone OS/VPS hoặc log hệ thống.

Kiểm tra: 85 unittest OK (50.161s); sau gom helper giá chạy lại 15 billing + 6 formatting/edit đạt. Node syntax và db check đạt, head vẫn e68143c20a75. Edge đã kiểm tra gõ số thành 1.000.000 đ, sửa số đầu, gửi giá/ngày qua form phòng lưu đúng, chặn ngày không tồn tại, preview/confirm sửa phiếu và giữ snapshot; QR/ảnh điện regression vẫn đạt. Chưa thử điện thoại thật, chưa triển khai VPS. Restart web dev/Ctrl+F5 để dùng. Gói ZIP V1.7.0 cũ không chứa bản sửa này.


## 2026-11-04 — Nội dung QR tùy chọn

V1.7.2: Thêm công tắc Tự điền nội dung chuyển khoản ở Nhận tiền cho root/Admin. Bật: tạo nội dung theo mã phiếu/phòng/tháng. Tắt: bỏ hoàn toàn tag 62/08 trong QR và ẩn dòng nội dung trên phiếu, để app ngân hàng/người chuyển dùng mặc định; app không kiểm soát chuỗi mặc định của ngân hàng. Số tiền cuối cùng, BIN/STK và ghi chú hiển thị không đổi. Cấu hình chung áp dụng ngay cho phiếu chưa thu.

Migration e68143c20a75 thêm PaymentSettings.auto_transfer_content Boolean non-null, mặc định true để giữ hành vi cấu hình cũ; checkbox bỏ chọn được máy chủ lưu false. DEV đã backup backups/pre-content-switch-v172.sqlite3 rồi upgrade/db check đạt. 79 unittest OK (49.330s), gồm kiểm tra cả bật/tắt, tag nội dung có/vắng và số tiền không đổi. Chưa triển khai VPS hoặc quét bằng app ngân hàng thật. Gói chdv-v1.7.0.zip cũ chưa chứa sửa này. Bước tiếp: restart web dev/Ctrl+F5, mở Nhận tiền đổi công tắc và lưu.


## 2026-11-04 — QR tạo cục bộ V1.7.0

V1.7.0: Đã hiện thực QR chuyển khoản tạo cục bộ bằng qrcode 8.2, TLV NAPAS/QRIBFTTA, CRC16-CCITT. Không gọi dịch vụ bên ngoài hoặc lưu ảnh cho từng phiếu. Dropdown 48 ngân hàng từ snapshot API Banks ngày 2026-11-04 ở app/data/banks.json; không có tác vụ mạng runtime. Admin chọn BIN và điền STK (giữ số 0 đầu, 1–19 ký tự ASCII chữ/số), tên chủ tài khoản, ghi chú. Máy chủ lấy ngân hàng từ allowlist, không tin tên ngân hàng gửi từ form. Ghi chú chỉ hiển thị trên phiếu, nội dung QR tự tạo theo P{id} {room} T{mmyyyy}; tiền dùng bill.total sau điều chỉnh, không nhận override từ query string.

Migration d57032b19f64 thêm bank_bin nullable, không đoán BIN từ tên cũ; admin cấu hình ngân hàng để bật QR mới. Ảnh QR cũ được giữ và dùng fallback khi chưa có BIN, không xóa dữ liệu cũ. QR đã thu/hủy/0 đồng không được phát; tổng trên 13 chữ số không sinh QR nhưng vẫn mở phiếu được. Thông tin nhận tiền là cấu hình chung hiện tại. Tên chủ TK không tự xác minh; không tự ghi nhận đã thu khi tạo/quét QR.

DEV đã backup backups/pre-local-vietqr-v162.sqlite3 và upgrade/db check đạt. QR đối chiếu vector nguồn độc lập và đọc ngược PNG bằng ZXing-C++; Edge kiểm tra QR từng phiếu chứa số cuối cùng 1.234 thay vì query giả 1, STK/nội dung đúng, QR crop trên mobile đọc được, responsive/in và regression ảnh điện đạt. ZXing-C++ chỉ dùng QA, không cần cài trên VPS. Chưa quét bằng app ngân hàng thật hoặc triển khai VPS, không xác nhận tương thích thực tế với mọi ngân hàng. Cần cài requirements mới, migration rồi restart web/worker khi đưa lên VPS; quét thử bằng ngân hàng để đối chiếu người nhận/số tiền/nội dung trước khi dùng gửi khách.


V1.6.1: Chỉ phân tích tự tạo QR từ dropdown ngân hàng (BIN) và STK. Đề xuất cấu hình chung, QR từng phiếu dùng tổng cuối cùng và nội dung mã phiếu/phòng/kỳ; tên chủ TK nhập tay, tạo QR không đồng nghĩa xác minh chủ TK hoặc xác nhận đã thu. Hai hướng: dịch vụ VietQR Quick Link hoặc tự mã hóa payload trên VPS; cần cân nhắc phụ thuộc mạng/dữ liệu gửi bên ngoài và kiểm tra quét thực tế. Chưa sửa code/schema/DB/VPS. Nguồn chính thức: https://www.vietqr.io/qr-dong và https://www.vietqr.io/api-bank .

## 2026-11-04 — Nhận tiền và QR V1.6.0

Đã thêm quản trị Nhận tiền cho root/Admin đã đăng nhập: ngân hàng, số tài khoản (giữ số 0 đầu), chủ tài khoản, ghi chú và upload/thay/xóa QR. Kiểm tra CSRF/quyền ở máy chủ. QR PNG/JPEG/WebP tối đa 5 MB/4096 px, đọc kiểm tra và mã hóa PNG lossless bỏ metadata; lưu riêng PHOTO_ROOT/payment bằng token ngẫu nhiên, không lưu ảnh gốc hoặc URL bên ngoài. Ảnh chỉ xem sau đăng nhập. Thông tin dùng chung hiện tại, không snapshot vào phiếu: đổi cấu hình cập nhật mọi phiếu chưa thanh toán. Phiếu đã thu/hủy ẩn phần chuyển khoản. QR do admin lấy từ ứng dụng ngân hàng, không tự sinh/đọc hoặc đổi số tiền trong QR; cần dùng QR không cố định tiền và quét thử đúng tài khoản.

Thu gọn khoảng cách tiêu đề/thông tin/bảng/tổng/footer, đặt QR cạnh thông tin tài khoản. Có responsive 390px và CSS in. Chưa xác minh quét mã bằng điện thoại hoặc in giấy thật. QR trong kiểm tra là ảnh fixture, không phải QR thanh toán thật.

Migration mới c46f21a08e53 thêm payment_settings; DEV đã backup backups/pre-payment-settings-v160.sqlite3 rồi upgrade/db check đạt. Backup vận hành cần cả DB và instance/uploads (gồm payment). Không cập nhật VPS. 75 unittest đạt (48.815s), Edge headless đạt upload cấu hình/hiển thị phiếu desktop và 390px/print cùng regression ảnh điện. Ảnh xem thử exports/receipt-preview-desktop.png và exports/receipt-preview-mobile.png. Bước tiếp restart web dev, Ctrl+F5, mở Nhận tiền và cấu hình tài khoản thật trực tiếp trong app; khi triển khai VPS phải migrate trước mở web.


## 2026-11-04 — Phiếu tiền phòng V1.5.0

Kiểm tra: 73 unittest OK (44.715s), db check không phát sinh thay đổi, Node syntax đạt; dữ liệu các cột cũ so với backup giữ nguyên, SQLite integrity_check=ok.

V1.5.0: Đã triển khai trên dev trang phiếu riêng khi bấm ID, tổng tự tính và số thu cuối cùng kèm lý do bắt buộc khi khác tổng gốc; lịch sử phòng có cả phiếu hủy/đã thu. Máy chủ kiểm tra số nguyên không âm, giữ giá 0; Receipt thu theo số cuối cùng đã chốt. Phiếu cũ dùng tổng snapshot, không đổi tiền đã thu. Phiếu đã chốt bất biến, muốn đổi dùng hủy/lập lại theo quyền hiện có. Trang cần đăng nhập, có tiền bằng chữ, responsive và CSS in ẩn toolbar; chưa có link công khai/xuất ảnh tự động. Migration b35e10f97d42 đã áp dụng DEV sau backup backups/pre-bill-final-20261104-v150.sqlite3. Edge headless đạt desktop/390px/in; ảnh giả ở exports/receipt-preview-desktop.png và exports/receipt-preview-mobile.png. Chưa thử máy in giấy/điện thoại thật hoặc cập nhật VPS. Bước tiếp: restart web dev, Ctrl+F5; triển khai VPS cần upgrade DB trước mở web.


Cập nhật: 2026-11-04 (Asia/Saigon).

## Phiên bản hội thoại

- Phiên bản phản hồi gần nhất: V1.10.0.
- Nội dung: Xuất ảnh phiếu tại client với xem trước/tải/chia sẻ, trạng thái gọn và tổng một dòng bỏ tiền bằng chữ. DEV đã kiểm tra Edge, chưa mobile thật/VPS.
- Phản hồi tiếp theo tối thiểu V1.10.1; có thể tăng minor/major theo quy tắc mới trong AGENTS.md.
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

- V1.4.17: dùng skill imagegen để vẽ mockup, đã xem ảnh đầu ra: đủ 4 khoản, phép cộng 4.100.000 + 200.000 + 150.000 + 561.600 = 5.011.600 đ, trạng thái Chưa thanh toán, không thông tin khách thật/QR giả. Ảnh preview inline giữ ở đường dẫn mặc định generated_images của Codex, không tích hợp vào app. Chỉ cập nhật tài liệu thiết kế và phiên bản; inventory/check/diff đạt, không chạy suite nghiệp vụ vì chưa code. Khi triển khai phải dùng snapshot phiếu và trạng thái Receipt, phiếu hủy phải phân biệt rõ.

- V1.4.16: tin nhắn không rõ nội dung, đề nghị gửi lại. Không thao tác VPS hoặc thay code; vẫn chưa có kết quả cập nhật gói V1.4.13 trên VPS.

- V1.4.15 (2026-11-04): ảnh VPS xác nhận ZIP V1.4.13 ở /opt/chdv/chdv-v1.4.13.zip; kiểm tra đường dẫn /root báo FileNotFoundError, chưa phải ZIP hỏng. Sửa cả lệnh test và giải nén về /opt/chdv; giữ yêu cầu không backup lần này. Chưa có kết quả CRC/test/cập nhật hoặc restart web. Worker không cần dừng vì patch chỉ code web/billing.

- V1.4.14 (2026-11-04): ZIP code-only 5 file đã kiểm tra CRC và allowlist; chứa room_id/form mới và selected_room, không chứa runtime/migration. Bản VPS đã lên a24d09e86c31 theo log trước nên sửa này không cần nâng DB hoặc cài dependencies. Không tự thao tác VPS, chưa có kết quả upload; inventory/diff đạt, không chạy lại test vì chỉ đóng gói code đã đạt 67 tests/Edge ở lượt trước.

- V1.4.13 (2026-11-04): 67 unittest pass (38.671s), gồm 3 test room picker: gửi đúng ID và giữ chọn khi thiếu dữ liệu, đủ mã nhưng bỏ phiếu hiệu lực khỏi đề xuất theo kỳ/hủy phiếu mở lại, hết phòng khóa nút. Edge headless dùng DB/ảnh tạm: chọn T103 đến /rooms/3/bill đúng cả bật và tắt JS; option phòng đã có phiếu vẫn hiện nhưng disabled, các luồng ảnh cũ vẫn đạt/no pageerror. Node syntax đạt, inventory/diff đạt. Không đổi model/schema/DB thật, không tự cập nhật VPS. Bước tiếp restart dev/Ctrl+F5; gói V1.4.2 cũ không chứa sửa này, cần đóng gói mới nếu triển khai VPS.

- V1.4.12 (2026-11-04): giải thích VPS dùng systemd chdv/chdv-photos nên không cần giữ terminal, khác dev chạy thủ công hai terminal. Hướng dẫn systemctl status/start cho cả hai; nhận định enabled/active dựa log VPS người dùng đã gửi trước, không kiểm tra trực tiếp mới. Không chạy lệnh VPS hoặc đổi cấu hình. Inventory/diff đạt.

- V1.4.11 (2026-11-04): ảnh cho thấy terminal dev đã thoát Flask về prompt rồi chạy process-photos. Giải thích giữ terminal worker hiện tại, mở terminal thứ hai cùng thư mục dự án để chạy .venv Python flask run --port 5000; hai lệnh không chạy tuần tự trong cùng terminal. Không thao tác process/DB hoặc VPS. Inventory/diff đạt.

- V1.4.10 (2026-11-04): ảnh PowerShell xác nhận người dùng chọn y cho Stop-Process 4220, terminal trả prompt. Get-Process kiểm tra PID 4220 không còn chạy. Không suy ra mọi kết nối DB đều đã đóng; WAL/SHM còn có thể tồn tại. Không xóa file hoặc chạy checkpoint, không thay cấu hình. Inventory/diff đạt; nhắc mở lại worker bằng terminal riêng khi cần dùng upload dev.

- V1.4.9 (2026-11-04): người dùng hỏi SQLite dev không dừng, ảnh có WAL/SHM. Get-Process xác nhận worker nền đã tạo trước đó PID 4220 vẫn chạy; code lặp process_pending mỗi 2 giây. Giải thích SQLite không có service riêng và tắt web không dừng worker. Hướng dẫn Stop-Process -Id 4220 trên PowerShell cùng Ctrl+C terminal web để đóng các kết nối dev; chưa tự dừng worker vì lượt này chỉ hỏi nguyên nhân. Không xóa DB/WAL/SHM, không thao tác VPS. Inventory/diff đạt.

- V1.4.8 (2026-11-04): log VPS xác nhận chdv/chdv-photos enabled/active lúc vừa start, HTTPS /login 200 sau đó. Chưa nhận kết quả unittest VPS của bản V1.4.2, không suy ra test đã pass. Hướng dẫn Ctrl+F5 và kiểm tra một thumbnail/ảnh khóa ở kỳ đã có phiếu, thử thay ảnh chỉ trên kỳ chưa chốt với ảnh thật đúng phòng; không tạo/hủy phiếu hoặc sửa số để thử. Chưa có kết quả upload/thay/xóa file cũ trên browser VPS; backup /root/chdv-before-v142-mAvcspH9 cần giữ.

- V1.4.7 (2026-11-04): log VPS xác nhận tar backup kiểm tra không lỗi, giải nén/cấp quyền code/cài requirements, db upgrade f13a98c52b70 → a24d09e86c31, db check không drift và current head đúng. Hướng dẫn unittest, chỉ khi OK mới start chdv/chdv-photos và kiểm tra status/HTTPS. Chưa nhận kết quả tests/start hoặc ảnh trên VPS. Backup quay lui /root/chdv-before-v142-mAvcspH9; ZIP /root/chdv-v1.4.2.zip.

- V1.4.6 (2026-11-04): log VPS xác nhận chdv/chdv-photos inactive, backup-db hoàn tất, thư mục /root/chdv-before-v142-mAvcspH9 có DB, hai service và Nginx; dòng tên archive bị cắt ở project. Hướng dẫn tar -tzf archive >/dev/null trước thay code, sau đó giải nén ZIP /root/chdv-v1.4.2.zip, chown/chmod allowlist, pip requirements, db upgrade/check/current. Chưa nhận kết quả archive hoặc triển khai, dịch vụ còn dừng; chưa hướng dẫn start trước test.

- V1.4.5 (2026-11-04): log xác nhận /root/chdv-v1.4.2.zip zipfile -t Done testing. Hướng dẫn stop chdv/chdv-photos, xác nhận is-active đều inactive, backup-db và tar toàn project gồm uploads/.env (loại venv/cache/backups/ZIP), lưu systemd web/worker và Nginx vào thư mục mktemp riêng /root/chdv-before-v142-XXXXXXXX. Chưa nhận kết quả dừng/backup; chưa giải nén/migrate. Các lệnh tiếp dùng ZIP /root/chdv-v1.4.2.zip.

- V1.4.4 (2026-11-04): ảnh SFTP xác nhận chdv-v1.4.2.zip nằm /root/, lệnh kiểm tra /opt/chdv báo FileNotFoundError. Hướng dẫn zipfile -t /root/chdv-v1.4.2.zip; chưa kiểm tra ZIP thành công, chưa dừng dịch vụ/backup/giải nén. Các bước sau dùng đường dẫn ZIP /root/ nếu không chuyển file.

- V1.4.2 (2026-11-04): 64 unittest pass (46.535s), 16 test_photos pass (9.980s) sau điều chỉnh assertion IntegrityError. Có test unique DB, migration gộp nhóm trùng giữ ready mới nhất, thay thành công/xóa cũ, lỗi giữ fallback, không thay khi pending, khóa Root/Admin sau chốt phiếu và mở khóa khi phiếu bị hủy, không cho chốt tiền khi pending. Edge dữ liệu tạm đạt luồng V1.4.0 và thêm thay ảnh chỉ còn một thumbnail, dòng có phiếu không còn input upload/no JS errors. Đã dừng worker dev PID 4532, backup DB backups/pre-single-meter-photo-20261104.sqlite3 và ảnh backups/pre-single-meter-photo-files-20261104.zip, migrate a24d09e86c31, db check/integrity đạt, toàn bộ dữ liệu bảng nghiệp vụ khớp backup. Bản ghi ảnh điện trùng được gộp; file mồ côi được worker dọn sau 1 giờ, backup vẫn giữ ảnh cũ. Worker mới PID 4220 chạy ẩn cùng log paths cũ. Chưa cập nhật VPS; khi deploy phải backup DB+uploads và dừng cả web/worker trước migrate, sau đó restart cả hai. Chưa thử thực tế hai request song song trên VPS.

- V1.4.1 (2026-11-04): người dùng báo pending kéo dài ở dev. Kiểm tra job 1 pending, gốc tạm có, WebP chưa có; process-photos --once lấy được khóa và xử lý 1 job thành ready, gốc tạm đã xóa/WebP có. Đã Start-Process worker dev bằng .venv Python, WindowStyle Hidden, PID 4532; kiểm tra PID còn chạy và stderr rỗng. Log logs/photo-worker.stdout.log và photo-worker.stderr.log, ngoài Git. Không đổi code hoặc VPS; không cần chạy lại suite. Nếu worker này bị dừng/reboot, mở terminal chạy process-photos theo PHOTOS.md; không tự bật cùng Flask dev server. CIM liệt kê process bị Access denied, không dùng làm bằng chứng worker vắng; CLI lấy được khóa xác nhận không có worker giữ khóa lúc kiểm tra.

- V1.4.0 (2026-11-04): `.venv/Scripts/python.exe -m unittest discover -s tests`: 61 tests OK (41.992s); chạy lại 13 test_photos sau thêm assertion token không dùng cho owner khác: OK (9.251s). Script check_meter_photo_browser.py dùng Microsoft Edge headless và DB/ảnh tạm đạt: chọn/drop chưa tạo upload, lưu không ảnh, không gửi/mất ảnh của hàng chưa nhập số, upload bổ sung và upload kèm chốt mới, pending tự thành thumbnail, modal/Escape, giữ page marker/no reload, không pageerror. Cài Playwright vào venv chỉ cho QA, không thêm runtime dependency. Node syntax cả hai file JS đạt; db check không drift, không migration. Chưa thử mạng chậm/lớn/điện thoại thật và chưa cập nhật VPS. Bước tiếp chạy dev với worker, Ctrl+F5; nếu cập nhật VPS cần đóng gói code hiện tại, không dùng ZIP V1.3.4 cũ. Không thay .env/DB/ảnh dev.

- V1.3.13 (2026-11-04): chỉ phân tích theo yêu cầu chưa code, ghi METER_PHOTO_UX_PROPOSAL.md. Đề xuất bỏ bắt buộc ảnh chốt/sửa điện, preview kéo thả chưa upload, Lưu chỉ số kèm ảnh hoặc Lưu ảnh cho kỳ đã chốt, tiến độ byte 0–100 rồi polling job, thumbnail/modal trong bảng không reload. Đối chiếu code và MDN; chưa sửa app/test/VPS, chưa triển khai đề xuất. Inventory/diff đạt. Bước tiếp khi được yêu cầu triển khai: xử lý save/status AJAX, chống gửi trùng/phiên hết hạn, giữ worker/quyền riêng tư và kiểm thử luồng bất đồng bộ.

- V1.3.12 (2026-11-04): xác nhận có thể xóa riêng /opt/chdv/chdv-v1.3.4.zip sau khi giải nén/cập nhật, ứng dụng/worker không cần ZIP. Hướng dẫn rm -i đúng file, giữ /root/chdv-before-update-OREUjaIO và runtime; chưa có bằng chứng người dùng đã xóa, chưa nhận kiểm tra upload ảnh thực tế.

- V1.3.11 (2026-11-04): log VPS xác nhận chdv và chdv-photos enabled/active sau cập nhật, HTTPS /login 200 qua Nginx, cookie Secure. Hướng dẫn tải ảnh công tơ thực tế ở kỳ đã có, không đổi số; kiểm tra pending → Xem ảnh và tmp không còn .upload khi hàng đợi xong. Chưa nhận kết quả upload/nén hoặc xem ảnh; backup/restore DB+ảnh vẫn cần vận hành theo PHOTOS.md. Backup trước nâng cấp /root/chdv-before-update-OREUjaIO.

- V1.3.10 (2026-11-04): log VPS xác nhận 58 tests OK trong 41.727s, có DeprecationWarning datetime.utcnow tại app/auth/routes.py:43, chưa sửa ngoài phạm vi triển khai. Hướng dẫn cài/start worker, reload Nginx, start chdv và kiểm tra status/HTTPS. Chưa có log start dịch vụ hoặc upload thực tế sau cập nhật; backup quay lui /root/chdv-before-update-OREUjaIO.

- V1.3.9 (2026-11-04): người dùng gửi nginx -t syntax/test successful sau chỉnh site. Chưa có log cài worker từ đợt trước, nên nhắc install service/tạo uploads/daemon-reload trước enable. Hướng dẫn unittest trên VPS, nếu OK thì reload Nginx, enable/start worker và start chdv, kiểm tra status/curl HTTPS. Chưa nhận kết quả test/start/upload; không đánh dấu hoàn tất triển khai.

- V1.3.8 (2026-11-04): log VPS xác nhận giải nén/cấp quyền code, Pillow 13.0.0 cài thành công, upgrade 41eb1b88b816 → f13a98c52b70 và db check không drift. Hướng dẫn install worker service với mode 644 (shell còn umask 077), tạo uploads owner chdv, sửa Nginx 256k → 64m và nginx -t. Chưa start worker/web; chờ kết quả trước test/mở lại. Backup quay lui /root/chdv-before-update-OREUjaIO.

- V1.3.7 (2026-11-04): log xác nhận chdv đã stop, backup /root/chdv-before-update-OREUjaIO gồm database.sqlite3, project.tar.gz, chdv.service, nginx-chdv.conf. Hướng dẫn giải nén ZIP code, chown/chmod code vì shell umask 077, pip requirements, db upgrade/check; chưa nhận kết quả. Sau đó cần test VPS, Nginx 64m, worker service và mở lại web; chưa đánh dấu triển khai hoàn tất.

- V1.3.6 (2026-11-04): người dùng gửi zipfile -t /opt/chdv/chdv-v1.3.4.zip: Done testing. Hướng dẫn dừng chdv, tạo thư mục backup riêng dưới /root bằng mktemp, backup-db và tar toàn bộ project (loại .venv/cache/backups/ZIP) cùng systemd/Nginx. Chưa nhận kết quả backup; chưa giải nén/migrate. Web dự kiến tạm không truy cập sau stop; nếu lỗi phải dừng bước tiếp và gửi kết quả.

- V1.3.5 (2026-11-04): ảnh SFTP xác nhận ZIP nằm /opt/chdv/chdv-v1.3.4.zip; lệnh kiểm tra dùng /root/chdv-upload nên FileNotFoundError, chưa chứng minh ZIP hỏng. Hướng dẫn kiểm tra đúng đường dẫn; chưa giải nén hoặc cập nhật VPS. cls không có trên Ubuntu, dùng clear nếu cần. Chờ kết quả ZIP trước backup/cập nhật.

- V1.3.2: đọc log người dùng và DB local xác nhận no such table: photo, schema 41eb1b88b816. Backup trước upgrade rồi kiểm tra schema không drift, integrity ok, toàn bộ dòng/cột các bảng cũ khớp backup; smoke GET /electricity/ có phiên xác thực trả 200, không chỉnh user. Inventory/diff đạt; không chạy lại suite vì không đổi code. Không chứng minh bản copy live từ VPS có đầy đủ WAL, chỉ xác nhận dữ liệu bản nhập được giữ khi migrate.

- V1.3.1: đã tạo lại .env dev bị mất từ .env.example, SECRET_KEY ngẫu nhiên mới, DATABASE_URL local và COOKIE_SECURE=false; không đặt/reset mật khẩu root, không đổi DB hoặc VPS. App đọc cấu hình được và test client GET /login HTTP 200. Khóa mới làm phiên dev cũ hết hiệu lực. Inventory/diff đạt; không chạy lại suite nghiệp vụ vì chỉ khôi phục cấu hình local.

- V1.3.0: `.venv/Scripts/python.exe -m unittest discover -s tests`: 57 tests pass (34.859s), gồm 9 test ảnh: thiếu ảnh/rollback, upload giả/quá byte/pixel/ảnh động, quyền/CSRF/413, giữ ảnh theo đợt thuê, sửa điện bắt buộc ảnh mới, EXIF/resize/WebP/xóa gốc, worker lỗi/reupload/khôi phục sau rename, orphan cleanup và khóa worker. Pillow 13.0.0 cài riêng trong .venv (system-site-packages cho dependencies đã có), không đổi Python toàn cục. Migration f13a98c52b70 đã backup `backups/pre-photos-20261103-v130.sqlite3` rồi upgrade local; số dòng các bảng nghiệp vụ không đổi, integrity_check ok và db check không drift. Node syntax và inventory/diff đạt. Không tự khởi động worker nền lâu dài; mở terminal chạy process-photos theo PHOTOS.md khi thử dev. Chưa browser E2E, kiểm tra độ rõ ảnh hợp đồng thực tế, Ubuntu worker/HTTPS upload hoặc restore bộ DB+ảnh. Bước tiếp: thử ảnh giả qua UI dev, sau đó cập nhật VPS từng bước, tăng Nginx 64m, cài dependencies/migration và bật chdv-photos. Backup phải thêm uploads; không chỉ DB.

- V1.2.28: đã kiểm tra đường dẫn xóa nằm trong instance dev, xóa 23 mục artifact UI; liệt kê sau dọn chỉ còn .gitkeep và chdv.sqlite3 (94.208 byte), SHA256 DB trước/sau giống nhau. Inventory và diff whitespace đạt; không chạy lại test nghiệp vụ. Khi cần kiểm tra hình ảnh, tạo lại artifact; các ảnh/HTML cũ được nhắc trong bàn giao phía dưới đã được dọn.

- V1.2.3: đối chiếu code/config và nguồn chính thức để viết DEPLOY_UBUNTU.md; inventory và diff whitespace đạt. Chưa chạy lệnh Ubuntu, test Python 3.12, HTTPS hoặc restore trên VPS; không chạy lại test nghiệp vụ vì chỉ sửa tài liệu. Bước tiếp: xác định domain, cổng SSH, giữ DB cũ hay tạo mới và thực hiện hướng dẫn. Gunicorn chưa khóa phiên bản; lịch backup ngoài máy chưa triển khai.

- V1.2.2: 47 test suite pass; 12 test_billing pass sau khi th?m test helper. refactor giá điện và query đọc, không DB. Lịch sử không fallback giá hiện tại; màn nhập vẫn fallback có nhãn. Không gom validation kỳ vì cách báo lỗi khác nhau. Bước tiếp nếu cần: rà macro trường giá form phòng/phiếu; không gom khác biệt nghiệp vụ. Chưa browser QA.

- V1.2.1: 14 test_contracts pass. template form phòng đổi utility Bootstrap để rộng theo khung, phí 1/2/3 cột, thanh lưu trong luồng bình thường. Chưa browser QA. Bước tiếp kiểm tra thực tế desktop/mobile và chọn Đang thuê để mở ô khách; không thay logic disabled.

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

Kiểm tra V1.7.0: 78 unittest OK (50.165s), DB check/integrity đạt, cột dữ liệu cũ giữ nguyên so với backup. Edge đọc được QR ảnh gốc/crop mobile qua ZXing; không pageerror. Chưa quét app ngân hàng thật.

V1.7.1: Xác nhận QR cục bộ chạy trên local Windows; db current đã kiểm tra d57032b19f64 (head). Hướng dẫn chạy web bằng venv, vào Nhận tiền cấu hình và mở phiếu chưa thu để quét thử. Không đổi code hoặc thao tác VPS.

V1.7.2 — Edge headless đạt kiểm tra bật/tắt công tắc qua giao diện, lưu rồi đọc lại; ZXing đọc QR sau khi tắt không còn mã nội dung, số tiền vẫn 1.234. Không pageerror.

Kiểm tra V1.9.0: 88 unittest OK (50.065s); Edge đạt kiểm tra chỉ một ô lý do, ẩn khi không đổi giá/đổi hạn, hiện và bắt buộc khi đổi tiền, lưu xong thấy nhật ký dưới form. Ảnh fixture exports/bill-change-history.png. Node syntax, db check, integrity_check và foreign_key_check đạt; dữ liệu các cột cũ giữ nguyên so với backup. Chưa quét ngân hàng/điện thoại thật hoặc triển khai VPS.

V1.9.1: Giải thích luồng sửa chỉ số điện hiện có: nếu có phiếu hiệu lực thì root hủy phiếu trước; vào Chỉ số điện/Sửa điện, nhập lý do, preview/xác nhận rồi lập lại phiếu. Nếu đã thu cần root hoàn tác ghi nhận thu trước hủy; không tự hoàn tiền thật. Kỳ sau bị đồng bộ đầu kỳ cũng phải gỡ phiếu khóa liên quan. Chỉ hướng dẫn, đã đối chiếu service/route/template, không sửa code/DB/VPS hoặc chạy lại suite.

Kiểm tra V1.9.2: 88 unittest OK (50.854s), đăng nhập tách root/Admin để kiểm tra quyền thực tế. Admin bị chặn sửa điện/ảnh khi còn phiếu, hủy có lý do và audit đúng Admin rồi sửa được; phiếu đã thu không hủy được, reverse vẫn 403 cho Admin. Edge đạt widget vẫn hiện, thử lưu khi khóa nhận lỗi, ảnh đã lưu không đổi; regression QR/form/nhật ký đạt. Không thay schema hoặc thao tác VPS.

V1.10.0 — Kiểm tra cuối Edge: xuất PNG desktop/mobile thành công, QR đọc lại được; nhánh canShare=false vẫn có tải ảnh, hủy share không báo lỗi, lỗi decode QR hiện thông báo và nút lưu dùng lại được. Không pageerror, không POST/upload trong xuất ảnh; đã xem trực tiếp PNG và screenshot mobile. Chưa kiểm tra album native trên điện thoại thật.
