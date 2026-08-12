from tests.conftest import get_test_connection
from src.database.data_loader import insert_country

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

