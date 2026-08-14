from src.main.api.generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel
from typing import Annotated


class CreateUserRequest(BaseModel):
    username: Annotated[str, CreationRule(regex=r"^[a-zA-Z0-9]{3,15}$")]
    password: Annotated [str, CreationRule(regex=r"^[A-Z]{3}-[a-z]{1}[0-9]{2}[!$_]{4}$")]
    role: Annotated[str, CreationRule(regex=r"^ROLE_USER")]
