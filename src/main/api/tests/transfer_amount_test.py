from src.main.api.data.data import TRANSFER_AMOUNT


class TestTransfer:
    def test_transfer_amount_between_own_accounts(
            self,
            create_transfer,
            create_user_account,
            second_user_account,
            create_deposit
    ):
        account_id_1 = create_user_account.json()["id"]
        account_id_2 = second_user_account.json()["id"]
        account_amount_1 = create_deposit.json()["balance"]

        assert create_transfer.status_code == 200
        assert create_transfer.json()["fromAccountId"] == account_id_1
        assert create_transfer.json()["toAccountId"] == account_id_2
        assert create_transfer.json()["fromAccountIdBalance"] == account_amount_1 - TRANSFER_AMOUNT
