from src.main.api.configs.config import Config
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.base_model import BaseModel
from typing import Optional
from pydantic import TypeAdapter
import allure



class ValidateCrudRequester(HttpRequester):
    def __init__(self, request_spec, endpoint, response_spec):
        super().__init__(request_spec, endpoint, response_spec)
        self.crud_requester = CrudRequester(
            request_spec=request_spec,
            endpoint=endpoint,
            response_spec=response_spec
        )

    def _validate(self, response):
        model = self.endpoint.value.response_model
        if model is None:
            return response
        return TypeAdapter(model).validate_python(response.json())

    def post(self, model: Optional[BaseModel] = None):
        response = self._validate(self.crud_requester.post(model))
        with allure.step(f'POST {Config.fetch("backendUrl")}{self.endpoint.value.url} and Validated Model'):
            allure.attach(f'Validated Model response: {self.endpoint.value.response_model.__name__}')
        return response


    def get(self, entity_id: Optional[int] = None):
        return self._validate(self.crud_requester.get(entity_id))

    def delete(self, entity_id: Optional[int] = None):
        return self._validate(self.crud_requester.delete(entity_id))
