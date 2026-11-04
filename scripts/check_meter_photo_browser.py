"""Optional browser check: pip install playwright; uses installed Microsoft Edge.

All records/files live in a temporary directory, never the development database.
"""
import sys
import tempfile
import threading
from io import BytesIO
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PIL import Image
from playwright.sync_api import sync_playwright
from werkzeug.serving import make_server

from app import create_app
from app.extensions import db
from app.models import ElectricityReading, MonthlyBill, Photo, Room, Tenancy, User
from app.services.photos import process_pending


def main():
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        app = create_app({"TESTING": True, "SECRET_KEY": "browser-test-only", "SESSION_COOKIE_SECURE": False,
                          "SQLALCHEMY_DATABASE_URI": "sqlite:///" + (root / 'test.sqlite3').as_posix(),
                          "PHOTO_ROOT": str(root / 'uploads')})
        with app.app_context():
            db.create_all()
            user = User(username='root', must_change_password=False, is_root=True)
            user.set_password('BrowserTest123!')
            db.session.add_all([user, Room(code='T101'), Room(code='T102')])
            db.session.commit()
        image = BytesIO()
        Image.new('RGB', (200, 100), 'blue').save(image, 'JPEG')
        server = make_server('127.0.0.1', 0, app, threaded=True)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(channel='msedge', headless=True)
                page = browser.new_page()
                errors = []
                page.on('pageerror', lambda error: errors.append(str(error)))
                base = f'http://127.0.0.1:{server.server_port}'
                page.goto(base + '/login')
                page.locator('[name=username]').fill('root')
                page.locator('[name=password]').fill('BrowserTest123!')
                page.locator('button[type=submit]').click()
                page.goto(base + '/electricity/?period=2026-01')
                page.wait_for_function("document.querySelector('#electricity-form').dataset.photoBound === '1'")
                page.evaluate('window.testPageMarker = 123')
                save_requests = []
                page.on('request', lambda request: save_requests.append(request.post_data_buffer) if request.method == 'POST' and '/electricity/?' in request.url else None)
                payload = {"name": 'meter.jpg', "mimeType": 'image/jpeg', "buffer": image.getvalue()}
                first = page.locator('.reading-row').nth(0)
                second = page.locator('.reading-row').nth(1)
                second.locator('input[type=file]').set_input_files(payload)
                assert second.locator('.photo-preview img').count() == 1
                with app.app_context():
                    assert db.session.query(Photo).count() == 0
                first.locator('.start-value').fill('0')
                first.locator('.end-value').fill('10')
                page.locator('#electricity-form button[type=submit]').click()
                first.locator('.photo-save').wait_for(state='attached')
                assert b'filename=' not in save_requests[-1], 'Unsubmitted row image was sent'
                assert page.evaluate('window.testPageMarker') == 123
                assert second.locator('input[type=file]').evaluate('(input) => input.files.length') == 1
                with app.app_context():
                    assert db.session.query(ElectricityReading).count() == 1
                    assert db.session.query(Photo).count() == 0
                # Drop a real file; still no upload until Save photo.
                first.locator('.photo-drop').evaluate('''(element, bytes) => {
                    const transfer = new DataTransfer();
                    transfer.items.add(new File([new Uint8Array(bytes)], 'meter.jpg', {type:'image/jpeg'}));
                    element.dispatchEvent(new DragEvent('drop', {dataTransfer:transfer, bubbles:true}));
                }''', list(image.getvalue()))
                first.locator('.photo-preview img').wait_for()
                with app.app_context():
                    assert db.session.query(Photo).count() == 0
                first.locator('.photo-save').click()
                first.locator('[data-photo-pending]').wait_for()
                with app.app_context():
                    assert db.session.query(Photo).count() == 1
                    process_pending()
                first.locator('.saved-photos img').wait_for(timeout=15000)
                assert page.evaluate('window.testPageMarker') == 123
                assert second.locator('input[type=file]').evaluate('(input) => input.files.length') == 1
                page.wait_for_function('Boolean(window.bootstrap)', timeout=15000)
                first.locator('.saved-photos .photo-open').click()
                page.locator('#meter-photo-modal.show').wait_for()
                page.evaluate('''() => new Promise(resolve => {
                    const modal = document.querySelector('#meter-photo-modal');
                    if (!bootstrap.Modal.getInstance(modal)._isTransitioning) resolve();
                    else modal.addEventListener('shown.bs.modal', resolve, {once:true});
                })''')
                page.keyboard.press('Escape')
                page.locator('#meter-photo-modal').wait_for(state='hidden')
                second.locator('.start-value').fill('0')
                second.locator('.end-value').fill('30')
                page.locator('#electricity-form button[type=submit]').click()
                second.locator('[data-photo-pending]').wait_for()
                assert page.evaluate('window.testPageMarker') == 123
                with app.app_context():
                    assert db.session.query(ElectricityReading).count() == 2
                    assert db.session.query(Photo).count() == 2
                    process_pending()
                second.locator('.saved-photos img').wait_for(timeout=15000)
                first.locator('input[type=file]').set_input_files(payload)
                first.locator('.photo-save').click()
                first.locator('[data-photo-pending]').wait_for()
                assert first.locator('.saved-photos img').count() == 1
                with app.app_context():
                    assert db.session.query(Photo).count() == 2
                    process_pending()
                first.locator('[data-photo-pending]').wait_for(state='detached', timeout=15000)
                assert first.locator('.saved-photos img').count() == 1
                assert page.locator('#electricity-form button[type=submit]').is_disabled()
                with app.app_context():
                    reading = db.session.scalar(db.select(ElectricityReading).order_by(ElectricityReading.id))
                    tenant = Tenancy(room_id=reading.room_id, tenant_name='Browser fixture')
                    db.session.add(tenant)
                    db.session.flush()
                    db.session.add(MonthlyBill(room_id=reading.room_id, tenancy_id=tenant.id, period=reading.period,
                        tenant_name=tenant.tenant_name, room_code='T101', start_value=0, end_value=10,
                        rent_price=0, water_price=0, service_price=0, electricity_price=0, people_count=1,
                        due_date=date(2026, 1, 31), created_by=reading.created_by))
                    db.session.commit()
                page.goto(base + '/electricity/?period=2026-01')
                assert first.locator('input[type=file]').count() == 0
                assert first.locator('.saved-photos img').count() == 1
                assert second.locator('input[type=file]').count() == 1
                with app.app_context():
                    room = Room(code='T103')
                    db.session.add(room)
                    db.session.flush()
                    room_id = room.id
                    db.session.add(Tenancy(room_id=room.id, tenant_name='Bill picker fixture', contract_start=date(2025, 1, 1),
                        contract_end=date(2027, 1, 1), rent_price=1000, water_price=0, service_price=0, electricity_price=0, payment_day=1))
                    db.session.add(ElectricityReading(room_id=room.id, period='2026-01', start_value=0, end_value=1,
                        created_by=db.session.scalar(db.select(User.id))))
                    db.session.commit()
                page.goto(base + '/bills?period=2026-01')
                assert page.locator('#bill-room option').count() == 3
                assert page.locator('#bill-room option').first.get_attribute('disabled') is not None, page.locator('#bill-room').inner_html()
                page.locator('#bill-room').select_option(str(room_id))
                page.locator('#bill-create').click()
                page.wait_for_url(f'**/rooms/{room_id}/bill?period=2026-01')
                assert 'T103' in page.locator('h1').inner_text()
                # The same room selection works without JavaScript/HTMX.
                plain = browser.new_context(java_script_enabled=False)
                plain.add_cookies(page.context.cookies())
                plain_page = plain.new_page()
                plain_page.goto(base + '/bills?period=2026-01')
                plain_page.locator('#bill-room').select_option(str(room_id))
                plain_page.locator('#bill-create').click()
                plain_page.wait_for_url(f'**/rooms/{room_id}/bill?period=2026-01')
                plain.close()
                assert not errors, errors
                browser.close()
                print('Browser checks passed: photo upload/replacement/modal, locked photo UI, bill room picker with and without JavaScript, no page errors.')
        finally:
            server.shutdown()
            thread.join()
            with app.app_context():
                db.session.remove()
                db.engine.dispose()


if __name__ == '__main__':
    main()
