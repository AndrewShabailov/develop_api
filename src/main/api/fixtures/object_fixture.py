import pytest
from typing import List, Any
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_response import CreateUserResponse


@pytest.fixture
def created_obj():
    objects: List[Any] = []
    yield objects
    clean_user(objects)


def clean_user(objects: List[Any]):
    api_manager = ApiManager(objects)
    for u in objects:
        if isinstance(u, CreateUserResponse):
            try:
                api_manager.admin_steps.delete_user(u.id)
            except AssertionError:
                pass
