import pytest
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestAdmin:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_create_user_valid(self, api_manager, create_user_request):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

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
    def test_negative_create_user_invalid(self, username, password, api_manager):
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.create_invalid_user(create_user_request)

    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_all_users(self, api_manager, create_user_request):
        created_user = api_manager.admin_steps.create_user(create_user_request)
        users_list = api_manager.admin_steps.get_users()

        assert created_user.username in [user.username for user in users_list]

    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_delete_user(self, api_manager, create_user_request):
        created_user = api_manager.admin_steps.create_user(create_user_request)
        delete_response = api_manager.admin_steps.delete_user(created_user.id)

        assert delete_response.json()["message"] == "User deleted successfully", \
            f"Message: {delete_response.json()}"

    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_delete_all_users(self, api_manager, create_user_request):
        api_manager.admin_steps.create_user(create_user_request)
        user_count_before = len(api_manager.admin_steps.get_users())
        delete_result = api_manager.admin_steps.delete_all_users().json()
        users_after = api_manager.admin_steps.get_users()

        assert user_count_before == delete_result["deleted_count"] + 1
        assert delete_result["message"] == "All users except current admin deleted successfully"
        assert len(users_after) == 1, f"There are {len(users_after)} users"

    @pytest.mark.known_bug('Response has wrong error message. Expected: "User already exists"')
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_create_user_with_the_same_name_negative(self, api_manager, create_user_request):
        api_manager.admin_steps.create_user(create_user_request)

        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=api_manager.admin_steps.username,
                password=api_manager.admin_steps.password
            ),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_conflict()
        ).post(create_user_request)

        assert response.json()["error"] == "User already has maximum number of accounts(2)"

    @pytest.mark.known_bug('Response has wrong status code, error message.'
                           'Expected: status - 403, error - Admin access required')
    def test_negative_user_gets_list_of_all_users(self, create_user_request):

        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.ADMIN_GET_USERS,
            ResponseSpecs.request_unauthorized()
        ).get()

        assert response.json()["error"] == "Forbidden: Admin access required"


    def test_delete_non_existing_user_negative(self, api_manager):

        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=api_manager.admin_steps.username,
                password=api_manager.admin_steps.password
            ),
            Endpoint.ADMIN_DELETE_USER,
            ResponseSpecs.request_not_found()
        ).delete(0)

        assert response.json()["error"] == "User not found"

    @pytest.mark.known_bug('Response has wrong status code, error message.'
                           'Expected: status - 403, error - Admin access required')
    def test_delete_all_users_negative(self, create_user_request):

        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.ADMIN_DELETE_ALL_USERS,
            ResponseSpecs.request_unauthorized()
        ).delete()

        assert response.json()["error"] == "Forbidden: Admin access required"
