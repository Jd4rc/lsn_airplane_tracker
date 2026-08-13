from src.models.aircraft import Aircraft
from tests.conftest import get_test_connection
from src.database.data_loader import insert_country, insert_aircraft_list


def test_insert_country():
    country_id = insert_country(
        name="Germany",
        south_lat=47.0,
        north_lat=55.0,
        west_lon=5.0,
        east_lon=15.0,
    )

    assert country_id is not None

    with get_test_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT 
                    id,
                    name,
                    south_lat,
                    north_lat,
                    west_lon,
                    east_lon
                FROM countries
                WHERE id = %s;
                """,
                (country_id,),
            )

            result = cursor.fetchone()

            assert result == (
                country_id,
                'Germany',
                47.0,
                55.0,
                5.0,
                15.0,
            )

def test_insert_country_updates_existing_country():
    first_id = insert_country(
        name="Germany",
        south_lat=47.0,
        north_lat=55.0,
        west_lon=5.0,
        east_lon=15.0,
    )

    second_id = insert_country(
        name="Germany",
        south_lat=48.0,
        north_lat=56.0,
        west_lon=6.0,
        east_lon=16.0,
    )

    assert first_id == second_id

    with get_test_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    name,
                    south_lat,
                    north_lat,
                    west_lon,
                    east_lon
                FROM countries
                WHERE name = %s;
                """,
                ("Germany",),
            )

            result = cur.fetchone()

            cur.execute(
                """
                SELECT COUNT(*)
                FROM countries
                WHERE name = %s;
                """,
                ("Germany",),
            )

            count = cur.fetchone()[0]

    assert count == 1

    assert result == (
        "Germany",
        48.0,
        56.0,
        6.0,
        16.0,
    )


def test_insert_aircraft_list():
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
            velocity=200.0,
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

    with get_test_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT 
                    icao24,
                    callsign,
                    origin_country,
                    longitude,
                    latitude,
                    baro_altitude,
                    velocity,
                    true_track,
                    on_ground,
                    country_id
                FROM aeroplanes
                WHERE country_id = %s
                ORDER BY id;
                """,
                (country_id,),
            )

            result = cur.fetchall()

            assert result == [
                (
                    "abc001",
                    "GER001",
                    "Germany",
                    10.0,
                    50.0,
                    10000.0,
                    200.0,
                    90.0,
                    False,
                    country_id
                ),
                (
                    "abc002",
                    "GER002",
                    "Germany",
                    11.0,
                    51.0,
                    12000.0,
                    300.0,
                    120.0,
                    False,
                    country_id
                )
            ]


def test_insert_aircraft_list_replaces_existing_aircraft():
    country_id = insert_country(
        name="Germany",
        south_lat=47.0,
        north_lat=55.0,
        west_lon=5.0,
        east_lon=15.0,
    )

    old_aircraft_list = [
        Aircraft(
            icao24="abc001",
            callsign="OLD001",
            origin_country="Germany",
            longitude=10.0,
            latitude=50.0,
            altitude=10000.0,
            velocity=200.0,
            heading=90.0,
            on_ground=False,
        ),
        Aircraft(
            icao24="abc002",
            callsign="OLD002",
            origin_country="Germany",
            longitude=11.0,
            latitude=51.0,
            altitude=11000.0,
            velocity=250.0,
            heading=100.0,
            on_ground=False,
        ),
    ]

    insert_aircraft_list(old_aircraft_list, country_id)

    new_aircraft_list = [
        Aircraft(
            icao24="xyz001",
            callsign="NEW001",
            origin_country="Germany",
            longitude=12.0,
            latitude=52.0,
            altitude=12000.0,
            velocity=300.0,
            heading=120.0,
            on_ground=False,
        ),
    ]

    insert_aircraft_list(new_aircraft_list, country_id)

    with get_test_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT icao24, callsign
                FROM aeroplanes
                WHERE country_id = %s;
                """,
                (country_id,),
            )

            result = cur.fetchall()

    assert result == [
        ("xyz001", "NEW001"),
    ]

