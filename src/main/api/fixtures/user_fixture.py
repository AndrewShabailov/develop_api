import pytest
import random

from typing import Any
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator


@pytest.fixture
def create_user_request(api_manager: ApiManager, created_obj: CreateUserRequest) -> CreateUserRequest:
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    response = api_manager.admin_steps.create_user(user_request)
    created_obj.append(response)
    return user_request

@pytest.fixture
def credit_user_request(api_manager: ApiManager) -> CreateUserRequest:
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.credit_user(user_request)
    return user_request

@pytest.fixture
def credit_account(api_manager: ApiManager, credit_user_request: CreateUserRequest) -> CreateAccountResponse:
    return api_manager.user_steps.create_account(credit_user_request)

@pytest.fixture
def new_account(api_manager: ApiManager, create_user_request: CreateUserRequest):
    return api_manager.user_steps.create_account(create_user_request)

@pytest.fixture
def deposit_data(new_account: CreateAccountResponse):
    amount = RandomModelGenerator._generate_deposit_amount(int)
    return {
        "amount": amount,
        "expected_balance": new_account.balance + amount
    }

@pytest.fixture
def credit_data():
    return {
        "amount": random.randint(5000, 15000),
        "term_months": random.randint(1, 12),
        "invalid_credit_amount": random.randint(15000, 150000),
        "invalid_repay_amount": 1
    }

@pytest.fixture
def account_with_deposit(api_manager: ApiManager, create_user_request: CreateUserRequest):
    account_1 = api_manager.user_steps.create_account(create_user_request)
    deposit = RandomModelGenerator._generate_deposit_amount(int)

    deposit_response = api_manager.user_steps.deposit_account(
        create_user_request,
        account_id=account_1.id,
        amount=deposit
    )
    return {
        "account_id": account_1.id,
        "balance": deposit_response.balance
    }

@pytest.fixture
def destination_account(api_manager: ApiManager, create_user_request: CreateUserRequest):
    account_2 = api_manager.user_steps.create_account(create_user_request)
    return account_2.id

@pytest.fixture
def transfer_data(account_with_deposit: dict[str, Any]):
    account_1_balance = account_with_deposit["balance"]
    transfer_amount = random.randint(500, int(account_1_balance))

    return {
        "amount": transfer_amount,
        "expected_balance": account_1_balance - transfer_amount
    }

@pytest.fixture
def active_credit(
        api_manager: ApiManager,
        credit_user_request: CreateUserRequest,
        credit_account: CreateAccountResponse,
        credit_data: dict
):
    credit_response = api_manager.user_steps.credit_user_request(
        create_user_request=credit_user_request,
        account_id=credit_account.id,
        amount=credit_data["amount"],
        term_months=credit_data["term_months"]
    )
    return {
        "user_request": credit_user_request,
        "account_id": credit_account.id,
        "credit_response": credit_response
    }
