import pytest
from src.main.api.config import *
from src.main.api.data.data import *
from src.main.api.utils.request import delete, get, post

@pytest.fixture
def user_name():
    return f"m{random.randint(1, 100)}q{random.randint(100, 9999)}x"

@pytest.fixture
def credit_user_name():
    return f"credit{random.randint(1, 100)}q{random.randint(100, 9999)}x"

@pytest.fixture
def login_user(admin_token, user_name):
    post(
        ADMIN_CREATE,
        json={
            "username": user_name,
            "password": USER_PASSWORD,
            "role": ROLE_USER
        },
        token=admin_token,
    )
    response = post(
        AUTH_LOGIN,
        json={
            "username": user_name,
            "password": USER_PASSWORD
        }
    )
    return response

@pytest.fixture
def login_admin():
    return post(
        AUTH_LOGIN,
        json={
            "username": ADMIN_USERNAME,
            "password": ADMIN_PASSWORD
        }
    )

@pytest.fixture
def admin_token(login_admin):
    return login_admin.json().get("token")

@pytest.fixture
def user_token(create_user, user_name):
    response = post(
        AUTH_LOGIN,
        json={"username": user_name, "password": USER_PASSWORD}
    )
    return response.json().get("token")

@pytest.fixture
def credit_token(create_credit_user, credit_user_name):
    response = post(
        AUTH_LOGIN,
        json={"username": credit_user_name, "password": USER_PASSWORD}
    )
    return response.json().get("token")

@pytest.fixture
def create_user(admin_token, user_name):
    return post(
        ADMIN_CREATE,
        json={
            "username": user_name,
            "password": USER_PASSWORD,
            "role": ROLE_USER
        },
        token=admin_token
    )

@pytest.fixture
def create_credit_user(admin_token, credit_user_name):
    return post(
        ADMIN_CREATE,
        json={
            "username": credit_user_name,
            "password": USER_PASSWORD,
            "role": ROLE_CREDIT_SECRET
        },
        token=admin_token
    )


@pytest.fixture
def create_user_account(user_token):
    return post(
        ACCOUNT_CREATE,
        token=user_token,
        expected_status=201
    )

@pytest.fixture
def second_user_account(user_token):
    return post(
        ACCOUNT_CREATE,
        token=user_token,
        expected_status=201
    )

@pytest.fixture
def create_credit_user_account(credit_token):
    return post(
        ACCOUNT_CREATE,
        token=credit_token,
        expected_status=201
    )

@pytest.fixture
def create_deposit(create_user_account, user_token):
    return post(
        ACCOUNT_DEPOSIT,
        json={
            "accountId": create_user_account.json()["id"],
            "amount": AMOUNT
        },
        token=user_token
    )

@pytest.fixture
def create_transfer(create_user_account, second_user_account, user_token, create_deposit):
    return post(
        ACCOUNT_TRANSFER,
        json={
            "fromAccountId": create_user_account.json()["id"],
            "toAccountId": second_user_account.json()["id"],
            "amount": TRANSFER_AMOUNT
        },
        token=user_token
    )

@pytest.fixture
def transactions_history(create_transfer, user_token):
    account_id = create_transfer.json().get("fromAccountId")
    return get(
        f'{ACCOUNT_TRANSACTIONS}{account_id}',
        token=user_token,
        expected_status=200
    )

@pytest.fixture
def all_users(admin_token):
    return get(ALL_USERS, token=admin_token)

@pytest.fixture
def delete_user(create_user, admin_token):
    return delete(
        f"{DELETE_USER}{create_user.json()['id']}",
        token=admin_token
    )

@pytest.fixture
def delete_all_users(admin_token):
    return delete(DELETE_ALL_USERS, token=admin_token)

@pytest.fixture
def credit_request(create_credit_user_account, credit_token):
    response =  post(
        CREDIT_REQUEST,
        json={
            "accountId": create_credit_user_account.json()["id"],
            "amount": CREDIT_AMOUNT,
            "termMonths": TERM_MONTHS
        },
        token=credit_token,
        expected_status=201
    )
    print(response.json())
    return response

@pytest.fixture
def credit_repay(credit_request, credit_token, create_credit_user_account):
    account_id = create_credit_user_account.json()["id"]
    response = post(
        CREDIT_REPAY,
        json={
                "creditId": credit_request.json()["creditId"],
                "accountId": account_id,
                "amount": credit_request.json()["amount"]
        },
        token=credit_token
        )
    return response

@pytest.fixture
def credit_history(credit_request, credit_token, create_credit_user_account):
    response = get(
        CREDIT_HISTORY,
        token=credit_token
    )
    return response
