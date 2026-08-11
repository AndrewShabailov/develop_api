import pytest
from src.main.api.clients.account_api import AccountApi
from src.main.api.clients.admin_api import AdminApi
from src.main.api.data.data import *
from src.main.api.clients.credit_api import CreditApi
from src.main.api.clients.auth_api import AuthApi

@pytest.fixture
def user_name():
    return f"m{random.randint(1, 100)}q{random.randint(100, 9999)}x"

@pytest.fixture
def credit_user_name():
    return f"credit{random.randint(1, 100)}q{random.randint(100, 9999)}x"

@pytest.fixture
def login_user(admin_token, user_name):
    admin_api = AdminApi(admin_token)
    admin_api.admin_create(
        username=user_name,
        password=USER_PASSWORD,
        role=ROLE_USER
    )
    auth_api = AuthApi(user_name, USER_PASSWORD)
    response = auth_api.login()
    return response

@pytest.fixture
def login_admin():
    auth_api = AuthApi(ADMIN_USERNAME, ADMIN_PASSWORD)
    response = auth_api.login()
    return response

@pytest.fixture
def admin_token():
    auth_api = AuthApi(ADMIN_USERNAME, ADMIN_PASSWORD)
    response = auth_api.login()
    return response.json().get("token")

@pytest.fixture
def user_token(create_user, user_name):
    auth_api = AuthApi(user_name, USER_PASSWORD)
    response = auth_api.login()
    return response.json().get("token")

@pytest.fixture
def credit_token(create_credit_user, credit_user_name):
    auth_api = AuthApi(credit_user_name, USER_PASSWORD)
    response = auth_api.login()
    return response.json().get("token")

@pytest.fixture
def get_all_users(admin_token):
    admin_api = AdminApi(admin_token)
    response = admin_api.get_all_users()
    return response

@pytest.fixture
def create_user(admin_token, user_name):
    admin_api = AdminApi(admin_token)
    response = admin_api.admin_create(
        username=user_name,
        password=USER_PASSWORD,
        role=ROLE_USER
    )
    return response

@pytest.fixture
def create_credit_user(admin_token, credit_user_name):
    admin_api = AdminApi(admin_token)
    response = admin_api.admin_create(
        username=credit_user_name,
        password=USER_PASSWORD,
        role=ROLE_CREDIT_SECRET
    )
    return response

@pytest.fixture
def create_user_account(user_token):
    account_api = AccountApi(user_token)
    response = account_api.account_create()
    return response

@pytest.fixture
def second_user_account(user_token):
    account_api = AccountApi(user_token)
    response = account_api.account_create()
    return response

@pytest.fixture
def create_credit_user_account(credit_token):
    account_api = AccountApi(credit_token)
    response = account_api.account_create()
    return response

@pytest.fixture
def deposit_account(create_user_account, user_token):
    account_api = AccountApi(user_token)
    response = account_api.account_deposit(
        account_id=create_user_account.json()["id"],
        amount=AMOUNT
    )
    return response

@pytest.fixture
def account_transfer(deposit_account, second_user_account, user_token):
    account_api = AccountApi(user_token)
    response = account_api.account_transfer(
        from_account_id=deposit_account.json()["id"],
        to_account_id=second_user_account.json()["id"],
        amount=TRANSFER_AMOUNT
    )
    return response

@pytest.fixture
def transactions_history(account_transfer, user_token):
    account_id = account_transfer.json().get("fromAccountId")
    account_api = AccountApi(user_token)
    response = account_api.get_account_transactions(
        account_id=account_id
    )
    return response

@pytest.fixture
def delete_all_users(admin_token):
    admin_api = AdminApi(admin_token)
    response = admin_api.delete_all_users()
    return response

@pytest.fixture
def delete_user(create_user, admin_token):
    admin_api = AdminApi(admin_token)
    response = admin_api.delete_user(create_user.json()["id"])
    return response

@pytest.fixture
def credit_request(create_credit_user_account, credit_token):
    credit_api = CreditApi(credit_token)
    response = credit_api.request_credit(
        account_id=create_credit_user_account.json()["id"],
        amount=CREDIT_AMOUNT,
        term_months=TERM_MONTHS
    )
    return response

@pytest.fixture
def credit_repay(credit_request, credit_token, create_credit_user_account):
    credit_api = CreditApi(credit_token)
    account_id = create_credit_user_account.json()["id"]
    response = credit_api.repay_credit(
        credit_id=credit_request.json()["creditId"],
        account_id=account_id,
        amount=credit_request.json()["amount"]
    )
    return response

@pytest.fixture
def credit_history(credit_request, credit_token, create_credit_user_account):
    credit_api = CreditApi(credit_token)
    response = credit_api.get_credit_history()
    return response
