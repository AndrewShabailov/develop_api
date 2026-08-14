import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator

@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request
