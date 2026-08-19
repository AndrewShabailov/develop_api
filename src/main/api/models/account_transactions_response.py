from pydantic import BaseModel
from typing import List, Optional


class TransactionModel(BaseModel):
    transactionId: int
    type: str
    amount: float
    fromAccountId: Optional[int] = None
    toAccountId: Optional[int] = None
    createdAt: str


class AccountTransactionsResponse(BaseModel):
    id: int
    number: str
    balance: float
    transactions: List[TransactionModel]
