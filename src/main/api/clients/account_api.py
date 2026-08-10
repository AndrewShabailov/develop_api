from src.main.api.config import ACCOUNT_CREATE, ACCOUNT_DEPOSIT, ACCOUNT_TRANSFER, ACCOUNT_TRANSACTIONS
from src.main.api.utils.request import post, get


class AccountApi:
    def __init__(self, token):
        self.token = token

    def account_create(self):
        response = post(
            ACCOUNT_CREATE,
            token=self.token,
            expected_status=201
        )
        return response

    def account_deposit(self, account_id, amount):
        response = post(
            ACCOUNT_DEPOSIT,
            json={
                "accountId": account_id ,
                "amount": amount
            },
            token=self.token
        )
        return response

    def account_transfer(self, from_account_id, to_account_id, amount):
        response = post(
            ACCOUNT_TRANSFER,
            json={
                "fromAccountId": from_account_id,
                "toAccountId": to_account_id,
                "amount": amount
            },
            token=self.token
        )
        return response

    def get_account_transactions(self, account_id):
        response = get(
            f"{ACCOUNT_TRANSACTIONS}{account_id}",
            token=self.token
        )
        return response
