class TestDeleteUser:
    def test_delete_user(self, delete_user):
        assert delete_user.json()["message"] == "User deleted successfully",\
            f"Message: {delete_user.json()}"

    def test_delete_all_users(self, delete_all_users):
        assert delete_all_users.json()["message"] == "All users except current admin deleted successfully",\
            f"Message: {delete_all_users.json()}"
