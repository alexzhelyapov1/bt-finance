from finance import DB

TARGET_PLACE = 'RMB Наличка'
# TARGET_PLACE = 'Alipay'

db = DB()

(db.filter(lambda t: t.place == TARGET_PLACE)
   .sort()                        # Сортировка по дате (возрастание)
   .show(f"Выписка: {TARGET_PLACE}")
   .balance())                    # Итоговый остаток