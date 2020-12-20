import unittest, sys, os
sys.path.append(os.path.abspath('../sample'))
from sample import upw

class derive_key_from(unittest.TestCase):

    def test_knownHash(self):
        self.assertTrue(upw.derive_key_from('masterkey', 'domain.ltd') == 'f9d5d47b84fa29e7aa79ffed83e74ba9acf20ccb06a622b6a824b8a66fd79122')

class authenticate(unittest.TestCase):

    def test_knownLogin(self):
        user = upw.authenticate('login', 'masterpassword')
        self.assertTrue(user['login'] == 'login' and user['masterkey'] == '8685c92f56bd0762da8a86301523c3dece86b0725c52c545749dd36415ba8d7f')

class hash(unittest.TestCase):

    def test_hash(self):
        self.assertEqual(upw.hash('abc'), 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')
        self.assertEqual(upw.hash('qwerty'), '65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5')

if __name__ == '__main__':
    unittest.main()
