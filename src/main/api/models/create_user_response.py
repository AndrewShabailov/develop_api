from typing import Optional

from src.main.api.models.base_model import BaseModel


class CreateUserResponse(BaseModel):
    id: int
    username: str
    password: Optional[str] = None
    role: str
