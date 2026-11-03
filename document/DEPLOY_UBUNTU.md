# Đưa CHDV Manager lên Ubuntu 24.04 bằng MobaXterm

V1.3.0 bổ sung upload ảnh: cần chạy thêm worker deploy/chdv-photos.service và backup cả instance/uploads. Với VPS đã triển khai, xem PHOTOS.md trước khi cập nhật; cấu hình Nginx cũ 256k phải tăng lên 64m. Pillow 13.0.0 yêu cầu Python >=3.11.

Ngày phân tích: 2026-11-03. Đây là hướng dẫn đề xuất, chưa thực thi hoặc kiểm chứng trên VPS. Giữ Flask + SQLite; không cần Node, build frontend hay cài MySQL. Local đã kiểm thử Python 3.11.9; Python 3.12 trên Ubuntu 24.04 cần kiểm thử trước khi mở sử dụng thật.

## Mô hình và thư mục

Trình duyệt → HTTPS/Nginx → Gunicorn ở 127.0.0.1:8000 → Flask → SQLite trên đĩa VPS. systemd giữ ứng dụng chạy khi đóng SSH và tự khởi động sau reboot. Tài khoản Linux `chdv` khác tài khoản root đăng nhập trong ứng dụng.

```text
/opt/chdv/
  app/                  # Toàn bộ code, templates, static và vendor
  migrations/           # Toàn bộ lịch sử migration
  tests/                # Để kiểm thử trước khi vận hành
  requirements.txt
  wsgi.py
  .env.example
  .env                  # Tạo riêng trên VPS, không công khai
  .venv/                # Tạo trên Ubuntu
  instance/
    chdv.sqlite3        # Database vận hành
  backups/              # Backup riêng, không phục vụ qua web
/etc/systemd/system/chdv.service
/etc/nginx/sites-available/chdv
/etc/nginx/sites-enabled/chdv
```

DB mặc định nằm dưới `instance/` vì app cố định instance_path. Database WAL cần quyền ghi cả thư mục để tạo các file `-wal`/`-shm`. Không đặt database hoặc .env trong static hoặc Nginx root.

## Chuẩn bị và chuyển file

Cần IP VPS, username SSH, cổng SSH và mật khẩu/key. Nên có domain/subdomain trỏ bản ghi A về IP; nếu có AAAA phải trỏ đúng IPv6. VPS đang có web khác cần kiểm tra cổng 80/443 và cấu hình hiện tại trước, không ghi đè site khác.

MobaXterm: Session → SSH → Remote host/IP → Specify username → đúng cổng SSH; chọn private key trong Advanced SSH settings nếu dùng key. Sau khi kết nối, thanh SFTP bên trái dùng để kéo thả file. Tạo thư mục trước; upload vào thư mục home của tài khoản SSH, sau đó dùng sudo copy đúng danh sách file vào /opt/chdv nếu SFTP không có quyền ghi.

Chép `app/`, `migrations/`, `tests/`, `requirements.txt`, `wsgi.py`, `.env.example`. Có thể chép thêm `document/`, `scripts/`, README.md để tra cứu. Không chép `.git/`, venv Windows, `__pycache__/`, log, ảnh kiểm thử trong instance, .env local hoặc toàn bộ backup cũ.

Nếu giữ dữ liệu hiện tại, tạm ngừng nhập liệu local từ lúc backup đến khi chuyển sang VPS. Tại thư mục dự án trên Windows, dùng Python đang chạy được app:

```powershell
python -m flask --app wsgi backup-db backups/to-vps.sqlite3
```

Đích phải chưa tồn tại; chọn tên mới nếu đã có. Chép bản backup này vào `/opt/chdv/instance/chdv.sqlite3` chỉ ở lần cài đầu, khi đích chưa có DB và chưa chạy ứng dụng. Không chép riêng DB đang mở vì có thể bỏ sót WAL. Bản backup mang theo tài khoản, mật khẩu đã hash và dữ liệu nghiệp vụ; đăng nhập bằng tài khoản hiện có. Nếu bắt đầu trống thì không chép DB.

## Cài môi trường Ubuntu

Các lệnh sau dùng tài khoản SSH có sudo, trên VPS cài mới. Nếu đăng nhập Linux root có thể bỏ sudo. Dừng và xử lý lỗi từng bước trước khi tiếp tục.

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nginx sqlite3 ufw certbot python3-certbot-nginx
sudo adduser --system --group --home /opt/chdv --no-create-home chdv
sudo install -d -o chdv -g chdv -m 750 /opt/chdv
sudo install -d -o chdv -g chdv -m 700 /opt/chdv/instance /opt/chdv/backups
```

Sau khi copy code và bản backup (nếu có) vào đúng vị trí:

```bash
sudo chown -R chdv:chdv /opt/chdv
sudo chmod 700 /opt/chdv/instance /opt/chdv/backups
sudo -u chdv python3 -m venv /opt/chdv/.venv
cd /opt/chdv
sudo -u chdv .venv/bin/python -m pip install -r requirements.txt
sudo -u chdv .venv/bin/python -m pip install gunicorn
sudo -u chdv .venv/bin/python -m unittest discover -s tests -v
```

Gunicorn chưa có trong requirements.txt hiện tại. Trước vận hành cần rà phiên bản/bảo mật của dependencies và ghi lại phiên bản Gunicorn đã kiểm thử vào cấu hình triển khai có khóa phiên bản; không coi cài thành công là đã kiểm chứng production.

## Cấu hình môi trường và database

Tạo `/opt/chdv/.env` bằng `sudo nano /opt/chdv/.env`, chỉ khi chưa có file. Ví dụ:

```dotenv
SECRET_KEY=THAY_BANG_KHOA_NGAU_NHIEN_RIENG
DATABASE_URL=sqlite:////opt/chdv/instance/chdv.sqlite3
COOKIE_SECURE=true
INITIAL_ADMIN_USERNAME=root
INITIAL_ADMIN_PASSWORD=
```

Tạo khóa bằng `.venv/bin/python -c 'import secrets; print(secrets.token_hex(32))'`, dán vào .env. Giữ khóa ổn định khi restart/cập nhật; đổi khóa làm mất phiên đăng nhập. Không gửi khóa hoặc mật khẩu vào chat/Git/log. APP_ENV hiện chưa được code sử dụng để bật chế độ production; không bật FLASK_DEBUG.

```bash
sudo chown chdv:chdv /opt/chdv/.env
sudo chmod 600 /opt/chdv/.env
sudo -u chdv .venv/bin/python -m flask --app wsgi db upgrade
sudo -u chdv .venv/bin/python -m flask --app wsgi db current
sudo -u chdv .venv/bin/python -m flask --app wsgi db check
```

Nếu dùng DB trống: điền mật khẩu khởi tạo riêng ít nhất 8 ký tự vào .env, chạy `sudo -u chdv .venv/bin/python -m flask --app wsgi init-admin`, sau đó xóa giá trị INITIAL_ADMIN_PASSWORD. Đăng nhập lần đầu phải đổi mật khẩu. Nếu chuyển DB cũ, không cần tạo lại root; init-admin không reset mật khẩu root đang tồn tại.

## systemd

Tạo `/etc/systemd/system/chdv.service` bằng sudo nano:

```ini
[Unit]
Description=CHDV Manager
After=network.target

[Service]
User=chdv
Group=chdv
WorkingDirectory=/opt/chdv
Environment=PYTHONUNBUFFERED=1
ExecStart=/opt/chdv/.venv/bin/gunicorn --workers 1 --bind 127.0.0.1:8000 --forwarded-allow-ips=127.0.0.1 --error-logfile - wsgi:app
Restart=on-failure
RestartSec=5
UMask=0077
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

App tự đọc .env theo đường dẫn dự án, không cần source file .env trong shell. Khởi đầu một worker phù hợp quy mô nhỏ/SQLite; đo tải rồi mới điều chỉnh. Không dùng --preload hoặc chạy flask run công khai.

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now chdv
sudo systemctl status chdv --no-pager
curl -I http://127.0.0.1:8000/login
```

## Nginx, firewall và HTTPS

Thay `chdv.example.com` bằng tên miền thật. Tạo `/etc/nginx/sites-available/chdv`:

```nginx
server {
    listen 80;
    server_name chdv.example.com;
    client_max_body_size 64m;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Nginx chỉ proxy, không public cả /opt/chdv. Gunicorn chỉ tin proxy loopback, đọc X-Forwarded-Proto để WSGI nhận HTTPS. App hiện chưa dùng ProxyFix; nếu bổ sung lấy IP thật hoặc thêm nhiều tầng proxy cần cấu hình trust đúng số tầng và kiểm thử, không tự tin header từ Internet.

```bash
sudo ln -s /etc/nginx/sites-available/chdv /etc/nginx/sites-enabled/chdv
sudo nginx -t
sudo systemctl reload nginx
```

Mở cổng SSH thực tế trước khi bật UFW; `OpenSSH` thường là 22, nếu VPS dùng cổng khác phải allow cổng đó thay cho ví dụ. Giữ phiên SSH hiện tại và thử thêm một kết nối sau khi bật firewall. Đồng thời mở cổng tại firewall/security group của nhà cung cấp VPS.

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
sudo certbot --nginx -d chdv.example.com
sudo certbot renew --dry-run
```

Lệnh Certbot cần DNS đúng và port 80/443 truy cập được. Chọn chuyển HTTP sang HTTPS. COOKIE_SECURE=true chỉ đăng nhập qua HTTPS. Nếu chưa có domain, có thể kiểm tra ứng dụng qua SSH tunnel riêng thay vì gửi mật khẩu/dữ liệu khách qua HTTP công khai; hoàn tất domain/HTTPS trước dùng thật. Không mở cổng 8000 ra Internet.

## Kiểm tra, backup và cập nhật

Kiểm tra HTTPS, đăng nhập/đổi mật khẩu, quyền root/Admin, danh sách và chi tiết phòng, chuyển kỳ điện, chốt/thu tiền bằng dữ liệu thử; không ghi giao dịch thử vào dữ liệu thật. Kiểm tra CSS/JS: Bootstrap hiện tải CDN jsDelivr, trình duyệt cần kết nối được CDN. Thử đóng SSH và reboot VPS có kiểm soát rồi truy cập lại. Xem lỗi bằng `sudo journalctl -u chdv -n 100 --no-pager` và `/var/log/nginx/error.log`; không đưa dữ liệu nhạy cảm vào nội dung log/chia sẻ.

Backup thủ công trên VPS:

```bash
cd /opt/chdv
sudo -u chdv .venv/bin/python -m flask --app wsgi backup-db "/opt/chdv/backups/chdv-$(date +%Y%m%d-%H%M%S).sqlite3"
```

Trước dùng thật cần thêm lịch backup hằng ngày bằng timer/cron, giới hạn thời gian giữ bản, cảnh báo thất bại và bản sao bảo mật ngoài VPS. Kéo bản backup bằng SFTP về nơi riêng; không đặt trong Git. Diễn tập khôi phục vào DB thử: kiểm tra integrity_check, migration và dữ liệu. Khi restore thật phải dừng mọi tiến trình truy cập DB, giữ bản hiện tại cùng sidecar để quay lui, rồi mới thay DB và xử lý sidecar cũ; không ghi đè DB đang chạy.

Khi cập nhật: dừng dịch vụ và thao tác ghi khác, backup → chép code/migrations/requirements mới → cài dependencies → db upgrade → kiểm tra → restart. Giữ .env, instance và backups; không kéo nguyên thư mục Windows đè lên runtime. Nếu migration lỗi, giữ dịch vụ dừng để xử lý; rollback cần code và database tương thích.

## Nguồn tham khảo

- Flask production: https://flask.palletsprojects.com/en/stable/deploying/
- Flask/Gunicorn: https://flask.palletsprojects.com/en/stable/deploying/gunicorn/
- Gunicorn/Nginx: https://gunicorn.org/deploy/
- Proxy trust: https://flask.palletsprojects.com/en/stable/deploying/proxy_fix/
- Ubuntu firewall: https://ubuntu.com/server/docs/firewalls/
