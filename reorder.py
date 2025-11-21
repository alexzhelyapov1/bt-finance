from finance import DB

db = DB()

# Сортируем список транзакций напрямую
# python sort стабилен, поэтому сортируем сначала по вторичному ключу (дата), потом по первичному (место)
db._all_txs.sort(key=lambda t: t.date, reverse=True)
db._all_txs.sort(key=lambda t: t.place)

db.commit()