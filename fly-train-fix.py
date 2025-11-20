import csv
from pathlib import Path
from finance.storage.csv_storage import CsvStorage
from finance.models.schemas import Transaction

DB_PATH = Path("data/finance.csv")

def update_categories():
    storage = CsvStorage(DB_PATH)
    
    # 1. Загружаем все данные
    transactions = storage.get_all()
    updated_count = 0

    # 2. Проходимся по списку и обновляем
    for t in transactions:
        title_lower = t.title.lower()
        if "поезд" in title_lower or "самолет" in title_lower:
            # Проверяем, не стоит ли уже нужная категория, чтобы не считать лишнего
            if t.category != "Travel":
                t.category = "Travel"
                updated_count += 1
                print(f"Обновлено: {t.title} -> Travel")

    if updated_count == 0:
        print("Нет записей для обновления.")
        return

    # 3. Перезаписываем файл (нужно добавить этот функционал, так как storage.append только добавляет)
    # Реализуем простую перезапись прямо здесь, используя логику из CsvStorage
    
    print(f"Сохранение {updated_count} изменений...")
    
    with open(DB_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CsvStorage.FIELDNAMES)
        writer.writeheader()
        
        for t in transactions:
            row = t.model_dump()
            row["id"] = str(row["id"])
            row["date"] = row["date"].isoformat()
            row["currency"] = row["currency"].value
            row["op_type"] = row["op_type"].value
            row["tags"] = "|".join(row["tags"])
            writer.writerow(row)

    print("Готово.")

if __name__ == "__main__":
    update_categories()