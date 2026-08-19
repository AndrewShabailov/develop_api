import requests
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.requests.requester import Requester


class CreateAccountRequester(Requester):
    def post(self, model=None) -> CreateAccountRequester:
        url=f"{self.base_url}/account/create"
        response = requests.post(
            url=url,
            headers=self.headers
    )
        self.response_spec(response)
        return CreateAccountResponse(**response.json())
