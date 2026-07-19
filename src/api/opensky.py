from typing import Any, cast

import requests

from api.base import BaseAPIClient, JSONData


class OpenSkyAPIClient(BaseAPIClient):
    """Клиент для работы с API OpenSky."""

    BASE_URL = "https://opensky-network.org/api"
    USER_AGENT = (
        "lsn-airplane-tracker/0.1.0 "
        "(https://github.com/Jd4rc/lsn_airplane_tracker)"
    )

    def get_data(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> JSONData:
        """Выполняет GET-запрос к API OpenSky и возвращает JSON-ответ."""

        response = requests.get(
            url=f"{self.BASE_URL}{endpoint}",
            params=params,
            headers={ 'User-Agent': self.USER_AGENT},
            timeout=10,
        )

        response.raise_for_status()

        return cast(JSONData, response.json())