import pytest
import random
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator
from typing import Any

@pytest.fixture
def create_user_request(api_manager: ApiManager, created_obj: CreateUserRequest) -> CreateUserRequest:
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    response = api_manager.admin_steps.create_user(user_request)
    created_obj.append(response)
    return user_request

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

