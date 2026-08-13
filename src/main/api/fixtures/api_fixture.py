import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.login_user_response import User


@pytest.fixture
def api_manager(created_obj, username=user.username, password=user.password):
    return ApiManager(created_obj)
