import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.db.crud.user_crud import UserCrudDb as User
from sqlalchemy.orm.session import Session


class TestAdmin:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_create_user_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        role_from_db = User.get_user_by_role(db_session, create_user_request.role)

        assert user_from_db.username == create_user_request.username, "Created user not in DB"
        assert role_from_db.role == create_user_request.role, "Created user role not in DB"

    @pytest.mark.parametrize(
        "username, password",
        [
            ("абв", "Pas!sw0rd"),
            ("ab", "Pas!sw0rd"),
            ("abv!", "Pas!sw0rd"),
            ("Max1", "Pas!sw0гд"),
            ("Maxx2", "Pas!sw0"),
            ("Maxx3", "pas!sw0rd"),
            ("Maxx4", "PAS!SWORD"),
            ("Maxx5", "PASSSWORD"),
            ("Maxx6", "PAS!SWRRD")
        ]
    )
    def test_negative_create_user_invalid(self, db_session: Session, username: str, password: str, api_manager: ApiManager):
        create_user_request = CreateUserRequest(
            username=username,
            password=password,
            role="ROLE_USER"
        )
        api_manager.admin_steps.create_invalid_user(create_user_request)
        user_from_db = User.get_user_by_username(db_session, create_user_request.username)

        assert user_from_db is None, "User is created"

    def test_all_users(
            self,
            api_manager: ApiManager
    ):

        response = api_manager.admin_steps.get_users()

        assert len(response) != 0, f"Users list: {len(response)} users"

    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_delete_user(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest
    ):

        created_user = api_manager.admin_steps.create_user(create_user_request)
        delete_response = api_manager.admin_steps.delete_user(created_user.id)

        assert delete_response.json()["message"] == "User deleted successfully", \
            f"Message: {delete_response.json()}"

        user_from_db = User.get_user_by_id(db_session, created_user.id)

        assert user_from_db is not None, f"User with ID {created_user.id} not found in database"
        assert user_from_db.deleted_at is not None, f"User with ID {created_user.id} was not soft-deleted"

    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_delete_all_users(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest
    ):

        created_user = api_manager.admin_steps.create_user(create_user_request)
        delete_result = api_manager.admin_steps.delete_all_users().json()

        assert delete_result["message"] == "All users except current admin deleted successfully"

        user_from_db = User.get_user_by_id(db_session, created_user.id)
        assert user_from_db is not None, f"User not found in DB"
        assert user_from_db.deleted_at is not None, f"User with ID {created_user.id} was not soft-deleted!"

        admin_from_db = User.get_user_by_username(db_session, api_manager.admin_steps.username)
        assert admin_from_db is not None, "Current admin not found in database"
        assert admin_from_db.deleted_at is None, "Current admin was incorrectly deleted!"


    @pytest.mark.known_bug('Response has wrong error message. Expected: "User already exists"')
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_create_user_with_the_same_name_negative(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest
    ):
        api_manager.admin_steps.create_user(create_user_request)

        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=api_manager.admin_steps.username,
                password=api_manager.admin_steps.password
            ),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_conflict()
        ).post(create_user_request)

        assert response.json()["error"] == "User already has maximum number of accounts(2)",\
            f"Unexpected error message: {response.json()['error']}"

        users_in_db = User.has_unique_name(db_session, api_manager.admin_steps.username)

        assert len(users_in_db) == 1,\
            f"Error: duplicate user was created in the database! Count: {len(users_in_db)}"

    @pytest.mark.known_bug('Response has wrong status code, error message.'
                           'Expected: status - 403, error - Admin access required')
    def test_negative_user_gets_list_of_all_users(
            self,
            create_user_request: CreateUserRequest
    ):

        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.ADMIN_GET_USERS,
            ResponseSpecs.request_unauthorized()
        ).get()

        assert response.json()["error"] == "Forbidden: Admin access required",\
            f"Unexpected error message: {response.json()['error']}"


    def test_delete_non_existing_user_negative(
            self,
            db_session: Session,
            api_manager: ApiManager
    ):

        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=api_manager.admin_steps.username,
                password=api_manager.admin_steps.password
            ),
            Endpoint.ADMIN_DELETE_USER,
            ResponseSpecs.request_not_found()
        ).delete(0)

        assert response.json()["error"] == "User not found",\
            f"Unexpected error: {response.json()['error']}"

        nonexisting_user = User.get_user_by_id(db_session, 0)
        assert nonexisting_user is None, f"Non-existing user {nonexisting_user} was found in database"

    @pytest.mark.known_bug('Response has wrong status code, error message.'
                           'Expected: status - 403, error - Admin access required')
    def test_delete_all_users_negative(self, create_user_request: CreateUserRequest):

        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.ADMIN_DELETE_ALL_USERS,
            ResponseSpecs.request_unauthorized()
        ).delete()

        assert response.json()["error"] == "Forbidden: Admin access required",\
            f"Unexpected error: {response.json()['error']}"
