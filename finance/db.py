import csv
from pathlib import Path
from datetime import datetime
from typing import List, Callable, Optional

from .models import Transaction, Currency, OperationType
from . import view

DB_PATH = Path("data/finance.csv")

class Query:
    def __init__(self, transactions: List[Transaction]):
        self._txs = transactions

    def __len__(self): return len(self._txs)
    def __iter__(self): return iter(self._txs)
    def __getitem__(self, item): return self._txs[item]

    @property
    def items(self) -> List[Transaction]:
        return self._txs

    def filter(self, func: Callable[[Transaction], bool]) -> 'Query':
        return Query([t for t in self._txs if func(t)])

    def sort(self, key=lambda t: t.date, reverse=False) -> 'Query':
        return Query(sorted(self._txs, key=key, reverse=reverse))

    def each(self, func: Callable[[Transaction], None]) -> 'Query':
        for t in self._txs:
            func(t)
        return self

    def show(self, title: str = "Транзакции"):
        view.render_table(self._txs, title)
        return self

    def balance(self):
        view.render_balance(self._txs)
        return self


class DB(Query):
    FIELDNAMES = ["id", "date", "title", "category", "place", "amount", "currency", "rate", "op_type", "tags"]

    def __init__(self, path=DB_PATH):
        self.path = path
        self._load()
        super().__init__(self._all_txs)

    def _load(self):
        self._all_txs = []
        if not self.path.exists(): return
        with open(self.path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    row['tags'] = row['tags'].split("|") if row['tags'] else []
                    self._all_txs.append(Transaction(**row))
                except Exception: continue

    def commit(self):
        with open(self.path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
            writer.writeheader()
            for t in self._all_txs:
                data = t.model_dump()
                data['id'] = str(data['id'])
                data['date'] = data['date'].isoformat()
                data['currency'] = data['currency'].value
                data['op_type'] = data['op_type'].value
                data['tags'] = "|".join(data['tags'])
                writer.writerow(data)
        print(f"💾 Database saved ({len(self._all_txs)} records).")

    def add(self, title, amount, place, op_type, currency=Currency.RUB, category=None, tags=None, date=None, rate=1.0):
        t = Transaction(
            title=title, amount=amount, place=place, op_type=op_type,
            currency=currency, category=category, tags=tags or [],
            date=date or datetime.now(), rate=rate
        )
        self._all_txs.append(t)
        return t