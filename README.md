# CHDV Manager Basic

Ứng dụng Flask quản lý căn hộ dịch vụ bằng bảng, một project và SQLite cục bộ.

## V1 đã có

- Đăng nhập, đăng xuất, đổi mật khẩu; bắt buộc đổi mật khẩu lần đầu cho cả root và Admin mới.
- Root tạo, khóa/mở khóa và đặt lại mật khẩu Admin. Admin quản lý phòng/điện, không quản lý tài khoản.
- Danh sách, tìm kiếm, thêm/sửa phòng, nhiều người/xe và lịch sử các đợt thuê.
- Chốt điện theo tháng/từng phần, tự lấy đầu kỳ từ kỳ trước; không ghi đè kỳ đã chốt.
- Chi tiết phòng, lịch sử thuê/điện; ngừng sử dụng thay vì xóa phòng có lịch sử.
- Migration, CSRF, hash mật khẩu, CLI backup SQLite và kiểm thử.

## Chạy local trên Windows

Máy hiện tại đã có .env, database và root được khởi tạo. Mật khẩu bootstrap theo yêu cầu được giữ ở .env ngoài Git; đăng nhập lần đầu phải đổi mật khẩu.

    python -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    .\.venv\Scripts\python.exe -m flask --app wsgi db upgrade
    .\.venv\Scripts\python.exe -m flask --app wsgi init-admin
    .\.venv\Scripts\python.exe -m flask --app wsgi run --host 127.0.0.1 --port 5000

Mở **http://127.0.0.1:5000**. Nếu dùng Python đã có dependencies, thay đường dẫn Python của venv bằng lệnh python.

Với bản clone mới: copy .env.example thành .env, tạo SECRET_KEY ngẫu nhiên và đặt INITIAL_ADMIN_PASSWORD trước khi chạy. Không dùng khóa mẫu. init-admin chỉ tạo root nếu chưa tồn tại, không reset mật khẩu đã đổi. Sau bootstrap có thể xóa INITIAL_ADMIN_PASSWORD khỏi .env.

## Kiểm tra

    python -m unittest discover -s tests -v
    python -m flask --app wsgi db check
    python scripts/update_docs.py
    python scripts/update_docs.py --check

## Tài liệu và giới hạn

Đọc [tiến độ](document/STATUS.md), [hướng dẫn dev](document/DEVELOPMENT.md), [bàn giao](document/HANDOFF.md) hoặc [mục lục](document/README.md).

V1 dùng chỉ số nguyên kWh; chưa sửa điện cũ, thay đồng hồ, quản lý tiền hoặc báo cáo. Backup ngoài máy chủ và HTTPS production cần cấu hình khi triển khai. Chưa kiểm tra giao diện bằng trình duyệt tự động.
