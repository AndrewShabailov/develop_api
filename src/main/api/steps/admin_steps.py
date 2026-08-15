from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class AdminSteps(BaseSteps):
    def create_user(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=self.username, password=self.password),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_ok()
        ).post(create_user_request)

        self.created_obj.append(response)
        return response

    def credit_user(self, create_user_request: CreateUserRequest):
        create_user_request.role = "ROLE_CREDIT_SECRET"
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=self.username, password=self.password),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_ok()
        ).post(create_user_request)

        self.created_obj.append(response)
        return response

    def delete_user(self, user_id: int):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=self.username, password=self.password),
            Endpoint.ADMIN_DELETE_USER,
            ResponseSpecs.request_ok()
        ).delete(user_id)
        return response

    def delete_all_users(self):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=self.username, password=self.password),
            Endpoint.ADMIN_DELETE_ALL_USERS,
            ResponseSpecs.request_ok()
        ).delete()
        return response

    def create_invalid_user(self, create_user_request: CreateUserRequest):
        CrudRequester(
            RequestSpecs.auth_headers(username=self.username, password=self.password),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_bad()
        ).post(create_user_request)

    def login_user(self, login_user_request: LoginUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.unauth_headers(),
            Endpoint.LOGIN_USER,
            ResponseSpecs.request_ok()
        ).post(login_user_request)
        return response

    def get_users(self):
        return ValidateCrudRequester(
            RequestSpecs.auth_headers(username=self.username, password=self.password),
            Endpoint.ADMIN_GET_USERS,
            ResponseSpecs.request_ok()
        ).get()
