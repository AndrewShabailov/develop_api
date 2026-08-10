from src.main.api.config import ADMIN_CREATE, ALL_USERS, DELETE_ALL_USERS, DELETE_USER
from src.main.api.utils.request import post, get, delete


class AdminApi:
    def __init__(self, token):
        self.token = token

    def admin_create(self, username, password, role):
        response = post(
            ADMIN_CREATE,
            json={
                "username": username,
                "password": password,
                "role": role
            },
            token=self.token
        )
        return response

    def get_all_users(self):
        response = get(
            ALL_USERS,
            token=self.token
        )
        return response

    def delete_all_users(self):
        response = delete(
            DELETE_ALL_USERS,
            token=self.token
        )
        return response

    def delete_user(self, id_to_delete):
        response = delete(
            f"{DELETE_USER}{id_to_delete}",
            token=self.token
        )
        return response
