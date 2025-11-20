import csv
from pathlib import Path
from finance.storage.csv_storage import CsvStorage

DB_PATH = Path("data/finance.csv")

def group_and_rewrite():
    storage = CsvStorage(DB_PATH)
    transactions = storage.get_all()

    if not transactions:
        print("База данных пуста.")
        return

    transactions.sort(key=lambda x: x.date, reverse=True)
    transactions.sort(key=lambda x: x.place)

    print(f"Перегруппировка {len(transactions)} записей по счетам...")

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

    print("Файл успешно перезаписан.")

if __name__ == "__main__":
    group_and_rewrite()