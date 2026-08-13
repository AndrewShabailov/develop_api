import pytest
from src.main.api.configs.config import CREDIT_REQUEST, CREDIT_REPAY, CREDIT_HISTORY
from src.main.api.utils.request import post, get


class TestCredit:
    def test_credit_request(self, credit_request, create_credit_user_account):
        assert credit_request.json()["id"] == create_credit_user_account.json()["id"]
        assert credit_request.json()["amount"] == credit_request.json()["balance"]

    def test_credit_repay(self, credit_repay, credit_request):
        assert credit_request.json()["amount"] == credit_repay.json()["amountDeposited"]

    def test_credit_history(self, credit_request, credit_history):
        credit_id = credit_request.json()["creditId"]
        assert credit_id in [credit["creditId"] for credit in credit_history.json()["credits"]]

    @pytest.mark.known_bug('This test should return 422 status code. 400 - temporary solution')
    def test_credit_request_negative(self, create_credit_user_account, credit_token):
        response = post(
            CREDIT_REQUEST,
            {
                "accountId": create_credit_user_account.json()["id"],
                "amount": 25000,
                "termMonths": 12
            },
            token=credit_token,
            expected_status=400
        )
        assert response.json()["error"] == "Amount must be between 5000 and 15000"

    @pytest.mark.known_bug(
        "This test returned wrong error."
        "Expected message - 'Repayment amount exceeds remaining debt'"
    )
    def test_credit_repay_negative(self, credit_request, create_credit_user_account, credit_token):
        response = post(
            CREDIT_REPAY,
            json={
                "creditId": credit_request.json()["creditId"],
                "accountId": create_credit_user_account.json()["id"],
                "amount": 1
            },
            token=credit_token,
            expected_status=422
        )
        assert response.json()["error"] == (f"The amount is not enough."
                                            f" Credit balance: -{credit_request.json()['balance']}")

    @pytest.mark.known_bug(
        "This test returned wrong error."
        "Expected message - 'Access denied'")
    def test_credit_history_negative(self, admin_token):
        response = get(
            CREDIT_HISTORY,
            token=admin_token,
            expected_status=403
        )
        assert '403 Forbidden' in response.text

