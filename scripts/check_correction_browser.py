"""Optional Edge QA for correction preview and independent photo upload."""
import sys
import tempfile
import threading
from io import BytesIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PIL import Image
from playwright.sync_api import expect, sync_playwright
from werkzeug.serving import make_server

from app import create_app
from app.extensions import db
from app.models import ElectricityReading, Photo, ReadingRevision, Room, User
from app.services.photos import process_pending


def main():
    with tempfile.TemporaryDirectory() as tmp:
        app = create_app({
            'TESTING': True, 'SECRET_KEY': 'browser-qa', 'SESSION_COOKIE_SECURE': False,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + (Path(tmp) / 'qa.sqlite3').as_posix(),
            'PHOTO_ROOT': str(Path(tmp) / 'uploads'),
        })
        with app.app_context():
            db.create_all()
            user = User(username='qa', is_root=True, must_change_password=False)
            user.set_password('BrowserQa123!')
            room = Room(code='QA101')
            empty_room = Room(code='QA102')
            db.session.add_all([user, room, empty_room])
            db.session.flush()
            reading = ElectricityReading(room_id=room.id, period='2026-01', start_value=0,
                                         end_value=10, created_by=user.id)
            db.session.add(reading)
            db.session.commit()
            reading_id = reading.id
            empty_room_id = empty_room.id
        server = make_server('127.0.0.1', 0, app, threaded=True)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with sync_playwright() as pw:
                browser = pw.chromium.launch(channel='msedge', headless=True)
                page = browser.new_page(viewport={'width': 390, 'height': 844})
                cache = Path('exports/browser-assets')
                for suffix, name, mime in (
                    ('css/bootstrap.min.css', 'bootstrap-5.3.8.min.css', 'text/css'),
                    ('js/bootstrap.bundle.min.js', 'bootstrap-5.3.8.bundle.min.js', 'application/javascript'),
                ):
                    if (cache / name).exists():
                        page.route('https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/' + suffix,
                                   lambda route, request, name=name, mime=mime: route.fulfill(
                                       path=str(cache / name), content_type=mime,
                                       headers={'Access-Control-Allow-Origin': '*'}))
                errors = []
                page.on('pageerror', lambda error: errors.append(str(error)))
                base = f'http://127.0.0.1:{server.server_port}'
                page.goto(base + '/login')
                page.locator('[name=username]').fill('qa')
                page.locator('[name=password]').fill('BrowserQa123!')
                page.locator('button[type=submit]').click()
                image = BytesIO()
                Image.new('RGB', (50, 50), 'blue').save(image, 'PNG')
                page.goto(base + '/electricity/?period=2026-01')
                empty_row = page.locator(f'.reading-row[data-room-id="{empty_room_id}"]')
                empty_row.locator('input[type=file]').set_input_files({
                    'name': 'before-reading.png', 'mimeType': 'image/png', 'buffer': image.getvalue(),
                })
                empty_row.locator('.photo-save').click()
                expect(empty_row.locator('.photo-message')).to_have_text('Đã nhận ảnh.')
                with app.app_context():
                    assert db.session.scalar(db.select(ElectricityReading.id).where(ElectricityReading.room_id == empty_room_id)) is None
                    draft_id = db.session.scalar(db.select(Photo.id).where(Photo.room_id == empty_room_id))
                    assert draft_id is not None
                page.reload()
                expect(empty_row.locator('[data-photo-pending]')).to_be_visible()
                with app.app_context():
                    process_pending()
                expect(empty_row.locator('.saved-photos img')).to_be_visible(timeout=15000)
                page.screenshot(path='exports/meter-before-reading.png', full_page=True)
                empty_row.locator('.start-value').fill('0')
                empty_row.locator('.end-value').fill('20')
                page.locator('#electricity-form button[type=submit]').click()
                expect(empty_row.locator('.meter-status')).to_contain_text('Đã lưu')
                with app.app_context():
                    photo = db.session.get(Photo, draft_id)
                    assert photo.room_id is None and photo.reading_id is not None
                    assert db.session.get(ElectricityReading, photo.reading_id).end_value == 20
                path = f'/electricity/{reading_id}/correct'
                page.goto(base + path)
                form = page.locator('#meter-correction-form')
                start, end = form.locator('[name=start_value]'), form.locator('[name=end_value]')
                assert abs(start.bounding_box()['y'] - end.bounding_box()['y']) < 2
                start.fill('')
                end.fill('')
                page.locator('.meter-photo-widget input[type=file]').set_input_files({
                    'name': 'qa.png', 'mimeType': 'image/png', 'buffer': image.getvalue(),
                })
                page.locator('.photo-save').click()
                expect(page.locator('.photo-message')).to_have_text('Đã nhận ảnh.')
                with app.app_context():
                    assert db.session.scalar(db.select(db.func.count()).select_from(Photo).where(Photo.reading_id == reading_id)) == 1
                    assert db.session.get(ElectricityReading, reading_id).end_value == 10
                start.fill('0')
                end.fill('15')
                form.locator('[name=reason]').fill('QA correction')
                page.evaluate('window.correctionMarker = 1')
                form.locator('button[type=submit]').click()
                dialog = page.locator('#meter-correction-preview')
                expect(dialog).to_be_visible()
                assert page.evaluate('window.correctionMarker') == 1
                with app.app_context():
                    assert db.session.get(ElectricityReading, reading_id).end_value == 10
                page.screenshot(path='exports/correction-mobile-preview.png', full_page=True)
                dialog.get_by_role('button', name='Nhập lại').click()
                expect(dialog).not_to_be_visible()
                expect(end).to_have_value('15')
                form.locator('button[type=submit]').click()
                expect(dialog).to_be_visible()
                dialog.get_by_role('button', name='Xác nhận sửa').click()
                expect(page.locator('.alert-success')).to_be_visible()
                with app.app_context():
                    assert db.session.get(ElectricityReading, reading_id).end_value == 15
                    assert db.session.scalar(db.select(db.func.count()).select_from(ReadingRevision)) == 1
                assert not errors, errors
                browser.close()
            print('Correction browser QA passed: two inputs, photo-only, preview/cancel/confirm.')
        finally:
            server.shutdown()
            thread.join()
            with app.app_context():
                db.session.remove()
                db.engine.dispose()


if __name__ == '__main__':
    main()
