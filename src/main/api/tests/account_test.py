import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.user_fixture import destination_account, account_with_deposit
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from sqlalchemy.orm.session import Session


class TestCreateAccount:
    def test_admin_creates_new_account(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest
    ):
        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0.0, "Initial balance is NOT 0.0"
        assert response.id is not None, "Response does not contain 'id'"

        account_from_db = Account.get_account_by_id(db_session, response.id)

        assert account_from_db.id == response.id, "Account is not created in DB"
        assert account_from_db.balance is not None, "Balance is not created in DB"


    def test_user_deposits_to_his_account(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            new_account: CreateAccountResponse,
            deposit_data: dict
    ):

        deposit_response = api_manager.user_steps.deposit_account(
            create_user_request=create_user_request,
            account_id=new_account.id,
            amount=deposit_data["amount"]
        )

        assert deposit_response.balance == deposit_data["expected_balance"], \
            (f"Deposit failed! Expected balance: {deposit_data['expected_balance']},"
             f" but got: {deposit_response.balance}")


    def test_user_transfers_to_his_account(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            account_with_deposit: dict,
            destination_account: int,
            transfer_data: dict
    ):

        response = api_manager.user_steps.transfer_account(
            create_user_request,
            from_account_id=account_with_deposit["account_id"],
            to_account_id=destination_account,
            amount=transfer_data["amount"]
        )

        assert response.fromAccountId == account_with_deposit["account_id"], "Accounts have different id"
        assert response.toAccountId == destination_account, "Accounts have different id"
        assert response.fromAccountIdBalance == transfer_data["expected_balance"], \
            (f"Transfer balance check failed! Expected: {transfer_data['expected_balance']},"
             f" got: {response.fromAccountIdBalance}")


    def test_admin_get_account_transactions(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            account_with_deposit: dict
    ):

        response = api_manager.user_steps.get_account_transactions(
            create_user_request,
            account_id=account_with_deposit["account_id"]
        )

        transaction_id = response.transactions[0].transactionId

        assert len(response.transactions) > 0, "Transactions list is empty"
        assert transaction_id in [t.transactionId for t in response.transactions],\
            "Transaction id is not in transactions list"


    def test_negative_admin_creates_his_bank_account(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest
    ):

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
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            deposit_data: dict,
            new_account: CreateAccountResponse
    ):

        response = CrudRequester(
            RequestSpecs.base_headers(),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_unauthorized()
        ).post(
            DepositAccountRequest(
                accountId=new_account.id,
                amount=deposit_data["amount"]
            )
        )

        assert response.json()["message"] == "JWT Token not found",\
            f"Unexpected error message: {response.json()['message']}"

    @pytest.mark.known_bug('Response has wrong "error". Expected: "Invalid request body"')
    def test_negative_user_transfer_with_no_amount_in_body(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            account_with_deposit: dict,
            destination_account: int
    ):

        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.request_bad()
        ).post(
            {
                "fromAccountId": account_with_deposit["account_id"],
                "toAccountId": destination_account
            }
        )

        assert response.json()["error"] == "Amount is required",\
            f"Unexpected error: {response.json()['error']}"


    def test_negative_get_transactions_history_with_non_existing_user_id(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest
    ):

        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.GET_ACCOUNT_TRANSACTIONS,
            ResponseSpecs.request_bad()
        ).get(entity_id=0)

        assert response.json()["error"] == "Invalid account ID format",\
            f"Unexpected error: {response.json()['error']}"
