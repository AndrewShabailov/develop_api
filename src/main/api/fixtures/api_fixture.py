import pytest
from src.main.api.classes.api_manager import ApiManager


@pytest.fixture
def api_manager(created_obj: ApiManager) -> ApiManager:
    return ApiManager(created_obj)
