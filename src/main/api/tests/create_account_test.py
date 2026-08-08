class TestCreateAccount:
    def test_create_account(self, create_user_account):

        assert create_user_account.status_code == 201, "Status code is not 201"
        assert create_user_account.json()['balance'] == 0, "Initial balance is NOT 0"
