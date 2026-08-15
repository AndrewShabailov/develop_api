import random
import pytest

from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestCredit:
    @pytest.mark.known_bug("Expected 'accountId' instead of 'id' in response")
    def test_credit_request(
            self,
            api_manager,
            created_obj
    ):
        user_request = RandomModelGenerator.generate(CreateUserRequest)
        user_response = api_manager.admin_steps.credit_user(user_request)
        created_obj.append(user_response)

        account_response = api_manager.user_steps.create_account(user_request)
        account_id = account_response.id

        response = api_manager.user_steps.credit_user_request(
            create_user_request=user_request,
            account_id=account_id,
            amount=random.randint(5000, 15000),
            term_months=random.randint(1, 12)
        )
        assert response.id == account_id
        assert response.amount == response.balance


    def test_credit_repay(
            self,
            api_manager,
            created_obj
    ):
        user_request = RandomModelGenerator.generate(CreateUserRequest)
        user_response = api_manager.admin_steps.credit_user(user_request)
        created_obj.append(user_response)

        account_response = api_manager.user_steps.create_account(user_request)
        account_id = account_response.id

        credit_response = api_manager.user_steps.credit_user_request(
            create_user_request=user_request,
            account_id=account_id,
            amount=random.randint(5000, 15000),
            term_months=random.randint(1, 12)
        )

        credit_id = credit_response.creditId
        credit_amount = credit_response.amount

        repay_response = api_manager.user_steps.credit_repay(
            create_user_request=user_request,
            credit_id=credit_id,
            account_id=account_id,
            amount=credit_amount
        )
        assert credit_response.amount == repay_response.amountDeposited
        assert credit_id == repay_response.creditId

    def test_credit_history(
            self,
            api_manager,
            created_obj
    ):
        user_request = RandomModelGenerator.generate(CreateUserRequest)
        user_response = api_manager.admin_steps.credit_user(user_request)
        created_obj.append(user_response)

        account_response = api_manager.user_steps.create_account(user_request)
        account_id = account_response.id

        credit_response = api_manager.user_steps.credit_user_request(
            create_user_request=user_request,
            account_id=account_id,
            amount=random.randint(5000, 15000),
            term_months=random.randint(1, 12)
        )

        credit_id = credit_response.creditId
        credit_history = api_manager.user_steps.get_credit_history(create_user_request=user_request)
        assert credit_id in [credit.creditId for credit in credit_history.credits]

    @pytest.mark.known_bug('This test should return 422 status code. 400 - temporary solution')
    def test_negative_credit_request_with_over_amount(
            self,
            api_manager,
            created_obj
    ):
        user_request = RandomModelGenerator.generate(CreateUserRequest)
        user_response = api_manager.admin_steps.credit_user(user_request)
        created_obj.append(user_response)

        account_response = api_manager.user_steps.create_account(user_request)
        account_id = account_response.id

        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=user_request.username,
                password=user_request.password,
            ),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_bad()
        ).post(
            {
                "accountId": account_id,
                "amount": 25000,
                "termMonths": random.randint(1, 12)
            }
        )
        assert response.json()["error"] == "Amount must be between 5000 and 15000"

    @pytest.mark.known_bug(
        "This test returned wrong error."
        "Expected message - 'Repayment amount exceeds remaining debt'"
    )
    def test_credit_repay_with_less_amount(
            self,
            api_manager,
            created_obj
    ):
        user_request = RandomModelGenerator.generate(CreateUserRequest)
        user_response = api_manager.admin_steps.credit_user(user_request)
        created_obj.append(user_response)

        account_response = api_manager.user_steps.create_account(user_request)
        account_id = account_response.id

        credit_response = api_manager.user_steps.credit_user_request(
            create_user_request=user_request,
            account_id=account_id,
            amount=random.randint(5000, 15000),
            term_months=random.randint(1, 12)
        )

        credit_id = credit_response.creditId

        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=user_request.username,
                password=user_request.password,
            ),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_unprocessable_entity()
        ).post(
            {
                "creditId": credit_id,
                "accountId": account_id,
                "amount": 1
            }
        )
        print(response.json()["error"])
        assert response.json()["error"] == (f"The amount is not enough."
                                            f" Credit balance: -{int(credit_response.balance)}")

    @pytest.mark.known_bug(
        "This test returned wrong error."
        "Expected message - 'Access denied'")
    def test_negative_get_credit_history_with_admin_role(self, api_manager):

        response = CrudRequester(
            api_manager.admin_steps.auth,
            Endpoint.GET_CREDIT_HISTORY,
            ResponseSpecs.request_forbidden()
        ).get()
        assert response.json()["detail"] == "Forbidden: ROLE_CREDIT access required"
