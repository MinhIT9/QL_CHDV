# Hướng dẫn phát triển

## Hiện trạng

Repo mới có sườn. Chưa có lệnh chạy Flask, chưa có DB và chưa cài thư viện. Các file requirements hiện là chỗ giữ danh sách dự kiến; cài chúng chưa tạo ra ứng dụng.

Script tài liệu chỉ cần Python 3.9+ và thư viện chuẩn. Khi triển khai Flask cần chốt phiên bản Python và dependencies riêng.

## Chu trình mỗi thay đổi

1. Đọc `STATUS.md`, `HANDOFF.md` và yêu cầu hiện tại.
2. Thực hiện thay đổi đúng phạm vi.
3. Chạy kiểm tra phù hợp với thay đổi.
4. Cập nhật tiến độ, bàn giao, changelog; ghi quyết định nếu có.
5. Sinh lại danh mục file và kiểm tra:

```powershell
python scripts/update_docs.py
python scripts/update_docs.py --check
```

`INVENTORY.md` được sinh tự động; các tài liệu nghiệp vụ cần dev/agent cập nhật có kiểm chứng theo `AGENTS.md`. Quy tắc này hướng dẫn agent và dev, không phải tiến trình nền tự theo dõi máy tính.

## Tự cập nhật trước commit (tùy chọn)

Repo có `.githooks/pre-commit`. Chưa thay đổi cấu hình Git cục bộ. Muốn bật trong repo này:

```powershell
git config --local core.hooksPath .githooks
```

Hook chạy script sinh danh mục và chặn commit nếu `INVENTORY.md` trong vùng stage chưa khớp kết quả sinh. Khi bị chặn, xem file rồi chạy `git add document/INVENTORY.md` và commit lại. Hook không tự stage file và không tự viết tiến độ chức năng.

Nếu đã có hook riêng, cần ghép quy trình thay vì thay đường dẫn tùy tiện. Môi trường chạy hook cần lệnh `python` trỏ tới Python 3.9+.

## Git và dữ liệu cục bộ

- `.env.example` được commit, `.env` thật bị bỏ qua.
- DB SQLite, WAL/SHM, log, backup, upload, export và môi trường ảo bị bỏ qua.
- Lockfile dependencies và migration tương lai phải commit.
- `.gitignore` không gỡ file đã được Git theo dõi và không thay thế phân quyền/bảo mật.
- Không chọn license thay chủ dự án; chưa có giấy phép phát hành.
