"""Демонстрация работы системы банковских счетов."""

from bank_account import BankAccount, InsufficientFundsError

ivan = BankAccount("Иван Иванов", "KG-0001")
petr = BankAccount("Пётр Петров", "KG-0002")
print("Создан счёт:", ivan)
print("Счёт пуст?", ivan.is_empty())

print("\nПополнение на 1000 ->", ivan.deposit(1000))
print("Снятие 250        ->", ivan.withdraw(250))
ivan.transfer(petr, 300)
print("Перевод 300 Петру:  Иван =", ivan.get_balance(), "| Пётр =", petr.get_balance())
print("Счёт пуст?", ivan.is_empty())

print("\nПроверка ошибок:")
for title, action in [
    ("Снять 5000", lambda: ivan.withdraw(5000)),
    ("Пополнить на -100", lambda: ivan.deposit(-100)),
    ("Пополнить на '100'", lambda: ivan.deposit("100")),
    ("Перевести 9999", lambda: ivan.transfer(petr, 9999)),
    ("Перевести себе", lambda: ivan.transfer(ivan, 10)),
]:
    try:
        action()
    except (ValueError, TypeError, InsufficientFundsError) as e:
        print(f"  {title:<20} -> {type(e).__name__}: {e}")
print("Балансы не изменились: Иван =", ivan.get_balance(), "| Пётр =", petr.get_balance())
