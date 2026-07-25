from unittest.mock import Mock

import pytest

from src.models.aircraft import Aircraft
from src.services.flight_service import FlightService


def create_aircraft(
    callsign: str,
    altitude: float | None,
    on_ground: bool = False,
) -> Aircraft:
    return Aircraft(
        icao24="abc123",
        callsign=callsign,
        latitude=55.0,
        longitude=37.0,
        altitude=altitude,
        velocity=200.0,
        heading=90.0,
        on_ground=on_ground,
    )


def test_get_area_bounds():
    nominatim_client = Mock()
    opensky_client = Mock()

    nominatim_client.search.return_value = [
        {
            "boundingbox": [
                "52.3382448",
                "52.6755087",
                "13.088345",
                "13.7611609",
            ]
        }
    ]

    service = FlightService(
        nominatim_client=nominatim_client,
        opensky_client=opensky_client,
    )

    result = service.get_area_bounds("Berlin")

    assert result == (
        52.3382448,
        52.6755087,
        13.088345,
        13.7611609,
    )

    nominatim_client.search.assert_called_once_with("Berlin")


def test_get_area_bounds_raises_error_when_location_not_found():
    nominatim_client = Mock()
    opensky_client = Mock()

    nominatim_client.search.return_value = []

    service = FlightService(
        nominatim_client=nominatim_client,
        opensky_client=opensky_client,
    )

    with pytest.raises(
        ValueError,
        match="Место не найдено: Berlin",
    ):
        service.get_area_bounds("Berlin")


def test_get_area_bounds_raises_error_when_response_is_not_list():
    nominatim_client = Mock()
    opensky_client = Mock()

    nominatim_client.search.return_value = {"error": "incorrect"}

    service = FlightService(
        nominatim_client=nominatim_client,
        opensky_client=opensky_client,
    )

    with pytest.raises(ValueError):
        service.get_area_bounds("Berlin")


def test_get_area_bounds_raises_error_for_invalid_bounding_box():
    nominatim_client = Mock()
    opensky_client = Mock()

    nominatim_client.search.return_value = [{"boundingbox": ["52.3", "52.7"]}]

    service = FlightService(
        nominatim_client=nominatim_client,
        opensky_client=opensky_client,
    )

    with pytest.raises(
        ValueError,
        match="Nominatim вернул некорректный",
    ):
        service.get_area_bounds("Berlin")


def test_get_raw_flights(monkeypatch):
    nominatim_client = Mock()
    opensky_client = Mock()

    service = FlightService(
        nominatim_client=nominatim_client,
        opensky_client=opensky_client,
    )

    monkeypatch.setattr(
        service,
        "get_area_bounds",
        lambda location: (52.3, 52.7, 13.0, 13.8),
    )

    expected_response = {
        "time": 123456,
        "states": [],
    }

    opensky_client.get_states.return_value = expected_response

    result = service.get_raw_flights("Berlin")

    assert result == expected_response

    opensky_client.get_states.assert_called_once_with(
        lamin=52.3,
        lamax=52.7,
        lomin=13.0,
        lomax=13.8,
    )


def test_get_aircraft_by_location(monkeypatch):
    nominatim_client = Mock()
    opensky_client = Mock()

    service = FlightService(
        nominatim_client=nominatim_client,
        opensky_client=opensky_client,
    )

    raw_response = {
        "time": 123456,
        "states": [
            [
                "abc123",
                "TEST123 ",
                "Germany",
                123,
                456,
                13.4,
                52.5,
                10000.0,
                False,
                250.0,
                180.0,
            ]
        ],
    }

    monkeypatch.setattr(
        service,
        "get_raw_flights",
        lambda location: raw_response,
    )

    result = service.get_aircraft_by_location("Berlin")

    assert len(result) == 1
    assert isinstance(result[0], Aircraft)
    assert result[0].icao24 == "abc123"


def test_get_aircraft_by_location_returns_empty_list_when_states_is_none(
    monkeypatch,
):
    service = FlightService(Mock(), Mock())

    monkeypatch.setattr(
        service,
        "get_raw_flights",
        lambda location: {
            "time": 123456,
            "states": None,
        },
    )

    result = service.get_aircraft_by_location("Berlin")

    assert result == []


def test_get_top_aircraft_by_altitude_sorts_aircraft():
    service = FlightService(Mock(), Mock())

    service.get_aircraft_by_location = Mock(
        return_value=[
            create_aircraft("low", 1000.0),
            create_aircraft("high", 3000.0),
            create_aircraft("middle", 2000.0),
        ]
    )

    result = service.get_top_aircraft_by_altitude(
        "Moscow",
        limit=3,
    )

    assert [aircraft.callsign for aircraft in result] == ["high", "middle", "low"]


def test_get_top_aircraft_by_altitude_limit():
    service = FlightService(Mock(), Mock())

    service.get_aircraft_by_location = Mock(
        return_value=[
            create_aircraft("low", 1000.0),
            create_aircraft("high", 3000.0),
            create_aircraft("middle", 2000.0),
        ]
    )

    result = service.get_top_aircraft_by_altitude(
        "Moscow",
        limit=2,
    )

    assert [aircraft.callsign for aircraft in result] == [
        "high",
        "middle",
    ]


def test_get_top_aircraft_by_altitude_with_none_altitude():
    service = FlightService(Mock(), Mock())

    service.get_aircraft_by_location = Mock(
        return_value=[
            create_aircraft("low", 1000.0),
            create_aircraft("high", None),
            create_aircraft("middle", None),
        ]
    )

    result = service.get_top_aircraft_by_altitude(
        "Moscow",
        limit=5,
    )

    assert [aircraft.callsign for aircraft in result] == [
        "low",
    ]


@pytest.mark.parametrize(
    "limit",
    [
        0,
        -1,
        -15,
    ],
)
def test_get_top_aircraft_by_altitude_with_raises_invalid_limit(limit):
    service = FlightService(Mock(), Mock())

    with pytest.raises(ValueError, match="Лимит должен быть больше нуля"):
        service.get_top_aircraft_by_altitude(
            location="Moscow",
            limit=limit,
        )
