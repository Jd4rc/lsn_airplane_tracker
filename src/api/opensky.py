from typing import Any

from api.base import BaseAPIClient, JSONData


class OpenSkyAPIClient(BaseAPIClient):
    """Клиент для работы с API OpenSky."""

    BASE_URL = "https://opensky-network.org/api"

    def get_data(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> JSONData:
        pass