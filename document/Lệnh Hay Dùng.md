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

