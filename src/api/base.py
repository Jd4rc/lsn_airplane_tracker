from abc import ABC
from abc import abstractmethod
from typing import Any

type JSONData = dict[str, Any] | list[dict[str, Any]]


class BaseAPIClient(ABC):

    @abstractmethod
    def get_data(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> JSONData:
        """Получить и вернуть JSON-данные от API"""
        pass
