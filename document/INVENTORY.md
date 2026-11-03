# Danh mục file tự sinh

Sinh bằng `python scripts/update_docs.py`. Không sửa tay.

Danh mục file không phải danh sách chức năng hoàn thành. Xem [STATUS.md](STATUS.md).
Không liệt kê môi trường ảo, dữ liệu runtime và các nhóm file nhạy cảm phổ biến.
Script chỉ ghi đường dẫn, không đọc nội dung file; không thay thế kiểm tra secrets.

```text
.env.example
.gitattributes
.githooks/pre-commit
.gitignore
AGENTS.md
README.md
app/__init__.py
app/auth/.gitkeep
app/auth/__init__.py
app/auth/routes.py
app/electricity/.gitkeep
app/electricity/__init__.py
app/electricity/billing_routes.py
app/electricity/routes.py
app/extensions.py
app/models/.gitkeep
app/models/__init__.py
app/rooms/.gitkeep
app/rooms/__init__.py
app/rooms/routes.py
app/services/.gitkeep
app/services/__init__.py
app/services/billing.py
app/services/contracts.py
app/services/electricity.py
app/services/rooms.py
app/static/css/.gitkeep
app/static/css/app.css
app/static/images/.gitkeep
app/static/images/favicon.svg
app/static/images/residence.svg
app/static/js/.gitkeep
app/static/js/app.js
app/static/vendor/.gitkeep
app/static/vendor/HTMX-LICENSE.txt
app/static/vendor/htmx.min.js
app/templates/auth/.gitkeep
app/templates/auth/accounts.html
app/templates/auth/change_password.html
app/templates/auth/login.html
app/templates/base.html
app/templates/billing/form.html
app/templates/billing/index.html
app/templates/electricity/.gitkeep
app/templates/electricity/correct.html
app/templates/electricity/index.html
app/templates/electricity/reading_meta.html
app/templates/error.html
app/templates/partials/.gitkeep
app/templates/partials/icons.html
app/templates/rooms/.gitkeep
app/templates/rooms/detail.html
app/templates/rooms/form.html
app/templates/rooms/index.html
app/templates/rooms/remove.html
app/templates/rooms/renew.html
backups/.gitkeep
document/ARCHITECTURE.md
document/BILLING_CORRECTIONS_PROPOSAL.md
document/CHANGELOG.md
document/DATA_MODEL.md
document/DECISIONS.md
document/DEVELOPMENT.md
document/FEES_CONTRACTS_PROPOSAL.md
document/HANDOFF.md
document/INVENTORY.md
document/README.md
document/SCOPE.md
document/STATUS.md
document/UI_DESIGN.md
instance/.gitkeep
logs/.gitkeep
migrations/README
migrations/alembic.ini
migrations/env.py
migrations/script.py.mako
migrations/versions/0fecdf9f864b_monthly_bills_and_reading_revisions.py
migrations/versions/a65b2f9c018e_deposit_and_unified_start.py
migrations/versions/b71c430e92ad_tenancy_rent.py
migrations/versions/c83e4d16b2a0_tenancy_electricity_price.py
migrations/versions/d94f512a37b1_reading_price.py
migrations/versions/dd7493777e83_fees_and_contracts.py
migrations/versions/e9329a770fe9_initial_schema.py
requirements-dev.txt
requirements.txt
scripts/update_docs.py
tests/.gitkeep
tests/test_billing.py
tests/test_contracts.py
tests/test_v1.py
wsgi.py
```

Tổng: 91 file (bao gồm file danh mục này).
