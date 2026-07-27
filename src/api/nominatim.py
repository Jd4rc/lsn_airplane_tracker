from typing import Any
from typing import cast

import requests

from src.api.base import BaseAPIClient
from src.api.base import JSONData


class NominaAPIClient(BaseAPIClient):
    """Клиент для работы с API Nominatim OpenStreetMap."""

    BASE_URL = "https://nominatim.openstreetmap.org"

    def get_data(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> JSONData:
        """Выполняет GET-запрос к API Nominatim и возвращает JSON-ответ."""
        response = requests.get(
            url=f"{self.BASE_URL}{endpoint}",
            params=params,
            headers={"User-Agent": ("lsn-airplane-tracker/0.1.0 " "(https://github.com/Jd4rc/lsn_airplane_tracker)")},
            timeout=10,
        )

        response.raise_for_status()

        return cast(JSONData, response.json())

    def search(
        self,
        query: str,
        limit: int = 1,
    ) -> JSONData:
        """Ищет географический объект по названию и возвращает результаты поиска."""
        return self.get_data(
            "/search",
            {
                "q": query,
                "format": "json",
                "limit": limit,
            },
        )
