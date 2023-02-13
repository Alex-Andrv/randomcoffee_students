import unittest

from app.tgbot.utils.Email import Email


class EmailTest(unittest.TestCase):

    def test_valid_mail(self):
        self.assertTrue(Email.is_valid_email("ankitrai326@niuitmo.ru"))
        self.assertTrue(Email.is_valid_email("my.ownsite@niuitmo.ru"))
        self.assertTrue(Email.is_valid_email("28822882@niuitmo.ru"))
        self.assertTrue(Email.is_valid_email("sadas288.22882sdasd@niuitmo.ru"))
        self.assertTrue(Email.is_valid_email("niuitmossss@niuitmo.ru"))

    def test_invalid_mail(self):
        self.assertFalse(Email.is_valid_email("my.ownsite@niuitmo.ru@@@@@"))
        self.assertFalse(Email.is_valid_email("ankitrai326@niuitmo.com"))
        self.assertFalse(Email.is_valid_email("ankitrai326@nuitmo.ru"))
        self.assertFalse(Email.is_valid_email("ankitrai326@itmo.ru"))
        self.assertFalse(Email.is_valid_email("ankitrai326@ifmo.ru"))
        self.assertFalse(Email.is_valid_email("niuit@@mossss@niuitmo.ru"))


if __name__ == '__main__':
    unittest.main()
