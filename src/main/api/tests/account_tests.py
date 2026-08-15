import pytest
import random

from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestCreateAccount:
    def test_admin_creates_new_account(
            self,
            api_manager,
            create_user_request
    ):
        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0.0, "Initial balance is NOT 0.0"
        assert response.id is not None, "Response does not contain 'id'"

    def test_user_deposits_to_his_account(
            self,
            api_manager,
            create_user_request
    ):

        account_response = api_manager.user_steps.create_account(create_user_request)
        initial_balance= account_response.balance
        account_id = account_response.id
        deposit = random.randint(1000, 9000)
        expected_balance = initial_balance + deposit

        deposit_response = api_manager.user_steps.deposit_account(
            create_user_request,
            account_id=account_id,
            amount=deposit
        )
        assert deposit_response.balance == expected_balance,\
            f"Deposit failed! Expected balance: {expected_balance}, but got: {deposit_response.balance}"

    def test_user_transfers_to_his_account(
            self,
            api_manager,
            create_user_request
    ):
        account_response_1 = api_manager.user_steps.create_account(create_user_request)

        initial_balance = account_response_1.balance
        deposit = random.randint(1000, 9000)
        account_1_balance = initial_balance + deposit
        account_id_1 = account_response_1.id

        api_manager.user_steps.deposit_account(
            create_user_request,
            account_id=account_id_1,
            amount=deposit
        )
        transfer_amount = random.randint(500, int(account_1_balance))
        account_response_2 = api_manager.user_steps.create_account(create_user_request)
        account_id_2 = account_response_2.id

        response = api_manager.user_steps.transfer_account(
            create_user_request,
            from_account_id=account_id_1,
            to_account_id=account_id_2,
            amount=transfer_amount
        )
        assert response.fromAccountId == account_id_1
        assert response.toAccountId == account_id_2
        assert response.fromAccountIdBalance == account_1_balance - transfer_amount

    def test_admin_get_account_transactions(
            self,
            api_manager,
            create_user_request
    ):
        account_response = api_manager.user_steps.create_account(create_user_request)
        account_id = account_response.id

        deposit_amount = random.randint(1000, 9000)
        api_manager.user_steps.deposit_account(
            create_user_request,
            account_id=account_id,
            amount=deposit_amount
        )
        response = api_manager.user_steps.get_account_transactions(
            create_user_request,
            account_id=account_id
        )
        assert len(response.transactions) > 0, "Transactions list is empty"

        transaction_id = response.transactions[0].transactionId
        assert transaction_id in [t.transactionId for t in response.transactions]

    def test_negative_admin_create_his_bank_account(
            self,
            api_manager,
            create_user_request
    ):
        api_manager.user_steps.create_account(create_user_request)
        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=api_manager.admin_steps.username,
                password=api_manager.admin_steps.password
            ),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_forbidden()
        ).post(create_user_request)
        assert response.json()["error"] == "Admins cannot create bank accounts"

    @pytest.mark.known_bug('Response has wrong JSON key "message". Expected: "error"')
    def test_negative_user_deposits_to_his_account_with_no_token(
            self,
            api_manager,
            create_user_request
    ):
        account_response = api_manager.user_steps.create_account(create_user_request)
        account_id = account_response.id
        deposit = random.randint(1000, 9000)

        response = CrudRequester(
            RequestSpecs.base_headers(),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_unauthorized()
        ).post(
            DepositAccountRequest(
                accountId=account_id,
                amount=deposit
            )
        )
        assert response.json()["message"] == "JWT Token not found"

    @pytest.mark.known_bug('Response has wrong "error". Expected: "Invalid request body"')
    def test_negative_user_transfer_with_no_amount_in_body(
            self,
            api_manager,
            create_user_request
    ):
        account_response_1 = api_manager.user_steps.create_account(create_user_request)

        initial_balance = account_response_1.balance
        deposit = random.randint(1000, 9000)
        account_1_balance = initial_balance + deposit
        account_id_1 = account_response_1.id

        api_manager.user_steps.deposit_account(
            create_user_request,
            account_id=account_id_1,
            amount=deposit
        )
        account_response_2 = api_manager.user_steps.create_account(create_user_request)
        account_id_2 = account_response_2.id

        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.request_bad()
        ).post(
            {
                "fromAccountId": account_id_1,
                "toAccountId": account_id_2
            }
        )
        assert response.json()["error"] == "Amount is required"

    def test_negative_get_transactions_history_with_non_existing_user_id(
            self,
            api_manager,
            create_user_request
    ):
        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.GET_ACCOUNT_TRANSACTIONS,
            ResponseSpecs.request_bad()
        ).get(entity_id=0)

        assert response.json()["error"] == "Invalid account ID format"
