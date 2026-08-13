from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.base_model import BaseModel
from typing import Optional
from pydantic import TypeAdapter


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
        return self._validate(self.crud_requester.post(model))

    def get(self, entity_id: Optional[int] = None):
        return self._validate(self.crud_requester.get(entity_id))

    def delete(self, entity_id: Optional[int] = None):
        return self._validate(self.crud_requester.delete(entity_id))
