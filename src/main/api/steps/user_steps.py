from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(
            self,
            create_user_request: CreateUserRequest
    ):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response

    def deposit_account(
            self,
            create_user_request: CreateUserRequest,
            account_id,amount
    ):
        deposit_payload = DepositAccountRequest(
            accountId=account_id,
            amount=amount
        )
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_ok()
        ).post(deposit_payload)
        return response

    def transfer_account(
            self,
            create_user_request: CreateUserRequest,
            from_account_id,
            to_account_id,
            amount
    ):
        transfer_payload = TransferAccountRequest(
            fromAccountId=from_account_id,
            toAccountId=to_account_id,
            amount=amount
        )
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.request_ok()
        ).post(transfer_payload)
        return response

    def get_account_transactions(
            self,
            create_user_request: CreateUserRequest,
            account_id
    ):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.GET_ACCOUNT_TRANSACTIONS,
            ResponseSpecs.request_ok()
        ).get(entity_id=account_id)
        return response


