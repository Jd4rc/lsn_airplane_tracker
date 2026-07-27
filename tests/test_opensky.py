from unittest.mock import patch

import pytest
import requests

from src.api.opensky import OpenSkyAPIClient


@patch("src.api.opensky.requests.get")
def test_get_data_calls_requests_get_with_correct_arguments(mock_get):
    client = OpenSkyAPIClient()

    expected = {
        "time": 1784427348,
        "states": [
            [
                "503efe",
                "VEDLYS 2",
                "Lithuania",
                1784427348,
                1784427348,
                25.2805,
                54.6413,
                None,
                True,
                4.89,
                8.44,
                None,
                None,
                None,
                None,
                False,
                0,
            ]
        ],
    }

    mock_response = mock_get.return_value
    mock_response.json.return_value = expected

    result = client.get_data(
        "/states/all",
        params={
            "lamin": 51.2,
            "lomin": 23.1,
            "lamax": 56.2,
            "lomax": 32.8,
        },
    )

    assert result == expected

    mock_response.raise_for_status.assert_called_once_with()

    mock_get.assert_called_once_with(
        url=f"{client.BASE_URL}/states/all",
        params={
            "lamin": 51.2,
            "lomin": 23.1,
            "lamax": 56.2,
            "lomax": 32.8,
        },
        headers={"User-Agent": client.USER_AGENT},
        timeout=10,
    )


@patch("src.api.opensky.requests.get")
def test_get_data_raises_http_error(mock_get):
    client = OpenSkyAPIClient()

    mock_response = mock_get.return_value
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()

    with pytest.raises(requests.exceptions.HTTPError):
        client.get_data(
            "/states/all",
            params={
                "lamin": 51.2,
                "lomin": 23.1,
                "lamax": 56.2,
                "lomax": 32.8,
            },
        )

    mock_response.raise_for_status.assert_called_once_with()
    mock_response.json.assert_not_called()


@patch("src.api.opensky.requests.get")
def test_get_data_raises_connection_error(mock_get):
    client = OpenSkyAPIClient()

    mock_get.side_effect = requests.exceptions.ConnectionError()
    with pytest.raises(requests.exceptions.ConnectionError):
        client.get_data(
            "/states/all",
            params={
                "lamin": 51.2,
                "lomin": 23.1,
                "lamax": 56.2,
                "lomax": 32.8,
            },
        )

    mock_get.assert_called_once_with(
        url=f"{client.BASE_URL}/states/all",
        params={
            "lamin": 51.2,
            "lomin": 23.1,
            "lamax": 56.2,
            "lomax": 32.8,
        },
        headers={"User-Agent": client.USER_AGENT},
        timeout=10,
    )


@patch("src.api.opensky.requests.get")
def test_get_data_raises_timeout(mock_get):
    client = OpenSkyAPIClient()

    mock_get.side_effect = requests.Timeout("Connection timed out")
    with pytest.raises(requests.Timeout):
        client.get_data(
            "/states/all",
            params={
                "lamin": 51.2,
                "lomin": 23.1,
                "lamax": 56.2,
                "lomax": 32.8,
            },
        )

    mock_get.assert_called_once_with(
        url=f"{client.BASE_URL}/states/all",
        params={
            "lamin": 51.2,
            "lomin": 23.1,
            "lamax": 56.2,
            "lomax": 32.8,
        },
        headers={"User-Agent": client.USER_AGENT},
        timeout=10,
    )


@patch("src.api.opensky.requests.get")
def test_get_data_raises_error_for_invalid_json(mock_get):
    client = OpenSkyAPIClient()

    mock_response = mock_get.return_value

    mock_response.json.side_effect = requests.exceptions.JSONDecodeError("Invalid JSON", "Invalid JSON", 0)

    with pytest.raises(requests.exceptions.JSONDecodeError):
        client.get_data(
            "/states/all",
            params={
                "lamin": 51.2,
                "lomin": 23.1,
                "lamax": 56.2,
                "lomax": 32.8,
            },
        )

    mock_response.raise_for_status.assert_called_once_with()
    mock_response.json.assert_called_once_with()


@patch("src.api.opensky.requests.get")
def test_get_data_passes_none_when_params_not_set(mock_get):
    client = OpenSkyAPIClient()

    mock_response = mock_get.return_value
    mock_response.json.return_value = {}

    result = client.get_data(
        "/states/all",
    )

    assert result == {}

    mock_get.assert_called_once_with(
        url=f"{client.BASE_URL}/states/all",
        params=None,
        headers={"User-Agent": client.USER_AGENT},
        timeout=10,
    )

    mock_response.raise_for_status.assert_called_once_with()


def test_get_states(monkeypatch):
    client = OpenSkyAPIClient()

    expected_response = {
        "time": 123456,
        "states": [],
    }

    def mock_get_data(endpoint, params):
        assert endpoint == "/states/all"
        assert params == {
            "lamin": 52.3,
            "lamax": 52.7,
            "lomin": 13.0,
            "lomax": 13.8,
        }

        return expected_response

    monkeypatch.setattr(client, "get_data", mock_get_data)

    result = client.get_states(
        lamin=52.3,
        lamax=52.7,
        lomin=13.0,
        lomax=13.8,
    )

    assert result == expected_response
