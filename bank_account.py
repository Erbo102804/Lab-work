"""Система работы с банковскими счетами."""

import math
from numbers import Real


class InsufficientFundsError(Exception):
    """Недостаточно средств на счёте для выполнения операции."""


class BankAccount:
    """Банковский счёт: владелец, номер счёта и текущий баланс."""

    def __init__(self, owner, account_number):
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("Имя владельца должно быть непустой строкой")
        if not isinstance(account_number, str) or not account_number.strip():
            raise ValueError("Номер счёта должен быть непустой строкой")

        self._owner = owner.strip()
        self._account_number = account_number.strip()
        self._balance = 0

    @property
    def owner(self):
        return self._owner

    @property
    def account_number(self):
        return self._account_number

    @property
    def balance(self):
        return self._balance

    @staticmethod
    def _validate_amount(amount):
        """Проверяет, что сумма — конечное положительное число."""
        if isinstance(amount, bool) or not isinstance(amount, Real):
            raise TypeError("Сумма должна быть числом")
        if not math.isfinite(amount):
            raise ValueError("Сумма должна быть конечным числом")
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")

    def deposit(self, amount):
        """Пополняет счёт на указанную сумму и возвращает новый баланс."""
        self._validate_amount(amount)
        self._balance += amount
        return self._balance

    def withdraw(self, amount):
        """Снимает указанную сумму со счёта и возвращает новый баланс."""
        self._validate_amount(amount)
        if amount > self._balance:
            raise InsufficientFundsError(
                f"Недостаточно средств: баланс {self._balance}, запрошено {amount}"
            )
        self._balance -= amount
        return self._balance

    def transfer(self, target, amount):
        """Переводит сумму на другой счёт.

        Все проверки выполняются до изменения балансов, поэтому при ошибке
        состояние обоих счетов остаётся прежним.
        """
        if not isinstance(target, BankAccount):
            raise TypeError("Получатель должен быть банковским счётом")
        if target is self:
            raise ValueError("Нельзя перевести средства на тот же счёт")
        self._validate_amount(amount)
        if amount > self._balance:
            raise InsufficientFundsError(
                f"Недостаточно средств для перевода: баланс {self._balance}, "
                f"запрошено {amount}"
            )
        self._balance -= amount
        target._balance += amount

    def get_balance(self):
        """Возвращает текущий баланс счёта."""
        return self._balance

    def is_empty(self):
        """Возвращает True, если баланс счёта равен нулю."""
        return self._balance == 0

    def __repr__(self):
        return (
            f"BankAccount(owner={self._owner!r}, "
            f"account_number={self._account_number!r}, balance={self._balance!r})"
        )
