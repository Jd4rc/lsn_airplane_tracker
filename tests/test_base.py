import pytest

from src.api.base import BaseAPIClient


def test_api_base_cannot_be_initialized():
    with pytest.raises(TypeError):
        BaseAPIClient()


def test_child_without_get_data_cannot_be_initialized():
    class TestAPIWithoutGetData(BaseAPIClient):
        pass

    with pytest.raises(TypeError):
        TestAPIWithoutGetData()


def test_child_with_get_data_can_be_initialized():
    class TestAPIWithGetData(BaseAPIClient):
        def get_data(self, endpoint, params=None):
            return {"data": "data"}

    api = TestAPIWithGetData()

    assert isinstance(api, TestAPIWithGetData)
