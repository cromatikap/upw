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
    
class derive_key_from(unittest.TestCase):

    def test_knownHash(self):
        self.assertTrue(Crypto.derive_key_from('masterkey', 'domain.ltd') == 'f9d5d47b84fa29e7aa79ffed83e74ba9acf20ccb06a622b6a824b8a66fd79122')

class hash(unittest.TestCase):

    def test_hash(self):
        self.assertEqual(Crypto.hash('abc'), 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')
        self.assertEqual(Crypto.hash('qwerty'), '65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5')