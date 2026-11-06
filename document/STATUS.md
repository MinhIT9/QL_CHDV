# Tiến độ thực tế

V1.11.0 (2026-11-06): Theo xác nhận người dùng, cho phép lưu ảnh cho phòng chưa chốt số điện. Photo có thêm room_id/period làm chủ tạm, unique một ảnh/phòng/kỳ và CHECK chỉ đúng một chủ; migration 08a365e42c97 không đổi dữ liệu ảnh cũ. API kind=meter kiểm tra active/kỳ hợp lệ không tương lai, retry token đúng chủ và khóa phiếu; stage/worker dùng hàng đợi/nén/fallback sẵn có. Bảng điện hiện ảnh chưa có reading, có nút Lưu ảnh độc lập; khi chốt số điện, chuyển cùng Photo sang reading trong giao dịch, giữ ID/token/job, không tạo số điện giả hay upload lại. Hàng khác chưa gửi vẫn giữ ảnh/input; phòng có ảnh được archive thay vì xóa. 93 unittest toàn bộ OK (60.973s) trước khi bổ sung một test phân kỳ; sau bổ sung, 22 test_photos OK (12.698s), gồm phân kỳ, pending/rollback, thay thế/fallback, khóa root/admin qua endpoint mới, unique, giữ ảnh khi ngừng phòng và downgrade guard. Edge QA tổng thể ảnh OK; QA tập trung xác minh upload không nhập số, reload/polling ảnh nén, chốt nhận cùng ảnh, popup sửa điện/confirm không pageerror. Kiểm tra migration upgrade/check/downgrade/upgrade trên DB tạm đạt; DBcheckdev đạt, Node syntax/docs/diff check đạt. DB dev đã backup instance/backups/chdv-before-v1.11.0-fb185de7.sqlite3 và upgrade từ f79254d31b86 lên 08a365e42c97. Cần khởi động lại web/worker dev rồi Ctrl+F5. Chưa triển khai VPS; bản VPS tiếp theo phải dừng cả web/worker, backup DB+uploads và db upgrade trước chạy code mới. Không thêm dependency.

V1.10.22 (2026-11-06): Trang Sửa điện dùng hai ô đầu/cuối trên một hàng Bootstrap col-6. Xem trước POST qua fetch, máy chủ kiểm tra nghiệp vụ rồi trả dialog trước/sau các kỳ bị ảnh hưởng và lý do; không ghi DB tới khi xác nhận. Confirm giữ snapshot input riêng và stamp, vẫn dùng kiểm tra máy chủ/khóa phiếu/lịch sử hiện có. Nhập lại/Esc đóng dialog giữ form; có fallback POST/dialog mở khi không JS. Ảnh trên trang Sửa điện lưu độc lập, không validate số điện/lý do, sửa thông báo chọn ảnh cho đúng nút Lưu ảnh. Đã xác minh Edge390px: đầu/cuối cùng hàng, để trống số điện vẫn upload ảnh và DB chỉ số giữ nguyên, preview không reload/không ghi, cancel giữ form, confirm cập nhật và ghi1 revision, không pageerror; ảnh exports/correction-mobile-preview.png. 15 test_billing OK (8.516s), 16 test_photos OK; Node syntax/docs/diff check đạt. Cập nhật kỳ vọng test ngày theo nhãn/xuống dòng của V1.10.14. Chưa triển khai VPS, không đổi DB. Đã hỏi phạm vi ảnh trước số điện: thực hiện cho trang Sửa điện đang có reading; ảnh cho phòng chưa từng chốt vẫn chờ người dùng xác định, chưa thêm mô hình lưu ảnh room-period.

V1.10.20 (2026-11-06): Người dùng gửi log VPS V1.10.19: 17 tests OK (14.859s), hai dịch vụ active, HTTPS502 lúc khởi động rồi retry200. Yêu cầu mới sao lưu DB và ảnh. Hướng dẫn dừng cả chdv/chdv-photos với trap mở lại, tạo thư mục snapshot riêng dưới /opt/chdv/backups cho user chdv, backup-db vào file mới, copy toàn bộ instance/uploads gồm ảnh tạm/hàng chờ, nén database.sqlite3 + uploads và kiểm tra tar. Không copy trực tiếp DB đang chạy/WAL, không xóa nguồn. Chỉ hướng dẫn, chưa thực thi hay xác nhận có backup mới; archive không bao gồm .env hoặc code.

V1.10.19 (2026-11-06): Xuất exports/chdv-v1.10.19.zip gồm route điện, CSS, JS ảnh, base và test_v1 để cập nhật từ VPS đã lên V1.10.16. Nội dung ưu tiên phòng chưa chốt và đường phân cách V1.10.18. CRC/danh sách 5 file đạt; không .env/DB/uploads/dependencies/migration. Hướng dẫn upload đúng /opt/chdv, stop web/extract/quyền/test_v1/start/HTTPS retry, không backup theo yêu cầu các lượt trước; worker giữ chạy. Chưa thao tác VPS hoặc xác nhận triển khai.

V1.10.18 (2026-11-06): Đưa phòng chưa chốt điện lên đầu, giữ thứ tự mã phòng trong mỗi nhóm bằng stable sort. Sau lưu AJAX di chuyển node hàng theo thứ tự máy chủ, giữ dữ liệu/ảnh đang chọn của hàng chưa lưu và đánh lại số thứ tự desktop. Tăng đường ngăn phòng lên 2px #c4cfdd trên mobile/desktop; tăng phiên bản CSS/JS tránh cache. 17 test_v1 OK (11.208s), thêm xác minh thứ tự HTML thường/AJAX; Edge kiểm tra reorder giữ nguyên node và giá trị input đạt, Node syntax đạt. QA ảnh dùng locator theo room id để không phụ thuộc vị trí sau sắp xếp, chưa chạy lại toàn bộ QA ảnh trong lượt này. Không đổi DB, chưa triển khai VPS.

V1.10.17 (2026-11-06): Người dùng xác nhận cập nhật VPS patch V1.10.16: 16 test_photos OK trong 13.411s, chdv/chdv-photos active. HTTPS /login ban đầu 502, curl retry sau 2 giây nhận 200 OK, cookie Secure. Có khả năng web đang khởi động ở lần gọi đầu, chưa có log Gunicorn để xác minh nguyên nhân; không kết luận lỗi kéo dài. Bước tiếp Ctrl+F5 kiểm tra bảng phòng/điện mobile và popup khóa ảnh; chưa có xác nhận trực quan từ VPS. Không thay code hoặc thao tác VPS trong lượt này.

V1.10.16 (2026-11-06): Xuất exports/chdv-v1.10.16.zip, 8 file gồm CSS/base, danh sách phòng, 4 template điện và test_photos. Patch cho VPS đã lên V1.10.7, gồm bảng phòng mobile V1.10.11, bảng điện V1.10.14 và popup khóa ảnh V1.10.15. Đã kiểm tra CRC/danh sách file, không chứa .env/DB/uploads/dependencies/migrations. Hướng dẫn upload đúng /opt/chdv, kiểm tra ZIP trước stop web, giải nén/cấp quyền/test_photos/restart/HTTPS; trap mở lại web khi có lỗi, không dừng worker. Tiếp tục yêu cầu không backup của các lượt cập nhật gần nhất. Chưa thao tác hoặc xác minh triển khai VPS.

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


Cập nhật: 2026-11-04 (Asia/Saigon). Phiên bản hội thoại: V1.9.2.

V1.4.17: vẽ mockup phiếu gửi khách bằng imagegen built-in theo yêu cầu chỉ thiết kế, chưa code. Phiếu dọc trắng/mint/navy, tổng tiền nổi bật, bảng kê, dữ liệu minh họa; phân biệt chưa thanh toán với đã thu. Đã hiển thị ảnh và ghi BILL_RECEIPT_DESIGN.md, kiểm tra trực quan/số tiền, inventory/diff đạt. Chưa có route click ID/xuất phiếu trong app; không chạy test nghiệp vụ hoặc thao tác VPS.

V1.4.15: ảnh upload cho thấy ZIP ở /opt/chdv thay vì /root, hướng dẫn lại đúng đường dẫn test/giải nén. Không backup theo yêu cầu hiện có; chưa có kết quả triển khai. Chỉ sửa tài liệu, inventory/diff đạt.

V1.4.14: đóng gói exports/chdv-v1.4.13.zip chỉ 4 file app và test billing cho sửa chọn phòng; CRC/allowlist đạt, không .env/DB/migration. Theo yêu cầu bỏ backup lần cập nhật này, hướng dẫn upload /root/ rồi thay code và test/start web. Không đụng worker/schema, chưa có bằng chứng upload/triển khai. Inventory/diff đạt, không chạy lại suite đã đạt lượt trước.

V1.4.13: sửa lập phiếu tự quay phòng đầu bằng form GET room_id/period, bỏ JS đổi href. Giữ đủ mã phòng trong dropdown, option đã có phiếu hiệu lực cùng kỳ bị khóa/không đề xuất; hết phòng khóa nút; lỗi dữ liệu giữ lựa chọn. 67 tests và Edge bật/tắt JS đạt, Node/inventory/diff đạt. Không migration, không đổi DB dev hoặc VPS.

V1.4.12: giải thích web/worker VPS do systemd quản lý, không cần giữ hai terminal SSH; cung cấp lệnh kiểm tra hai service. Không có kiểm tra VPS mới, dựa cấu hình/log đã xác nhận trong hội thoại. Chỉ sửa tài liệu, inventory/diff đạt.

V1.4.11: làm rõ chạy web và worker dev ở hai terminal riêng theo ảnh người dùng; terminal đang chạy process-photos có thể đứng chờ bình thường. Chưa có bằng chứng mở lại web; không chạy lệnh/process/DB trong lượt này. Chỉ sửa tài liệu, inventory/diff đạt.

V1.4.10: người dùng đã xác nhận dừng worker dev PID 4220, kiểm tra tiến trình không còn. Không kết luận web/công cụ khác đã đóng DB; không xóa WAL/SHM. Chỉ cập nhật tài liệu, inventory/diff đạt; không chạy test nghiệp vụ hoặc thao tác VPS.

V1.4.9: xác nhận worker ảnh dev PID 4220 vẫn chạy, truy cập DB định kỳ 2 giây. Giải thích SQLite/WAL/SHM và hướng dẫn dừng worker cùng web nếu muốn dev ngừng hoàn toàn; chưa dừng tiến trình hoặc xóa file. Chỉ cập nhật tài liệu, inventory/diff đạt; không chạy test nghiệp vụ.

V1.4.8: log VPS xác nhận web/worker enabled và active sau start, HTTPS /login HTTP 200; dịch vụ đã mở lại. Chưa gửi kết quả unittest của bản cập nhật này hoặc kiểm tra ảnh thực tế, không đánh dấu test VPS đạt. Hướng dẫn xác minh thumbnail/thay ảnh/khóa theo phiếu trên dữ liệu phù hợp. Chỉ sửa tài liệu, inventory/diff đạt.

V1.4.7: log VPS xác nhận backup archive đạt, code/requirements cập nhật, migration a24d09e86c31 head và db check đạt. Hướng dẫn test rồi mở lại cả web/worker nếu OK. Chưa nhận kết quả tests/start/kiểm tra ảnh thực tế, chưa đánh dấu triển khai hoàn tất. Chỉ sửa tài liệu, inventory/diff đạt.

V1.4.6: log VPS xác nhận hai dịch vụ dừng và backup-db thành công, bộ backup tại /root/chdv-before-v142-mAvcspH9. Tên archive trong kết quả bị cắt, hướng dẫn kiểm tra tar trước giải nén code/cài thư viện/migrate a24d09e86c31. Chưa nhận kết quả nâng cấp hoặc mở lại dịch vụ. Chỉ sửa tài liệu, inventory/diff đạt.

V1.4.5: người dùng xác nhận ZIP /root/chdv-v1.4.2.zip kiểm tra đạt. Hướng dẫn dừng web/worker và backup DB+project/uploads/.env/cấu hình trước cập nhật. Chưa nhận bằng chứng backup hoặc thay đổi code/schema VPS. Chỉ sửa tài liệu, inventory/diff đạt.

V1.4.4: ảnh cho thấy gói VPS ở /root/chdv-v1.4.2.zip, khác đường dẫn lệnh /opt/chdv nên không tìm thấy. Hướng dẫn kiểm tra đúng chỗ, chưa xác nhận ZIP hợp lệ hoặc thay đổi VPS. Chỉ sửa tài liệu, inventory/diff đạt.

V1.4.3: đóng gói exports/chdv-v1.4.2.zip từ HEAD sạch cho VPS, kiểm tra ZIP chứa code ảnh mới/migration a24d09e86c31 và không chứa cấu hình bí mật/runtime. Hướng dẫn upload vào /opt/chdv qua MobaXterm rồi kiểm tra ZIP. Chưa có bằng chứng upload/cập nhật VPS; đợt sau phải dừng web và worker, backup DB+ảnh trước migration gộp ảnh trùng. Chỉ đóng gói/tài liệu, inventory/diff đạt; không chạy lại suite đã kiểm thử.

V1.4.2: giới hạn một Photo/ID chốt điện bằng unique DB; lưu ảnh mới thay cùng record, giữ fallback trong lúc nén/lỗi, xóa file cũ sau ready. Phiếu tiền hiệu lực khóa thêm/thay cho Root/Admin, ẩn upload; pending chặn chốt phiếu. 64 tests, 16 test ảnh bổ sung và Edge thay/khóa thumbnail đạt; Node/db check/integrity đạt. Đã backup DB+ảnh rồi migrate dev a24d09e86c31, dữ liệu nghiệp vụ khớp backup; ảnh trùng giữ ready mới nhất. Worker dev khởi động lại PID 4220. Chưa cập nhật VPS hoặc test đồng thời trên VPS. Inventory/diff đạt.

V1.4.1: xử lý ảnh dev bị chờ do chưa có worker giữ khóa: job 1 từ pending → ready sau process-photos --once, đã có WebP và xóa gốc tạm. Khởi động worker nền ẩn dev PID 4532, kiểm tra còn chạy/stderr rỗng. Không đổi code/DB schema/VPS, không chạy lại suite; kiểm tra trực tiếp trạng thái/file và inventory/diff. Worker cần chạy lại sau khi bị dừng hoặc reboot máy.

V1.4.0: đã hiện thực ảnh điện tùy chọn khi chốt/sửa; drop/chọn chỉ preview local, lưu mới upload. Bảng có Lưu ảnh cho kỳ đã chốt, tiến độ byte 0–100 tách bước nén, polling theo lô tự cập nhật thumbnail; popup Bootstrap xem ảnh, không reload/mất ảnh chờ hàng khác. Retry bổ sung cùng token không tạo trùng, giữ quyền/CSRF và worker xóa gốc tạm; form thường có fallback khi tắt JS. 61 test Python đạt, 13 test ảnh đạt sau assertion bổ sung, Edge headless với dữ liệu tạm đạt luồng chính/drop/popup/no reload. Node/db check/inventory/diff đạt. Không migration/đổi dữ liệu dev; chưa cập nhật VPS, chưa thử mạng chậm/điện thoại thật. Xem PHOTOS.md.

V1.3.13: chỉ phân tích yêu cầu ảnh điện tùy chọn, thumbnail/modal, kéo thả chờ lưu, tiến độ upload và cập nhật bảng không reload; ghi METER_PHOTO_UX_PROPOSAL.md. App/VPS hiện vẫn có kiểm tra bắt buộc ảnh theo bản cũ, chưa sửa code/schema hoặc chạy test nghiệp vụ. Đối chiếu source/MDN, inventory/diff đạt.

V1.3.12: hướng dẫn xóa riêng ZIP triển khai /opt/chdv/chdv-v1.3.4.zip vì đã giải nén, giữ backup quay lui và runtime. Chưa thao tác xóa trên VPS; chưa có kết quả upload ảnh thực tế. Chỉ cập nhật tài liệu, inventory/diff đạt.

V1.3.11: log VPS xác nhận web/worker ảnh enabled và active; HTTPS /login trả 200, cookie Secure. Dịch vụ đã mở lại sau cập nhật; chưa có bằng chứng upload/nén/xóa gốc trên browser thật. Hướng dẫn bổ sung ảnh công tơ đúng kỳ không đổi số rồi kiểm tra ảnh nén/tmp. Chỉ sửa tài liệu, inventory/diff đạt; không tự thao tác dữ liệu VPS.

V1.3.10: người dùng gửi kết quả VPS 58 tests OK trong 41.727s. Cảnh báo datetime.utcnow tại auth/routes.py:43 không làm test lỗi; chưa sửa trong lượt triển khai. Hướng dẫn mở lại dịch vụ và kiểm tra HTTPS, chưa nhận kết quả status/upload ảnh. Chỉ sửa tài liệu, inventory/diff đạt; không tự chạy lệnh VPS.

V1.3.9: log nginx -t trên VPS đạt sau chỉnh site. Hướng dẫn test suite rồi mới mở lại web/worker và kiểm tra HTTPS. Nhắc cài worker nếu chưa làm vì chưa có log bước đó. Chưa có bằng chứng test hoặc start services/upload ảnh. Chỉ sửa tài liệu, inventory/diff đạt; không tự chạy lệnh VPS.

V1.3.8: log người dùng xác nhận code VPS đã giải nén/cấp quyền, Pillow 13.0.0 cài thành công, migration f13a98c52b70 và db check đạt. Hướng dẫn cài service worker, tạo uploads và Nginx 64m; chưa nhận kết quả, web vẫn dừng. Chưa test suite VPS hoặc upload thực tế. Chỉ sửa tài liệu, inventory/diff đạt; không tự chạy lệnh VPS.

V1.3.7: log VPS xác nhận web đã dừng và backup đầy đủ tại /root/chdv-before-update-OREUjaIO (DB/project/systemd/Nginx). Hướng dẫn giải nén code, quyền truy cập, cài thư viện và migration; chưa có kết quả cập nhật, web chưa mở lại. Chỉ sửa tài liệu, inventory/diff đạt; không tự chạy lệnh VPS.

V1.3.6: người dùng xác nhận ZIP VPS kiểm tra đạt Done testing. Hướng dẫn dừng web và backup DB/code/runtime/cấu hình vào thư mục riêng dưới /root trước khi cập nhật; chưa nhận bằng chứng backup, chưa thay code/schema VPS. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy lệnh VPS.

V1.3.5: ảnh VPS cho thấy ZIP đã upload tại /opt/chdv/chdv-v1.3.4.zip, khác đường dẫn kiểm tra /root/chdv-upload dẫn đến FileNotFoundError. Hướng dẫn kiểm tra lại đúng chỗ; chưa có kết quả tính toàn vẹn hoặc triển khai. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy lệnh VPS.

V1.3.4: đã chuẩn bị exports/chdv-v1.3.4.zip cho cập nhật VPS, kiểm tra ZIP và danh sách không chứa .env/runtime; code từ HEAD sạch. SSH trực tiếp không có host key tin cậy/phiên xác thực chia sẻ, hướng dẫn upload ZIP bằng MobaXterm. Chưa nhận bằng chứng upload hoặc thay đổi VPS; chưa dừng dịch vụ hay migrate production. Kiểm tra inventory/diff; không chạy lại test vì chỉ đóng gói code đã kiểm thử.

V1.3.3: bổ sung/xem ảnh công tơ ngay trên màn Sửa điện; form ảnh riêng không yêu cầu đổi số. Link từ bảng điện và redirect upload về đúng kỳ điện, bỏ form ảnh điện bên phòng (giữ xem lịch sử). Kiểm tra 10 test ảnh và 12 test billing đạt, inventory/diff đạt. Không đổi DB/nén; chưa browser QA/VPS.

V1.3.2: sửa lỗi dev thiếu bảng photo sau khi người dùng nhập DB VPS cũ. Đã backup bản nhập rồi upgrade từ 41eb1b88b816 lên f13a98c52b70. db check/integrity đạt, nội dung mọi bảng cũ khớp backup, GET /electricity/ với phiên đăng nhập trả 200. Không đổi tài khoản/mật khẩu hoặc VPS; không xác nhận tính đầy đủ của bản copy so với VPS/WAL. Kiểm tra inventory/diff; không chạy lại suite vì không đổi code.

V1.3.1: tạo lại .env dev bị xóa bằng mẫu và SECRET_KEY ngẫu nhiên mới; giữ database/tài khoản, COOKIE_SECURE=false để chạy HTTP local. Kiểm tra app load và /login HTTP 200, inventory/diff đạt; không chạy lại suite nghiệp vụ hoặc thao tác VPS. Phiên đăng nhập dev cũ hết hiệu lực do đổi khóa.

V1.3.0: đã hiện thực upload ảnh hợp đồng tùy chọn theo đợt thuê, ảnh điện bắt buộc khi chốt/sửa; dữ liệu cũ giữ nguyên và có thể bổ sung ảnh. Ảnh riêng tư ngoài static, kiểm tra JPEG/PNG/WebP 10 MB/24 MP, request 64 MB. Hàng đợi SQLite + một worker CLI có khóa OS nén WebP 2200 px/quality 82, bỏ metadata, xóa gốc tạm, báo pending/failed và cho tải lại. 57 tests pass với Pillow 13.0.0 trong .venv; Node syntax đạt. Migration f13a98c52b70 đã backup/upgrade local, số dòng nghiệp vụ giữ nguyên/integrity ok/db check không drift. Docs inventory/diff đạt. Có hướng dẫn PHOTOS.md và service worker Ubuntu; chưa cập nhật VPS hoặc chạy worker dev lâu dài, chưa browser QA/đánh giá ảnh chữ thực tế/restore DB+ảnh. Khi deploy cần Nginx 64m và bật worker; backup phải lưu thêm uploads.

V1.2.28: đã dọn 23 mục artifact kiểm tra UI trong instance dev theo yêu cầu. Chỉ còn .gitkeep và chdv.sqlite3; SHA256 database không đổi trước/sau. Không đổi code hoặc thao tác VPS. Inventory/diff đạt, không chạy test nghiệp vụ; các ảnh/HTML kiểm tra cũ không còn, cần tạo lại nếu muốn xem.

V1.2.27: chuyển ngữ cảnh về instance dev theo ảnh IDE; phân biệt database/.gitkeep với artifact kiểm tra giao diện. Chưa dọn file do người dùng chưa yêu cầu cụ thể. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy test nghiệp vụ hoặc thao tác VPS.

V1.2.26: kiểm tra danh sách instance local và giải thích DB/WAL/SHM trên VPS so với HTML/PNG kiểm tra giao diện local. Không xóa hoặc sửa runtime, không xác nhận nội dung VPS ngoài ảnh đã gửi. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy test nghiệp vụ.

V1.2.25: ảnh instance xác nhận DB có WAL/SHM. Làm rõ tải riêng DB hoặc tải tuần tự cả ba khi đang hoạt động không bảo đảm nhất quán; hướng dẫn backup-db rồi tải file kết quả, không dừng web. Chưa nhận bằng chứng backup/restore. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy lệnh VPS hoặc test nghiệp vụ.

V1.2.24: hướng dẫn danh sách cần lưu từ VPS để khôi phục dữ liệu/cấu hình, ưu tiên SQLite Backup API và tải bản backup qua SFTP; không copy riêng DB đang mở. Chưa nhận bằng chứng backup hoặc restore, chưa lập lịch. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy lệnh VPS hoặc test nghiệp vụ.

V1.2.23: ảnh access.log cho thấy nhiều request dò đường dẫn, các dòng hiển thị trả 301/404. Giải thích đây là dấu hiệu quét tự động, chưa có bằng chứng truy cập thành công từ ảnh; hướng dẫn lọc hiển thị gọn qua awk, không thay log gốc hoặc chặn IP. Chỉ sửa tài liệu, kiểm tra inventory/diff; chưa chạy lệnh hiển thị trên VPS.

V1.2.22: log systemctl xác nhận chdv/nginx enabled và active; đoạn journalctl gửi chỉ có startup, chưa thấy lỗi. Giải thích màn theo dõi chờ log mới và hướng dẫn xem access.log Nginx để theo dõi lượt truy cập. Chưa kiểm tra thực tế access.log trên VPS. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy test nghiệp vụ.

V1.2.21: người dùng báo ok và hỏi cách xem terminal/trạng thái web. Hướng dẫn systemctl, journalctl, curl HTTPS và log lỗi Nginx; giải thích systemd chạy nền, không có terminal Flask cần giữ mở. Chưa có log renew dry-run hoặc xác nhận riêng backup/restore/reboot. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy lệnh VPS hoặc test nghiệp vụ.

V1.2.20: log người dùng xác nhận Certbot đã cấp/cài HTTPS chdv.alominh.homes thành công, hạn 2027-02-01 và báo lập lịch gia hạn; UFW thêm rule Nginx Full nhưng chưa rõ active. Chưa có kết quả browser login/đổi mật khẩu, renew dry-run hoặc backup/restore/reboot. Hướng dẫn kiểm tra đăng nhập và gia hạn thử. Chỉ sửa tài liệu, kiểm tra inventory/diff; không tự chạy lệnh VPS hoặc test nghiệp vụ.

V1.2.19: ảnh người dùng xác nhận curl /login qua Nginx với Host chdv.alominh.homes trả HTTP 200. Hướng dẫn cho phép Nginx Full và cấp HTTPS qua Certbot; chưa có kết quả chứng chỉ hoặc kiểm tra HTTPS. Chỉ cập nhật tài liệu, kiểm tra inventory/diff; chưa chạy lệnh VPS hoặc test nghiệp vụ.

V1.2.18: log xác nhận nginx -t thành công nhưng curl qua Nginx /login với Host domain trả 404, chưa đạt proxy. Hướng dẫn đọc site/nginx -T và thử lại; chưa xác định nguyên nhân, chưa cấp HTTPS. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy lệnh VPS hoặc test nghiệp vụ.

V1.2.17: log VPS xác nhận systemd chdv enabled/active và Gunicorn /login trả HTTP 200 trên 127.0.0.1:8000, cookie Secure. Hướng dẫn cấu hình Nginx cho chdv.alominh.homes và kiểm tra proxy; chưa nhận kết quả Nginx, chưa cấp HTTPS. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy lệnh VPS hoặc test nghiệp vụ.

V1.2.16: ảnh vẫn ở shell /opt/chdv sau tạo root. Làm rõ cách mở nano trước khi dán cấu hình INI, chưa có bằng chứng tạo hoặc chạy service. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy test nghiệp vụ.

V1.2.15: người dùng gửi nslookup qua 1.1.1.1 xác nhận chdv.alominh.homes phân giải 103.167.88.214. Hướng dẫn systemd/Gunicorn loopback và curl nội bộ; chưa nhận kết quả. Chưa cấu hình Nginx/HTTPS cho app. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy lệnh VPS hoặc test nghiệp vụ.

V1.2.14: người dùng xác nhận IP VPS 103.167.88.214. Hướng dẫn sửa riêng A record chdv và kiểm tra DNS; chưa có kết quả thay đổi/phân giải. Chưa cấu hình service/HTTPS. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy lệnh VPS hoặc test nghiệp vụ.

V1.2.13: ảnh DNS hiển thị A chdv.alominh.homes về 103.75.183.230, khác IP SSH/eth0 Ubuntu ở ảnh trước (103.167.88.214). Đang yêu cầu xác minh IP Ubuntu và IP public trong bảng quản lý VPS trước khi sửa DNS hoặc cấu hình HTTPS. Chưa kết luận topology/NAT. Chỉ cập nhật tài liệu, kiểm tra inventory/diff; không chạy lệnh VPS.

V1.2.12: log người dùng xác nhận root được tạo trên VPS. Đã chọn domain chdv.alominh.homes và hướng dẫn A record trên Porkbun về IP VPS 103.167.88.214 theo ảnh SSH/eth0 trước. Chưa xác nhận DNS, service hoặc HTTPS; chưa xác nhận xóa mật khẩu khởi tạo. Đối chiếu hướng dẫn Porkbun chính thức, kiểm tra inventory/diff; không chạy test nghiệp vụ.

V1.2.11: log VPS xác nhận database mới đã upgrade đến 41eb1b88b816 (head). Đối chiếu code xác nhận APP_ENV chưa được sử dụng, không bắt buộc trong .env VPS. Chưa xác nhận tạo root/service/HTTPS. Chỉ cập nhật tài liệu, kiểm tra inventory/diff; không chạy lại test nghiệp vụ.

V1.2.10: log người dùng gửi xác nhận 48 tests OK trong 35.304s trên VPS. Đã chọn bắt đầu dữ liệu mới; hướng dẫn tạo .env riêng và chạy migration, chưa nhận kết quả. Chưa tạo root/service/HTTPS. Kiểm tra tài liệu inventory/diff; không tự chạy lệnh VPS hoặc chạy lại suite local.

V1.2.9: ảnh pip xác nhận cài requirements và Gunicorn 26.2.0 thành công trong venv trên VPS. Đã hướng dẫn unittest, chưa nhận kết quả; chờ chọn giữ DB local hay tạo mới. Chưa cấu hình .env/DB/service hoặc mở web. Chỉ sửa tài liệu, kiểm tra inventory/diff; chưa chạy test VPS thay người dùng.

V1.2.8: ảnh xác nhận tạo user chdv; giải thích cảnh báo home chưa tồn tại tại thời điểm adduser và cp -n. Chưa có bằng chứng venv/pip; hướng dẫn kiểm tra file và tiếp tục cài môi trường. Chỉ sửa tài liệu; kiểm tra inventory/diff, không chạy test nghiệp vụ hoặc lệnh VPS.

V1.2.7: ảnh apt hoàn tất về dấu nhắc root, không thấy lỗi trong phần hiển thị. Hướng dẫn chuẩn bị /opt/chdv, user dịch vụ, venv và cài thư viện; chưa nhận kết quả, chưa cấu hình .env/DB/service app. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy test nghiệp vụ.

V1.2.6: ảnh ls xác nhận danh sách code đã upload đúng cấp thư mục /root/chdv-upload, chưa kiểm tra toàn vẹn nội dung. Đang hướng dẫn cài gói hệ thống qua apt, chưa nhận kết quả cài đặt; chưa chuyển DB hoặc chạy web. Chỉ sửa tài liệu, kiểm tra inventory/diff; không chạy test nghiệp vụ.

V1.2.5: ảnh VPS xác nhận Ubuntu 24.04, chưa có listener cổng 80/443/8000 và đã tạo /root/chdv-upload. Đợt tiếp hướng dẫn upload code, chưa chuyển DB/.env hoặc cài dịch vụ. Chỉ cập nhật tài liệu; kiểm tra inventory/diff, không chạy test nghiệp vụ.

V1.2.4: ảnh người dùng xác nhận đã mở SSH root trên Ubuntu 24.04. Hướng dẫn ngắn đợt đầu: kiểm tra OS/cổng web và tạo thư mục upload; chưa nhận kết quả lệnh, chưa xác nhận cài đặt hoặc triển khai VPS. Chỉ cập nhật tài liệu, kiểm tra inventory/diff; không chạy lại test nghiệp vụ.

V1.2.3: đã phân tích và viết DEPLOY_UBUNTU.md cho Ubuntu 24.04/MobaXterm: danh sách copy, thư mục, cấu hình và chuyển DB bằng backup. Chỉ thay tài liệu; inventory/diff đạt. Chưa triển khai VPS, kiểm thử Python 3.12/HTTPS/restore hoặc chạy lại test nghiệp vụ.

V1.2.2: 47 test suite pass; 12 test_billing pass sau khi th?m test helper. gom reading_cost cho chọn nguồn giá/tính tiền điện ở lịch sử phòng và màn điện. room_query/active_bill_query vào services/queries.py, bỏ import giữa các route. Template lịch sử chỉ trình bày. Thêm test giá snapshot/phiếu 0/thiếu giá/fallback/chưa nhập, ghi quy ước tái sử dụng. Không đổi DB/nghiệp vụ; chưa rà hết template lặp hoặc browser QA.

V1.2.1: 14 test_contracts pass. form thêm/sửa phòng dùng Bootstrap mw-100/w-100 bỏ giới hạn 1000px, nhóm hợp đồng/phí dùng grid 1/2/3 cột theo màn hình, thanh lưu position-static để không phủ nội dung khi cuộn. Ô khách bị khóa khi trạng thái Trống là hành vi hiện có, giữ nguyên. Chưa browser QA; không đổi DB/nghiệp vụ.

V1.2.0: Bootstrap 5.3.8 CSS/bundle CDN có SRI; CSP cho phép jsDelivr. Chuyển nút/form/bảng/alert và tiện ích bố cục sang Bootstrap, bỏ CSS trùng. Sidebar bỏ animation lặp, khôi phục trạng thái lên html trước paint để tránh flash khi tải/chuyển HTMX. 47 test pass, Node syntax và 4 kiểm tra trạng thái trước paint pass. Chưa browser QA/CDN runtime; cần mạng cho Bootstrap. Không đổi DB/nghiệp vụ.

V1.1.24: thêm animation CSS ngắn 140–240ms cho trang/card, sidebar lúc hiện, thông báo/popover và phản hồi hover/nhấn. Không transform nội dung chứa sticky table/form; tôn trọng prefers-reduced-motion. Chỉ CSS/cache asset, không đổi nghiệp vụ/JS/DB. Kiểm tra tài liệu/diff; chưa browser QA hoặc chạy lại test nghiệp vụ.

V1.1.23: lịch sử điện chi tiết phòng thêm đơn giá và tiền điện tự tính; ưu tiên phiếu hiệu lực, sau đó giá snapshot của lần chốt điện. Dữ liệu cũ thiếu giá hiển thị chưa có giá đã lưu, không tự áp giá hiện tại vào lịch sử. Tài khoản chuyển cuối menu sidebar, trên hồ sơ. 11 test billing pass, có test giá snapshot/phiếu/0/thiếu giá; chưa browser QA. Không đổi schema.

V1.1.22: cập nhật AGENTS.md theo yêu cầu: tự tăng patch/minor/major theo mức thay đổi; code gọn, đúng chuẩn, format dễ đọc trong phạm vi sửa. Chỉ sửa tài liệu, không format lại app trong lượt này; không cần chạy test nghiệp vụ. Kiểm tra bằng script tài liệu và diff whitespace.

V1.1.21: bỏ dòng đếm xe trong hai bảng phòng, chỉ giữ biển số từng dòng; không có xe hiển thị dấu —. Xóa CSS vehicle-count không dùng. Kiểm tra render partial với 2 xe/không xe/không khách; không đổi nghiệp vụ/DB, chưa browser QA.

V1.1.20: tách dự tính tiền nước/dịch vụ ở chi tiết; bảng phòng gọn và đầy đủ có số xe/biển số từng dòng, tổng tiền nước theo người và tiền dịch vụ riêng. Giá hiện tại không thay phiếu snapshot. Căn phải tiền, căn giữa số người, biển số dạng nhãn, dòng xen kẽ/hover; giữ cuộn ngang và cột sticky. 5 test receipts và 3 render smoke pass (2 xe, nước 200.000, dịch vụ 150.000); chưa browser QA. Không đổi DB/nghiệp vụ.

V1.1.19: nút ẩn/hiện sidebar trên header, nhớ bằng localStorage có xử lý khi storage bị chặn; nội dung mở rộng khi ẩn. Chỉnh header tên trang/tài khoản và footer. Node syntax và 10 test billing pass; chưa browser QA lượt này. Không đổi nghiệp vụ/DB.

V1.1.18 Việt hóa chọn kỳ tháng tại ba màn hình bằng select Tháng/Năm, giữ dữ liệu YYYY-MM và nút Xem. Chỉ thay template/CSS, không DB/route.

V1.1.17 chỉ làm gọn dòng bảng tiền, trạng thái và nút nằm ngang, giữ cảnh báo quá hạn/popover. Không đổi nghiệp vụ/DB; kiểm tra render/luồng billing và receipts, chưa browser QA cho chỉnh sửa này.

V1.1.16 chỉ hướng dẫn sử dụng chuyển kỳ điện, không sửa app/DB, không chạy lại test. Chọn tháng cần bấm Xem kỳ; đầu kỳ lấy cuối tháng trước, chỉ lưu kỳ không ở tương lai.

V1.1.15 sửa UI menu thu tiền/history thành popover nổi không giãn dòng bảng. 5 test receipt pass và kiểm tra Edge row height128px trước/sau; không đổi nghiệp vụ/DB. Bộ46 test phía dưới là kết quả lượt triển khai trước.

V1.1.14 thêm ghi nhận thu đủ/hoàn tác có lịch sử, sort phiếu và bảng Phòng gọn/lọc theo thu từng kỳ. Chưa thu một phần, kết nối ngân hàng hoặc hoàn tiền tự động.

Đã có sửa điện, chốt tiền và xác nhận nhận đủ từng phiếu; phòng/điện cùng tháng, chưa chia ngày hoặc thu một phần.

Đã có đơn giá/hợp đồng/lịch nhắc; thu tiền là xác nhận thủ công bởi Admin, không tự kiểm chứng tiền vào ngân hàng.

**Đã triển khai V1 chạy local bằng Flask + SQLite. Chưa triển khai production.**

| Hạng mục | Trạng thái | Bằng chứng / giới hạn |
| --- | --- | --- |
| Flask factory, cấu hình .env | Đã có | app/__init__.py, wsgi.py; SECRET_KEY bắt buộc |
| Database, migrations | Đã có | Migration 41eb1b88b816 đã áp dụng local sau backup; WAL/FK/busy timeout |
| Root ban đầu | Đã tạo local | init-admin; mật khẩu ngoài Git, phải đổi lần đầu |
| Login/logout/đổi mật khẩu | Đã có | CSRF, scrypt, chặn nghiệp vụ khi chưa đổi pass |
| Quản lý tài khoản | Đã có | Chỉ root tạo/khóa/reset Admin; không khóa/reset root qua danh sách |
| Vô hiệu hóa phiên cũ | Đã có | Xoay token khi đổi/reset pass, khóa/mở tài khoản |
| Khóa tạm đăng nhập | Đã có | 5 lần sai khóa 5 phút; chưa rate limit theo IP ở proxy |
| Danh sách phòng | Đã nâng cấp | Mặc định gọn, giữ mã phòng; lọc đã thu/chưa thu/chưa chốt theo kỳ; tùy chọn đủ cột |
| Thêm/sửa phòng | Đã có | Mã duy nhất, nhiều người/xe mỗi dòng, đếm người tự động |
| Lịch sử khách thuê | Đã có | Chọn đổi khách mới để giữ đợt thuê cũ |
| Xóa/ngừng sử dụng phòng | Đã có | Có đợt thuê/điện thì ngừng sử dụng, giữ lịch sử |
| Chốt điện theo tháng | Đã có | Số nguyên, lưu từng phần, chống trùng kỳ, giao dịch nguyên tử |
| Chi tiết phòng | Đã có | Khách hiện tại, lịch sử thuê và điện |
| Giao diện | Đã nâng cấp V1.1.7 | Jinja2 + CSS riêng + SVG nội bộ; sidebar, login hai cột, bảng sticky, responsive; giữ nguyên chức năng |
| Backup | Có CLI thủ công | SQLite Backup API, đích mới; chưa lịch hoặc lưu ngoài máy |
| Phí nước/dịch vụ | Đã có | Theo đợt thuê, nguyên VND >=0, NULL legacy không phải miễn phí |
| Ngày hợp đồng/trả phòng | Đã có | DATE riêng; không dùng ngày tạo record để suy diễn |
| Gia hạn hợp đồng | Đã có | Xem trước/xác nhận; audit, giữ ngày neo, optimistic lock |
| Ngày đóng tiền | Có lịch nhắc | Ngày 1–31, tháng ngắn lấy cuối tháng; chưa ghi nhận đã đóng/còn nợ |
| Ngày bắt đầu thống nhất | Đã có | Gộp ngày vào ở vào contract_start; không còn ô nhập ngày vào riêng |
| Tiền cọc | Đã có | Theo đợt thuê, cho phép 0; chưa ghi nhận thu/hoàn cọc |
| Tiền phòng | Đã có | Theo tháng/đợt thuê, cho phép 0; giá cũ thiếu giữ NULL; tổng dự tính phòng+nước+dịch vụ chưa điện/cọc |
| Sửa số điện | Đã có | Preview, lý do, audit, cập nhật đầu kỳ sau; chặn nếu phiếu hiệu lực bị ảnh hưởng |
| Chốt tiền tháng | Đã có | Snapshot phòng/nước/dịch vụ/điện/người/hạn; chống trùng; root hủy có lý do và giữ lịch sử |
| Giá điện theo phòng | Đã có | Theo đợt thuê, cho phép 0; phiếu mới lấy giá hiện tại, phiếu cũ giữ snapshot |
| Ngày chốt/cập nhật điện | Đã có | Thời điểm tạo và revision gần nhất, hiển thị ngày giờ UTC+7 |
| Tiền điện ngay trên bảng | Đã có | Tính khi nhập; lưu snapshot giá; ưu tiên giá phiếu đã chốt; legacy thiếu giá có nhãn tạm tính |
| Thu đủ tiền | Đã có | Dropdown, ngày/người/số tiền; chống đúp; root hoàn tác giữ audit; phiếu đã thu xuống dưới |
| Kiểm thử | 46 test pass | unittest nghiệp vụ/permission/filter/sort/migration; Node syntax pass |
| Model/migration khớp nhau | Đã kiểm tra | flask db check không có schema drift |
| Browser/production | Có kiểm tra hình ảnh / chưa production | Edge headless với HTML dữ liệu giả ở desktop và root rộng 390px; chưa kiểm tra tương tác E2E, HTTPS, proxy, job backup |

## Giới hạn nghiệp vụ

- Sửa điện có lịch sử; không xóa lịch sử, chưa hỗ trợ thay đồng hồ. Root cần hủy phiếu tiền hiệu lực bị ảnh hưởng trước khi điều chỉnh điện.
- Không chèn kỳ trước khi đã có kỳ sau. Nếu có lịch sử, chỉ chốt nối tiếp kỳ liền trước.
- Phòng trống vẫn ghi điện. Phòng ngừng sử dụng không có trong bảng nhập.
- Chỉ số nguyên 0–2.147.483.647. Không chia tiền theo đợt thuê giữa tháng.
- Đã ghi nhận thu đủ thủ công; chưa thu một phần, sổ công nợ chi tiết, dashboard, nhiều tòa hoặc tài khoản chỉ xem. Phiếu là bảng tính nội bộ, không phải hóa đơn thuế.
- Phiếu đã chốt giữ snapshot giá/người/chỉ số; giá phiếu mới lấy từ thông tin phòng hiện tại. Form cũ bị chặn khi version đổi. Lập bù/lập lại kỳ cũ cũng gợi ý giá hiện tại; cần kiểm tra giá kỳ. Chưa lịch giá tự động hoặc điện khác tháng tiền phòng.
- Chưa lưu nháp dài hạn: màn hình xem trước rồi chốt trong một phiên. Kỳ vào/trả giữa tháng hoặc đổi khách bị chặn; chưa chia điện theo khách. Root hủy phiếu không có nghĩa hoàn tiền đã thu ngoài hệ thống.
- Gia hạn 1–120 tháng từ hạn cũ; hợp đồng quá hạn cần xác nhận. Hết hạn không tự trả phòng; đợt đã trả không gia hạn. Dữ liệu cũ có thể bổ sung dần; đợt mới cần đủ phí/ngày/lịch đóng.
- HTMX tăng tốc điều hướng; form POST thông thường. Thêm/sửa phòng là trang riêng, chưa popup.

Cách chạy và bằng chứng xem DEVELOPMENT.md, HANDOFF.md.

Kiểm tra V1.7.0: 78 unittest OK (50.165s), DB check/integrity đạt, cột dữ liệu cũ giữ nguyên so với backup. Edge đọc được QR ảnh gốc/crop mobile qua ZXing; không pageerror. Chưa quét app ngân hàng thật.

V1.7.2 — Edge headless đạt kiểm tra bật/tắt công tắc qua giao diện, lưu rồi đọc lại; ZXing đọc QR sau khi tắt không còn mã nội dung, số tiền vẫn 1.234. Không pageerror.

Kiểm tra V1.9.0: 88 unittest OK (50.065s); Edge đạt kiểm tra chỉ một ô lý do, ẩn khi không đổi giá/đổi hạn, hiện và bắt buộc khi đổi tiền, lưu xong thấy nhật ký dưới form. Ảnh fixture exports/bill-change-history.png. Node syntax, db check, integrity_check và foreign_key_check đạt; dữ liệu các cột cũ giữ nguyên so với backup. Chưa quét ngân hàng/điện thoại thật hoặc triển khai VPS.

Kiểm tra V1.9.2: 88 unittest OK (50.854s), đăng nhập tách root/Admin để kiểm tra quyền thực tế. Admin bị chặn sửa điện/ảnh khi còn phiếu, hủy có lý do và audit đúng Admin rồi sửa được; phiếu đã thu không hủy được, reverse vẫn 403 cho Admin. Edge đạt widget vẫn hiện, thử lưu khi khóa nhận lỗi, ảnh đã lưu không đổi; regression QR/form/nhật ký đạt. Không thay schema hoặc thao tác VPS.

V1.10.0 — Kiểm tra cuối Edge: xuất PNG desktop/mobile thành công, QR đọc lại được; nhánh canShare=false vẫn có tải ảnh, hủy share không báo lỗi, lỗi decode QR hiện thông báo và nút lưu dùng lại được. Không pageerror, không POST/upload trong xuất ảnh; đã xem trực tiếp PNG và screenshot mobile. Chưa kiểm tra album native trên điện thoại thật.
