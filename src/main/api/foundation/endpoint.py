from enum import Enum
from typing import Optional, Type, List, Any

from src.main.api.models.account_transactions_response import AccountTransactionsResponse
from src.main.api.models.base_model import BaseModel
from dataclasses import dataclass
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.deposit_account_response import DepositAccountResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.models.transfer_account_response import TransferAccountResponse


@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Any]


class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model = CreateUserRequest,
        url = "/admin/create",
        response_model = CreateUserResponse
    )

    ADMIN_DELETE_USER = EndpointConfiguration(
        request_model = None,
        url = "/admin/users",
        response_model = None
    )

    ADMIN_DELETE_ALL_USERS = EndpointConfiguration(
        request_model=None,
        url="/admin/users",
        response_model=None
    )

    LOGIN_USER = EndpointConfiguration(
        request_model = LoginUserRequest,
        url = "/auth/token/login",
        response_model = LoginUserResponse
    )

    CREATE_ACCOUNT = EndpointConfiguration(
        request_model = None,
        url = "/account/create",
        response_model = CreateAccountResponse
    )

    DEPOSIT_ACCOUNT = EndpointConfiguration(
        request_model=DepositAccountRequest,
        url="/account/deposit",
        response_model=DepositAccountResponse
    )

    TRANSFER_ACCOUNT = EndpointConfiguration(
        request_model=TransferAccountRequest,
        url="/account/transfer",
        response_model=TransferAccountResponse
    )

    GET_ACCOUNT_TRANSACTIONS = EndpointConfiguration(
        request_model=None,
        url="/account/transactions",
        response_model=AccountTransactionsResponse
    )

    CREDIT_REQUEST = EndpointConfiguration(
        request_model = CreditRequest,
        url="/credit/request",
        response_model=CreditResponse
    )

    ADMIN_GET_USERS = EndpointConfiguration(
        request_model=None,
        url="/admin/users",
        response_model=List[CreateUserResponse]
    )
