from src.main.api.data.data import AMOUNT, TRANSFER_AMOUNT


class TestCreateAccount:
    def test_create_account(self, create_user_account):

        assert create_user_account.json()['balance'] == 0, "Initial balance is NOT 0"
        assert "id" in create_user_account.json(), "Response does not contain 'id'"

    def test_deposit_account(self, deposit_account, create_user_account):
        initial_balance_1 = create_user_account.json()["balance"]
        account_amount = initial_balance_1 + AMOUNT

        assert deposit_account.json()['balance'] == account_amount, f"Deposit amount is not equal to {account_amount}"

    def test_account_transfer_between(
            self,
            deposit_account,
            account_transfer,
            second_user_account,
    ):
        account_id_1 = deposit_account.json()["id"]
        account_id_2 = second_user_account.json()["id"]
        account_amount_1 = deposit_account.json()["balance"]

        assert account_transfer.json()["fromAccountId"] == account_id_1
        assert account_transfer.json()["toAccountId"] == account_id_2
        assert account_transfer.json()["fromAccountIdBalance"] == account_amount_1 - TRANSFER_AMOUNT

    def test_get_transactions_history(self, transactions_history):
        transaction_id = transactions_history.json()["transactions"][0]["transactionId"]

        assert transaction_id in [t["transactionId"] for t in transactions_history.json()["transactions"]]
