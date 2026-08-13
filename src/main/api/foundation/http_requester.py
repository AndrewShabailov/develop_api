from src.main.api.foundation.endpoint import Endpoint
from typing import Dict, Callable, Optional
from src.main.api.configs.config import Config


class HttpRequester:
    def __init__(self, request_spec: Dict[str, str], endpoint: Endpoint, response_spec: Callable):
        self.request_spec = request_spec
        self.endpoint = endpoint
        self.response_spec = response_spec

    def _url(self, entity_id: Optional[int] = None) -> str:
        url = f"{Config.fetch('backendUrl')}{self.endpoint.value.url}"
        return f"{url}/{entity_id}" if entity_id is not None else url
