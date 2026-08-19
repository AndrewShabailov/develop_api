from src.main.api.models.base_model import BaseModel


class TransferAccountRequest(BaseModel):
    fromAccountId: int
    toAccountId: int
    amount: float
