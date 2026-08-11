from src.main.api.utils.request import post
from src.main.api.config import AUTH_LOGIN
from src.main.api.data.data import ADMIN_USERNAME, ROLE_ADMIN, ADMIN_PASSWORD


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
