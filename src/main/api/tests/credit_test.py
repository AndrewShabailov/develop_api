import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.fixtures.user_fixture import credit_user_request, active_credit
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestCredit:
    @pytest.mark.known_bug("Expected 'accountId' instead of 'id' in response")
    def test_credit_request(
            self,
            api_manager: ApiManager,
            credit_user_request: CreateUserRequest,
            credit_account: CreateAccountResponse,
            credit_data: dict
    ):

        response = api_manager.user_steps.credit_user_request(
            create_user_request=credit_user_request,
            account_id=credit_account.id,
            amount=credit_data["amount"],
            term_months=credit_data["term_months"]
        )

        assert response.id == credit_account.id, f"Wrong {response.id}"
        assert response.amount == response.balance, f"Wrong {response.amount}"

    def test_credit_repay(
            self,
            api_manager: ApiManager,
            active_credit: dict
    ):

        repay_response = api_manager.user_steps.credit_repay(
            create_user_request=active_credit["user_request"],
            credit_id=active_credit["credit_response"].creditId,
            account_id=active_credit["account_id"],
            amount=active_credit["credit_response"].amount
        )

        assert active_credit["credit_response"].amount == repay_response.amountDeposited, \
            (f"Amount mismatch! Expected: {active_credit['credit_response'].amount},"
             f" got: {repay_response.amountDeposited}")
        assert active_credit["credit_response"].creditId == repay_response.creditId, \
            (f"Credit ID mismatch! Expected: {active_credit['credit_response'].creditId},"
             f" got: {repay_response.creditId}")


    def test_credit_history(
            self,
            api_manager: ApiManager,
            active_credit: dict
    ):

        credit_id = active_credit["credit_response"].creditId
        credit_history = api_manager.user_steps.get_credit_history(active_credit["user_request"])
        assert credit_id in [credit.creditId for credit in credit_history.credits],\
            f"No {credit_id} in credit history"

    @pytest.mark.known_bug('This test should return 422 status code. 400 - temporary solution')
    def test_negative_credit_request_with_over_amount(
            self,
            api_manager: ApiManager,
            credit_account: CreateAccountResponse,
            credit_user_request: CreateUserRequest,
            credit_data: dict
    ):

        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=credit_user_request.username,
                password=credit_user_request.password,
            ),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_bad()
        ).post(
            {
                "accountId": credit_account.id,
                "amount": credit_data["invalid_credit_amount"],
                "termMonths": credit_data["term_months"]
            }
        )

        assert response.json()["error"] == "Amount must be between 5000 and 15000"

    @pytest.mark.known_bug(
        "This test returned wrong error."
        "Expected message - 'Repayment amount exceeds remaining debt'"
    )
    def test_negative_credit_repay_with_less_amount(
            self,
            api_manager: ApiManager,
            credit_user_request: CreateUserRequest,
            active_credit: dict,
            credit_data: dict
    ):

        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=credit_user_request.username,
                password=credit_user_request.password,
            ),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_unprocessable_entity()
        ).post(
            {
                "creditId": active_credit["credit_response"].creditId,
                "accountId": active_credit["account_id"],
                "amount": credit_data["invalid_repay_amount"]
            }
        )

        assert response.json()["error"] == (f"The amount is not enough."
                                            f" Credit balance: -{int(active_credit["credit_response"].balance)}"),\
            "Wrong error details"

    @pytest.mark.known_bug(
        "This test returned wrong error."
        "Expected message - 'Access denied'")
    def test_negative_get_credit_history_with_admin_role(self, api_manager: ApiManager):

        response = CrudRequester(
            api_manager.admin_steps.auth,
            Endpoint.GET_CREDIT_HISTORY,
            ResponseSpecs.request_forbidden()
        ).get()

        assert response.json()["detail"] == "Forbidden: ROLE_CREDIT access required", "Wrong error details"
