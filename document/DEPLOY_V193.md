# Cập nhật VPS lên bản V1.9.3

VPS: 103.167.88.214. Website: https://chdv.alominh.homes. Thư mục ứng dụng và nơi upload ZIP đều là **/opt/chdv**. Đây là hướng dẫn thao tác qua MobaXterm, chưa phải bằng chứng đã triển khai.

## 1. Upload và kiểm tra trước khi dừng web

Kéo exports/chdv-v1.9.3.zip từ máy dev vào /opt/chdv/ ở khung SFTP MobaXterm. Trên terminal VPS:

```bash
cd /opt/chdv
python3 -m zipfile -t /opt/chdv/chdv-v1.9.3.zip
```

Phải có Done testing. Nếu báo thiếu file, kiểm tra đúng thư mục upload; không tiếp tục khi chưa kiểm tra được ZIP.

Gói chỉ chứa app, migrations, tests, deploy, scripts, document, requirements.txt, wsgi.py, README.md và .env.example. Không có .env thật, database, ảnh upload hoặc venv.

## 2. Dừng cả hai service và backup nhất quán

Chạy cả khối trong một lần dán. Website tạm dừng đến khi hoàn tất bước 4. Khối dùng set -e trong subshell để dừng khi lỗi mà không đóng phiên SSH.

```bash
(
set -e
cd /opt/chdv
python3 -m zipfile -t /opt/chdv/chdv-v1.9.3.zip
systemctl stop chdv chdv-photos
umask 077
backup_dir=$(mktemp -d /root/chdv-before-v193-XXXXXXXX)
echo "BACKUP_DIR=$backup_dir"
test -d /opt/chdv/backups
db_backup="/opt/chdv/backups/$(basename "$backup_dir").sqlite3"
sudo -u chdv .venv/bin/python -m flask --app wsgi backup-db "$db_backup"
cp "$db_backup" "$backup_dir/database.sqlite3"
tar --exclude='./.venv' --exclude='./.cache' --exclude='./.gunicorn' --exclude='__pycache__' --exclude='./backups' --exclude='*.zip' -czf "$backup_dir/project.tar.gz" -C /opt/chdv .
cp /etc/systemd/system/chdv.service "$backup_dir/"
cp /etc/systemd/system/chdv-photos.service "$backup_dir/"
cp /etc/nginx/sites-available/chdv "$backup_dir/nginx-chdv.conf"
tar -tzf "$backup_dir/project.tar.gz" > /dev/null
ls -lh "$backup_dir"
)
```

Ghi lại BACKUP_DIR thực tế. Bộ backup gồm database nhất quán, code/.env/instance/uploads (cả ảnh đang chờ), cấu hình web/worker/Nginx. Giữ riêng tư bộ backup vì có dữ liệu thật và bí mật. Nếu bất kỳ lệnh backup lỗi, dừng ở đây, chưa giải nén code mới. Nếu cần mở lại bản cũ khi chưa thay code, chạy systemctl start chdv chdv-photos.

## 3. Thay code, cài thư viện, migrate và kiểm tra

Chỉ chạy sau khi bước 2 thành công. Không chép .env hoặc instance từ dev lên VPS.

```bash
(
set -e
cd /opt/chdv
python3 -m zipfile -e /opt/chdv/chdv-v1.9.3.zip /opt/chdv
chown -R chdv:chdv app migrations tests deploy scripts document requirements.txt wsgi.py README.md .env.example
chmod -R u+rwX,go-rwx app migrations tests deploy scripts document requirements.txt wsgi.py README.md .env.example
sudo -u chdv .venv/bin/python -m pip install -r requirements.txt
sudo -u chdv .venv/bin/python -m flask --app wsgi db upgrade
sudo -u chdv .venv/bin/python -m flask --app wsgi db check
sudo -u chdv .venv/bin/python -m flask --app wsgi db current
sudo -u chdv .venv/bin/python -m unittest discover -s tests
)
```

Head mong đợi: **f79254d31b86**. db check không có thao tác mới, tests phải OK. Nếu lỗi, giữ web/worker dừng và xem log; không tiếp tục mở web hoặc chạy downgrade/restore tùy ý.

## 4. Mở lại và kiểm tra website

```bash
systemctl start chdv chdv-photos
systemctl status chdv chdv-photos --no-pager -l
curl --retry 5 --retry-delay 2 --retry-all-errors --fail -I https://chdv.alominh.homes/login
```

Hai service cần active (running), /login trả HTTP 200. Không cần thay Nginx hoặc service unit hiện có cho bản cập nhật này.

Trình duyệt Ctrl+F5, kiểm tra Nhận tiền/QR, phiếu và nhật ký. Thử luồng sửa điện/ảnh trên dữ liệu thử: còn phiếu thì chặn, Admin hủy phiếu chưa thu với lý do rồi sửa được. Quét QR bằng app ngân hàng để đối chiếu người nhận, số tiền và nội dung; chưa cần thực hiện chuyển tiền. Giữ bộ backup sau cập nhật.
