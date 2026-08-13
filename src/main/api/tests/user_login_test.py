import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager):
        user_manager = ApiManager(created_obj, username=user.username, password=user.password)
        user_manager.admin_steps.get_users()  # → 403
        response = api_manager.admin_steps.login_user(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == "ROLE_ADMIN"

    def test_login_user(self, login_user, user_name):
        assert 'token' in login_user.json()
        assert login_user.json()["user"]["username"] == user_name, f"Username is NOT equal {user_name}"

    @pytest.mark.parametrize("invalid_user_name, invalid_user_password",
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
    def test_login_negative(
            self,
            invalid_user_name,
            invalid_user_password
    ):
        response = post(
            AUTH_LOGIN,
            json={"username": invalid_user_name, "password": invalid_user_password},
            expected_status=401
        )
        assert response.json()["error"] == "Invalid credentials"

    def test_login_admin_negative(self):
        response = post(
            AUTH_LOGIN,
            json={"username": ADMIN_USERNAME, "password": USER_PASSWORD},
            expected_status=401
        )
        assert response.json()["error"] == "Invalid credentials"

