from unittest.mock import Mock

from src import cli
from src.cli import print_aircraft
from src.models.aircraft import Aircraft


def make_aircraft() -> Aircraft:
    return Aircraft(
        icao24="abc123",
        callsign="TEST123",
        origin_country="Germany",
        longitude=13.4,
        latitude=52.5,
        altitude=8500.0,
        on_ground=False,
        velocity=220.0,
        heading=180.0,
    )

def test_print_aircraft(capsys):
    aircraft = Aircraft(
        icao24="918gg",
        callsign="TEST123",
        origin_country="Belarus",
        latitude=55.75,
        longitude=37.61,
        altitude=1000.0,
        velocity=200.0,
        heading=90.0,
        on_ground=False,
    )

    print_aircraft(aircraft)

    captured = capsys.readouterr()

    assert "ICAO24: 918gg" in captured.out
    assert "Callsign: TEST123" in captured.out
    assert "Altitude: 1000.0" in captured.out
    assert "Velocity: 200.0" in captured.out
    assert "Heading: 90.0" in captured.out
    assert "On ground: no" in captured.out


def test_print_aircraft_with_unknown_values(capsys) -> None:
    aircraft = Aircraft(
        icao24="918gg",
        callsign=None,
        origin_country="Belarus",
        latitude=None,
        longitude=None,
        altitude=None,
        velocity=None,
        heading=None,
        on_ground=True,
    )

    print_aircraft(aircraft)

    captured = capsys.readouterr()

    assert "ICAO24: 918gg" in captured.out
    assert "Callsign: unknown" in captured.out
    assert "Altitude: unknown" in captured.out
    assert "Velocity: unknown" in captured.out
    assert "Heading: unknown" in captured.out
    assert "On ground: yes" in captured.out


def test_handle_search(capsys, monkeypatch):
    aircraft = Aircraft(
        icao24="918gg",
        callsign="TEST123",
        origin_country="Belarus",
        latitude=55.75,
        longitude=37.61,
        altitude=1000.0,
        velocity=200.0,
        heading=90.0,
        on_ground=False,
    )

    def fake_get_aircraft_by_location(city: str) -> list[Aircraft]:
        return [aircraft]

    monkeypatch.setattr(
        cli.service,
        "get_aircraft_by_location",
        fake_get_aircraft_by_location,
    )

    cli.handle_search("Minsk")

    captured = capsys.readouterr()

    assert "Поиск самолётов для Minsk..." in captured.out
    assert "Найдено самолётов поблизости от Minsk: 1" in captured.out
    assert "ICAO24: 918gg" in captured.out


def test_handle_search_with_no_aircraft(capsys, monkeypatch):
    def fake_get_aircraft_by_location(city: str) -> list[Aircraft]:
        return []

    monkeypatch.setattr(
        cli.service,
        "get_aircraft_by_location",
        fake_get_aircraft_by_location,
    )

    cli.handle_search("Minsk")

    captured = capsys.readouterr()

    assert "Поиск самолётов для Minsk..." in captured.out
    assert "Самолётов поблизости от Minsk не найдено" in captured.out


def test_handle_search_with_country(monkeypatch, capsys):

    aircraft_list = [make_aircraft()]

    country_mock = Mock(return_value=aircraft_list)
    location_mock = Mock()
    altitude_mock = Mock()

    monkeypatch.setattr(
        cli.service,
        'get_aircraft_by_country',
        country_mock,
    )

    monkeypatch.setattr(
        cli.service,
        'get_aircraft_by_location',
        location_mock,
    )

    monkeypatch.setattr(
        cli.service,
        'get_top_aircraft_by_altitude',
        altitude_mock,
    )

    cli.handle_search(
        city="Berlin",
        country="Germany",
    )

    country_mock.assert_called_once_with("Berlin", "Germany")
    location_mock.assert_not_called()
    altitude_mock.assert_not_called()

    captured = capsys.readouterr()

    assert 'Berlin' in captured.out
    assert 'Germany' in captured.out
    assert 'TEST123' in captured.out


def test_handle_search_with_top_altitude(capsys, monkeypatch):
    aircraft_list = [make_aircraft()]

    country_mock = Mock()
    location_mock = Mock()
    altitude_mock = Mock(return_value=aircraft_list)

    monkeypatch.setattr(
        cli.service,
        'get_aircraft_by_country',
        country_mock,
    )

    monkeypatch.setattr(
        cli.service,
        'get_aircraft_by_location',
        location_mock,
    )

    monkeypatch.setattr(
        cli.service,
        'get_top_aircraft_by_altitude',
        altitude_mock,
    )

    cli.handle_search(
        city='Berlin',
        top_altitude=5,
    )

    altitude_mock.assert_called_once_with("Berlin", 5)
    country_mock.assert_not_called()
    location_mock.assert_not_called()

    captured = capsys.readouterr()

    assert 'Berlin' in captured.out
    assert 'топ-5' in captured.out
    assert 'TEST123' in captured.out

def test_handle_search_with_country_and_empty_aircraft(capsys, monkeypatch):
    country_mock = Mock(return_value=[])

    monkeypatch.setattr(
        cli.service,
        'get_aircraft_by_country',
        country_mock,
    )

    cli.handle_search(
        city='Berlin',
        country='Germany',
    )

    country_mock.assert_called_once_with('Berlin', 'Germany')

    captured = capsys.readouterr()

    assert 'Самолётов поблизости от Berlin не найдено' in captured.out

def test_handle_search_with_top_altitude_and_empty_aircraft(capsys, monkeypatch):
    altitude_mock = Mock(return_value=[])

    monkeypatch.setattr(
        cli.service,
        'get_top_aircraft_by_altitude',
        altitude_mock,
    )

    cli.handle_search(
        city='Berlin',
        top_altitude=5,
    )

    altitude_mock.assert_called_once_with('Berlin', 5)

    captured = capsys.readouterr()

    assert 'Самолётов поблизости от Berlin не найдено' in captured.out
