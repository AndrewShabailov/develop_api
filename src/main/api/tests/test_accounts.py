import pytest
from conftest import credit_token
from src.main.api.config import ACCOUNT_CREATE, ACCOUNT_DEPOSIT, ACCOUNT_TRANSFER, ACCOUNT_TRANSACTIONS
from src.main.api.data.data import AMOUNT, TRANSFER_AMOUNT
from src.main.api.utils.request import post, get


class TestCreateAccount:
    def test_create_account(self, create_user_account):

        assert create_user_account.json()['balance'] == 0, "Initial balance is NOT 0"
        assert "id" in create_user_account.json(), "Response does not contain 'id'"

    def test_deposit_account(self, deposit_account, create_user_account):
        initial_balance_1 = create_user_account.json()["balance"]
        account_amount = initial_balance_1 + AMOUNT

        assert deposit_account.json()['balance'] == account_amount, f"Deposit amount is not equal to {account_amount}"

    def test_account_transfer(
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

    def test_create_account_negative(self, admin_token):
        response = post(
            ACCOUNT_CREATE,
            token=admin_token,
            expected_status=403
        )
        assert response.json()["error"] == "Admins cannot create bank accounts"

    @pytest.mark.known_bug('Response has wrong JSON key "message". Expected: "error"')
    def test_deposit_account_negative(self, create_user_account):
        response = post(
            ACCOUNT_DEPOSIT,
            json={
                "accountId": create_user_account.json()["id"],
                "amount": 9000
            },
            expected_status=401
        )
        assert response.json()["message"] == "JWT Token not found"

    @pytest.mark.known_bug('Response has wrong "error". Expected: "Invalid request body"')
    def test_account_transfer_negative(
            self,
            credit_token,
            deposit_account,
            second_user_account,
    ):
        response = post(
            ACCOUNT_TRANSFER,
            json={
                "fromAccountId": deposit_account.json()["id"],
                "toAccountId": second_user_account.json()["id"],
                "amount": 0
            },
            token=credit_token,
            expected_status=400
        )
        print(response.json())
        assert response.json()["error"] == ("Amount must be greater than 0\n"
                                            "Amount must be between 500 and 10000")

    def test_get_transactions_history_negative(self, credit_token):
       response = get(
           f"{ACCOUNT_TRANSACTIONS}{0}",
           token=credit_token,
           expected_status=400
       )
       assert response.json()["error"] == "Invalid account ID format"
