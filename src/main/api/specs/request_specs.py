import requests
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.configs.config import Config


class RequestSpecs:

    @staticmethod
    def base_headers():
        return {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    @staticmethod
    def auth_headers(username: str, password: str):
        request = LoginUserRequest(username=username, password=password)
        response = requests.post(
            url=f"{Config.fetch('backendUrl')}/auth/token/login",
            json=request.model_dump(),
            headers=RequestSpecs.base_headers()
        )
        if response.status_code != 200:
            raise Exception(f"Failed to login: {response.status_code} {response.text}")

        token = LoginUserResponse(**response.json()).token
        headers = RequestSpecs.base_headers()
        headers["Authorization"] = f"Bearer {token}"
        return headers

    @staticmethod
    def unauth_headers():
        return RequestSpecs.base_headers()
