from src.main.api.models.base_model import BaseModel


class DepositAccountRequest(BaseModel):
    accountId: int
    amount: float
