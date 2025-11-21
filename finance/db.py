import csv
import uuid
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

                    # Обработка link_id при чтении (пустая строка -> None)
                    if 'link_id' in row and row['link_id']:
                        row['link_id'] = uuid.UUID(row['link_id'])
                    else:
                        row['link_id'] = None

                    self._all_txs.append(Transaction(**row))
                except Exception as e:
                    print(f"⚠️ Skipped bad row: {row.get('title', '?')} ({e})")
                    continue

        # --- ВАЛИДАЦИЯ ПРИ ЗАГРУЗКЕ ---
        # Проверяем только те трансферы, у которых УЖЕ проставлен link_id.
        # (Старые трансферы без link_id пока игнорируем или считаем легаси)
        self.check_integrity(silent_ok=True)

    def commit(self):
        fieldnames = self.FIELDNAMES + ["link_id"]
        with open(self.path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for t in self._all_txs:
                data = t.model_dump()
                data['id'] = str(data['id'])
                data['link_id'] = str(data['link_id']) if data['link_id'] else ""
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

    def _validate_transfer_group(self, txs: List[Transaction]):
        """Проверяет математическую корректность группы перевода."""
        if len(txs) < 2:
            raise ValueError(f"Transfer must have at least 2 legs, got {len(txs)}")

        total_rub = sum(t.amount * t.rate for t in txs)

        # Допускаем погрешность копеек из-за float (например 0.01)
        if abs(total_rub) > 0.1:
            debug_info = ", ".join([f"{t.amount} {t.currency.value} (x{t.rate})" for t in txs])
            raise ValueError(f"Transfer is not balanced! RUB sum = {total_rub:.2f}. Legs: {debug_info}")

    def add_transfer(self, title: str, legs: List[dict], date: datetime = None, tags: List[str] = None):
        """
        Атомарное создание перевода.
        legs: список словарей [{'place': 'Sber', 'amount': -100, 'currency': ...}, ...]
        """
        transfer_uuid = uuid.uuid4()
        tx_date = date or datetime.now()
        new_txs = []

        for leg in legs:
            # Формируем транзакцию
            t = Transaction(
                title=title,
                date=tx_date,
                op_type=OperationType.TRANSFER,
                tags=tags or [],
                link_id=transfer_uuid,
                **leg # place, amount, currency, rate, category(обычно None для трансфера)
            )
            new_txs.append(t)

        # Валидируем ВСЮ пачку перед добавлением
        self._validate_transfer_group(new_txs)

        # Если ок - добавляем
        self._all_txs.extend(new_txs)
        print(f"✅ Transfer added: {title} ({len(new_txs)} legs)")
        return new_txs

    def check_integrity(self, silent_ok=False):
        """Скрипт для проверки всей базы на корректность переводов."""
        from collections import defaultdict
        groups = defaultdict(list)

        for t in self._all_txs:
            if t.op_type == OperationType.TRANSFER and t.link_id:
                groups[t.link_id].append(t)

        errors = []
        for lid, txs in groups.items():
            try:
                self._validate_transfer_group(txs)
            except ValueError as e:
                errors.append(f"Link {lid} ('{txs[0].title}'): {e}")

        if errors:
            print(f"\n❌ [CRITICAL] DB Integrity Errors found ({len(errors)}):")
            for e in errors: print(f" - {e}")
            print("-" * 40 + "\n")
        elif not silent_ok:
            print("✅ Integrity Check Passed: All transfers are balanced.")