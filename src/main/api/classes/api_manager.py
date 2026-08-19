from typing import List, Any
from src.main.api.steps.admin_steps import AdminSteps
from src.main.api.steps.user_steps import UserSteps


class ApiManager:
    def __init__(self, created_obj: List[Any]):
        self.admin_steps = AdminSteps(created_obj)
        self.user_steps = UserSteps(created_obj)
