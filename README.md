# Система банковского счёта

Небольшая система для работы с банковскими счетами и набор модульных тестов на `unittest`.

## Файлы

- `bank_account.py` — класс `BankAccount` и исключение `InsufficientFundsError`.
- `test_bank_account.py` — модульные тесты.

## Возможности `BankAccount`

| Метод / свойство | Описание |
|---|---|
| `BankAccount(owner, account_number)` | Создание счёта; начальный баланс равен 0 |
| `owner`, `account_number`, `balance` | Данные счёта (только для чтения) |
| `deposit(amount)` | Пополнение счёта |
| `withdraw(amount)` | Снятие средств (не больше текущего баланса) |
| `transfer(target, amount)` | Перевод на другой счёт; при ошибке оба счёта не меняются |
| `get_balance()` | Текущий баланс |
| `is_empty()` | `True`, если баланс равен 0 |

Некорректные суммы (не число, ноль, отрицательные, `inf`/`nan`) вызывают `TypeError` или `ValueError`;
нехватка средств — `InsufficientFundsError`.

## Пример

```python
from bank_account import BankAccount

a = BankAccount("Иван Иванов", "KG-0001")
b = BankAccount("Пётр Петров", "KG-0002")
a.deposit(1000)
a.withdraw(200)
a.transfer(b, 300)
print(a.get_balance(), b.get_balance())  # 500 300
print(a.is_empty())                      # False
```

## Запуск тестов

```bash
python3 -m unittest -v
```
