import pytest
from sqlalchemy.orm.session import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.db.crud.user_crud import UserCrudDb as User


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(
            self,
            db_session: Session,
            api_manager: ApiManager):
        login_user_request = LoginUserRequest(username="admin", password="123456")
        response = api_manager.admin_steps.login_user(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == "ROLE_ADMIN"

        user_from_db = User.get_user_by_username(db_session, response.user.username)

        assert user_from_db.username == response.user.username, f"Username is NOT equal {response.user.username}"
        assert user_from_db.role == response.user.role, f"Role is NOT equal {response.role}"


    def test_login_user(
            self,
            db_session: Session,
            api_manager: ApiManager
    ):
        user = RandomModelGenerator.generate(CreateUserRequest)
        api_manager.admin_steps.create_user(user)
        login_user_request = LoginUserRequest(username=user.username, password=user.password)
        response = api_manager.admin_steps.login_user(login_user_request)

        assert user.username == response.user.username
        assert response.user.role == "ROLE_USER"
        assert 'token' in response.model_dump_json()
        assert user.username == response.user.username,\
            f"Username is NOT equal {user.username}"

        user_from_db = User.get_user_by_username(db_session, response.user.username)

        assert user_from_db.username == response.user.username, f"Username is NOT equal {response.user.username}"
        assert user_from_db.role == response.user.role, f"Role is NOT equal {response.role}"

    @pytest.mark.known_bug("Response has wrong error message. Expected: 'Missing username or password'")
    @pytest.mark.parametrize(
        "invalid_payload, expected_error",
        [
            (
                    {"username": "", "password": "Pas!sw0rd"},
                    'The key "username" must be a non-empty string.'
            ),
            (
                    {"username": "TestUser", "password": ""},
                    'The key "password" must be a non-empty string.'
            ),
        ]
    )
    def test_negative_missing_login_or_password(self, invalid_payload: dict, expected_error: str):

        response = CrudRequester(
            RequestSpecs.base_headers(),
            Endpoint.LOGIN_USER,
            ResponseSpecs.request_bad()
        ).post(
            invalid_payload
        )

        assert response.json()["error"] == expected_error, f"Unexpected error: {expected_error}"


    def test_negative_login_with_invalid_admin_name(self, api_manager: ApiManager):
        login_request = LoginUserRequest(username="adminn", password="123456")

        response = CrudRequester(
            RequestSpecs.base_headers(),
            Endpoint.LOGIN_USER,
            ResponseSpecs.request_unauthorized()
        ).post(login_request)

        assert response.json()["error"] == "Invalid credentials",\
            f"Unexpected error: {response.json()['error']}"
