from src import cli
from src.cli import print_aircraft
from src.models.aircraft import Aircraft


def test_print_aircraft(capsys):
    aircraft = Aircraft(
        icao24="918gg",
        callsign="TEST123",
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

    assert "Searching flights for Minsk..." in captured.out
    assert "Found 1 aircraft near Minsk" in captured.out
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

    assert "Searching flights for Minsk..." in captured.out
    assert "No aircraft found near Minsk" in captured.out
