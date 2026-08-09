class TestLoginUser:
    def test_login_user(self, login_user, user_name):
        assert login_user.json()["user"]["username"] == user_name, f"Username is NOT equal {user_name}"
