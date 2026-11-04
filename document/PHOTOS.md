# Ảnh hợp đồng và ảnh điện (V1.4.2)

## Cách dùng

- Thêm/sửa phòng đang thuê: tối đa 5 ảnh hợp đồng mỗi lần, không bắt buộc. Ảnh gắn với đợt thuê, không chuyển sang khách mới khi đổi khách.
- Chốt/sửa số điện không bắt buộc ảnh. Có thể chọn ảnh kèm lần lưu hoặc bổ sung sau; nếu đã chọn ảnh thì máy chủ vẫn kiểm tra định dạng/kích thước. Không có ảnh vẫn lưu được số điện hợp lệ.
- Mỗi ID chốt điện chỉ có một bản ghi ảnh. Lưu ảnh mới sẽ thay ảnh cũ: giữ bản cũ để xem trong lúc nén, chỉ xóa file cũ khi bản mới ready. Nếu nén lỗi, giữ ảnh cũ và báo lỗi cho tải lại. Không nhận thay tiếp khi job hiện tại còn pending.
- Khi đã chốt phiếu tiền hiệu lực cho cùng phòng/kỳ, Root và Admin đều không thêm/thay ảnh được, kể cả request trực tiếp. Giao diện chỉ cho xem. Phiếu đã hủy hiệu lực không còn khóa ảnh. Không chốt phiếu khi ảnh còn pending, tránh ảnh thay sau khi phiếu đã chốt; không có ảnh vẫn chốt tiền được.
- Ngay trong bảng Chỉ số điện: kéo file ảnh từ Explorer/Desktop hoặc chọn file, chỉ hiện preview Chưa tải lên. Bấm Lưu chỉ số mới gửi ảnh của các hàng có nhập số; ảnh chờ ở hàng khác không gửi và không bị mất. Phòng đã chốt có nút Lưu ảnh riêng, không cần sửa số hoặc chuyển trang.
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
