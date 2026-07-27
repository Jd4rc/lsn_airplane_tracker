from typing import Any
from typing import cast

import requests

from src.api.base import BaseAPIClient
from src.api.base import JSONData


class OpenSkyAPIClient(BaseAPIClient):
    """Клиент для работы с API OpenSky."""

    BASE_URL = "https://opensky-network.org/api"
    USER_AGENT = "lsn-airplane-tracker/0.1.0 " "(https://github.com/Jd4rc/lsn_airplane_tracker)"

    def get_data(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> JSONData:
        """Выполняет GET-запрос к API OpenSky и возвращает JSON-ответ."""

        response = requests.get(
            url=f"{self.BASE_URL}{endpoint}",
            params=params,
            headers={"User-Agent": self.USER_AGENT},
            timeout=10,
        )

        response.raise_for_status()

        return cast(JSONData, response.json())

    def get_states(
        self,
        lamin: float,
        lamax: float,
        lomin: float,
        lomax: float,
    ) -> JSONData:
        return self.get_data(
            endpoint="/states/all",
            params={
                "lamin": lamin,
                "lamax": lamax,
                "lomin": lomin,
                "lomax": lomax,
            },
        )
