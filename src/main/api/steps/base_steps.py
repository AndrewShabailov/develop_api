from typing import List, Any

from src.main.api.specs.request_specs import RequestSpecs


class BaseSteps:
    def __init__(self, created_obj: List[Any], username="admin", password="123456"):
        self.created_obj = created_obj
        self.auth = RequestSpecs.auth_headers(username, password)
