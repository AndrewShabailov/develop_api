import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator

@pytest.fixture
def create_user_request(api_manager: ApiManager, created_obj: CreateUserRequest) -> CreateUserRequest:
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    response = api_manager.admin_steps.create_user(user_request)
    created_obj.append(response)
    return user_request
