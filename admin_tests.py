import unittest
from main import add_customer_info, delete_customer_info, initial_setup, credential_check
from account_information import AccountInformation
from customer_information import CustomerInformation


class AdminTesting(unittest.TestCase):
    def test_add_customer(self):
        self.assertIsInstance(add_customer_info("test_user", "12345", "Test User", True), AccountInformation)

    def test_credential_check(self):
        self.assertIsInstance(credential_check("test_user", "12345"), CustomerInformation)

    def test_delete_customer(self):
        self.assertTrue(delete_customer_info("test_user"))


if __name__ == '__main__':
    initial_setup()
    unittest.main()
