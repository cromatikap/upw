import unittest, sys, os
sys.path.append(os.path.abspath('../sample'))
import upw

class authenticate(unittest.TestCase):

    def test_knownLogin(self):
        user = upw.authenticate('login', 'masterpassword')
        self.assertTrue(user['login'] == 'login' and user['masterkey'] == '8685c92f56bd0762da8a86301523c3dece86b0725c52c545749dd36415ba8d7f')

class deriveKeyFrom(unittest.TestCase):

    def test_knownHash(self):
        self.assertTrue(upw.deriveKeyFrom('masterkey', 'domain.ltd') == 'f9d5d47b84fa29e7aa79ffed83e74ba9acf20ccb06a622b6a824b8a66fd79122')

if __name__ == '__main__':
    unittest.main()
