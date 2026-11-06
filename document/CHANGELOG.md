# Lịch sử thay đổi

V1.10.15 (2026-11-06): Bỏ cảnh báo khóa ảnh hiển thị thường trực trong widget. Khi phiếu còn hiệu lực, hiện nút Chọn ảnh vàng; bấm mở native popover dùng cơ chế payment-panel hiện có, thông báo hủy phiếu chưa thu/root xử lý phiếu đã thu, đóng bằng ngoài/Esc/nút đóng. Popover nằm top layer không tăng chiều cao hàng và không bị vùng cuộn cắt. Không cung cấp file input khi khóa; kiểm tra máy chủ vẫn giữ nguyên. 16 test_photos OK (9.850s), gồm chặn trực tiếp root/admin và mở lại sau hủy phiếu. Edge assertions mở/đóng popup ở390px, không đổi chiều cao hàng, không vượt viewport, thao tác ảnh và không pageerror đều đạt; runner vẫn trả exit1 dù in passed và không traceback, hạn chế runner đã có từ lượt trước. Chưa triển khai VPS.

V1.10.14 (2026-11-06): Triển khai bảng chỉ số điện mobile <=680px: gom đầu/cuối, tiêu thụ/đơn giá, tiền thành ba dòng; mã phòng/trạng thái/sửa điện bên trái, ảnh nhỏ 44px và chọn ảnh bên phải. Hai cột Ngày chốt và Sửa đổi gần nhất vuốt ngang để xem, ngày/giờ hai dòng theo giờ Việt Nam hiện có. Giữ một bộ input/widget và bảng desktop, không đổi JS nghiệp vụ/DB/quyền. 16 test_photos và 17 test_v1 đạt; Edge chạy các assertion mobile 375/430px và desktop1280px, upload/thay ảnh/modal/lưu số điện/khóa phiếu đạt, không pageerror; đã xem ảnh exports/meter-mobile-layout.png. Lượt browser in thông báo passed nhưng runner trả exit1, không có traceback trong log stderr, nên chưa coi trạng thái thoát của runner là sạch. DB check không phát sinh migration; Node syntax, docs check và diff check đạt. Chưa triển khai VPS. Ghi nhận V1.10.13 ở lượt trước là yêu cầu thêm hai cột ngày, chưa được ghi vào HANDOFF khi đó.

V1.10.11 (2026-11-06): Theo yêu cầu giữ bảng như /bills, bỏ ghim ngang mã phòng/thao tác trên mobile <=680px cho cả bảng phòng gọn và đầy đủ, giữ ghim tiêu đề dọc và hành vi desktop. Bộ lọc phòng dùng lưới hai cột, tìm kiếm cả hàng; tăng phiên bản CSS tránh cache. Không đổi nghiệp vụ/DB. 17 test_v1 OK; kiểm tra CSS bằng Edge với cấu trúc bảng/bộ lọc ở 375/430/1280px đạt cuộn ngang, độ rộng bộ lọc và sticky desktop. Chưa kiểm tra trực quan trang thật có Bootstrap/CDN; lần thử render trang qua test client chưa đạt, không tính là kiểm tra trang thực hoàn thành. Chưa triển khai VPS.

V1.10.8 (2026-11-05): Người dùng cung cấp log cập nhật patch STK V1.10.7 trên VPS: ZIP Done testing, chdv và chdv-photos active, HTTPS /login HTTP 200. Ghi nhận triển khai theo log; chưa xác minh trực tiếp nhãn STK trên trang phiếu hoặc ảnh xuất. Bước tiếp mở phiếu và Ctrl+F5 để kiểm tra. Không backup theo yêu cầu, không đổi code trong lượt này.

V1.10.7 (2026-11-05): Xuất exports/chdv-v1.10.7.zip chỉ chứa app/templates/billing/detail.html thêm nhãn STK, dành cho VPS đã cập nhật V1.10.0. Đã kiểm tra CRC, danh sách file và nội dung nhãn. Hướng dẫn upload vào /opt/chdv rồi giải nén đúng đường dẫn, đặt quyền và restart web; không backup theo yêu cầu, không đổi DB/dependencies và không cần dừng worker ảnh. Chưa thực thi trên VPS.

V1.10.6 (2026-11-05): Thêm nhãn STK: trước số tài khoản trong phiếu tiền phòng, áp dụng cả bản in và ảnh xuất từ phiếu. Chỉ đổi nội dung template; chưa triển khai VPS. Kiểm tra tài liệu bằng update_docs.py và --check; không chạy lại unittest cho thay đổi nhãn hiển thị.

V1.10.5 (2026-11-05 Asia/Saigon): Người dùng xác nhận triển khai patch V1.10.0 trên VPS: ZIP Done testing, 6 test_bill_documents OK trong 4.635s, chdv/chdv-photos đều active, HTTPS /login HTTP 200 và cookie Secure. Cập nhật code/dịch vụ đạt theo log; chưa có bằng chứng thử nút xuất ảnh trên trình duyệt VPS/album điện thoại thật. DeprecationWarning datetime.utcnow ở auth/routes.py:43 không gây thất bại, chưa sửa ngoài phạm vi. Lần cập nhật này không backup theo yêu cầu; bộ backup V1.9.3 /root/chdv-before-v193-Vh5xOts7 vẫn là mốc trước đó. Bước tiếp Ctrl+F5, mở phiếu và thử Lưu ảnh phiếu/tải/chia sẻ.

V1.10.4 (2026-11-05 Asia/Saigon): Người dùng xác nhận ls -lb có /opt/chdv/chdv-v1.10.0.zip đúng 58861 byte và hostname -I=103.167.88.214. Đường dẫn/tên ZIP đã được xác nhận qua terminal, không kết luận nguyên nhân lần thiếu file trước. Hướng dẫn chạy lại khối test ZIP/stop web/extract/chown/chmod/test_bill_documents/start/status/HTTPS, không backup theo yêu cầu. Chưa có kết quả kiểm tra CRC hay triển khai mới trên VPS.

V1.10.2: VPS báo FileNotFoundError /opt/chdv/chdv-v1.10.0.zip ngay bước test ZIP. Vì set -e trong subshell, chưa chạy stop web/thay code/tests/start; lỗi apport /opt/chdv/-m là lỗi phụ khi báo exception. Chưa biết vị trí ZIP thực tế, không đoán là /root. Hướng dẫn find trong /root và /opt/chdv, hoặc upload bằng khung SFTP vào /opt/chdv, rồi test đúng đường dẫn trước khi chạy lại khối cập nhật. Giữ yêu cầu không backup. Không thao tác VPS hoặc sửa code.

V1.10.1: Theo yêu cầu chuẩn bị gói patch exports/chdv-v1.10.0.zip để upload /opt/chdv/, không backup lần này. Gói 7 file gồm route phiếu, receipt CSS/JS/template, html2canvas + LICENSE và test_bill_documents.py; dành cho VPS đã cập nhật V1.9.3 như phiên trước. Không có .env/DB/uploads/migration/requirements. Chỉ dừng web khi thay file, worker có thể giữ chạy; chạy bộ test phiếu rồi mở lại dịch vụ/kiểm tra HTTPS. Không cần pip hoặc db upgrade cho patch này. Chưa thao tác VPS hoặc xác nhận cập nhật; dùng kết quả 88 tests/Edge V1.10.0 đã ghi, không chạy lại chỉ vì đóng gói.

## 2026-11-04 — Lưu ảnh phiếu tại client

V1.10.0: Thêm nút Lưu ảnh phiếu trên trang phiếu. Dùng html2canvas 1.4.1 vendored (MIT, kèm LICENSE) tạo PNG rộng 1600 px hoàn toàn trong trình duyệt; chỉ chụp card, không toolbar/modal/nhật ký. Chờ font và ảnh QR decode, đưa pixel QR đã tải vào bản clone để tránh lấy lại QR khác với tài khoản đang hiển thị. Không thêm endpoint upload, không lưu file trên server/localStorage. Blob URL được thu hồi khi tạo ảnh mới/rời trang.

Mở dialog ảnh xem trước, có tải PNG; nếu navigator.canShare({files}) hỗ trợ thì hiện Chia sẻ / Lưu ảnh để người dùng chọn đích lưu. Tách bước tạo ảnh và chia sẻ để giữ user activation của lần bấm chia sẻ. Hủy share không báo lỗi; share không được có tải ảnh dự phòng; thiếu QR/không tạo ảnh được thì báo lỗi và giữ In phiếu. Không thể tự ghi vào album trên mọi trình duyệt; cần người dùng chọn lưu/chia sẻ/nhấn giữ ảnh. Chưa kiểm tra menu album trên iPhone/Android thật.

Thu nhỏ trạng thái nằm cạnh tháng, bỏ tiền bằng chữ khỏi phiếu và bỏ tính amount_words trong route; tổng tiền là một dòng lớn, co cỡ chữ khi màn hình hẹp/số dài. Giữ rõ trạng thái đã thu/hủy, QR và quy tắc tính tiền. Không đổi schema/dependencies Python hoặc thao tác VPS. Restart web dev/Ctrl+F5 để thử; các ZIP triển khai cũ không có tính năng này.

Kiểm tra hiện có: 88 unittest OK (49.117s); Node syntax đạt. Edge đã tạo/tải PNG desktop và mobile viewport, kích thước 1600 px, ZXing đọc được QR/số tiền; theo dõi request không có POST/upload trong export. Mock Web Share kiểm tra file và nhánh hủy; không coi mock là xác minh menu hệ điều hành. Ảnh fixture: exports/receipt-export-desktop.png, exports/receipt-export-mobile.png. QA dùng cache đúng Bootstrap 5.3.8 từ exports/browser-assets nếu có; không nới CSP và không cài thư viện QA lên VPS.


V1.9.13: Theo yêu cầu đã xóa toàn bộ mục tmux khỏi document/Lệnh Hay Dùng.md, giữ các hướng dẫn screen. Đã kiểm tra file không còn chuỗi tmux; chỉ sửa tài liệu, không gỡ phần mềm hoặc thao tác VPS.

V1.9.12: Người dùng xác nhận muốn screen quản lý phiên giữ chính pipeline log Nginx rút gọn trong ảnh. Hướng dẫn tạo shell screen -S chdv-web rồi chạy pipeline bên trong, detach Ctrl+A d, screen -ls/-r, -d -r khi Attached, chuyển phiên bằng detach/attach; đóng hẳn bằng Ctrl+C rồi exit. Phân biệt giữ phiên qua SSH với reboot. Không thay cấu hình/code/VPS; ghi lệnh vào Lệnh Hay Dùng.md.

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

V1.5.0: Đã triển khai trên dev trang phiếu riêng khi bấm ID, tổng tự tính và số thu cuối cùng kèm lý do bắt buộc khi khác tổng gốc; lịch sử phòng có cả phiếu hủy/đã thu. Máy chủ kiểm tra số nguyên không âm, giữ giá 0; Receipt thu theo số cuối cùng đã chốt. Phiếu cũ dùng tổng snapshot, không đổi tiền đã thu. Phiếu đã chốt bất biến, muốn đổi dùng hủy/lập lại theo quyền hiện có. Trang cần đăng nhập, có tiền bằng chữ, responsive và CSS in ẩn toolbar; chưa có link công khai/xuất ảnh tự động. Migration b35e10f97d42 đã áp dụng DEV sau backup backups/pre-bill-final-20261104-v150.sqlite3. Edge headless đạt desktop/390px/in; ảnh giả ở exports/receipt-preview-desktop.png và exports/receipt-preview-mobile.png. Chưa thử máy in giấy/điện thoại thật hoặc cập nhật VPS. Bước tiếp: restart web dev, Ctrl+F5; triển khai VPS cần upgrade DB trước mở web.


## 2026-11-04

- V1.4.17: tạo bản vẽ phiếu tiền phòng gửi khách bằng dữ liệu minh họa, ghi đề xuất bố cục/trạng thái trong BILL_RECEIPT_DESIGN.md; chưa sửa code theo yêu cầu.

- V1.4.15: sửa đường dẫn kiểm tra/giải nén gói V1.4.13 theo vị trí upload /opt/chdv trong ảnh VPS.

- V1.4.14: chuẩn bị gói cập nhật chọn phòng V1.4.13 gồm 5 file code/test; hướng dẫn VPS bỏ backup theo yêu cầu, không thay runtime/schema hoặc worker ảnh.

- V1.4.13: sửa chọn phòng lập phiếu qua form GET server, giữ lựa chọn khi báo lỗi; dropdown đủ phòng nhưng không đề xuất/lập mới phòng đã có phiếu hiệu lực trong kỳ. 67 tests và Edge bật/tắt JS đạt; chưa cập nhật VPS.

- V1.4.12: làm rõ VPS chạy web/worker bằng systemd, không cần hai terminal như dev.

- V1.4.11: hướng dẫn chạy Flask và worker ảnh ở hai terminal dev riêng, giải thích worker chờ không in log là bình thường.

- V1.4.10: xác nhận worker dev PID 4220 đã dừng sau thao tác PowerShell của người dùng.

- V1.4.9: kiểm tra worker dev PID 4220 còn chạy, giải thích SQLite còn truy cập sau khi tắt web và hướng dẫn dừng đúng tiến trình.

- V1.4.8: xác nhận web/worker VPS khởi động và HTTPS 200 từ log; chờ kết quả test và kiểm tra luồng ảnh thực tế.

- V1.4.7: xác nhận migration V1.4.2 VPS đạt head và không drift; hướng dẫn kiểm thử rồi khởi động web/worker, chờ kết quả.

- V1.4.6: ghi nhận dừng dịch vụ/backup VPS V1.4.2 từ log; hướng dẫn kiểm tra archive rồi cập nhật code và schema, chưa xác nhận thực thi.

- V1.4.5: xác nhận ZIP V1.4.2 VPS hợp lệ, hướng dẫn dừng web/worker và backup DB/ảnh/cấu hình trước migration một ảnh công tơ.

- V1.4.4: xác định gói ZIP được upload vào /root qua ảnh, sửa lệnh kiểm tra đường dẫn trước cập nhật VPS.

- V1.4.3: chuẩn bị và kiểm tra gói chdv-v1.4.2.zip cho cập nhật VPS, loại trừ .env/runtime; hướng dẫn upload theo từng đợt, chưa triển khai production.

- V1.4.2: mỗi ID chốt điện một ảnh, lưu ảnh mới thay cũ sau nén thành công và giữ fallback khi lỗi. Khóa ảnh theo phiếu tiền hiệu lực cho mọi vai trò, chặn chốt phiếu lúc pending; thêm unique/migration gộp ảnh cũ trùng. Backup/migrate dev và restart worker, 64 tests/Edge QA đạt; chưa cập nhật VPS.

- V1.4.1: xử lý ảnh dev đang pending bằng worker, xác nhận WebP/gốc tạm; khởi động worker nền dev cho các upload tiếp theo, không thay code hoặc VPS.

- V1.4.0: bỏ bắt buộc ảnh điện; thêm drop/preview chờ lưu, progress upload, polling thumbnail/modal ngay trong bảng và upload bổ sung không đổi số. Chống retry trùng ảnh, giữ hàng chưa lưu. 61 tests và Edge QA dữ liệu tạm đạt; không migration, chưa cập nhật VPS.

- V1.3.13: phân tích luồng ảnh điện tùy chọn, kéo thả chờ lưu, tiến độ upload và thumbnail/modal tự cập nhật; thêm đề xuất, chưa triển khai code theo yêu cầu.

- V1.3.12: hướng dẫn dọn ZIP triển khai đã dùng, giữ bản backup trước nâng cấp và dữ liệu runtime.

- V1.3.11: xác nhận web/worker VPS chạy và HTTPS 200 từ log; hướng dẫn xác minh upload/nén ảnh thực tế trước chốt kiểm tra tính năng.

- V1.3.10: xác nhận 58 test VPS đạt từ log, giải thích cảnh báo datetime và hướng dẫn mở lại web/worker để kiểm tra HTTPS.

- V1.3.9: xác nhận Nginx syntax đạt; hướng dẫn kiểm thử VPS, khởi động web/worker và kiểm tra HTTPS, chờ kết quả.

- V1.3.8: xác nhận cập nhật dependencies/schema VPS đạt từ log; hướng dẫn cài worker ảnh và sửa giới hạn upload Nginx, chưa mở web.

- V1.3.7: ghi nhận backup VPS trước cập nhật hoàn tất từ log; hướng dẫn triển khai code/thư viện/migration, chưa xác nhận thực thi.

- V1.3.6: ghi nhận gói ZIP VPS kiểm tra đạt; hướng dẫn dừng web và backup database, project cùng cấu hình trước khi triển khai.

- V1.3.5: xác định ZIP upload vào /opt/chdv qua ảnh, sửa hướng dẫn kiểm tra đường dẫn; chưa giải nén hoặc cập nhật VPS.

## 2026-11-03

- V1.3.4: chuẩn bị/kiểm tra gói ZIP cập nhật code ảnh cho VPS, loại trừ cấu hình bí mật và runtime; hướng dẫn chuyển bằng MobaXterm, chưa triển khai production.

- V1.3.3: chuyển form bổ sung ảnh công tơ sang màn điện, hiển thị ngay khi mở Sửa điện; upload giữ nguyên chỉ số và quay lại đúng kỳ, bỏ form ảnh điện khỏi chi tiết phòng.

- V1.3.2: backup và migrate DB VPS cũ vừa nhập vào dev để thêm bảng photo; giữ nguyên nội dung bảng cũ, kiểm tra schema/integrity và màn điện HTTP 200.

- V1.3.1: khôi phục .env dev bị mất từ mẫu với khóa ngẫu nhiên mới, giữ dữ liệu/tài khoản; kiểm tra load app và /login HTTP 200.

- V1.3.0: thêm upload hợp đồng tùy chọn, ảnh chốt/sửa điện bắt buộc, xem ảnh qua đăng nhập và bổ sung ảnh lịch sử. Thêm Photo/migration f13a98c52b70, worker SQLite/CLI nén WebP và xóa gốc tạm, xử lý lỗi/khôi phục sau crash, service Ubuntu và hướng dẫn backup DB+ảnh. Pillow 13.0.0; 57 tests pass. Đã backup/upgrade dev, chưa triển khai VPS hoặc browser QA.

- V1.2.28: dọn 23 mục file/thư mục kiểm tra UI trong instance dev; giữ .gitkeep và database, kiểm tra SHA256 DB không đổi. Không thay ứng dụng hoặc VPS.

- V1.2.27: làm rõ nội dung instance dev theo ảnh IDE; chưa xóa file hoặc đổi cấu hình.

- V1.2.26: giải thích vai trò thư mục instance, bộ file SQLite và các file kiểm tra giao diện local; không thay dữ liệu runtime.

- V1.2.25: giải thích backup SQLite đang chạy có WAL/SHM; hướng dẫn dùng CLI tạo bản nhất quán thay cho copy trực tiếp file runtime.

- V1.2.24: hướng dẫn lưu database nhất quán, .env, code và cấu hình systemd/Nginx từ VPS; phân biệt chứng chỉ có thể cấp lại và runtime không cần lưu.

- V1.2.23: giải thích access.log chứa request dò đường dẫn và hướng dẫn xem gọn các trường chính bằng awk; không thay cấu hình logging.

- V1.2.22: xác nhận trạng thái dịch vụ từ log, giải thích journalctl chờ dữ liệu mới và hướng dẫn theo dõi lượt truy cập qua log Nginx.

- V1.2.21: hướng dẫn theo dõi trạng thái dịch vụ, log ứng dụng trực tiếp và phản hồi HTTPS qua MobaXterm.

- V1.2.20: xác nhận HTTPS đã cấp/cài thành công từ log Certbot; hướng dẫn kiểm tra đăng nhập root, đổi mật khẩu và gia hạn thử, chưa đánh dấu vận hành hoàn tất.

- V1.2.19: xác nhận Nginx proxy trả 200 qua ảnh, hướng dẫn cấp HTTPS và chuyển HTTP sang HTTPS bằng Certbot; chờ kết quả.

- V1.2.18: ghi nhận Nginx syntax pass nhưng proxy trả 404; hướng dẫn thu thập cấu hình đang nạp và kiểm tra lại trước HTTPS.

- V1.2.17: ghi nhận systemd/Gunicorn chạy và /login HTTP 200 từ log; hướng dẫn Nginx reverse proxy cho domain, chờ kiểm tra trước HTTPS.

- V1.2.16: làm rõ thao tác mở nano từ terminal trước khi dán nội dung chdv.service; chờ người dùng mở trình soạn thảo.

- V1.2.15: xác nhận DNS đúng IP từ nslookup người dùng; hướng dẫn tạo/khởi động systemd Gunicorn và kiểm tra nội bộ.

- V1.2.14: chốt IP VPS 103.167.88.214 theo người dùng; hướng dẫn cập nhật riêng DNS chdv và kiểm tra phân giải.

- V1.2.13: phát hiện IP bản ghi chdv khác IP phiên SSH Ubuntu; hướng dẫn xác minh IP VPS trước bước cấu hình dịch vụ và HTTPS.

- V1.2.12: xác nhận tạo root từ log; hướng dẫn cấu hình DNS subdomain chdv.alominh.homes trên Porkbun, chờ kết quả trước cấu hình web/HTTPS.

- V1.2.11: ghi nhận migration VPS đạt head từ log; giải thích APP_ENV hiện chưa có tác dụng trong code và không bắt buộc cấu hình.

- V1.2.10: ghi nhận 48 test pass trên VPS từ log người dùng, chọn DB mới; hướng dẫn tạo .env bí mật riêng và khởi tạo schema qua migration, chờ kết quả.

- V1.2.9: ghi nhận pip cài thành công dependencies và Gunicorn 26.2.0 từ ảnh; hướng dẫn kiểm thử Ubuntu và xác định phương án dữ liệu trước khi cấu hình.

- V1.2.8: giải thích cảnh báo trong bước tạo user/copy code, hướng dẫn kiểm tra thư mục và tiếp tục venv/pip; chưa xác nhận cài thư viện.

- V1.2.7: ghi nhận apt hoàn tất từ ảnh, hướng dẫn tạo tài khoản/thư mục chạy ứng dụng và cài thư viện trong venv, chờ kết quả VPS.

- V1.2.6: xác nhận danh sách upload từ ảnh; hướng dẫn đợt cài gói hệ thống Ubuntu, chờ kết quả trước khi cấu hình thư mục ứng dụng.

- V1.2.5: ghi nhận kết quả kiểm tra VPS từ ảnh; hướng dẫn upload danh sách code cần thiết qua SFTP, chưa chuyển dữ liệu hoặc cài đặt.

- V1.2.4: chuyển sang hướng dẫn triển khai từng đợt ngắn; bắt đầu kiểm tra VPS và tạo thư mục upload, chờ kết quả người dùng trước đợt tiếp theo.

- V1.2.3: phân tích triển khai Ubuntu 24.04 qua MobaXterm; thêm hướng dẫn copy code/backup SQLite, thư mục, Gunicorn/systemd, Nginx/HTTPS và vận hành. Chưa thực thi trên VPS; không đổi app hoặc schema.

- V1.2.2: tái sử dụng reading_cost cho giá/tiền điện; query phòng/phiếu hiệu lực vào service, bỏ phụ thuộc giữa route; thêm test nguồn giá và quy ước tái sử dụng.

- V1.2.1: form phòng rộng theo khung, grid hợp đồng/phí responsive Bootstrap, bỏ sticky thanh lưu gây phủ nội dung.

- V1.2.0: Bootstrap 5.3.8 CSS/bundle CDN có SRI/CSP; nút/form/bảng/alert và tiện ích dùng Bootstrap, bỏ CSS trùng. Sidebar khôi phục trạng thái trước paint và bỏ animation lặp.

- V1.1.24: thêm chuyển động nhẹ khi hiện trang/sidebar/popover/thông báo, phản hồi hover/nhấn; tắt animation khi người dùng chọn giảm chuyển động.

- V1.1.23: lịch sử điện phòng thêm đơn giá/tiền điện tự tính từ giá đã lưu hoặc phiếu hiệu lực; Tài khoản đặt cuối sidebar trên hồ sơ.

- V1.1.22: cho agent tự tăng phiên bản theo mức thay đổi; bổ sung quy ước code ngắn gọn, chuẩn, format nhất quán và giữ phạm vi thay đổi.

- V1.1.21: bỏ dòng số lượng xe trong bảng phòng, giữ từng biển số một dòng; không xe hiển thị dấu —.

- V1.1.20: tách tiền nước/dịch vụ trong chi tiết; bảng phòng thêm số xe/biển số từng dòng, tiền nước tổng theo người, tiền dịch vụ riêng; căn chỉnh số tiền/nhãn xe/dòng bảng. Giữ nguyên phiếu đã chốt.

- V1.1.19: nút ẩn/hiện sidebar và nhớ lựa chọn trên trình duyệt; header tên trang/tài khoản, footer gọn đồng bộ. Không đổi nghiệp vụ.

- V1.1.18: thay bộ chọn month theo ngôn ngữ trình duyệt bằng danh sách Tháng/Năm tiếng Việt dùng chung cho Phòng, Điện và Chốt tiền; giữ YYYY-MM.

- V1.1.17: gom trạng thái/Thông tin thu/Lịch sử thu cùng hàng; bỏ nhãn Đã chốt tiền lặp, giữ Quá hạn; gộp phòng/khách và giảm padding bảng tiền. Chỉ sửa template/CSS.

- V1.1.16: giải thích chọn tháng rồi bấm Xem kỳ, đầu kỳ tự nối cuối kỳ trước và giới hạn chặn lưu tháng tương lai; không đổi chức năng.

- V1.1.15: sửa dropdown thu tiền/history kéo cao dòng và xô cột. Native popover top layer + fixed/JS tự neo, tránh clipping/vượt viewport; Escape/click ngoài/nút đóng. Giữ chức năng thu/hoàn tác/hủy.
- 5 test receipt pass, Node syntax pass; Edge fixture xác nhận dòng128px trước/sau mở, đã xem ảnh. Không thay database.

- V1.1.14: triển khai phân tích V1.1.13 — dropdown ghi nhận thu đủ, ngày/người/số tiền và lịch sử; root hoàn tác có lý do. Chặn hủy phiếu đã thu và gửi lại form cũ sau hoàn tác.
- Phiếu chưa thu ở trên/đã thu ở dưới/hủy cuối; bảng Phòng gọn mặc định, tiền kỳ từ snapshot, bộ lọc thu và chế độ đầy đủ giữ cột cũ.
- Migration 41eb1b88b816 đã backup/upgrade; 46 test pass. Chưa thu một phần/browser E2E cho UI mới.

- V1.1.12: bỏ giới hạn1000px riêng form chốt tiền; dùng chiều ngang còn lại, desktop chia input/preview hai cột, mobile xếp dọc. Không đổi chức năng.

- V1.1.11: thêm ngày giờ chốt, cập nhật lần cuối nếu có revision, đơn giá và tiền điện trong bảng. Nhập chỉ số tự hiện tiền/draft total, xử lý 0 và thiếu giá.
- Snapshot giá khi lưu điện mới; kỳ đã chốt tiền ưu tiên giá phiếu, legacy chưa có giá được ghi rõ tạm tính. Migration d94f512a37b1 đã backup/upgrade; 41 test và Node smoke test pass.

- V1.1.10: thêm giá điện trong thông tin phòng/đợt thuê và bảng/chi tiết/lịch sử. Phiếu mới lấy giá điện/nước/phòng hiện tại, không hồi tố phiếu đã chốt, chặn version cũ.
- Migration c83e4d16b2a0 giữ NULL legacy, đã backup/upgrade local. 39 test pass.

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
