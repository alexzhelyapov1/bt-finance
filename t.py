from finance import DB, Currency

db = DB()

# Пример: Перевод 100 USD со счета Cash (курс 90) -> на Tinkoff (получили 9000 RUB, курс 1)
# Сумма в рублях: (-100 * 90) + (9000 * 1) = -9000 + 9000 = 0. Валидно.

try:
    db.add_transfer(
        title="Обмен валюты",
        legs=[
            {"place": "Cash", "amount": -100, "currency": Currency.CNY, "rate": 90.0},
            {"place": "Tinkoff", "amount": 9000, "currency": Currency.RUB, "rate": 1.0}
        ]
    )
    db.commit()
except ValueError as e:
    print(f"Ошибка: {e}")