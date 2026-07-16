from typing import Any

import requests

from src.api.base import BaseAPIClient
from src.api.base import JSONData


class NominaAPIClient(BaseAPIClient):
    BASE_URL = "https://nominatim.openstreetmap.org/"

    def get_data(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> JSONData:

        response = requests.get(
            url= f'{self.BASE_URL}{endpoint}',
            params=params,
            headers={
                'User-Agent': ('lsn-airplane-tracker/0.1.0 '
                               '(https://github.com/Jd4rc/lsn_airplane_tracker)')
            },
            timeout=10,
        )

        response.raise_for_status()

        return response.json()

    def search(
            self,
            query: str,
            limit: int = 1,
    )-> JSONData:
        return self.get_data(
            '/search',
            {
                'q': query,
                'format': 'json',
                'limit': limit,
            },
        )