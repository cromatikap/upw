import unittest
from sample import Crypto

class TestCrypto(unittest.TestCase):

    def setUp(self):
        self.c = Crypto.Crypto('password')

    def test_instanciate(self):
        self.assertEqual(self.c.fernet._encryption_key, b'x<\xe8\x95\x8f5j\x83\x1dr\x05\xaaU\xc3%\x14')
        self.assertEqual(self.c.fernet._signing_key, b"\x06\xa7\x89\xdb*\xb9\xbfO\xc2\x17)'rT\x06\x83")
    
    def test_encrypt_and_decrypt(self):
        encrypted = self.c.encrypt({"domain": []})
        self.assertEqual(self.c.decrypt(encrypted), {"domain": []})