import unittest
from sample import password

class generate(unittest.TestCase):

    def test_passwordFormat(self):
        self.assertTrue(password.generate('masterkey', 'domain.ltd') == 'f9D#d4%B8$fA2^e7')

if __name__ == '__main__':
    unittest.main()
