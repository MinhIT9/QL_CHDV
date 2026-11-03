# Sửa điện và chốt tiền theo kỳ — phân tích và triển khai

Ngày: 2026-11-03. Phiên bản hội thoại: V1.1.8. Người dùng yêu cầu phân tích, chưa code chức năng.

## Hiện trạng đã đối chiếu code

- ElectricityReading chỉ lưu chỉ số và kỳ, không có đơn giá điện hoặc tiền điện. Đã lưu thì không sửa/ghi đè qua giao diện.
- monthly_total lấy giá phòng/nước/dịch vụ và số người hiện tại; chưa phải bản chốt tháng, không có snapshot lịch sử tiền.
- Chưa có phiếu tính tiền theo kỳ, điều chỉnh, thanh toán hoặc công nợ. Thay giá hiện tại chưa thể đại diện cho giá từng tháng.

## Sửa chỉ số nhập sai

- Chưa lưu: sửa ngay trên bảng, hiển thị tiêu thụ; cảnh báo tăng bất thường chỉ là cảnh báo, không chặn mức sử dụng hợp lệ.
- Đã lưu nhưng chưa chốt tiền: đề xuất sửa có revision (trước/sau, lý do bắt buộc, Admin, thời điểm), xem trước ảnh hưởng trước khi xác nhận.
- Nếu kỳ sau đã ghi: cuối kỳ vừa sửa là đầu kỳ sau. Giữ số đọc cuối thực tế của kỳ sau, tính lại tiêu thụ kỳ sau; không cộng/trừ hàng loạt các số đọc cuối của những kỳ sau nữa. Kiểm tra toàn chuỗi liên quan; nếu cuối mới vượt cuối kỳ sau hoặc dưới đầu kỳ thì từ chối và yêu cầu đối chiếu số đọc.
- Ví dụ: đầu tháng 11 =1250, cuối nhập1350 nhưng đúng1300; tháng 11 giảm100 xuống50 kWh. Tháng12 đã đọc1400 thì đầu tháng12 sửa1350 thành1300, tiêu thụ tăng50 lên100 kWh. Tháng1 không đổi nếu cuối tháng12 vẫn1400.
- Nếu đã chốt tiền: không sửa âm thầm phiếu đã chốt. Phiếu chưa thu có thể lập bản thay thế, giữ bản cũ và liên kết; phiếu đã thu dùng khoản điều chỉnh cộng/trừ có tham chiếu và không đổi lịch sử thực thu.
- Chênh lệch tính theo đơn giá snapshot của từng kỳ chịu ảnh hưởng, không dùng giá hiện tại; giảm/tăng kWh hai tháng không chắc triệt tiêu tiền nếu giá khác nhau.
- Thay đồng hồ/tua số là nghiệp vụ riêng, không bỏ điều kiện cuối>=đầu để sửa sai.
- Gợi ý quyền: Admin xử lý nháp/chưa chốt tiền; điều chỉnh kỳ đã chốt/đã thu giao root. Đây là đề xuất chưa chốt.

## Tách chốt điện và chốt tiền

- Chốt điện xác nhận số đọc/tiêu thụ. Chốt tiền xác nhận khách, kỳ, đơn giá và các khoản phải thu. Hai trạng thái độc lập.
- Luồng đề xuất: nhập/lưu điện → tạo phiếu nháp → kiểm tra dữ liệu → xem trước → chốt tiền → ghi nhận thu (bước sau nếu được yêu cầu).
- Snapshot khi chốt: room/tenancy và tên khách, kỳ tính tiền, kỳ/ngày đầu-cuối điện, chỉ số và revision dùng, kWh, đơn giá điện, tiền phòng, giá nước/số người tính phí, dịch vụ, các khoản điều chỉnh, hạn thanh toán, người/thời điểm chốt.
- Giá/số người có hiệu lực trong kỳ được điền mặc định, cho kiểm tra số người tính phí khi nháp. Không đọc lại người/giá hiện tại để tính phiếu đã chốt.
- Giá thay đổi cần mốc kỳ áp dụng. Không sửa giá tháng11 khi cấu hình giá tháng12. Có thể lấy giá hiện hành làm mặc định cho nháp, nhưng phải resolve đúng hiệu lực; không sao chép mù giá cũ nếu có thay đổi từ kỳ mới.
- Số tiền VND nguyên, tính ở server. NULL/chưa cấu hình không được coi là0. Chốt bị chặn nếu thiếu giá hoặc số điện cần thiết; miễn phí thì nhập0 rõ ràng.
- Tiền cọc nằm riêng, không tự cộng mỗi tháng hoặc bù tiền thuê.

## Xác định tháng tính tiền và kỳ điện

- Không mặc định nhãn tháng của điện bằng nhãn tháng thu tiền. Ví dụ nếu tiền phòng trả đầu tháng, phiếu tháng12 có thể gồm phòng/nước/dịch vụ tháng12 và điện tiêu thụ tháng11.
- Nếu thu tất cả cuối tháng, có thể cùng một nhãn tháng. Cần người dùng chọn trước triển khai.
- Giao diện phải ghi rõ kỳ tiền phòng, kỳ điện và ngày đến hạn. Không chốt điện tháng chưa có số đọc cuối bằng0 rồi coi như đã hoàn tất.
- Lần đầu vận hành, vào/ra giữa tháng và đổi khách cần mốc đọc bàn giao. Với đổi khách cùng phòng/tháng, dữ liệu điện phòng/tháng hiện tại không đủ chia chính xác: cần các đoạn số đọc theo đợt thuê hoặc xác nhận phân bổ, không tự gán toàn bộ cho khách mới.
- Phòng trống vẫn có điện nhưng không tự sinh phải thu cho khách không tồn tại.
- Chưa tự chia ngày ở V1; trước khi tính tiền cần chọn tính đủ tháng hay số ngày và cách làm tròn. Đây là vấn đề còn mở.

## Ràng buộc và dữ liệu đề xuất

- Phân biệt trạng thái tài liệu (nháp/đã chốt/bị thay thế) và thanh toán (chưa thu/thu một phần/đủ). Chốt không có nghĩa đã thu.
- Một phiếu gốc có hiệu lực mỗi đợt thuê/kỳ/loại kỳ đã định; phiếu thay thế/điều chỉnh có quan hệ tới gốc, không cho tạo trùng vì bấm hai lần.
- Revision số điện và các cập nhật đầu kỳ kế tiếp phải trong cùng giao dịch, kiểm tra version để chặn concurrent edit. Chốt phiếu kiểm tra reading revision chưa bị thay đổi sau khi xem trước.
- Không sửa/xóa phiếu đã thu; không xóa giao dịch thu thật khi điều chỉnh tiền. Tín dụng thu thừa được ghi rõ để hoàn hoặc cấn trừ có xác nhận.
- Dự kiến ReadingRevision, MonthlyStatement/StatementLine, StatementAdjustment; bảng hiệu lực giá khi cần lịch giá. Payment/Allocation chỉ thêm khi triển khai thực thu.
- Không dùng một cột tổng tiền trên Room để thay thế lịch sử các kỳ.

## Phạm vi nên làm tiếp

1. Sửa điện có revision và kiểm tra kỳ sau.
2. Đơn giá điện có hiệu lực theo kỳ; phiếu nháp/chốt tiền lưu snapshot.
3. Theo dõi thu và điều chỉnh tiền đã thu khi được yêu cầu.

Cần chốt cách thu đầu/cuối tháng và cách tính khi vào/ra giữa tháng trước khi code phần chốt tiền. Chưa sửa schema, backend, giao diện hoặc DB trong lượt phân tích này.

## Phạm vi đã triển khai V1.1.9

Người dùng yêu cầu nâng cấp, ưu tiên code gọn. Triển khai revision số điện, preview ảnh hưởng kỳ sau, chốt snapshot từng tháng, chống stale/trùng và root hủy phiếu có audit. Dùng cùng kỳ phòng/điện; giá Admin xác nhận trên từng phiếu, chưa lịch giá tự động. Không thực thu, công nợ, chia ngày hoặc điện khác kỳ. Kỳ vào/trả/đổi khách giữa tháng bị chặn. Phần khái niệm nháp dài hạn/thay thế/điều chỉnh đã thu ở trên vẫn là thiết kế tương lai, chưa phải chức năng.
