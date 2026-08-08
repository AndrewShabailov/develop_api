from src.main.api.data.data import AMOUNT


class TestDeposit:
    def test_add_deposit(self, create_deposit, create_user_account):

        initial_balance_1 = create_user_account.json()["balance"]
        account_amount = initial_balance_1 + AMOUNT

        assert create_deposit.status_code == 200, "Status code is NOT 200"
        assert create_deposit.json()['balance'] == account_amount, f"Deposit amount is not equal to {account_amount}"
