# Tiền và ngày giờ dùng chung — V1.8.0

## Python

app/utils/formatting.py đăng ký vnd, money_input, business_date, date_input, local_date, local_datetime và period_label cho Jinja. Dùng parse_money cho tiền; không dùng cho số lượng hoặc STK. Chấp nhận 1000000, 1.000.000 hoặc 1.000.000 đ; từ chối số âm, lẻ, dấu phẩy, nhóm sai và vượt giới hạn. Blank giữ None, 0 là giá trị hợp lệ. Giá thường giữ giới hạn int32, số cuối phiếu int64.

Ngày dùng read_date/parse_date: dd/mm/yyyy trên UI, ISO vẫn chấp nhận cho giao thức cũ. Business date không đổi múi giờ; timestamp naive trong DB được hiểu UTC rồi chuyển UTC+7. local_today/current_period dùng cùng múi giờ Việt Nam. Không thay dữ liệu timestamps cũ hoặc timezone hệ điều hành.

## Trình duyệt

Nạp formats.js trước app.js. Thêm data-money/inputmode=numeric cho giá hoặc tiền và filter money_input cho value; giữ max để validate. Không áp cho STK, mã phòng, số người hoặc kWh. Thêm data-date/inputmode=numeric với placeholder dd/mm/yyyy và filter date_input cho ngày. Form text không phụ thuộc định dạng date picker của hệ điều hành; chưa thêm lịch popup.

AppFormat.money dùng BigInt, moneyDigits đọc chuỗi đã nhóm; không dùng parseFloat/Number để tính tiền. Enhancement được gọi lại khi HTMX thay DOM, không gắn listener lặp. Server luôn kiểm tra lại, form không JS vẫn gửi được giá/ngày định dạng Việt Nam. Hidden values/URL giữ định dạng canonical để không phá giao thức.

## Sửa phiếu

/bills/<id>/edit chỉ sửa phiếu chưa thu/còn hiệu lực. Dùng snapshot gốc và stamp chống form cũ, không suy ra giá từ hợp đồng hiện tại. Xem trước không ghi DB. Xác nhận tạo ID mới, giữ bản cũ hủy và ghi lý do/actor/time/ID thay thế; mọi bước chung transaction, rollback khi lỗi. Số điện muốn sửa vẫn theo luồng riêng. Phiếu đã thu phải hoàn tác thu theo quyền root trước khi có thể sửa.

## Kiểm tra

85 unittest đạt; timezone qua ranh giới ngày/tháng, leap day, tiền 0/thiếu/int64, reject format sai, snapshot/paid/stale/repeat/rollback được kiểm tra. Edge QA trong scripts/check_meter_photo_browser.py dùng dữ liệu giả, kiểm tra nhập/lưu tiền/ngày và sửa phiếu. Không thao tác dữ liệu thật hoặc VPS trong QA.
