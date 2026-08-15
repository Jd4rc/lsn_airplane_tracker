from src.database.connection import get_connection
from src.models.aircraft import Aircraft


def insert_country(
    name: str,
    south_lat: float,
    north_lat: float,
    west_lon: float,
    east_lon: float,
) -> int:
    """Добавляет страну в БД и возвращает её id."""

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO countries (
                    name,
                    south_lat,
                    north_lat,
                    west_lon,
                    east_lon
                )
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (name)
                DO UPDATE SET
                    south_lat = EXCLUDED.south_lat,
                    north_lat = EXCLUDED.north_lat,
                    west_lon = EXCLUDED.west_lon,
                    east_lon = EXCLUDED.east_lon
                RETURNING id;
                """,
                (
                    name,
                    south_lat,
                    north_lat,
                    west_lon,
                    east_lon,
                ),
            )

            result = cur.fetchone()

            if result is None:
                raise RuntimeError("Не удалось получить id страны")

            return int(result[0])


def insert_aircraft_list(
    aircraft_list: list[Aircraft],
    country_id: int,
) -> None:
    """Добавляет самолёт в БД и возвращает его id."""

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM aeroplanes
                WHERE country_id = %s;
                """,
                (country_id,),
            )

            for aircraft in aircraft_list:
                cur.execute(
                    """
                    INSERT INTO aeroplanes (
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
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (
                        aircraft.icao24,
                        aircraft.callsign,
                        aircraft.origin_country,
                        aircraft.longitude,
                        aircraft.latitude,
                        aircraft.altitude,
                        aircraft.velocity,
                        aircraft.heading,
                        aircraft.on_ground,
                        country_id,
                    ),
                )
