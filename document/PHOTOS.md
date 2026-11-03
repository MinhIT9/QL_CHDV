# Ảnh hợp đồng và ảnh điện (V1.3.0)

## Cách dùng

- Thêm/sửa phòng đang thuê: tối đa 5 ảnh hợp đồng mỗi lần, không bắt buộc. Ảnh gắn với đợt thuê, không chuyển sang khách mới khi đổi khách.
- Chốt số điện: mỗi phòng có nhập cuối kỳ phải chọn một ảnh. Phòng không nhập số được bỏ qua. Kiểm tra bắt buộc ở máy chủ.
- Sửa số điện: sau xem trước, chọn ảnh đối chiếu mới rồi xác nhận. Giữ ảnh cũ và lịch sử; kỳ sau được cập nhật đầu kỳ tự động không yêu cầu chụp lại cuối kỳ.
- Chi tiết phòng: xem ảnh theo đợt thuê/kỳ, bổ sung vào dữ liệu cũ hoặc tải lại nếu xử lý lỗi. Không ép dữ liệu cũ phải có ảnh khi migration.
- Nhận JPEG, PNG, WebP tĩnh, tối đa 10 MB và 24 megapixel/ảnh. Chưa nhận HEIC, PDF, SVG hoặc ảnh động. Mỗi request tối đa 64 MB; nhiều phòng hãy lưu từng phần. Sau lỗi form cần chọn lại file.
- Hiện trạng thái đang xử lý/lỗi; tải lại trang sau vài giây để xem liên kết ảnh. Chỉ Root/Admin đã đăng nhập và đã đổi mật khẩu bắt buộc mới xem/bổ sung ảnh, cùng phạm vi quyền phòng hiện tại.

## Lưu trữ và hàng đợi

```text
instance/uploads/
  tmp/          # Ảnh gốc tạm, không phục vụ HTTP
  contracts/    # WebP ảnh hợp đồng theo token ngẫu nhiên
  electricity/  # WebP ảnh điện theo token ngẫu nhiên
  worker.lock   # Khóa một tiến trình worker
```

Bảng photo chứa token, chủ sở hữu (đợt thuê hoặc lần chốt điện), người tải, thời điểm và trạng thái pending/ready/failed. Record ảnh và nghiệp vụ được commit cùng giao dịch. Nếu nghiệp vụ thất bại, rollback DB và xóa ảnh tạm của request.

Upload dùng tên ngẫu nhiên, không dùng đường dẫn khách gửi; kiểm tra byte ảnh/kích thước trước khi vào hàng đợi. Một worker CLI xử lý nền, không chạy thread trong request/Gunicorn, không cần Redis/Celery. Hàng đợi SQLite còn nguyên khi restart. Khóa hệ điều hành ngăn hai worker cùng xử lý thư mục.

Worker xoay theo EXIF, thu cạnh dài tối đa 2200 px, chuyển WebP quality 82, bỏ metadata. Ghi .part rồi rename nguyên tử; chỉ trạng thái ready mới được route đăng nhập phục vụ. Nén có mất chi tiết, cần kiểm tra chữ hợp đồng/số đồng hồ đủ rõ trước dùng thật; không cam kết nhỏ hơn đầu vào cho mọi ảnh vốn đã rất nhỏ.

Sau khi trạng thái cuối được commit, xóa ảnh gốc tạm cả khi thành công hoặc lỗi. Lỗi ảnh cần tải lại; dữ liệu chốt đã nhận được giữ, giao diện báo lỗi ảnh. Nếu worker chết sau rename nhưng trước commit, lần sau nhận file đích và hoàn tất trạng thái. Worker dọn ảnh tạm không thuộc pending sau 1 giờ để xử lý phần sót do crash; khi worker dừng, ảnh chờ vẫn ở tmp cho đến khi worker chạy lại. Cần theo dõi worker và dung lượng đĩa.

Ảnh chỉ trả qua /photos/<id> với xác thực, Cache-Control no-store. Không thêm Nginx alias hoặc đặt uploads vào static. Log lỗi worker chỉ chứa ID job, không chứa tên khách/ảnh hoặc nội dung lỗi decoder.

## Chạy dev

Cài requirements trong venv, backup database rồi chạy migration. Migration f13a98c52b70 chỉ thêm bảng photo, giữ dữ liệu nghiệp vụ cũ.

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
