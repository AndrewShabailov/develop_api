import pytest
from conftest import user_name
from src.main.api.clients import admin_api
from src.main.api.config import ALL_USERS, ADMIN_CREATE, DELETE_USER, DELETE_ALL_USERS
from src.main.api.data.data import USER_PASSWORD


class TestAdmin:
    def test_create_user(self, create_user, user_name):
        assert create_user.status_code == 200, "Status code is not 200"
        assert create_user.json()["role"] == "ROLE_USER", "Role is not equal to ROLE_USER"
        assert create_user.json()["username"] == user_name, f"Username is not equal to {user_name}"

    def test_all_users(self,create_user, get_all_users):
        user_id = create_user.json()["id"]
        assert user_id in [user["id"] for user in get_all_users.json()]

    def test_delete_user(self, delete_user):
        assert delete_user.json()["message"] == "User deleted successfully",\
            f"Message: {delete_user.json()}"

    def test_delete_all_users(self, get_all_users, delete_all_users, admin_token):
        user_count_before = len(get_all_users.json())
        deleted_count = delete_all_users.json()["deleted_count"]

        assert user_count_before == deleted_count + 1
        assert delete_all_users.json()["message"] == "All users except current admin deleted successfully"

        response_after = admin_api.get(ALL_USERS, token=admin_token)
        users_after = response_after.json()

        assert len(users_after) == 1, f"There are {len(users_after)} users"

    @pytest.mark.known_bug('Response has wrong error message. Expected: "User already exists"')
    def test_create_user_negative(self, admin_token, user_name):
        admin_api.post(
            ADMIN_CREATE,
            json={
                "username": user_name,
                "password": USER_PASSWORD,
                "role": "ROLE_USER",
            },
            token=admin_token,
        )
        response = admin_api.post(
            ADMIN_CREATE,
            json={
                "username": user_name,
                "password": USER_PASSWORD,
                "role": "ROLE_USER",
            },
            token=admin_token,
            expected_status=409
        )
        assert response.json()["error"] == "User already has maximum number of accounts(2)"

    @pytest.mark.known_bug('Response has wrong status code, error message.'
                           'Expected: status - 403, error - Admin access required')
    def test_all_users_negative(self, create_user, user_token):
        response = admin_api.get(
            ALL_USERS,
            token=user_token,
            expected_status=401
        )
        assert response.json()["error"] == "Forbidden: Admin access required"


    def test_delete_user_negative(self, admin_token):
        response = admin_api.delete(
            f'{DELETE_USER}{0}',
            token=admin_token,
            expected_status=404
        )
        assert response.json()["error"] == "User not found"

    @pytest.mark.known_bug('Response has wrong status code, error message.'
                           'Expected: status - 403, error - Admin access required')
    def test_delete_all_users_negative(self, user_token):
        response = admin_api.delete(
            DELETE_ALL_USERS,
            token=user_token,
            expected_status=401
        )
        assert response.json()["error"] == "Forbidden: Admin access required"
