# Phí và hợp đồng — phân tích và phạm vi đã triển khai

Phân tích ban đầu: V1.1.3. Người dùng đã yêu cầu triển khai ở V1.1.4. Phạm vi thực tế ghi ở cuối file và STATUS.md; nội dung phân tích dưới đây giữ làm bối cảnh.

## Khoảng trống trước khi triển khai

- Tenancy.started_at/ended_at đang ghi thời điểm hệ thống tạo/kết thúc đợt thuê, không đủ để coi là ngày vào thực tế hoặc ngày hết hạn hợp đồng.
- Chưa có đơn giá nước, phí dịch vụ, lịch đóng tiền, hợp đồng hoặc lịch sử gia hạn/thanh toán.

## Đề xuất tối giản

- Nước: VND/người/tháng; dịch vụ: VND/phòng/tháng. Ví dụ 100.000 và 150.000 chỉ là ví dụ, không tự áp cho dữ liệu thật.
- Tiền lưu số nguyên VND >=0; 0 hợp lệ, khác với để trống/chưa cấu hình. Không dùng float hoặc kiểm tra truthiness làm mất giá trị 0.
- Giá gắn với đợt thuê/điều khoản hợp đồng; giá mặc định cấp phòng nếu thêm chỉ dùng để điền sẵn, không tự thay giá hợp đồng đang chạy.
- Tổng nước = đơn giá x số người tính phí của kỳ. Tổng người gồm khách chính. Cần chốt chính sách thay đổi người hoặc vào/ra giữa tháng; đề xuất ban đầu không tự chia ngày, cho xác nhận số người tính phí từng kỳ.
- Khi có khoản phải thu theo kỳ phải chụp lại đơn giá, số người và số tiền; sửa khách/giá hiện tại không đổi kỳ đã chốt. Chưa triển khai hóa đơn trong lượt phân tích.

## Ngày và hợp đồng

- Ngày vào thực tế, ngày bắt đầu hợp đồng, ngày hết hạn hợp đồng, ngày trả phòng thực tế là các ý nghĩa riêng; không dùng chung created_at hoặc ended_at hệ thống.
- Ngày nghiệp vụ dùng DATE theo Asia/Saigon; thời điểm audit dùng UTC.
- Ngày hết hạn >= ngày bắt đầu; ngày trả thực tế >= ngày vào. Có thể trả sớm hoặc ở quá hạn.
- Hết hạn hợp đồng không tự trả phòng hoặc chuyển phòng thành trống.
- V1 mở rộng nên ưu tiên hợp đồng đã bắt đầu; hợp đồng tương lai cần luồng đặt trước riêng, không tự coi khách đã vào ở.
- Gia hạn giữ nguyên đợt thuê/khách, ghi riêng lịch sử gồm hạn cũ/mới, số tháng, ngày thao tác, Admin và ghi chú.
- Số tháng gia hạn là số nguyên dương. Hạn mới tính từ hạn cũ, không tự từ ngày thao tác. Không gia hạn đợt đã trả phòng; quá hạn phải cảnh báo và xác nhận mốc.
- Cộng tháng theo lịch, không x30 ngày; tháng ngắn lấy ngày hợp lệ cuối tháng, giữ ngày neo để tránh trôi khi gia hạn nhiều lần. Ví dụ neo 31: 31/01/2027 +1 tháng = 28/02/2027; gia hạn tiếp theo trở lại 31/03/2027.
- Chặn bấm gia hạn lặp/giao dịch đồng thời; kiểm tra hạn cũ còn đúng trước khi ghi trong một giao dịch.

## Lịch đóng tiền

- Tách ngày đến hạn định kỳ và ngày thanh toán thực tế.
- Đề xuất ngày đóng hằng tháng 1–31; tháng không có ngày đó dùng ngày cuối tháng, vẫn giữ ngày neo gốc.
- Mỗi kỳ cần ngày đến hạn cụ thể, không chỉ một ngày lặp để suy diễn lịch sử.
- Chưa có ghi nhận thu tiền thì không hiển thị “Đã đóng”, “Còn nợ” như kết quả đã xác minh. Đến hạn chỉ là nhắc lịch.
- Nếu quản lý thu tiền sau này: ghi nhiều lần thu, số tiền >0, ngày thực thu, kỳ/đợt thuê, người ghi; không dùng một ô ngày đóng tiền ghi đè qua từng tháng. Khoản thu 0 không thay thế “không phát sinh phí”.

## Dữ liệu cũ và giao diện

- Migration không giả định ngày tạo record là ngày vào, không biến phí chưa biết thành miễn phí 0. Cho hiển thị “Chưa cập nhật” và bổ sung thủ công.
- Form phòng thêm nhóm hợp đồng/phí khi đang thuê; chi tiết có lịch sử gia hạn; danh sách chỉ thêm hạn hợp đồng/ngày đến hạn nếu cần.
- Ngừng sử dụng phòng có khách phải có thao tác kết thúc đợt thuê rõ ràng, xác nhận ngày trả; không âm thầm coi là đã thanh toán.
- Trường nghiệp vụ bắt buộc áp dụng cho đợt/hợp đồng mới; bản cũ thiếu thông tin cần trạng thái bổ sung thay vì bị gán dữ liệu giả.

## Các lựa chọn lúc phân tích

1. Nước/dịch vụ mặc định mỗi tháng; có chia ngày vào/ra giữa tháng không?
2. Ngày đóng tiền là hạn thanh toán hằng tháng, hay cần quản lý cả giao dịch thực thu?
3. Chỉ lưu hai đơn giá và nhắc lịch, hay mở rộng tính phải thu (khi đó còn cần tiền thuê, giá điện và các quy tắc kỳ tính)?

## Đã triển khai V1.1.4

- Chọn phương án lưu đơn giá + lịch nhắc; chưa chia phí giữa tháng hoặc tính khoản phải thu/thực thu. Dự tính tháng đủ theo người hiện tại được ghi rõ trên giao diện.
- Các ngày và phí nằm trong Tenancy; nullable để không giả dữ liệu cũ. Đợt thuê mới bắt buộc đủ ngày vào/bắt đầu/hết hạn, hai giá và ngày đóng 1–31.
- Lịch đóng là ngày đến hạn tham chiếu theo điều khoản hiện tại của kỳ đang xem, không phải lịch sử nghĩa vụ thanh toán đã chốt. Chưa tạo bảng kỳ thu/snapshot/thanh toán.
- ContractRenewal lưu mỗi lần gia hạn; có bước preview/confirm, cờ xác nhận quá hạn, giữ ngày neo, số tháng 1–120 và version khóa lạc quan.
- Sau khi đã có gia hạn, không sửa trực tiếp ngày bắt đầu/hết hạn từ form phòng. Chưa có luồng sửa sai lịch sử gia hạn.
- Ngày trả thực tế bắt buộc khi đổi khách/ngừng sử dụng; không gán ngày hệ thống cho ngày khách trả. Cùng ngày trả và vào khách mới được phép.
- Migration dd7493777e83 dùng ADD COLUMN có CHECK để không rebuild bảng cha có liên kết trên SQLite; DB local đã backup trước upgrade.
- Chưa có đặt trước tương lai, thay đồng hồ, tiền phòng/điện thành tiền hoặc hóa đơn. Yêu cầu audit/snapshot khi tính tiền sau này vẫn giữ nguyên.

## Yêu cầu thay thế V1.1.5

- Người dùng yêu cầu gộp ngày vào ở và ngày bắt đầu thành Ngày bắt đầu hợp đồng, thay thế quy tắc tách hai ngày ở phân tích cũ.
- Bổ sung tiền cọc theo đợt thuê (có thể 0), chưa quản lý thực thu/hoàn cọc. Xem DATA_MODEL.md và STATUS.md cho hành vi hiện tại.
