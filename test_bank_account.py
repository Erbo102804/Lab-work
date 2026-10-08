"""Модульные тесты для системы банковских счетов."""

import unittest

from bank_account import BankAccount, InsufficientFundsError


class TestAccountCreation(unittest.TestCase):
    def test_stores_owner_and_number(self):
        account = BankAccount("Иван Иванов", "KG-0001")
        self.assertEqual(account.owner, "Иван Иванов")
        self.assertEqual(account.account_number, "KG-0001")

    def test_initial_balance_is_zero(self):
        account = BankAccount("Иван Иванов", "KG-0001")
        self.assertEqual(account.get_balance(), 0)
        self.assertEqual(account.balance, 0)

    def test_new_account_is_empty(self):
        self.assertTrue(BankAccount("Иван Иванов", "KG-0001").is_empty())

    def test_invalid_owner(self):
        for owner in ("", "   ", None, 123):
            with self.subTest(owner=owner):
                with self.assertRaises(ValueError):
                    BankAccount(owner, "KG-0001")

    def test_invalid_account_number(self):
        for number in ("", "   ", None, 42):
            with self.subTest(number=number):
                with self.assertRaises(ValueError):
                    BankAccount("Иван Иванов", number)

    def test_attributes_are_read_only(self):
        account = BankAccount("Иван Иванов", "KG-0001")
        with self.assertRaises(AttributeError):
            account.balance = 1000
        with self.assertRaises(AttributeError):
            account.owner = "Пётр"
        with self.assertRaises(AttributeError):
            account.account_number = "KG-9999"


class TestDeposit(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount("Иван Иванов", "KG-0001")

    def test_deposit_increases_balance(self):
        self.account.deposit(100)
        self.assertEqual(self.account.get_balance(), 100)

    def test_deposit_returns_new_balance(self):
        self.assertEqual(self.account.deposit(250), 250)

    def test_multiple_deposits(self):
        self.account.deposit(100)
        self.account.deposit(50)
        self.assertEqual(self.account.get_balance(), 150)

    def test_deposit_float(self):
        self.account.deposit(10.5)
        self.assertAlmostEqual(self.account.get_balance(), 10.5)

    def test_deposit_makes_account_not_empty(self):
        self.account.deposit(1)
        self.assertFalse(self.account.is_empty())

    def test_deposit_zero_raises(self):
        with self.assertRaises(ValueError):
            self.account.deposit(0)
        self.assertEqual(self.account.get_balance(), 0)

    def test_deposit_negative_raises(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-100)
        self.assertEqual(self.account.get_balance(), 0)

    def test_deposit_non_finite_raises(self):
        for amount in (float("inf"), float("-inf"), float("nan")):
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    self.account.deposit(amount)
        self.assertEqual(self.account.get_balance(), 0)

    def test_deposit_wrong_type_raises(self):
        for amount in ("100", None, [100], True):
            with self.subTest(amount=amount):
                with self.assertRaises(TypeError):
                    self.account.deposit(amount)
        self.assertEqual(self.account.get_balance(), 0)


class TestWithdraw(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount("Иван Иванов", "KG-0001")
        self.account.deposit(500)

    def test_withdraw_decreases_balance(self):
        self.account.withdraw(200)
        self.assertEqual(self.account.get_balance(), 300)

    def test_withdraw_returns_new_balance(self):
        self.assertEqual(self.account.withdraw(100), 400)

    def test_withdraw_entire_balance(self):
        self.account.withdraw(500)
        self.assertEqual(self.account.get_balance(), 0)
        self.assertTrue(self.account.is_empty())

    def test_withdraw_more_than_balance_raises(self):
        with self.assertRaises(InsufficientFundsError):
            self.account.withdraw(501)
        self.assertEqual(self.account.get_balance(), 500)

    def test_withdraw_from_empty_account_raises(self):
        empty = BankAccount("Пётр Петров", "KG-0002")
        with self.assertRaises(InsufficientFundsError):
            empty.withdraw(1)
        self.assertEqual(empty.get_balance(), 0)

    def test_withdraw_negative_raises(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(-50)
        self.assertEqual(self.account.get_balance(), 500)

    def test_withdraw_zero_raises(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(0)
        self.assertEqual(self.account.get_balance(), 500)

    def test_withdraw_wrong_type_raises(self):
        with self.assertRaises(TypeError):
            self.account.withdraw("100")
        self.assertEqual(self.account.get_balance(), 500)


class TestTransfer(unittest.TestCase):
    def setUp(self):
        self.sender = BankAccount("Иван Иванов", "KG-0001")
        self.receiver = BankAccount("Пётр Петров", "KG-0002")
        self.sender.deposit(1000)
        self.receiver.deposit(200)

    def assertBalancesUnchanged(self):
        self.assertEqual(self.sender.get_balance(), 1000)
        self.assertEqual(self.receiver.get_balance(), 200)

    def test_successful_transfer(self):
        self.sender.transfer(self.receiver, 300)
        self.assertEqual(self.sender.get_balance(), 700)
        self.assertEqual(self.receiver.get_balance(), 500)

    def test_transfer_changes_are_equal(self):
        sender_before = self.sender.get_balance()
        receiver_before = self.receiver.get_balance()
        self.sender.transfer(self.receiver, 450)
        decrease = sender_before - self.sender.get_balance()
        increase = self.receiver.get_balance() - receiver_before
        self.assertEqual(decrease, 450)
        self.assertEqual(decrease, increase)

    def test_total_money_is_preserved(self):
        total = self.sender.get_balance() + self.receiver.get_balance()
        self.sender.transfer(self.receiver, 123)
        self.assertEqual(
            self.sender.get_balance() + self.receiver.get_balance(), total
        )

    def test_transfer_entire_balance(self):
        self.sender.transfer(self.receiver, 1000)
        self.assertTrue(self.sender.is_empty())
        self.assertEqual(self.receiver.get_balance(), 1200)

    def test_transfer_insufficient_funds(self):
        with self.assertRaises(InsufficientFundsError):
            self.sender.transfer(self.receiver, 1001)
        self.assertBalancesUnchanged()

    def test_transfer_negative_amount(self):
        with self.assertRaises(ValueError):
            self.sender.transfer(self.receiver, -100)
        self.assertBalancesUnchanged()

    def test_transfer_zero_amount(self):
        with self.assertRaises(ValueError):
            self.sender.transfer(self.receiver, 0)
        self.assertBalancesUnchanged()

    def test_transfer_wrong_amount_type(self):
        with self.assertRaises(TypeError):
            self.sender.transfer(self.receiver, "100")
        self.assertBalancesUnchanged()

    def test_transfer_to_non_account(self):
        with self.assertRaises(TypeError):
            self.sender.transfer("KG-0002", 100)
        self.assertEqual(self.sender.get_balance(), 1000)

    def test_transfer_to_self(self):
        with self.assertRaises(ValueError):
            self.sender.transfer(self.sender, 100)
        self.assertEqual(self.sender.get_balance(), 1000)

    def test_transfer_back_and_forth(self):
        self.sender.transfer(self.receiver, 300)
        self.receiver.transfer(self.sender, 100)
        self.assertEqual(self.sender.get_balance(), 800)
        self.assertEqual(self.receiver.get_balance(), 400)


class TestBalanceAndEmptiness(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount("Иван Иванов", "KG-0001")

    def test_balance_after_sequence_of_operations(self):
        other = BankAccount("Пётр Петров", "KG-0002")
        self.account.deposit(1000)
        self.account.withdraw(250)
        self.account.deposit(50)
        self.account.transfer(other, 300)
        self.assertEqual(self.account.get_balance(), 500)
        self.assertEqual(other.get_balance(), 300)

    def test_balance_unchanged_after_failed_operation(self):
        self.account.deposit(100)
        with self.assertRaises(InsufficientFundsError):
            self.account.withdraw(1000)
        self.assertEqual(self.account.get_balance(), 100)

    def test_is_empty_true_for_zero_balance(self):
        self.assertTrue(self.account.is_empty())

    def test_is_empty_false_for_positive_balance(self):
        self.account.deposit(0.01)
        self.assertFalse(self.account.is_empty())

    def test_is_empty_after_withdrawing_everything(self):
        self.account.deposit(300)
        self.account.withdraw(300)
        self.assertTrue(self.account.is_empty())


if __name__ == "__main__":
    unittest.main()
