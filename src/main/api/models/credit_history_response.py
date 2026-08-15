from typing import List
from src.main.api.models.base_model import BaseModel


class CreditItem(BaseModel):
    creditId: int
    accountId: int
    amount: float
    termMonths: int
    balance: float
    createdAt: str


class CreditHistoryResponse(BaseModel):
    userId: int
    credits: List[CreditItem]
