import json

from src.models.aircraft import Aircraft
from src.storage.json_storage import JsonStorage


def test_save_creates_json_storage(tmp_path):
    storage = JsonStorage(data_directory=tmp_path)

    aircraft = [
        Aircraft(
            icao24="152022",
            callsign="AFL1544",
            latitude=55.75,
            longitude=37.61,
            altitude=4503.42,
            velocity=27.57,
            heading=75.96,
            on_ground=False,
        )
    ]

    storage.save(aircraft=aircraft, location="Moscow")

    files = list(tmp_path.glob("moscow_*.json"))

    assert len(files) == 1


def test_save_creates_correct_json_data(tmp_path):
    storage = JsonStorage(data_directory=tmp_path)

    aircraft = [
        Aircraft(
            icao24="152022",
            callsign="AFL1544",
            latitude=55.75,
            longitude=37.61,
            altitude=4503.42,
            velocity=27.57,
            heading=75.96,
            on_ground=False,
        )
    ]

    storage.save(aircraft=aircraft, location="Moscow")

    saved_file = next(tmp_path.glob("moscow_*.json"))

    with open(saved_file, encoding="utf-8") as f:
        saved_data = json.load(f)

    assert saved_data == {
        "location": "Moscow",
        "aircraft": [
            {
                "icao24": "152022",
                "callsign": "AFL1544",
                "latitude": 55.75,
                "longitude": 37.61,
                "altitude": 4503.42,
                "velocity": 27.57,
                "heading": 75.96,
                "on_ground": False,
            }
        ],
    }


def test_save_writes_all_aircraft(tmp_path):
    storage = JsonStorage(data_directory=tmp_path)

    aircraft = [
        Aircraft(
            icao24="152022",
            callsign="AFL1544",
            latitude=55.75,
            longitude=37.61,
            altitude=4503.42,
            velocity=27.57,
            heading=75.96,
            on_ground=False,
        ),
        Aircraft(
            icao24="151d8b",
            callsign="AFL1518",
            latitude=55.80,
            longitude=37.70,
            altitude=906.78,
            velocity=27.99,
            heading=162.9,
            on_ground=False,
        ),
    ]

    storage.save(aircraft=aircraft, location="Moscow")

    file = next(tmp_path.glob("moscow_*.json"))

    with file.open(encoding="utf-8") as f:
        saved_data = json.load(f)

    assert len(saved_data["aircraft"]) == 2
    assert saved_data["aircraft"][0]["icao24"] == "152022"
    assert saved_data["aircraft"][1]["icao24"] == "151d8b"
