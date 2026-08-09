class TestCreditRequest:
    def test_credit_request(self, credit_request, create_credit_user_account):
        assert credit_request.json()["id"] == create_credit_user_account.json()["id"]
        assert credit_request.json()["amount"] == credit_request.json()["balance"]
