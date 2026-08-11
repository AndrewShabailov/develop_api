class TestCredit:
    def test_credit_request(self, credit_request, create_credit_user_account):
        assert credit_request.json()["id"] == create_credit_user_account.json()["id"]
        assert credit_request.json()["amount"] == credit_request.json()["balance"]

    def test_credit_repay(self, credit_repay, credit_request):
        assert credit_request.json()["amount"] == credit_repay.json()["amountDeposited"]

    def test_credit_history(self, credit_request, credit_history):
        credit_id = credit_request.json()["creditId"]
        print(credit_history.json())
        assert credit_id in [credit["creditId"] for credit in credit_history.json()["credits"]]
