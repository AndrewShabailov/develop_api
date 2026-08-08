import requests
import pytest
from src.main.api.data.data import *
from src.main.api.config import *


@pytest.fixture
def user_name():
    user_name = f"m{random.randint(1, 100)}q{random.randint(100, 9999)}x"
    return user_name

@pytest.fixture
def admin_token(login_admin):
    admin_token = login_admin.json().get("token")
    print(f"admin_token: {admin_token}")
    return admin_token

@pytest.fixture
def user_token(login_user):
    user_token = login_user.json().get("token")
    print(f"user_token: {user_token}")
    return user_token

@pytest.fixture
def login_admin():
    response = requests.post(
        url=f"{BASE_URL}{AUTH_LOGIN}",
        json={
            "username": ADMIN_USERNAME,
            "password": ADMIN_PASSWORD
        }
    )
    print(f"login_admin_response: {response}")
    return response

@pytest.fixture
def login_user(admin_token, user_name):
    requests.post(
        url=f"{BASE_URL}{ADMIN_CREATE}",
        json={
            "username": user_name,
            "password": USER_PASSWORD,
            "role": "ROLE_USER"
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {admin_token}"
        }
    )
    response = requests.post(
        url=f"{BASE_URL}{AUTH_LOGIN}",
        json={
            "username": user_name,
            "password": USER_PASSWORD,
        }
    )
    print(f"login_user response: {response}")
    return response

@pytest.fixture
def create_user(admin_token, user_name):
    response = requests.post(
        url=f"{BASE_URL}{ADMIN_CREATE}",
        json={
            "username": user_name,
            "password": USER_PASSWORD,
            "role": "ROLE_USER"
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {admin_token}"
        }
    )
    print(f"create_user response: {response.text}")
    return response

@pytest.fixture
def create_user_account(create_user, user_token):
    response = requests.post(
        f"{BASE_URL}{ACCOUNT_CREATE}",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {user_token}"
        }
    )
    return response

@pytest.fixture
def second_user_account(create_user, user_token):
    response = requests.post(
        f"{BASE_URL}{ACCOUNT_CREATE}",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {user_token}"
        }
    )
    return response

@pytest.fixture
def create_deposit(create_user_account, user_token):
    response = requests.post(
        url=f"{BASE_URL}{ACCOUNT_DEPOSIT}",
        json={
            "accountId": create_user_account.json()["id"],
            "amount": AMOUNT
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {user_token}"
        }
    )
    return response

@pytest.fixture
def create_transfer(create_user_account, second_user_account, user_token, create_deposit):
    account_id_1 = create_user_account.json()["id"]
    account_id_2 = second_user_account.json().get("id")

    response = requests.post(
        url=f"{BASE_URL}{ACCOUNT_TRANSFER}",
        json={
            "fromAccountId": account_id_1,
            "toAccountId": account_id_2,
            "amount": TRANSFER_AMOUNT
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {user_token}"
        }
    )
    return response

@pytest.fixture
def transactions_history(create_transfer, user_token):
    account_id = create_transfer.json().get("fromAccountId")
    response = requests.get(
        url=f"{BASE_URL}{ACCOUNT_TRANSACTIONS}{account_id}",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {user_token}"
        }
    )
    print(f"transactions_history response: {response.json()}")
    return response
