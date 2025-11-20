import csv
from pathlib import Path
from datetime import datetime

# Импортируем Service и Storage, а также Enum'ы
from finance.core.services import FinanceService
from finance.storage.csv_storage import CsvStorage
from finance.models.schemas import Currency, OperationType

# Настройки
SOURCE_FILES = ['tricount.csv']
# SOURCE_FILES = ['alipay-expenditure.csv', 'alipay-income.csv']
DB_PATH = Path("data/finance.csv")
CNY_RATE = 11.8788

def clean_category(category: str) -> str:
    # if category == 'Groceries':
    #     return 'Food & Dining'
    return category

def import_data():
    # Инициализируем приложение (Storage + Service)
    storage = CsvStorage(DB_PATH)
    service = FinanceService(storage)

    count = 0
    print(f"Начинаем импорт в {DB_PATH}...")

    for filename in SOURCE_FILES:
        file_path = Path(filename)
        if not file_path.exists():
            print(f"[WARNING] Файл {filename} не найден, пропускаем.")
            continue

        print(f"Обработка {filename}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                try:
                    raw_amount = float(row['Amount'])

                    # Фильтрация (как в твоем pandas скрипте)
                    if raw_amount >= 0:
                        continue
                    if row['Category'] == 'Transfers':
                        continue

                    amount = abs(raw_amount)

                    # Парсинг даты
                    dt = datetime.strptime(row['Date'], "%Y-%m-%d %H:%M:%S")

                    category = clean_category(row['Category'])

                    # Используем СЕРВИС для добавления.
                    # Теперь мы можем передать дату 'date=dt'
                    service.add_transaction(
                        title=row['English Translation'],
                        place="Tricount",
                        amount=amount,
                        currency=Currency.CNY,
                        op_type=OperationType.SPEND,
                        category=category,
                        rate=CNY_RATE,
                        tags=["import"],
                        date=dt  # <--- Вот ключевое изменение
                    )
                    count += 1

                except KeyError as e:
                    print(f"[ERROR] В файле {filename} нет колонки: {e}")
                    break
                except ValueError as e:
                    print(f"[ERROR] Ошибка данных в строке: {row.get('Date', 'Unknown')} - {e}")
                    continue

    print(f"\nГотово! Импортировано записей: {count}")

if __name__ == "__main__":
    import_data()