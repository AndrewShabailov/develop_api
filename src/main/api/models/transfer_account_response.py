from src.main.api.models.base_model import BaseModel


class TransferAccountResponse(BaseModel):
    fromAccountId: int
    toAccountId: int
    fromAccountIdBalance: float
