from src.main.api.models.base_model import BaseModel


class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: str
