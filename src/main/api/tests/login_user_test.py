class TestLoginUser:
    def test_login_user(self, login_user, user_name):
        assert login_user.status_code == 200, "Status code is NOT 200"
        assert login_user.json()["user"]["username"] == user_name, f"Username is NOT equal {user_name}"
