# Ảnh hợp đồng và ảnh điện (V1.11.0)

## Lưu ảnh trước số điện — V1.11.0

- Trong bảng điện, chọn/kéo ảnh rồi bấm **Lưu ảnh**, không cần nhập đầu/cuối kỳ. Preview chưa bấm lưu vẫn chỉ ở client.
- Ảnh lưu theo phòng và kỳ tháng; reload vẫn thấy thumbnail/trạng thái nén. Chỉ một ảnh mỗi phòng/kỳ, thay mới giữ ảnh cũ đến khi nén xong.
- Khi bấm Lưu chỉ số, ảnh đã lưu được tự gắn vào reading thật; không cần upload lại. Ảnh pending vẫn tiếp tục nén; chốt phiếu tiền vẫn chờ job hoàn tất. Có thể chọn ảnh mới kèm Lưu chỉ số như trước.
- Upload trước số điện không chốt kỳ, không tạo reading/số điện giả, không thay thống kê tiêu thụ. Phòng active/kỳ không tương lai được kiểm tra máy chủ; phiếu tiền còn hiệu lực vẫn khóa sửa ảnh.
- Backup CSDL và toàn bộ uploads, dừng web/worker rồi chạy `python -m flask --app wsgi db upgrade` tới 08a365e42c97 trước khi chạy bản mới. Không có dependency mới. Dữ liệu/file cũ được giữ nguyên.



## Cách dùng

- Thêm/sửa phòng đang thuê: tối đa 5 ảnh hợp đồng mỗi lần, không bắt buộc. Ảnh gắn với đợt thuê, không chuyển sang khách mới khi đổi khách.
- Chốt/sửa số điện không bắt buộc ảnh. Có thể chọn ảnh kèm lần lưu hoặc bổ sung sau; nếu đã chọn ảnh thì máy chủ vẫn kiểm tra định dạng/kích thước. Không có ảnh vẫn lưu được số điện hợp lệ.
- Mỗi ID chốt điện chỉ có một bản ghi ảnh. Lưu ảnh mới sẽ thay ảnh cũ: giữ bản cũ để xem trong lúc nén, chỉ xóa file cũ khi bản mới ready. Nếu nén lỗi, giữ ảnh cũ và báo lỗi cho tải lại. Không nhận thay tiếp khi job hiện tại còn pending.
- Khi đã chốt phiếu tiền hiệu lực cho cùng phòng/kỳ, Root và Admin đều không thêm/thay ảnh được, kể cả request trực tiếp. Giao diện hiện nút vàng để xem thông báo khóa; không mở chọn file. Phiếu đã hủy hiệu lực không còn khóa ảnh. Không chốt phiếu khi ảnh còn pending, tránh ảnh thay sau khi phiếu đã chốt; không có ảnh vẫn chốt tiền được.
- Ngay trong bảng Chỉ số điện: kéo file ảnh từ Explorer/Desktop hoặc chọn file, chỉ hiện preview Chưa tải lên. Bấm Lưu chỉ số mới gửi ảnh của các hàng có nhập số; ảnh chờ ở hàng khác không gửi và không bị mất. Cả phòng chưa chốt và đã chốt đều có nút Lưu ảnh riêng, không cần nhập/sửa số hoặc chuyển trang.
- Hiện tiến độ upload 0–100% theo byte, sau đó trạng thái đang xử lý riêng. Khi worker nén xong, polling theo lô tự hiện thumbnail trong ô, không reload trang. Click thumbnail mở modal Bootstrap; Escape/nút đóng thoát popup. Ảnh lớn là WebP đã nén, không khôi phục gốc đã xóa.
- Màn Sửa điện cũng có vùng thay ảnh trực tiếp trước khi chốt phiếu. Chi tiết phòng chỉ bổ sung ảnh hợp đồng; lịch sử điện xem ảnh hiện tại của từng lần chốt. Lịch sử chỉ số vẫn được giữ, ảnh cũ bị xóa khi thay thành công.
- Nhận JPEG, PNG, WebP tĩnh, tối đa 10 MB và 24 megapixel/ảnh. Chưa nhận HEIC, PDF, SVG hoặc ảnh động. Mỗi request tối đa 64 MB; nhiều phòng hãy lưu từng phần. Sau lỗi form cần chọn lại file.
- Polling khoảng 2 giây khi có pending, tối đa khoảng 60 giây rồi cho bấm kiểm tra lại; lỗi mạng không coi là ảnh hỏng. Nút bỏ ảnh chỉ bỏ file đang chọn, không xóa ảnh đã lưu. Gửi lại cùng mã upload không tạo thêm ảnh. Hết phiên/413/lỗi mạng có thông báo và giữ ảnh chờ; sau kết quả lưu không rõ cần kiểm tra trước khi gửi lại.
- Chỉ Root/Admin đã đăng nhập và đã đổi mật khẩu bắt buộc mới xem/bổ sung ảnh. Kéo từ website/ứng dụng khác cần nguồn cung cấp File thực; nếu chỉ có URL, tải ảnh về máy rồi chọn file. Không tự tải URL từ server. Tắt JavaScript vẫn lưu form chỉ số được; bổ sung ảnh ở form thường tại Sửa điện, không có tiến độ/popup tự động.

## Lưu trữ và hàng đợi

```text
instance/uploads/
  tmp/          # Ảnh gốc tạm, không phục vụ HTTP
  contracts/    # WebP ảnh hợp đồng theo token ngẫu nhiên
  electricity/  # WebP ảnh điện theo token ngẫu nhiên
  worker.lock   # Khóa một tiến trình worker
```

Bảng photo chứa token, previous_token dự phòng khi thay ảnh, chủ sở hữu (đợt thuê hoặc lần chốt điện), người tải, thời điểm và trạng thái pending/ready/failed. Unique reading_id chặn nhiều bản ghi ảnh điện. Record ảnh và nghiệp vụ commit cùng giao dịch. Nếu nghiệp vụ thất bại, rollback DB và xóa ảnh tạm của request.

Upload dùng tên ngẫu nhiên, không dùng đường dẫn khách gửi; kiểm tra byte ảnh/kích thước trước khi vào hàng đợi. Một worker CLI xử lý nền, không chạy thread trong request/Gunicorn, không cần Redis/Celery. Hàng đợi SQLite còn nguyên khi restart. Khóa hệ điều hành ngăn hai worker cùng xử lý thư mục.

Worker xoay theo EXIF, thu cạnh dài tối đa 2200 px, chuyển WebP quality 82, bỏ metadata. Ghi .part rồi rename nguyên tử; chỉ trạng thái ready mới được route đăng nhập phục vụ. Nén có mất chi tiết, cần kiểm tra chữ hợp đồng/số đồng hồ đủ rõ trước dùng thật; không cam kết nhỏ hơn đầu vào cho mọi ảnh vốn đã rất nhỏ.

Sau khi trạng thái cuối được commit, xóa ảnh gốc tạm cả khi thành công hoặc lỗi. Lỗi ảnh cần tải lại; dữ liệu chốt đã nhận được giữ, giao diện báo lỗi ảnh. Nếu worker chết sau rename nhưng trước commit, lần sau nhận file đích và hoàn tất trạng thái. Worker dọn ảnh tạm không thuộc pending sau 1 giờ để xử lý phần sót do crash; khi worker dừng, ảnh chờ vẫn ở tmp cho đến khi worker chạy lại. Cần theo dõi worker và dung lượng đĩa.

Ảnh chỉ trả qua /photos/<id> với xác thực, Cache-Control no-store. Không thêm Nginx alias hoặc đặt uploads vào static. Log lỗi worker chỉ chứa ID job, không chứa tên khách/ảnh hoặc nội dung lỗi decoder.

## Chạy dev

V1.4.2 cần migration a24d09e86c31: backup DB và toàn bộ uploads, dừng web/worker rồi db upgrade. Với ID có nhiều ảnh cũ, migration giữ ảnh ready mới nhất, hoặc job mới nhất nếu chưa có ready; bỏ các record thừa. File không còn tham chiếu được worker dọn sau 1 giờ; bộ backup trước nâng cấp giữ toàn bộ ảnh cũ. Ảnh hợp đồng không giới hạn bởi unique reading_id. Có script kiểm thử browser tùy chọn `python scripts/check_meter_photo_browser.py` (Playwright và Edge), dùng DB/ảnh tạm. Runtime không thêm dependency mới.

Cài requirements trong venv, backup database và uploads rồi chạy migration a24d09e86c31 khi web/worker dừng. Migration này thêm cột fallback và gộp ảnh điện trùng, không đổi chỉ số/phiếu/tài khoản.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app wsgi db upgrade
```

Mở terminal riêng cùng thư mục dự án:

```powershell
.\.venv\Scripts\python.exe -m flask --app wsgi process-photos
```

Ctrl+C dừng worker, không dừng web. Thêm --once để xử lý hàng đợi hiện có rồi thoát. Web/worker cần cùng .env, database và uploads. Không có worker thì ảnh chỉ ở trạng thái đang xử lý.

## Cập nhật VPS hiện có

Chưa tự triển khai trên VPS. Tạm dừng nhập liệu/web và worker nếu đã có, backup DB/ảnh, chép code/migrations/requirements và deploy/chdv-photos.service; giữ .env/instance. Cài dependencies và chạy db upgrade trước khi mở web. Pillow 13.0.0 cần Python >=3.11; Ubuntu đang dùng 3.12 phù hợp yêu cầu phiên bản nhưng cần chạy test lại trên VPS.

Trong site Nginx chdv ở server HTTPS, đổi `client_max_body_size 256k;` thành `client_max_body_size 64m;`. Kiểm tra cả khối HTTP nếu có giới hạn riêng; giữ cấu hình chứng chỉ Certbot. Chạy nginx -t rồi reload.

Từ /opt/chdv, sau khi upload service:

```bash
cp deploy/chdv-photos.service /etc/systemd/system/chdv-photos.service
install -d -o chdv -g chdv -m 700 /opt/chdv/instance/uploads
systemctl daemon-reload
systemctl enable --now chdv-photos
systemctl restart chdv
systemctl status chdv chdv-photos --no-pager
journalctl -u chdv-photos -n 50 --no-pager
```

Thử upload bằng tài khoản hợp lệ, kiểm tra pending → ready, xem ảnh nén và tmp không còn gốc tương ứng. Thử restart worker khi có hàng đợi. Không đánh dấu đã triển khai chỉ vì có service file trong repo.

## Backup/khôi phục

Backup DB không chứa byte ảnh. Cần lưu thêm toàn bộ instance/uploads, .env và code/schema tương ứng. Để có bộ backup nhất quán: dừng web/worker và mọi tác vụ ghi → backup-db → copy uploads → mở lại worker/web. Ảnh pending cần tmp tương ứng; không bỏ tmp nếu hàng đợi chưa xong. Bảo vệ bộ backup vì ảnh có thể chứa thông tin hợp đồng/khách.

Restore DB/uploads tương ứng khi web/worker dừng, cấp owner chdv và quyền riêng tư, migrate nếu cần, chạy worker và kiểm tra ảnh. worker.lock không cần restore; OS lock hết khi tiến trình chết. Chưa diễn tập restore ảnh vận hành trên VPS.

## Nguồn

- Pillow WebP/metadata: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
- Pillow security: https://pillow.readthedocs.io/en/stable/handbook/security.html

## V1.6.0 — QR nhận tiền

Cấu hình /settings/payment dành cho root/Admin; service payment_settings lưu DB và ảnh riêng dưới uploads/payment. Route ảnh yêu cầu đăng nhập. Thay ảnh lưu file mới trước commit, dọn file cũ sau commit; khi lỗi commit xóa file mới. QR PNG lossless để giữ cạnh mã; không qua worker ảnh điện. Phiếu chưa thu hiển thị QR cạnh tài khoản, phiếu đã thu/hủy ẩn chuyển khoản. Không sinh QR hoặc tự xác minh dữ liệu ngân hàng từ ảnh. Backup cả DB và uploads; migration c46f21a08e53.

## V1.7.0 — Tạo QR cục bộ

V1.7.0: Đã hiện thực QR chuyển khoản tạo cục bộ bằng qrcode 8.2, TLV NAPAS/QRIBFTTA, CRC16-CCITT. Không gọi dịch vụ bên ngoài hoặc lưu ảnh cho từng phiếu. Dropdown 48 ngân hàng từ snapshot API Banks ngày 2026-11-04 ở app/data/banks.json; không có tác vụ mạng runtime. Admin chọn BIN và điền STK (giữ số 0 đầu, 1–19 ký tự ASCII chữ/số), tên chủ tài khoản, ghi chú. Máy chủ lấy ngân hàng từ allowlist, không tin tên ngân hàng gửi từ form. Ghi chú chỉ hiển thị trên phiếu, nội dung QR tự tạo theo P{id} {room} T{mmyyyy}; tiền dùng bill.total sau điều chỉnh, không nhận override từ query string.

Migration d57032b19f64 thêm bank_bin nullable, không đoán BIN từ tên cũ; admin cấu hình ngân hàng để bật QR mới. Ảnh QR cũ được giữ và dùng fallback khi chưa có BIN, không xóa dữ liệu cũ. QR đã thu/hủy/0 đồng không được phát; tổng trên 13 chữ số không sinh QR nhưng vẫn mở phiếu được. Thông tin nhận tiền là cấu hình chung hiện tại. Tên chủ TK không tự xác minh; không tự ghi nhận đã thu khi tạo/quét QR.

DEV đã backup backups/pre-local-vietqr-v162.sqlite3 và upgrade/db check đạt. QR đối chiếu vector nguồn độc lập và đọc ngược PNG bằng ZXing-C++; Edge kiểm tra QR từng phiếu chứa số cuối cùng 1.234 thay vì query giả 1, STK/nội dung đúng, QR crop trên mobile đọc được, responsive/in và regression ảnh điện đạt. ZXing-C++ chỉ dùng QA, không cần cài trên VPS. Chưa quét bằng app ngân hàng thật hoặc triển khai VPS, không xác nhận tương thích thực tế với mọi ngân hàng. Cần cài requirements mới, migration rồi restart web/worker khi đưa lên VPS; quét thử bằng ngân hàng để đối chiếu người nhận/số tiền/nội dung trước khi dùng gửi khách.

## V1.9.2 — Quyền sửa điện và ảnh công tơ

Admin và root được hủy phiếu chưa thu với lý do để mở khóa sửa điện/ảnh. Phiếu đã thu vẫn chặn hủy; chỉ root có quyền hoàn tác ghi nhận thu. Các mô tả trước đây yêu cầu root hủy cả phiếu chưa thu được thay bằng quy tắc này. Link sửa điện và ô chọn/thay ảnh luôn hiện; còn phiếu hiệu lực thì service từ chối lưu với thông báo cần hủy trước. Bảo toàn kiểm tra kỳ sau, serializing ghi SQLite và snapshot phiếu cũ. Không thay schema.
