from abc import ABC, abstractmethod
from typing import Dict, Callable
from src.main.api.models.base_model import BaseModel


class Requester(ABC):
    def __init__(self, request_spec: Dict[str, str], response_spec: Callable):
        self.headers = request_spec["headers"]
        self.base_url = request_spec["base_url"]
        self.response_spec = response_spec

    @abstractmethod
    def post(self, model: BaseModel):...

    @abstractmethod
    def get(self, model: BaseModel): ...
