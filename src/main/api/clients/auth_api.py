from src.main.api.config import AUTH_LOGIN
from src.main.api.utils.request import post


class AuthApi:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        response = post(
            AUTH_LOGIN,
            json={
                "username": self.username,
                "password": self.password
            }
        )
        return response
