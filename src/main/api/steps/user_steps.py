from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest
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
            account_id: int,
            amount:float
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
            from_account_id: int,
            to_account_id: int,
            amount:float
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
            account_id: int
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

    def credit_user_request(
            self,
            create_user_request: CreateUserRequest,
            account_id: int,
            amount: float,
            term_months: int
    ):
        credit_payload = CreditRequest(
            accountId=account_id,
            amount=amount,
            termMonths=term_months
        )
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_created()
        ).post(credit_payload)
        return response

    def credit_repay(
            self,
            create_user_request: CreateUserRequest,
            credit_id: int,
            account_id: int,
            amount: float
    ):
        credit_repay_payload = CreditRepayRequest(
            creditId=credit_id,
            accountId=account_id,
            amount=amount
        )
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok()
        ).post(credit_repay_payload)
        return response

    def get_credit_history(
            self,
            create_user_request: CreateUserRequest
    ):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.GET_CREDIT_HISTORY,
            ResponseSpecs.request_ok()
        ).get()
        return response
