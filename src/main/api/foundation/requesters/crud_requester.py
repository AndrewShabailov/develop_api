import requests
import allure

from src.main.api.configs.config import Config
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.models.base_model import BaseModel
from typing import Optional, Union
from requests import Response


class CrudRequester(HttpRequester):
    def post(self, model: Optional[Union[BaseModel, dict]]) -> Response:
        if model is None:
            body = None
        elif isinstance(model, dict):
            body = model
        else:
            body = model.model_dump()

        with allure.step(f'POST {Config.fetch("backendUrl")}{self.endpoint.value.url}'):
            allure.attach(str(body), "Request body", allure.attachment_type.JSON)
        response = requests.post(
            url=self._url(),
            headers=self.request_spec,
            json=body
        )

        allure.attach(
            response.text,
            "Response body",
            allure.attachment_type.JSON
        )
        self.response_spec(response)
        return response

    def get(self, entity_id: Optional[int] = None) -> Response:

        allure.step(f'GET {Config.fetch("backendUrl")}{self.endpoint.value.url}')

        response = requests.get(
            url=self._url(entity_id),
            headers=self.request_spec
        )
        self.response_spec(response)
        allure.attach(
            response.text,
            "Response body",
            allure.attachment_type.JSON
        )
        return response

    def delete(self, entity_id: Optional[int] = None) -> Response:
        allure.step(f'GET {Config.fetch("backendUrl")}{self.endpoint.value.url}')
        response = requests.delete(
            url=self._url(entity_id),
            headers=self.request_spec
        )
        self.response_spec(response)
        allure.attach(
            response.text,
            "Response body",
            allure.attachment_type.JSON
        )
        return response
