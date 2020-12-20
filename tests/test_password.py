import unittest
from sample import password

class generate(unittest.TestCase):

    def test_password_format(self):
        self.assertTrue(password.generate('masterkey', 'domain.ltd') == 'f9D#d4%B8$fA2^e7')

class process_letter(unittest.TestCase):

    def test_letter_unchanged(self):
        self.assertEqual(password.process_letter('a', 0), 'a')
        self.assertEqual(password.process_letter('b', 2), 'b')
        self.assertEqual(password.process_letter('c', 6), 'c')

    def test_letter_to_uppercase(self):
        self.assertEqual(password.process_letter('d', 1), 'D')
        self.assertEqual(password.process_letter('e', 3), 'E')
        self.assertEqual(password.process_letter('f', 9), 'F')

class process_digit(unittest.TestCase):

    def test_digit_unchanged(self):
        self.assertEqual(password.process_digit('1', 0), '1')
        self.assertEqual(password.process_digit('2', 2), '2')
        self.assertEqual(password.process_digit('2', 4), '2')
        self.assertEqual(password.process_digit('2', 6), '2')
        self.assertEqual(password.process_digit('3', 8), '3')
        self.assertEqual(password.process_digit('3', 10), '3')
        self.assertEqual(password.process_digit('3', 12), '3')
        self.assertEqual(password.process_digit('3', 14), '3')
        self.assertEqual(password.process_digit('3', 16), '3')

    def test_digit_to_special_char(self):
        self.assertEqual(password.process_digit('1', 1), '#')
        self.assertEqual(password.process_digit('2', 3), '%')
        self.assertEqual(password.process_digit('3', 5), '$')
        self.assertEqual(password.process_digit('4', 7), '^')
        self.assertEqual(password.process_digit('5', 9), '@')
        self.assertEqual(password.process_digit('6', 11), '?')
        self.assertEqual(password.process_digit('7', 13), '!')
        self.assertEqual(password.process_digit('8', 15), '&')
        self.assertEqual(password.process_digit('9', 17), '*')

if __name__ == '__main__':
    unittest.main()
