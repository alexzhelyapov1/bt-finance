import csv
from pathlib import Path
from finance.storage.csv_storage import CsvStorage
from finance.models.schemas import OperationType

DB_PATH = Path("data/finance.csv")

def migrate_signs():
    storage = CsvStorage(DB_PATH)
    transactions = storage.get_all()
    
    count = 0
    
    print("Начинаем миграцию знаков...")

    for t in transactions:
        # Если это Трата или Дано в долг - сумма должна быть отрицательной
        if t.op_type in [OperationType.SPEND, OperationType.LENT]:
            if t.amount > 0:
                t.amount = -t.amount
                count += 1
        
        # Если это Приход или Возврат долга - сумма должна быть положительной
        elif t.op_type in [OperationType.INCOME, OperationType.RETURNED]:
            if t.amount < 0:
                t.amount = abs(t.amount)
                count += 1
                
        # TRANSFER оставляем как есть, так как они могут быть и + и - 
        # (в зависимости от того, пополнение это или списание)

    print(f"Изменено {count} записей.")
    
    # Перезапись файла
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

    print("Миграция завершена.")

if __name__ == "__main__":
    migrate_signs()