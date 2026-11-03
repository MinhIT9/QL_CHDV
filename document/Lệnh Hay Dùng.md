VPS:

xem terminal chdv
tail -n 10 -F /var/log/nginx/access.log | awk '{gsub(/"/,"",$6); printf "%-15s %s %-5s %-35s %s\n", $1,$4,$6,$7,$9; fflush()}'

backups csdl trên ubuntu
cd /opt/chdv
sudo -u chdv .venv/bin/python -m flask --app wsgi backup-db "/opt/chdv/backups/chdv-$(date +%Y%m%d-%H%M%S).sqlite3"

