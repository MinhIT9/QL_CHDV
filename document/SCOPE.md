# Phạm vi V1

V1.8.0 mở sửa phiếu tiền chưa thu cho root/Admin: preview/xác nhận/lý do, tạo bản thay thế và giữ nguyên bản cũ; phiếu đã thu/hủy không sửa. Giao diện toàn web dùng tiền nhóm dấu chấm + đ, ngày dd/mm/yyyy, giờ UTC+7; lưu trữ vẫn số nguyên/UTC. Các mô tả V1 cũ bên dưới là mốc phạm vi trước khi bổ sung này.

V1.4.2: một ảnh công tơ mỗi ID chốt điện; lưu ảnh mới thay ảnh cũ sau nén thành công. Phiếu tiền hiệu lực khóa thêm/thay ảnh cho Root/Admin, kể cả ảnh đang trống. Chờ xử lý ảnh xong mới chốt phiếu. Ảnh vẫn không bắt buộc, ảnh hợp đồng không đổi.

V1.4.0 thay yêu cầu bắt buộc ảnh điện trước đây: chốt/sửa được phép không ảnh, bổ sung ngay trong bảng; kéo thả chọn trước, lưu mới upload, progress và tự hiện thumbnail/modal không reload. Giữ worker/quyền xem riêng tư, không đổi DB. Ảnh hợp đồng vẫn tùy chọn.

V1.3.0: ảnh hợp đồng tùy chọn theo đợt thuê, ảnh điện bắt buộc khi chốt/sửa số mới; bổ sung ảnh lịch sử. Upload JPEG/PNG/WebP, worker nền nén WebP và xóa gốc tạm; ảnh chỉ xem qua đăng nhập. Không OCR, HEIC/PDF, xóa ảnh hoặc lưu ảnh gốc dài hạn. Worker CLI/systemd cùng project, không thêm dịch vụ hàng đợi ngoài. Xem PHOTOS.md.

V1.1.14: xác nhận thu đủ từng phiếu, ngày/người/số tiền và root hoàn tác có lịch sử; phiếu đã thu xuống dưới. Bảng Phòng gọn, lọc thu theo tháng, chế độ đầy đủ. Chưa thu một phần/hoàn tiền tự động/đối soát ngân hàng; không thêm công nợ phức tạp.

V1.1.11 thêm ngày giờ chốt/cập nhật lần cuối và tự tính tiền điện trên bảng. Không tự tạo phiếu, không đổi chức năng thực thu; tiền trước chốt phiếu chỉ là dự tính theo giá lưu (hoặc giá hiện tại có nhãn khi legacy chưa biết).

V1.1.10 bổ sung giá điện trong phòng/đợt thuê. Giá điện/nước/phòng mới gợi ý cho phiếu lập sau; phiếu đã chốt giữ nguyên, form mở trước thay đổi cần tải lại. Không tự tra giá theo lịch tháng khi lập bù.

## Mở rộng V1.1.9

- Sửa số điện có preview, lý do và lịch sử; đồng bộ đầu kỳ kế tiếp khi cần. Phiếu tiền hiệu lực khóa các kỳ bị ảnh hưởng cho đến khi root hủy có lý do.
- Chốt tiền theo tháng lưu snapshot giá/người/điện; một phiếu hiệu lực/phòng/kỳ. Giá từng phiếu độc lập các tháng, không tự đổi giá hợp đồng.
- Giới hạn triển khai gọn: phòng/điện cùng tháng và một khách đủ tháng. Chưa thực thu/công nợ/chia ngày/lịch giá tự động; không cộng cọc vào phiếu.

## Mục tiêu

Quản lý CHDV ban đầu khoảng 7 phòng, một Admin, ưu tiên bảng và thao tác nhập nhanh. Không có dashboard biểu đồ, quản lý tiền hoặc báo cáo trong V1.

## Năm màn hình

1. Đăng nhập Admin bằng tài khoản và mật khẩu.
2. Danh sách phòng: mã, trạng thái, khách chính, số người, người ở cùng, xe và điện theo kỳ.
3. Thêm/sửa phòng: thông tin phòng và khách, danh sách người ở cùng, nhiều biển số.
4. Chốt điện: chọn kỳ, nhập chỉ số cuối, hiển thị đầu kỳ và tiêu thụ.
5. Chi tiết phòng: thông tin hiện tại và lịch sử điện.

## Quy tắc đã nêu

- Mã phòng duy nhất; một phòng có nhiều người ở cùng và nhiều xe.
- Chỉ Admin được thêm/sửa/xóa phòng.
- Phòng có lịch sử được chuyển ngừng sử dụng thay vì xóa vĩnh viễn.
- Tiêu thụ = chỉ số cuối - chỉ số đầu.
- Đầu kỳ lấy từ cuối kỳ trước; lần đầu được nhập thủ công.
- Không chấp nhận cuối kỳ nhỏ hơn đầu kỳ. Thay đồng hồ là trường hợp riêng.
- Giữ lịch sử từng kỳ, không ghi đè lịch sử cũ.

## Quy tắc đã chọn khi triển khai V1 (2026-11-02)

- Ba trạng thái: trống, đang thuê, ngừng sử dụng.
- Số người tự tính từ khách chính và người ở cùng.
- Lưu đợt thuê để không mất khách cũ khi đổi khách.
- Một bản chốt cho mỗi phòng/kỳ; V1 chưa mở sửa/xóa bản chốt, chưa có audit điều chỉnh.
- Cho lưu một phần danh sách phòng; phòng trống vẫn được ghi điện.
- Khi thiếu kỳ trước, yêu cầu xử lý rõ thay vì coi tiêu thụ nhiều tháng là một tháng.
- Thay đồng hồ tạm hoãn trong V1; không chèn lùi khi đã có kỳ sau.
- Chỉ số điện nguyên kWh. Người/xe mỗi dòng; số người tự tính; đợt thuê giữ khách cũ.
- Root quản lý tài khoản; tài khoản mới và root bootstrap bắt đổi pass lần đầu, ít nhất 8 ký tự.

Trạng thái và giới hạn thực tế xem `STATUS.md`; quyết định xem `DECISIONS.md`.

## Mở rộng đã triển khai — V1.1.4

- Đơn giá nước/người/tháng và dịch vụ/phòng/tháng theo đợt thuê; cho phép 0. Không tự áp giá ví dụ cho dữ liệu cũ.
- Ngày vào thực tế, bắt đầu/hết hạn hợp đồng, trả phòng thực tế; lịch đóng tiền ngày 1–31 hằng tháng, tháng ngắn lấy ngày cuối tháng.
- Gia hạn hợp đồng đang thuê, 1–120 tháng từ hạn cũ; giữ ngày neo, xem trước/xác nhận, lịch sử Admin/thời điểm/hạn cũ-mới; chặn stale form và ghi đồng thời.
- Hợp đồng hết hạn không tự trả phòng. Đổi khách/ngừng sử dụng có khách phải xác nhận ngày trả thực tế.
- Chỉ lưu đơn giá và lịch nhắc; dự tính tháng đủ theo người hiện tại không phải hóa đơn. Chưa chia ngày, chốt số người tính phí, snapshot khoản phải thu hoặc ghi nhận thực thu.

## Điều chỉnh V1.1.5

- Ngày vào ở và ngày bắt đầu gộp thành Ngày bắt đầu hợp đồng; không nhập hai ngày độc lập.
- Tiền cọc theo đợt thuê, cho phép 0; hiển thị trong bảng/form/chi tiết/lịch sử, không tính vào phí tháng và chưa quản lý thực thu/hoàn cọc.

## Điều chỉnh V1.1.6

- Tiền phòng/tháng theo đợt thuê, cho phép 0, hiển thị form/bảng/chi tiết/lịch sử. Tổng dự tính gồm phòng+nước+dịch vụ, không gồm điện/cọc; chưa chia ngày hoặc tạo hóa đơn.

## V1.9.2 — Quyền sửa điện và ảnh công tơ

Admin và root được hủy phiếu chưa thu với lý do để mở khóa sửa điện/ảnh. Phiếu đã thu vẫn chặn hủy; chỉ root có quyền hoàn tác ghi nhận thu. Các mô tả trước đây yêu cầu root hủy cả phiếu chưa thu được thay bằng quy tắc này. Link sửa điện và ô chọn/thay ảnh luôn hiện; còn phiếu hiệu lực thì service từ chối lưu với thông báo cần hủy trước. Bảo toàn kiểm tra kỳ sau, serializing ghi SQLite và snapshot phiếu cũ. Không thay schema.
