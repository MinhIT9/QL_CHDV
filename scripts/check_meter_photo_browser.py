"""Optional browser check: pip install playwright zxing-cpp; uses installed Edge.

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
import zxingcpp
from playwright.sync_api import expect, sync_playwright
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
                asset_cache = Path(__file__).resolve().parents[1] / 'exports' / 'browser-assets'
                for suffix, name, content_type in [
                    ('dist/css/bootstrap.min.css', 'bootstrap-5.3.8.min.css', 'text/css'),
                    ('dist/js/bootstrap.bundle.min.js', 'bootstrap-5.3.8.bundle.min.js', 'application/javascript'),
                ]:
                    if (asset_cache / name).is_file():
                        page.route('https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/' + suffix,
                                   lambda route, request, name=name, content_type=content_type: route.fulfill(
                                       path=str(asset_cache / name), content_type=content_type,
                                       headers={'Access-Control-Allow-Origin': '*'}))
                errors = []
                page.on('pageerror', lambda error: errors.append(str(error)))
                base = f'http://127.0.0.1:{server.server_port}'
                page.goto(base + '/login')
                page.locator('[name=username]').fill('root')
                page.locator('[name=password]').fill('BrowserTest123!')
                page.locator('button[type=submit]').click()
                page.goto(base + '/electricity/?period=2026-01')
                expect(page.locator('#electricity-form')).to_have_attribute('data-photo-bound', '1')
                for width in (375, 430):
                    page.set_viewport_size({'width': width, 'height': 844})
                    row = page.locator('.reading-row').first
                    assert row.evaluate('(e) => getComputedStyle(e).display') == 'grid'
                    scroll = page.locator('#electricity-form .table-scroll')
                    scroll.evaluate('(e) => e.scrollLeft = 0')
                    photo = row.locator('.meter-photo-cell').bounding_box()
                    created = row.locator('.meter-created').bounding_box()
                    assert photo['x'] < created['x']
                    assert row.locator('.end-value').is_visible()
                    scroll.evaluate('(e) => e.scrollLeft = e.scrollWidth')
                    assert row.locator('.meter-updated').bounding_box()['x'] < width
                    scroll.evaluate('(e) => e.scrollLeft = 0')
                page.set_viewport_size({'width': 1280, 'height': 900})
                assert page.locator('.reading-row').first.evaluate('(e) => getComputedStyle(e).display') == 'table-row'
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
                assert page.evaluate('() => Boolean(window.bootstrap)')
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
                page.set_viewport_size({'width': 390, 'height': 844})
                page.locator('#electricity-form .table-scroll').evaluate('(e) => e.scrollLeft = 0')
                mobile_row = page.locator('.reading-row').first
                assert mobile_row.locator('.photo-thumb').bounding_box()['width'] == 44
                assert mobile_row.bounding_box()['height'] < 260
                Path('exports').mkdir(exist_ok=True)
                page.screenshot(path='exports/meter-mobile-layout.png', full_page=True)
                page.set_viewport_size({'width': 1280, 'height': 900})

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
                page.set_viewport_size({'width': 390, 'height': 844})
                locked_button = first.locator('button[popovertarget]').first
                panel = first.locator('[popover]')
                expect(panel).not_to_be_visible()
                height = first.bounding_box()['height']
                locked_button.click()
                expect(panel).to_be_visible()
                expect(panel).to_contain_text('hủy phiếu chưa thu')
                assert first.bounding_box()['height'] == height
                assert panel.bounding_box()['x'] >= 0
                assert panel.bounding_box()['x'] + panel.bounding_box()['width'] <= 390
                page.keyboard.press('Escape')
                expect(panel).not_to_be_visible()
                page.set_viewport_size({'width': 1280, 'height': 900})
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
                final = page.locator('[name=final_amount]')
                assert final.input_value() == '1.000 đ'
                final.fill('1234')
                assert page.locator('[name=adjustment_reason]').get_attribute('required') is not None
                page.locator('[name=adjustment_reason]').fill('Browser rounding fixture')
                page.locator('button[name=action][value=preview]').click()
                page.locator('button[name=action][value=confirm]').wait_for()
                assert page.locator('[name=final_amount]').input_value() == '1.234 đ'
                page.locator('button[name=action][value=confirm]').click()
                page.wait_for_url('**/bills?period=2026-01')
                page.goto(base + '/settings/payment')
                page.locator('[name=bank_bin]').select_option('970436')
                page.locator('[name=account_number]').fill('00123456789')
                page.locator('[name=account_name]').fill('DEMO ACCOUNT')
                page.locator('[name=auto_transfer_content]').check()
                page.locator('[name=note]').fill('Ghi mã phòng và tháng thanh toán')
                page.get_by_role('button', name='Lưu thông tin nhận tiền').click()
                expect(page.locator('img[alt="QR nhận tiền hiện tại"]')).to_be_visible()
                page.goto(base + '/bills?period=2026-01')
                with app.app_context():
                    bill = db.session.scalar(db.select(MonthlyBill).where(MonthlyBill.room_id == room_id))
                    bill_id = bill.id
                    assert bill.total == 1234
                page.locator(f'a[href="/bills/{bill_id}"]').click()
                page.wait_for_url(f'**/bills/{bill_id}')
                assert page.locator('.receipt-sheet').is_visible()
                assert page.locator('.receipt-payment img').is_visible()
                qr_response = page.request.get(base + f'/bills/{bill_id}/qr?amount=1')
                decoded = zxingcpp.read_barcode(Image.open(BytesIO(qr_response.body())))
                assert decoded is not None
                assert '54041234' in decoded.text
                assert '011100123456789' in decoded.text
                assert f'P{bill_id} T103 T012026' in decoded.text
                assert page.locator('.receipt-total b').inner_text().startswith('1.234')
                assert page.locator('#sidebar').count() == 0
                page.set_viewport_size({'width': 1000, 'height': 1100})
                exports = Path(__file__).resolve().parents[1] / 'exports'
                exports.mkdir(exist_ok=True)
                page.screenshot(path=str(exports / 'receipt-preview-desktop.png'), full_page=True)
                assert 'Bằng chữ:' not in page.locator('.receipt-sheet').inner_text()
                assert page.locator('.receipt-state').bounding_box()['height'] < 25
                export_requests = []
                def record_export_request(request):
                    export_requests.append(request.method)
                page.on('request', record_export_request)
                page.evaluate("""() => {
                    Object.defineProperty(navigator, 'canShare', {configurable: true, value: () => true});
                    Object.defineProperty(navigator, 'share', {configurable: true, value: async data => {
                        window.sharedImage = {name: data.files[0].name, size: data.files[0].size, type: data.files[0].type};
                    }});
                }""")
                page.locator('#save-receipt').click()
                page.locator('#receipt-image-dialog').wait_for(state='visible')
                page.locator('#share-receipt-image').click()
                assert page.evaluate('window.sharedImage.type') == 'image/png'
                with page.expect_download() as download_info:
                    page.locator('#download-receipt-image').click()
                exported = exports / 'receipt-export-desktop.png'
                download_info.value.save_as(str(exported))
                with Image.open(exported) as png:
                    assert png.width == 1600
                    exported_qr = zxingcpp.read_barcode(png)
                    assert exported_qr is not None
                    assert '54041234' in exported_qr.text
                assert not any(method != 'GET' for method in export_requests), export_requests
                page.remove_listener('request', record_export_request)
                page.locator('#close-receipt-image').click()
                page.set_viewport_size({'width': 390, 'height': 844})
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                qr_crop = page.locator('.receipt-payment img').screenshot()
                assert zxingcpp.read_barcode(Image.open(BytesIO(qr_crop))) is not None
                page.screenshot(path=str(exports / 'receipt-preview-mobile.png'), full_page=True)
                assert page.locator('.receipt-total b').evaluate('(element) => element.scrollWidth <= element.clientWidth')
                page.locator('#save-receipt').click()
                page.locator('#receipt-image-dialog').wait_for(state='visible')
                with page.expect_download() as mobile_download:
                    page.locator('#download-receipt-image').click()
                mobile_download.value.save_as(str(exports / 'receipt-export-mobile.png'))
                with Image.open(exports / 'receipt-export-mobile.png') as png:
                    assert png.width == 1600
                    assert zxingcpp.read_barcode(png) is not None
                page.evaluate("Object.defineProperty(navigator, 'share', {configurable:true, value:async () => { throw new DOMException('cancel', 'AbortError'); }})")
                page.locator('#share-receipt-image').click()
                assert page.locator('#receipt-share-message').inner_text() == ''
                page.locator('#close-receipt-image').click()
                page.evaluate("Object.defineProperty(navigator, 'canShare', {configurable:true, value:() => false})")
                page.locator('.receipt-payment img').evaluate("image => { image.decode = () => Promise.reject(new Error('fixture')); }")
                page.locator('#save-receipt').click()
                expect(page.locator('#receipt-export-message')).to_contain_text('Không tạo được ảnh phiếu')
                expect(page.locator('#save-receipt')).to_be_enabled()
                page.locator('.receipt-payment img').evaluate('image => { delete image.decode; }')
                page.locator('#save-receipt').click()
                page.locator('#receipt-image-dialog').wait_for(state='visible')
                assert not page.locator('#share-receipt-image').is_visible()
                assert page.locator('#download-receipt-image').is_visible()
                page.locator('#close-receipt-image').click()
                page.emulate_media(media='print')
                assert not page.locator('.receipt-toolbar').is_visible()
                page.emulate_media(media='screen')
                page.goto(base + '/settings/payment')
                page.locator('[name=auto_transfer_content]').uncheck()
                page.get_by_role('button', name='Lưu thông tin nhận tiền').click()
                assert not page.locator('[name=auto_transfer_content]').is_checked()
                page.goto(base + f'/bills/{bill_id}')
                assert 'Nội dung:' not in page.locator('.receipt-payment').inner_text()
                without_content = page.request.get(base + f'/bills/{bill_id}/qr')
                decoded_without_content = zxingcpp.read_barcode(Image.open(BytesIO(without_content.body())))
                assert decoded_without_content is not None
                assert '54041234' in decoded_without_content.text
                assert f'P{bill_id} T103 T012026' not in decoded_without_content.text
                page.goto(base + f'/rooms/{room_id}')
                assert page.locator(f'a[href="/bills/{bill_id}"]').count() >= 1
                # Shared input formatting roundtrips through the room form.
                page.goto(base + f'/rooms/{room_id}/edit')
                rent = page.locator('[name=rent_price]')
                rent.fill('')
                rent.press_sequentially('1000000')
                assert rent.input_value() == '1.000.000 đ'
                rent.evaluate('(input) => input.setSelectionRange(0, 1)')
                rent.press('2')
                assert rent.input_value() == '2.000.000 đ'
                rent.fill('1.234.567 đ')
                date_field = page.locator('[name=contract_start]')
                assert date_field.input_value() == '01/01/2025'
                date_field.fill('31/02/2025')
                assert not date_field.evaluate('(input) => input.checkValidity()')
                date_field.fill('')
                date_field.press_sequentially('01012025')
                assert date_field.input_value() == '01/01/2025'
                assert date_field.evaluate('(input) => input.checkValidity()')
                page.get_by_role('button', name='Lưu phòng', exact=True).click()
                page.wait_for_url(f'**/rooms/{room_id}')
                with app.app_context():
                    assert db.session.get(Room, room_id).current_tenancy.rent_price == 1234567
                page.goto(base + '/bills?period=2026-01')
                page.locator(f'a[href="/bills/{bill_id}/edit"]').click()
                # Edit starts from bill snapshot, not the newly changed contract price.
                assert page.locator('[name=rent_price]').input_value() == '1.000 đ'
                page.locator('[data-price-reason]').wait_for(state='hidden', timeout=5000)
                page.locator('[name=payment_day]').fill('6')
                assert not page.locator('[data-price-reason]').is_visible()
                page.locator('[name=final_amount]').fill('2000')
                assert page.locator('[data-price-reason]').is_visible()
                assert page.locator('[name=adjustment_reason]').get_attribute('required') is not None
                assert page.locator('[name=edit_reason]').count() == 0
                assert page.locator('[name=adjustment_reason]').count() == 1
                page.locator('[name=adjustment_reason]').fill('Browser bill correction fixture')
                page.locator('button[name=action][value=preview]').click()
                page.locator('button[name=action][value=confirm]').wait_for()
                assert page.locator('[name=final_amount]').input_value() == '2.000 đ'
                page.set_viewport_size({'width': 1200, 'height': 900})
                assert page.locator('.bill-fields').bounding_box()['x'] < page.locator('.bill-summary').bounding_box()['x']
                page.screenshot(path=str(exports / 'bill-edit-preview.png'), full_page=True)
                page.locator('button[name=action][value=confirm]').click()
                with app.app_context():
                    replacement = db.session.scalar(db.select(MonthlyBill).where(MonthlyBill.room_id == room_id, MonthlyBill.cancelled_at.is_(None)))
                    replacement_id = replacement.id
                    assert replacement.total == 2000
                    assert db.session.get(MonthlyBill, bill_id).cancelled_at is not None
                page.wait_for_url(f'**/bills/{replacement_id}/edit')
                assert page.locator('#bill-change-history').is_visible()
                assert 'Browser bill correction fixture' in page.locator('#bill-change-history').inner_text()
                page.screenshot(path=str(exports / 'bill-change-history.png'), full_page=True)
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
