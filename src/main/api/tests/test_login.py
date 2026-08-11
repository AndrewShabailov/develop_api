import pytest
from src.main.api.utils.request import post
from src.main.api.config import AUTH_LOGIN
from src.main.api.data.data import ADMIN_USERNAME, ROLE_ADMIN, ADMIN_PASSWORD, USER_PASSWORD


class TestLogin:
    def test_login_admin(self):
        response = post(
            AUTH_LOGIN,
            json={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD},
            expected_status=200
        )
        assert 'token' in response.json()
        assert response.json()["user"]["username"] == ADMIN_USERNAME
        assert response.json()["user"]["role"] == ROLE_ADMIN

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

