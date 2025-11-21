import uuid
from finance import DB, OperationType

db = DB()

def merge_transfers(amount):
    # 1. Ищем свободные трансферы с такой суммой (по модулю)
    candidates = list(db.filter(lambda t:
        t.op_type == OperationType.UNKNOWN_TRANSFER
        and not t.link_id
        # and (abs(t.amount) in [1000, 5000, 4000])
    ).show())

    if len(candidates) < 2:
        return print(f"⚠️ Меньше 2 записей для суммы {amount}")

    # 2. Если записей > 2 — спрашиваем пользователя
    selected = candidates
    if len(candidates) > 2:
        print(f"\nНайдено {len(candidates)} записей для {amount}:")
        for i, t in enumerate(candidates):
            print(f"[{i}] {t.date.date()} | {t.place} | {t.amount:+.2f} {t.currency.value} | {t.title}")

        idxs = input("Введите индексы для объединения (через запятую): ")
        selected = [candidates[int(i.strip())] for i in idxs.split(",")]

    # print("Found:")
    # for i in candidates:
    #     print(f"")
    # 3. Выбираем дату
    unique_dates = sorted(list({t.date for t in selected}))
    master_date = unique_dates[0]

    if len(unique_dates) > 1:
        print("\nКакую дату использовать?")
        for i, d in enumerate(unique_dates): print(f"[{i}] {d}")
        master_date = unique_dates[int(input("Индекс даты: "))]

    # 4. Линкуем
    link_id = uuid.uuid4()
    for t in selected:
        t.link_id = link_id
        t.date = master_date

    db.commit()
    print(f"✅ Объединено {len(selected)} записей.")



# (db.filter(lambda t: t.op_type == OperationType.UNKNOWN_TRANSFER)
#    .show("Обновленные записи"))



# Пример использования:
merge_transfers(60007)


db.commit()