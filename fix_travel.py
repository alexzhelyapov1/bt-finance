from finance import DB

db = DB()

def set_travel(t):
    t.category = "Travel"

# 1. Найти
# 2. Применить функцию изменения
# 3. Показать, что изменилось (для контроля)
(db.filter(lambda t: "поезд" in t.title.lower() or "самолет" in t.title.lower())
   .each(set_travel)
   .show("Обновленные записи"))

# 4. Сохранить изменения на диск
db.commit()