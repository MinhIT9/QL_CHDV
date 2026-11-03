# Bàn giao

Cập nhật: 2026-11-03 (Asia/Saigon).

## Phiên bản hội thoại

- Phiên bản phản hồi gần nhất: V1.1.9.
- Nội dung: sửa điện có lịch sử và chốt tiền riêng từng tháng; triển khai gọn, chưa thực thu/chia ngày.
- Phản hồi tiếp theo dùng V1.1.10. Tăng số cuối sau mỗi final; đây không phải phiên bản phát hành.
- Quy tắc đầy đủ ở AGENTS.md, mục “Phiên bản ở cuối phản hồi”.

## Đã làm

- App factory, .env cục bộ có SECRET_KEY ngẫu nhiên, SQLAlchemy, Flask-Login, CSRF và Flask-Migrate.
- instance/chdv.sqlite3 đã upgrade migration 0fecdf9f864b sau backup backups/pre-billing-*.sqlite3; root và dữ liệu hiện có được giữ. Không ghi mật khẩu vào tài liệu/fixtures/repo.
- Root và Admin mới phải đổi pass lần đầu: 8–128 ký tự, khác pass cũ, kiểm tra phía máy chủ.
- Root tạo/khóa/mở/reset Admin; mọi Admin có quyền phòng/điện, không có đăng ký công khai.
- Năm màn hình nghiệp vụ, cùng đổi mật khẩu và quản lý tài khoản root.
- Phòng có đợt thuê/người/xe; chốt điện nối tiếp tháng, không ghi đè dữ liệu cũ.
- HTMX và license lưu nội bộ, CSS riêng; không cần CDN lúc chạy.
- FE V1.1.7: sidebar xanh đậm/điểm nhấn mint, nền sáng, icon SVG nội bộ, trang đăng nhập hai cột có minh họa SVG. Thiết kế dùng chung cho mọi trang; bảng cố định mã phòng/thao tác khi cuộn, form rõ nhóm, responsive, focus bàn phím và reduced-motion. Không đổi route/model/service/JS nghiệp vụ.
- CLI backup nhất quán và bộ test tích hợp.
- Phí nước/người/tháng, dịch vụ/phòng/tháng cho phép 0; NULL của dữ liệu cũ là chưa biết. Hiển thị dự tính phí tháng đủ, chưa phải hóa đơn.
- Chỉ còn ngày bắt đầu hợp đồng (cũng là ngày vào ở), ngày hết hạn/trả thực tế và lịch đóng 1–31. move_in_date chỉ giữ làm cột legacy, không có ô nhập riêng; save/checkout đồng bộ theo contract_start.
- Tiền cọc theo đợt thuê: nguyên VND >=0, NULL legacy là chưa cập nhật. Có trên form/bảng/chi tiết/lịch sử, không cộng vào phí tháng hoặc xác nhận đã thu/hoàn.
- Tiền phòng rent_price theo đợt thuê, nguyên VND >=0, NULL legacy chưa cập nhật. Form/bảng/chi tiết/lịch sử có giá tháng; monthly_total = tiền phòng + nước + dịch vụ, chưa điện, không cọc. Gia hạn giữ giá hiện tại; khách mới nhập giá riêng.
- Gia hạn xem trước/xác nhận, 1–120 tháng, giữ ngày neo, audit Admin/thời điểm/hạn cũ-mới; version chống sửa/gia hạn lặp. Hợp đồng đã gia hạn không sửa trực tiếp ngày bắt đầu/hết hạn qua form.
- Đổi khách/ngừng sử dụng cần ngày trả thực tế và đúng version đợt thuê. Dữ liệu cũ không bị đoán ngày hoặc gán miễn phí.
- V1.1.9: link Sửa điện tại màn hình điện, preview/confirm, lý do bắt buộc, ReadingRevision lưu trước/sau/Admin/thời điểm, đồng bộ đầu kỳ sau khi cần. Chặn sửa nếu có phiếu tiền hiệu lực trong các kỳ bị ảnh hưởng.
- Menu Chốt tiền: chọn kỳ/phòng, nhập giá điện và kiểm tra giá phòng/nước/dịch vụ, số người; preview rồi chốt snapshot MonthlyBill. Phòng và điện cùng kỳ; không tự tính lại phiếu cũ khi đổi giá. Root có thể hủy hiệu lực có lý do, giữ bản cũ, lập lại; chưa theo dõi thực thu.
- Chỉ chốt tiền một đợt thuê xác định đủ tháng; thiếu điện, ngày không rõ, vào/trả giữa tháng hoặc đổi khách cùng kỳ bị chặn. Không có engine lịch giá tự động: giá trên form là gợi ý, Admin xác nhận cho từng kỳ.

## Kiểm tra

- 38 unittest pass: bộ 31 cũ và 7 test sửa điện/ảnh hưởng kỳ sau/audit/stale, snapshot giá độc lập tháng, chống trùng, quyền root hủy, giá 0/âm/thiếu, chặn giữa tháng/thiếu điện và render/quyền trang mới.
- flask db check: không schema drift. node --check app/static/js/app.js: hợp lệ.
- Test client trên app local: /login trả HTTP 200; chưa đổi mật khẩu root thật khi test.
- .env, DB và SQLite sidecars bị Git ignore. Chưa commit/push trong lượt này.
- Đã kiểm tra ảnh tĩnh bằng Edge headless: đăng nhập/bảng phòng/form desktop và bố cục 390px với dữ liệu giả từ DB tạm. Ảnh trong instance/ui-*.png, ngoài Git. Edge có viewport tối thiểu ~492px nên bản 390px giới hạn chiều rộng root trong fixture, cùng breakpoint mobile. Chưa kiểm tra tương tác browser end-to-end trên server thật hoặc thiết bị điện thoại.
- Chưa bật Git hook, hosting hoặc lịch backup tự động.

## Chạy tiếp

    python -m flask --app wsgi run --host 127.0.0.1 --port 5000

Mở http://127.0.0.1:5000, đăng nhập root bằng pass bootstrap đã cung cấp rồi đổi pass. Clone mới làm theo README.md để tạo môi trường, .env, migration, root.

## Việc tiếp theo

- Đã triển khai phương án gọn trong BILLING_CORRECTIONS_PROPOSAL.md: cùng kỳ phòng/điện, form preview tạm (không lưu nháp), snapshot chốt, hủy/lập lại khi sai. Phần thực thu, công nợ, điện khác kỳ, chia ngày, lịch giá tự động chưa làm.

- FEES_CONTRACTS_PROPOSAL.md đã được triển khai theo phương án tối giản: chỉ lưu đơn giá/nhắc lịch, không chia ngày hoặc quản lý thực thu. Nếu cần tính phải thu, thiết kế kỳ/snapshot và giao dịch thu tiền riêng trước.

- Người dùng nhập thử phòng/xe/điện trên browser, nhất là điện thoại.
- Người dùng nhập thử hai luồng mới; chưa kiểm tra tương tác browser E2E cho module billing.
- Chốt luồng thay đồng hồ khi cần.
- Trước production: WSGI server, HTTPS/cookie secure, lịch backup ngoài máy, diễn tập restore và rà soát dependencies.

Xem STATUS.md để biết giới hạn chính xác.
