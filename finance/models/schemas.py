import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

class Currency(str, Enum):
    RUB = "RUB"
    CNY = "CNY"
    EUR = "EUR"

class OperationType(str, Enum):
    SPEND = "SPEND"
    INCOME = "INCOME"
    TRANSFER = "TRANSFER"
    LENT = "LENT" 
    RETURNED = "RETURNED" 

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

    @model_validator(mode='after')
    def check_category_logic(self):
        if self.op_type == OperationType.SPEND and not self.category:
            raise ValueError("Category is required for SPEND operations")
        if self.op_type != OperationType.SPEND and self.category:
            self.category = None
        return self

    @field_validator('rate')
    def validate_rate(cls, v, info):
        values = info.data
        if values.get('currency') == Currency.RUB and v != 1.0:
            return 1.0
        return v