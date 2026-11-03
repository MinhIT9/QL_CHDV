# CHDV Manager Basic

Ứng dụng Flask quản lý căn hộ dịch vụ bằng bảng, một project và SQLite cục bộ.

## V1 đã có

- Đăng nhập, đăng xuất, đổi mật khẩu; bắt buộc đổi mật khẩu lần đầu cho cả root và Admin mới.
- Root tạo, khóa/mở khóa và đặt lại mật khẩu Admin. Admin quản lý phòng/điện, không quản lý tài khoản.
- Danh sách, tìm kiếm, thêm/sửa phòng, nhiều người/xe và lịch sử các đợt thuê.
- Chốt điện theo tháng/từng phần, tự lấy đầu kỳ từ kỳ trước; không ghi đè kỳ đã chốt.
- Chi tiết phòng, lịch sử thuê/điện; ngừng sử dụng thay vì xóa phòng có lịch sử.
- Migration, CSRF, hash mật khẩu, CLI backup SQLite và kiểm thử.
- Phí nước/người và dịch vụ/phòng (cho phép 0); ngày vào/hợp đồng/trả phòng, lịch đóng tiền hằng tháng và gia hạn có lịch sử.
- Ngày vào ở dùng chung Ngày bắt đầu hợp đồng. Có tiền cọc theo đợt thuê (cho phép 0), không cộng vào phí tháng; chưa quản lý thu/hoàn cọc.
- Có tiền phòng/tháng theo đợt thuê; tổng dự tính phòng + nước + dịch vụ, chưa gồm điện và tiền cọc.
- Giao diện V1.1.7: sidebar navy/mint, đăng nhập hai cột, SVG nội bộ, bảng sticky và form responsive. Xem [thiết kế giao diện](document/UI_DESIGN.md).
- Sửa điện có lịch sử/ảnh hưởng kỳ sau; menu Chốt tiền lưu giá, số người và điện riêng từng tháng. Root hủy phiếu có lý do và giữ bản cũ khi cần lập lại.

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

V1 dùng chỉ số nguyên kWh; chưa thay đồng hồ, thực thu/công nợ hoặc báo cáo. Phiếu tiền chỉ hỗ trợ phòng/điện cùng kỳ và đợt thuê đủ tháng; chưa chia ngày hoặc lập lịch giá tự động. Chốt tiền không xác nhận đã thu. Backup ngoài máy chủ và HTTPS production cần cấu hình khi triển khai. Đã review ảnh tĩnh FE; module billing chưa kiểm tra browser end-to-end.
