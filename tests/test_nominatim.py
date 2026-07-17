from unittest.mock import Mock
from unittest.mock import patch

import pytest
import requests

from src.api.nominatim import NominaAPIClient


def test_search_calls_get_data_with_correct_arguments(monkeypatch):
    client = NominaAPIClient()

    expected = []

    mock_get_data = Mock(return_value=expected)

    monkeypatch.setattr(client, "get_data", mock_get_data)

    result = client.search("Minsk")

    assert result == expected

    mock_get_data.assert_called_once_with("/search", {"q": "Minsk", "format": "json", "limit": 1})


def test_search_uses_custom_limit(monkeypatch):
    client = NominaAPIClient()

    expected = []

    mock_get_data = Mock(return_value=expected)

    monkeypatch.setattr(client, "get_data", mock_get_data)

    result = client.search("Minsk", 10)

    assert result == expected

    mock_get_data.assert_called_once_with("/search", {"q": "Minsk", "format": "json", "limit": 10})


@patch("src.api.nominatim.requests.get")
def test_get_data(mock_get):
    client = NominaAPIClient()

    expected = [
        {
            "boundingbox": ["52.5170798", "52.5173311", "13.3975116", "13.3981577"],
        }
    ]

    mock_response = mock_get.return_value
    mock_response.json.return_value = expected

    result = client.get_data(
        "/search",
        {
            "q": "Berlin",
        },
    )

    assert result == expected

    mock_get.assert_called_once_with(
        url="https://nominatim.openstreetmap.org/search",
        params={
            "q": "Berlin",
        },
        headers={"User-Agent": ("lsn-airplane-tracker/0.1.0 " "(https://github.com/Jd4rc/lsn_airplane_tracker)")},
        timeout=10,
    )

    mock_response.raise_for_status.assert_called_once_with()
    mock_response.json.assert_called_once_with()


@patch("src.api.nominatim.requests.get")
def test_get_data_raises_http_error(mock_get):
    client = NominaAPIClient()

    mock_response = mock_get.return_value
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()

    with pytest.raises(requests.exceptions.HTTPError):
        client.get_data(
            "/search",
            {
                "q": "Berlin",
            },
        )

    mock_response.raise_for_status.assert_called_once_with()
    mock_response.json.assert_not_called()


@patch("src.api.nominatim.requests.get")
def test_get_data_raises_connection_error(mock_get):
    client = NominaAPIClient()

    mock_get.side_effect = requests.exceptions.ConnectionError()
    with pytest.raises(requests.exceptions.ConnectionError):
        client.get_data(
            "/search",
            {
                "q": "Berlin",
            },
        )


@patch("src.api.nominatim.requests.get")
def test_get_data_raises_timeout(mock_get):
    client = NominaAPIClient()

    mock_get.side_effect = requests.Timeout("Connection timed out")
    with pytest.raises(requests.Timeout):
        client.get_data(
            "/search",
            {
                "q": "Berlin",
            },
        )


@patch("src.api.nominatim.requests.get")
def test_get_data_raises_error_for_invalid_json(mock_get):
    client = NominaAPIClient()

    mock_response = mock_get.return_value

    mock_response.json.side_effect = requests.exceptions.JSONDecodeError("Invalid JSON", "Invalid JSON", 0)

    with pytest.raises(requests.exceptions.JSONDecodeError):
        client.get_data(
            "/search",
            {
                "q": "Berlin",
            },
        )

    mock_response.raise_for_status.assert_called_once_with()
    mock_response.json.assert_called_once_with()


@patch("src.api.nominatim.requests.get")
def test_get_data_passes_none_when_params_not_set(mock_get):
    client = NominaAPIClient()

    mock_response = mock_get.return_value
    mock_response.json.return_value = {}

    result = client.get_data(
        "/search",
    )

    assert result == {}

    mock_get.assert_called_once_with(
        url="https://nominatim.openstreetmap.org/search",
        params=None,
        headers={"User-Agent": ("lsn-airplane-tracker/0.1.0 " "(https://github.com/Jd4rc/lsn_airplane_tracker)")},
        timeout=10,
    )

    mock_response.raise_for_status.assert_called_once_with()
