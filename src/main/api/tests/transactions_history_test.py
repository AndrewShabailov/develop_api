class TestTransactionsHistory:
    def test_transactions_history(self, transactions_history):
        assert transactions_history.status_code == 200
        assert transactions_history.json() is not None, "History is empty"