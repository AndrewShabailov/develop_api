from src.main.api.clients import admin_api
from src.main.api.config import ALL_USERS


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
