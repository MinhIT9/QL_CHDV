# Hướng dẫn phát triển và vận hành local

V1.1.11: migration mới nhất d94f512a37b1 đã backup/upgrade local. Bảng điện hiển thị ngày giờ lưu/sửa gần nhất và tự tính tiền; đơn giá được chụp khi lưu điện mới. Bản cũ chưa biết giá được ghi tạm tính, phiếu hiệu lực luôn ưu tiên hơn dự tính. Ctrl+F5 sau khởi động lại để nạp CSS/JS mới.

V1.1.10: migration mới nhất c83e4d16b2a0 đã backup/upgrade local. Giá điện nhập trong form phòng, cho phép 0. Sửa giá chỉ đổi gợi ý phiếu lập sau; phiếu đã chốt giữ nguyên. Nếu form chốt tiền báo dữ liệu đã đổi, tải lại để nhận giá mới. Khi lập bù/lập lại kỳ cũ cần xác nhận đúng giá vì mặc định vẫn là giá hiện tại.

## Thiết lập

Đã kiểm thử với Python 3.11.9. Dependencies trực tiếp khóa trong requirements.txt; test dùng unittest. Lượt triển khai dùng dependencies sẵn có, không cài thêm vào Python toàn cục.

    python -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    Copy-Item .env.example .env

Chỉ copy mẫu khi chưa có .env; không ghi đè cấu hình đang dùng. Điền SECRET_KEY ngẫu nhiên, INITIAL_ADMIN_PASSWORD và URL database. .env.example không chứa pass thật. Có thể tạo khóa bằng Python secrets.token_hex(32).

    .\.venv\Scripts\python.exe -m flask --app wsgi db upgrade
    .\.venv\Scripts\python.exe -m flask --app wsgi init-admin
    .\.venv\Scripts\python.exe -m flask --app wsgi run --host 127.0.0.1 --port 5000

init-admin không thay mật khẩu root tồn tại. Database vận hành dùng migration, không db.create_all(). Flask dev server chỉ dùng local.

## Tài khoản

- Root cấp tài khoản Admin và pass tạm >=8 ký tự qua menu Tài khoản.
- Cả root bootstrap và Admin mới phải đổi pass trước khi làm việc.
- Pass mới 8–128 ký tự, khác pass cũ, không khoảng trắng đầu/cuối; xác nhận và nhập pass hiện tại.
- Reset bắt đổi lại, hủy phiên cũ; khóa/mở tài khoản cũng xoay token. Không xóa tài khoản để giữ liên kết điện.
- 5 lần login sai khóa tạm 5 phút. Root reset pass xóa khóa tạm Admin. Chưa phục hồi root qua web.
- Tên tài khoản chữ thường, 3–64 ký tự [a-z0-9_.-], bắt đầu bằng chữ/số.

## Kiểm tra và migration

    python -m unittest discover -s tests -v
    python -m flask --app wsgi db check
    node --check app/static/js/app.js
    python scripts/update_docs.py
    python scripts/update_docs.py --check

Tests dùng SQLite tạm, không dữ liệu thật. Test HTML/CSRF không thay thế browser QA của HTMX/JS/responsive. Chưa có browser QA tự động.

Đổi schema: sửa model → flask db migrate -m ten_thay_doi → review → backup DB → flask db upgrade. Luôn thêm --app wsgi khi dùng CLI, commit migration cùng code.

## Backup/khôi phục

Migration mới nhất dd7493777e83 đã được áp dụng trên máy hiện tại sau backup trong backups/pre-fees-contracts-*.sqlite3. Migration thêm nullable, giữ nguyên dữ liệu cũ. Downgrade dùng native DROP COLUMN nên yêu cầu SQLite >=3.35 và sẽ mất các thông tin phí/hợp đồng mới; không chạy trên dữ liệu vận hành khi chưa có kế hoạch khôi phục.

    python -m flask --app wsgi backup-db backups/chdv-before-change.sqlite3

Đích phải mới, không ghi đè. CLI dùng SQLite Backup API để nhất quán khi DB đang hoạt động. Chưa có lịch hằng ngày hoặc đích ngoài máy.

Khôi phục: dừng mọi tiến trình truy cập DB, giữ bản hiện tại để có đường quay lui, kiểm tra PRAGMA integrity_check của backup, thay DB khi mọi kết nối đã đóng. Chỉ xử lý WAL/SHM sau khi chắc chắn không còn kết nối. Chạy migration phù hợp, mở lại và kiểm tra dữ liệu/quyền. Chưa diễn tập restore vào database vận hành.

## Phí, hợp đồng và thao tác phòng

V1.1.9 (migration 0fecdf9f864b) đã backup/upgrade local. Sửa điện: vào Chỉ số điện → Sửa điện → nhập số/lý do → xem trước → xác nhận. Kỳ sau được đồng bộ đầu kỳ và có audit; chỉ số cuối thực tế giữ nguyên.

Chốt tiền: menu Chốt tiền → chọn tháng/phòng → xác nhận bốn giá, số người và ngày đến hạn → xem trước → chốt. Phòng và điện cùng tháng; giá là snapshot riêng mỗi phiếu, không thay hợp đồng hoặc các tháng khác. Chưa thực thu/chia ngày/lịch giá tự động. Khi sai: root hủy hiệu lực phiếu với lý do (kể cả phiếu kỳ kế tiếp nếu bị ảnh hưởng), sửa điện rồi lập lại. Nếu đã thu ngoài hệ thống phải đối chiếu riêng; hủy phiếu không hoàn tiền.

V1.1.6 thêm tiền phòng/tháng (rent_price); đợt mới bắt buộc nhập, cho phép 0, legacy NULL chưa cập nhật. Giá giữ qua gia hạn và lưu theo lịch sử khách. Tổng dự tính phòng+nước+dịch vụ chưa điện/cọc/chia ngày. Migration mới nhất b71c430e92ad đã backup/upgrade local.

Từ V1.1.5 chỉ nhập Ngày bắt đầu hợp đồng, đồng thời là ngày vào ở. Tiền cọc nhập số nguyên VND (0 nếu không cọc); dữ liệu cũ NULL là chưa cập nhật. Không cộng cọc vào phí tháng hoặc hiểu là đã thu/hoàn. Migration mới nhất a65b2f9c018e đã backup và áp dụng local; khởi động lại Flask để nạp code mới.

- Khi tạo đợt thuê mới: nhập đủ giá nước/người/tháng, dịch vụ/phòng/tháng (0 nếu miễn phí), ngày vào thực tế, bắt đầu/hết hạn hợp đồng và ngày đóng 1–31.
- Bản cũ có thể bổ sung dần; trường đã có không được xóa về trống. Hết hạn không tự trả phòng. Không nhận ngày vào/bắt đầu tương lai trong luồng thuê hiện tại.
- Chi tiết phòng có nút Gia hạn: nhập số tháng/ghi chú, xem trước rồi xác nhận; hợp đồng quá hạn phải xác nhận mốc cũ. Giữ khách/phí/lịch đóng; lưu lịch sử. Tháng ngắn giữ ngày neo, không cộng x30 ngày.
- Form có ID/version đợt thuê; thông báo biểu mẫu cũ cần tải lại khi có người sửa/gia hạn trước. Không tự bỏ kiểm tra này bằng cách xóa trường ẩn.
- Đổi khách, chuyển trống hoặc ngừng phòng có khách phải nhập ngày trả thực tế; ngày trả không trước ngày vào hoặc sau hôm nay.
- Giá và lịch đóng ở bảng là thông tin hiện tại. Dự tính tháng đủ chưa chia ngày, chưa ghi nhận khoản phải thu/thực thu. Không dùng để kết luận nợ hoặc đã thanh toán.

## Production

Cần WSGI server, HTTPS, COOKIE_SECURE=true, SECRET_KEY ổn định/bí mật, backup hằng ngày ngoài máy, diễn tập restore, quyền file DB và kiểm tra/cập nhật dependencies. DB trên volume bền vững. Không bật debugger công khai.

## Tài liệu và Git

FE V1.1.7 dùng design system trong app/static/css/app.css; xem UI_DESIGN.md trước khi sửa UI. Có ảnh review dữ liệu giả trong instance/ui-*.png (ngoài Git). Không có migration mới cho đợt nâng FE; Ctrl+F5 nếu browser còn dùng CSS cũ. Đã review ảnh tĩnh, chưa browser E2E.

Cập nhật STATUS.md, HANDOFF.md, CHANGELOG.md sau mỗi thay đổi; sửa kiến trúc/phạm vi/quyết định khi cần. Chạy sinh danh mục và --check. Agent tuân AGENTS.md, bao gồm số phiên bản cuối phản hồi.

INVENTORY.md tự sinh; chức năng phải được đánh dấu dựa trên kiểm tra thực tế. Hook local tùy chọn:

    git config --local core.hooksPath .githooks

Chưa tự bật hook; nếu có hook riêng cần ghép. Hook không tự stage, yêu cầu review/stage danh mục khi thay đổi.

.env, DB/WAL/SHM, backup, upload/export/log và venv bị ignore. Migration/requirements phải theo dõi. Ignore không gỡ file đã track. Không đưa pass/dữ liệu thật vào tài liệu. Chưa chọn license cho mã dự án; license HTMX kèm static/vendor.
