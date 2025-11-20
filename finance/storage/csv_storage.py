import csv
import uuid
from datetime import datetime
from pathlib import Path
from typing import List

from finance.models.schemas import Transaction, Currency, OperationType
from finance.storage.base import IStorage

class CsvStorage(IStorage):
    FIELDNAMES = [
        "id", "date", "title", "category", "place", 
        "amount", "currency", "rate", "op_type", "tags"
    ]

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self._ensure_file()

    def _ensure_file(self):
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
                writer.writeheader()

    def get_all(self) -> List[Transaction]:
        transactions = []
        with open(self.file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    tags_list = row["tags"].split("|") if row["tags"] else []
                    t = Transaction(
                        id=uuid.UUID(row["id"]),
                        date=datetime.fromisoformat(row["date"]),
                        title=row["title"],
                        category=row["category"] or None,
                        place=row["place"],
                        amount=float(row["amount"]),
                        currency=Currency(row["currency"]),
                        rate=float(row["rate"]),
                        op_type=OperationType(row["op_type"]),
                        tags=tags_list
                    )
                    transactions.append(t)
                except ValueError:
                    continue
        return transactions

    def append(self, transaction: Transaction):
        row = transaction.model_dump()
        row["id"] = str(row["id"])
        row["date"] = row["date"].isoformat()
        row["currency"] = row["currency"].value
        row["op_type"] = row["op_type"].value
        row["tags"] = "|".join(row["tags"])
        
        with open(self.file_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
            writer.writerow(row)