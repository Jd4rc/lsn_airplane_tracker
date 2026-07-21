import pytest

from models.aircraft import Aircraft

def test_from_opensky():
    # Arrange
    state = [
        'abc123',
        '  124',
        1591,
        616161,
        9891,
        165.151115,
        1415.116165,
        1415.116165,
        False,
        65.197,
        166.151165
    ]

    # Act
    aircraft = Aircraft.from_opensky(state)

    # Assert
    assert aircraft.icao24 == 'abc123'
    assert aircraft.callsign == '124'
    assert aircraft.longitude == 165.151115
    assert aircraft.latitude == 1415.116165
    assert aircraft.altitude == 1415.116165
    assert aircraft.on_ground is False
    assert aircraft.velocity == 65.197
    assert aircraft.heading == 166.151165


def test_from_opensky_with_none_callsign():
    state = [
        'abc123',
        None,
        1591,
        616161,
        9891,
        165.151115,
        1415.116165,
        1415.116165,
        False,
        65.197,
        166.151165
    ]

    aircraft = Aircraft.from_opensky(state)

    assert aircraft.icao24 == 'abc123'
    assert aircraft.callsign is None
    assert aircraft.longitude == 165.151115
    assert aircraft.latitude == 1415.116165
    assert aircraft.altitude == 1415.116165
    assert aircraft.on_ground is False
    assert aircraft.velocity == 65.197
    assert aircraft.heading == 166.151165

def test_from_opensky_with_empty_callsign():
    state = [
        'abc123',
        '',
        1591,
        616161,
        9891,
        165.151115,
        1415.116165,
        1415.116165,
        False,
        65.197,
        166.151165
    ]

    aircraft = Aircraft.from_opensky(state)

    assert aircraft.icao24 == 'abc123'
    assert aircraft.callsign is None
    assert aircraft.longitude == 165.151115
    assert aircraft.latitude == 1415.116165
    assert aircraft.altitude == 1415.116165
    assert aircraft.on_ground is False
    assert aircraft.velocity == 65.197
    assert aircraft.heading == 166.151165


def test_from_opensky_with_none_optional_fields():
    state = [
        'abc123',
        '  151gfg',
        None,
        None,
        None,
        None,
        None,
        None,
        False,
        None,
        None
    ]

    aircraft = Aircraft.from_opensky(state)

    assert aircraft.icao24 == 'abc123'
    assert aircraft.callsign == '151gfg'
    assert aircraft.longitude is None
    assert aircraft.latitude is None
    assert aircraft.altitude is None
    assert aircraft.on_ground is False
    assert aircraft.velocity is None
    assert aircraft.heading is None


def test_from_opensky_with_empty_state():
    state = []
    with pytest.raises(IndexError):
        Aircraft.from_opensky(state)


