import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager: ApiManager):
        login_user_request = LoginUserRequest(username="admin", password="123456")
        response = api_manager.admin_steps.login_user(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == "ROLE_ADMIN"

    def test_login_user(self, api_manager: ApiManager):
        user = RandomModelGenerator.generate(CreateUserRequest)
        api_manager.admin_steps.create_user(user)
        login_user_request = LoginUserRequest(username=user.username, password=user.password)
        response = api_manager.admin_steps.login_user(login_user_request)

        assert user.username == response.user.username
        assert response.user.role == "ROLE_USER"
        assert 'token' in response.model_dump_json()
        assert user.username == response.user.username,\
            f"Username is NOT equal {user.username}"

    @pytest.mark.known_bug("Response has wrong error message. Expected: 'Missing username or password'")
    @pytest.mark.parametrize("invalid_payload",
                             [
                                 {"username": "", "password": "Pas!sw0rd"},
                                 {"username": "TestUser", "password": ""}
                             ]
                             )
    def test_negative_missing_login_or_password(self, invalid_payload: dict):
        response = CrudRequester(
            RequestSpecs.base_headers(),
            Endpoint.LOGIN_USER,
            ResponseSpecs.request_bad()
        ).post(
            invalid_payload
        )
        invalid_key = [k for k, v in invalid_payload.items() if v == ""][0]
        expected_error = f'The key "{invalid_key}" must be a non-empty string.'

        assert response.json()["error"] == expected_error


    def test_negative_login_with_invalid_admin_name(self, api_manager: ApiManager):
        login_request = LoginUserRequest(username="adminn", password="123456")

        response = CrudRequester(
            RequestSpecs.base_headers(),
            Endpoint.LOGIN_USER,
            ResponseSpecs.request_unauthorized()
        ).post(login_request)

        assert response.json()["error"] == "Invalid credentials"
