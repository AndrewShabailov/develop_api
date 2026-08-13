import requests
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.models.base_model import BaseModel
from typing import Optional
from requests import Response


class CrudRequester(HttpRequester):
    def post(self, model: Optional[BaseModel]) -> Response:
        body = model.model_dump() if model is not None else None

        response = requests.post(
            url=self._url(),
            headers=self.request_spec,
            json=body
        )
        self.response_spec(response)
        return response

    def get(self, entity_id: Optional[int] = None) -> Response:
        response = requests.get(
            url=self._url(entity_id),
            headers=self.request_spec
        )
        self.response_spec(response)
        return response

    def delete(self, entity_id: Optional[int] = None) -> Response:
        response = requests.delete(
            url=self._url(entity_id),
            headers=self.request_spec
        )
        self.response_spec(response)
        return response
