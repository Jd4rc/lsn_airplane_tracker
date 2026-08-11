from flake8.options import manager

from src.database.connection import get_connection
from src.database.db_manager import DBManager
from src.database.data_loader import insert_country, insert_aircraft_list
from src.models.aircraft import Aircraft


def test_get_countries_and_aeroplanes_count():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                TRUNCATE TABLE aeroplanes, countries
                RESTART IDENTITY CASCADE;
                """
            )

    insert_country(
        name="Germany",
        south_lat=47.0,
        north_lat=55.0,
        west_lon=5.0,
        east_lon=15.0,
    )

    insert_country(
        name="France",
        south_lat=42.0,
        north_lat=51.0,
        west_lon=-5.0,
        east_lon=8.0,
    )

    manager = DBManager()

    result = manager.get_countries_and_aeroplanes_count()

    assert result == [
        ('France', 0),
        ('Germany', 0),
    ]


def test_get_countries_and_aeroplanes_count_with_aircraft():
    germany_id = insert_country(
        name="Germany",
        south_lat=47.0,
        north_lat=55.0,
        west_lon=5.0,
        east_lon=15.0,
    )

    france_id = insert_country(
        name="France",
        south_lat=42.0,
        north_lat=51.0,
        west_lon=-5.0,
        east_lon=8.0,
    )

    german_aircraft = [
        Aircraft(
            icao24="abc001",
            callsign="GER001",
            origin_country="Germany",
            longitude=10.0,
            latitude=50.0,
            altitude=10000.0,
            velocity=250.0,
            heading=90.0,
            on_ground=False,
        ),
        Aircraft(
            icao24="abc002",
            callsign="GER002",
            origin_country="Germany",
            longitude=11.0,
            latitude=51.0,
            altitude=12000.0,
            velocity=300.0,
            heading=120.0,
            on_ground=False,
        ),
    ]

    french_aircraft = [
        Aircraft(
            icao24="def001",
            callsign="FRA001",
            origin_country="France",
            longitude=2.0,
            latitude=48.0,
            altitude=9000.0,
            velocity=220.0,
            heading=180.0,
            on_ground=False,
        ),
    ]

    insert_aircraft_list(german_aircraft, germany_id)
    insert_aircraft_list(french_aircraft, france_id)

    manager = DBManager()

    result = manager.get_countries_and_aeroplanes_count()
    assert result == [
        ('France', 1),
        ('Germany', 2),
    ]

def test_get_all_aeroplanes():
    country_id = insert_country(
        name="Germany",
        south_lat=47.0,
        north_lat=55.0,
        west_lon=5.0,
        east_lon=15.0,
    )

    aircraft_list = [
        Aircraft(
            icao24="abc001",
            callsign="GER001",
            origin_country="Germany",
            longitude=10.0,
            latitude=50.0,
            altitude=10000.0,
            velocity=250.0,
            heading=90.0,
            on_ground=False,
        ),
        Aircraft(
            icao24="abc002",
            callsign="GER002",
            origin_country="Germany",
            longitude=11.0,
            latitude=51.0,
            altitude=12000.0,
            velocity=300.0,
            heading=120.0,
            on_ground=False,
        ),
    ]

    insert_aircraft_list(aircraft_list, country_id)

    manager = DBManager()

    result = manager.get_all_aeroplanes()

    assert len(result) == 2

    assert result[0][1] == 'abc001'
    assert result[1][1] == 'abc002'

