import unittest
from sample import User

class TestUser(unittest.TestCase):

    def setUp(self):
        self.u = User.User('login', 'master_password')
    
    def test_instanciate(self):
        self.assertEqual(self.u.login, 'login')
        self.assertEqual(self.u.masterkey, 'a3256259dd4dddff42c0d905c28ba0ea16b9773fb1799cf370f901ca63291b02')
        self.assertEqual(self.u.Crypto.fernet._encryption_key, b'-\xfe\xc0\x95\x98\xaa\x0f\x93\x19$\t\xb66\x87\x80\xd0')
        self.assertEqual(self.u.Crypto.fernet._signing_key, b'\xdd\xfb\x84P*F\x01+\x03^\xb5\x04C\xc5\xaa\xee')
        self.assertEqual(self.u.hash, '7c27501ccf62659a28d8b9b7fb8b756b13261eb4')
        self.assertEqual(self.u.emojish, '😍 😉')

    def test_add_domain(self):
        self.assertTrue(self.u.add_domain('domain.ltd'))
        self.assertFalse(self.u.add_domain('domain.ltd'))
        self.assertTrue(self.u.add_domain('domain2.ltd'))
        self.assertEqual(self.u.get_domains(), ['domain.ltd', 'domain2.ltd'])

    def test_del_domain(self):
        self.assertTrue(self.u.del_domain('domain.ltd'))
        self.assertEqual(self.u.get_domains(), ['domain2.ltd'])
        self.assertFalse(self.u.del_domain('unknown.ltd'))