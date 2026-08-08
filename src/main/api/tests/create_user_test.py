class TestCreateUser:
    def test_create_user(self,create_user, user_name):

        assert create_user.status_code == 200, "Status code is not 200"
        assert create_user.json()["role"] == "ROLE_USER", "Role is not equal to ROLE_USER"
        assert create_user.json()["username"] == user_name, f"Username is not equal to {user_name}"
