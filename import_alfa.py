from datetime import datetime
from finance import DB, OperationType, Currency

db = DB()
PLACE = "Альфа"

def add(date_str, title, amount, op_type, cat=None):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    db.add(
        title=title,
        amount=amount,
        place=PLACE,
        op_type=op_type,
        currency=Currency.RUB,
        category=cat,
        date=dt,
        tags=['Alpha-Imported']
    )

# --- 18 Ноября ---
add("2025-11-18", "Выплата за операции покупок (Кэшбэк)", 5000, OperationType.INCOME)
add("2025-11-18", "Никита О. (Сбербанк)", -2000, OperationType.UNKNOWN_TRANSFER)
add("2025-11-18", "Мария К. (Т-Банк)", -2000, OperationType.UNKNOWN_TRANSFER)

# --- 11 Ноября ---
db.add_transfer(
    title="Обмен валюты",
    legs=[
        {"place": "Альфа", "amount": -1000, "currency": Currency.RUB, "rate": 1.0},
        {"place": "Альфа-Инвест", "amount": 1000, "currency": Currency.RUB, "rate": 1.0}
    ],
    date=datetime.strptime('2025-11-11', "%Y-%m-%d"),
    tags=['Alpha-Imported'],
)

add("2025-11-11", "Выплата в рамках 10 000 руб", 1000, OperationType.INCOME)

# --- 9 Ноября ---
add("2025-11-09", "Комиссия за подписку Альфа", -399, OperationType.SPEND, "Service")

# --- 28 Октября ---
db.add_transfer(
    title="Обмен валюты",
    legs=[
        {"place": "Альфа", "amount": -2000, "currency": Currency.RUB, "rate": 1.0},
        {"place": "Альфа-Инвест", "amount": 2000, "currency": Currency.RUB, "rate": 1.0}
    ],
    date=datetime.strptime('2025-10-28', "%Y-%m-%d"),
    tags=['Alpha-Imported'],
)

# --- 17 Октября ---
add("2025-10-17", "Выплата в рамках Программы лояльности", 2000, OperationType.INCOME)

# --- 16 Октября ---
add("2025-10-16", "Выплата в рамках Программы лояльности", 3000, OperationType.INCOME)

# --- 15 Октября ---
add("2025-10-15", "Оплата АльфаТревел", -4717.51, OperationType.SPEND, "Travel")

add("2025-10-10", "Выплата в рамках Программы лояльности", 2000, OperationType.INCOME)
add("2025-10-10", "Выплата в рамках Программы лояльности", 2000, OperationType.INCOME)
add("2025-10-10", "Выплата в рамках Программы лояльности", 500, OperationType.INCOME)

# --- 9 Октября ---
add("2025-10-09", "Alfa-Travel Avia", -124334, OperationType.SPEND, "Travel")
add("2025-10-09", "Алексей Ж. (Входящий)", 150000, OperationType.UNKNOWN_TRANSFER)
add("2025-10-09", "Пополнение из другого банка (Т-Банк)", 10, OperationType.UNKNOWN_TRANSFER)
add("2025-10-09", "Алексей Ж.", 10, OperationType.UNKNOWN_TRANSFER)

db.commit()