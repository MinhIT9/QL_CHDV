VPS:

xem terminal chdv
tail -n 10 -F /var/log/nginx/access.log | awk '{gsub(/"/,"",$6); printf "%-15s %s %-5s %-35s %s\n", $1,$4,$6,$7,$9; fflush()}'

backups csdl trên ubuntu
cd /opt/chdv
sudo -u chdv .venv/bin/python -m flask --app wsgi backup-db "/opt/chdv/backups/chdv-$(date +%Y%m%d-%H%M%S).sqlite3"

1. Tạm dừng web và tạo thư mục backup
Website sẽ tạm không truy cập được.
systemctl stop chdv
umask 077
backup_dir=$(mktemp -d /root/chdv-before-update-XXXXXXXX)
echo "$backup_dir"

2. Backup database
cd /opt/chdv
db_backup="/opt/chdv/backups/$(basename "$backup_dir").sqlite3"
sudo -u chdv .venv/bin/python -m flask --app wsgi backup-db "$db_backup"
cp "$db_backup" "$backup_dir/database.sqlite3"

3. Lưu code, dữ liệu và cấu hình hiện tại
tar --exclude='./.venv' --exclude='./.cache' --exclude='__pycache__' --exclude='./backups' --exclude='*.zip' -czf "$backup_dir/project.tar.gz" -C /opt/chdv .
cp /etc/systemd/system/chdv.service "$backup_dir/"
cp /etc/nginx/sites-available/chdv "$backup_dir/nginx-chdv.conf"
ls -lh "$backup_dir"

Cài worker và mở lại website
install -m 644 deploy/chdv-photos.service /etc/systemd/system/chdv-photos.service
install -d -o chdv -g chdv -m 700 /opt/chdv/instance/uploads
systemctl daemon-reload
systemctl reload nginx
systemctl enable --now chdv-photos
systemctl start chdv

-----
chạy project dev
.\.venv\Scripts\python.exe -m flask --app wsgi run --port 5000
.\.venv\Scripts\python.exe -m flask --app wsgi process-photos

## Giữ phiên xem log bằng screen

```bash
apt install -y screen
screen -dmS chdv-log bash -c 'journalctl -u chdv -u chdv-photos -n 50 -f; exec bash'
screen -r chdv-log
```

Rời phiên mà không dừng: Ctrl+A rồi d. Xem phiên: screen -ls. Nếu phiên còn attached ở kết nối khác và cần chuyển về kết nối hiện tại: screen -d -r chdv-log (ngắt phiên hiển thị bên kia). screen -dmS tạo phiên chạy nền, không tự chia ô màn hình. Web vẫn do systemd chạy.


## Xem request web thay vì log khởi động service

Nếu đang ở journalctl, Ctrl+C chỉ dừng xem log, không tắt web. Trong chính screen đó chạy:

```bash
tail -n 10 -F /var/log/nginx/access.log | awk '{gsub(/"/,"",$6); printf "%-15s %s %-5s %-45s %s\n", $1,substr($4,2),$6,$7,$9; fflush()}'
```

Hiện IP, thời gian, GET/POST, đường dẫn, mã HTTP. Mở hoặc tải lại website để thấy dòng mới. Nginx access log là request vào VPS; journalctl chdv là log service/lỗi app, không mặc định có mọi request. Giữ phiên: Ctrl+A rồi d; trở lại: screen -r chdv-log.


## Screen giữ log rút gọn — thao tác chuẩn

Nếu đang ở tail ngoài screen, Ctrl+C về shell trước. Tạo một phiên shell, rồi chạy pipeline bên trong để Ctrl+C không làm phiên kết thúc:

```bash
screen -S chdv-web
```

Trong screen:

```bash
tail -n 10 -F /var/log/nginx/access.log | awk '{gsub(/"/,"",$6); printf "%-15s %s %-5s %-45s %s\n", $1,substr($4,2),$6,$7,$9; fflush()}'
```

- Giữ phiên và về shell SSH: Ctrl+A, thả phím, nhấn d (không gõ nguyên chuỗi ^Ad).
- Liệt kê: screen -ls.
- Vào lại: screen -r chdv-web. Nếu có nhiều phiên cùng tên dùng PID.tên lấy từ screen -ls.
- Nếu phiên còn Attached ở kết nối cũ: screen -d -r chdv-web (tách màn hình kết nối cũ và gắn vào kết nối hiện tại).
- Tạo phiên khác: screen -S work. Chuyển từ phiên đang mở: Ctrl+A rồi d, sau đó screen -r tên_phiên. Không mở screen lồng nhau.
- Kết thúc hẳn phiên: Ctrl+C dừng tail, rồi exit trong shell screen. Web systemd vẫn chạy.

Detach trước khi đóng MobaXterm; SSH lại vào cùng VPS/user rồi screen -r chdv-web để tiếp tục. Phiên giữ qua ngắt SSH nhưng không qua reboot VPS.
