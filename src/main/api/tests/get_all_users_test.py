class TestAllUsers:
    def test_all_users(self, all_users):
        response = all_users
        users = response.json()

        assert isinstance(users, list)
        assert len(users) > 0
