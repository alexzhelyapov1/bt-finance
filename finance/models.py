import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, model_validator

class Currency(str, Enum):
    RUB = "RUB"; CNY = "CNY"; EUR = "EUR"

class OperationType(str, Enum):
    SPEND = "SPEND"; INCOME = "INCOME"; TRANSFER = "TRANSFER"; LENT = "LENT"; RETURNED = "RETURNED"; UNKNOWN_TRANSFER = "UNKNOWN_TRANSFER"

class Transaction(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    date: datetime = Field(default_factory=datetime.now)
    title: str
    category: Optional[str] = None
    place: str
    amount: float
    currency: Currency
    rate: float = 1.0
    op_type: OperationType
    tags: List[str] = Field(default_factory=list)
    link_id: Optional[uuid.UUID] = None

    @model_validator(mode='after')
    def validate_logic(self):
        if self.op_type == OperationType.SPEND and not self.category:
            raise ValueError("Category required for SPEND")
        if self.op_type != OperationType.SPEND and self.category:
            self.category = None
        # Валидация перевода: link_id желателен, но не обязателен (чтобы не ломать старые записи сразу)
        return self

    @model_validator(mode='after')
    def validate_transfer_has_link(self):
        if self.op_type == OperationType.TRANSFER and not self.link_id:
            raise ValueError("Transfer operation must have a link_id")
        return self
