from src.main.api.data.data import *

class TestLoginAdmin:
    def test_login_admin(self,login_admin):
        assert login_admin.status_code == 200, "Login Admin failed"
        assert login_admin.json()["user"]["username"] == ADMIN_USERNAME, "Username is NOT admin"
        assert login_admin.json()["user"]["role"] == ROLE_ADMIN, "Role is NOT admin"
