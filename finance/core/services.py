from typing import List, Dict, Optional  # Добавили Optional
from datetime import datetime

from finance.models.schemas import Transaction, Currency, OperationType
from finance.storage.base import IStorage

class FinanceService:
    def __init__(self, storage: IStorage):
        self.storage = storage

    # Добавили аргумент date: Optional[datetime] = None
    def add_transaction(self, title: str, place: str, amount: float, 
                        currency: Currency, op_type: OperationType, 
                        category: str = None, rate: float = 1.0, 
                        tags: List[str] = None, date: Optional[datetime] = None) -> Transaction:
        
        if currency == Currency.RUB:
            rate = 1.0
        
        # Если date не передан, Pydantic сам вызовет default_factory=datetime.now
        # Но нам нужно передать его в конструктор, если он есть.
        
        # Формируем аргументы для создания
        tx_data = {
            "title": title,
            "place": place,
            "amount": amount,
            "currency": currency,
            "op_type": op_type,
            "category": category,
            "rate": rate,
            "tags": tags or []
        }
        
        # Если дата передана явно, добавляем её
        if date:
            tx_data["date"] = date

        transaction = Transaction(**tx_data)
        self.storage.append(transaction)
        return transaction

    def get_history(self) -> List[Transaction]:
        return sorted(self.storage.get_all(), key=lambda x: x.date, reverse=True)

    def calculate_balance(self) -> Dict[str, float]:
        transactions = self.storage.get_all()
        total_rub = 0.0
        currency_balances = {c.value: 0.0 for c in Currency}

        for t in transactions:
            val = t.amount
            currency_balances[t.currency.value] += val
            total_rub += val * t.rate
            
        return {
            "total_rub_eq": total_rub,
            "currencies": currency_balances
        }