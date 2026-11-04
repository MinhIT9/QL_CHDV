import unittest
from types import SimpleNamespace

from app.services.vietqr import payload, transfer_content


class VietQRTests(unittest.TestCase):
    def test_external_known_vectors_include_crc(self):
        # Published vectors: github.com/sunary/vietqr, vietqr_test.go.
        self.assertEqual(payload('970416', '13579', 120000),
                         '00020101021238490010A000000727011900069704160105135790208QRIBFTTA530370454061200005802VN63049A71')
        self.assertEqual(payload('970418', '1234567890'),
                         '00020101021138540010A00000072701240006970418011012345678900208QRIBFTTA53037045802VN6304995B')

    def test_validation_and_stable_bill_content(self):
        for args in [('999999', '123'), ('970416', '../123'), ('970416', '1'*20),
                     ('970416', '123', 0), ('970416', '123', -1), ('970416', '123', 10**13),
                     ('970416', '123', 1.5), ('970416', '123', 1, 'á')]:
            with self.assertRaises(ValueError):
                payload(*args)
        bill = SimpleNamespace(id=12, room_code='L3T', period='2026-11')
        self.assertEqual(transfer_content(bill), 'P12 L3T T112026')
        self.assertIn('01100012345678', payload('970436', '0012345678', 6231000, transfer_content(bill)))
