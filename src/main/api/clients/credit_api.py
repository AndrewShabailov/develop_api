from src.main.api.config import CREDIT_REPAY, CREDIT_REQUEST, CREDIT_HISTORY
from src.main.api.utils.request import post, get


class CreditApi:
    def __init__(self, token):
        self.token = token

    def request_credit(self, account_id, amount, term_months):
        response = post(
            CREDIT_REQUEST,
            json={
                "accountId": account_id,
                "amount": amount,
                "termMonths": term_months
            },
            token=self.token,
            expected_status=201
        )
        return response

    def repay_credit(self, credit_id, account_id, amount):
        response = post(
            CREDIT_REPAY,
            json={
                "creditId": credit_id,
                "accountId": account_id,
                "amount": amount
            },
            token=self.token
        )
        return response

    def get_credit_history(self):
        response = get(
            CREDIT_HISTORY,
            token=self.token
        )
        return response
