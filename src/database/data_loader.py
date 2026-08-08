from src.database.connection import get_connection


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

            return result[0]


def insert_aircraft(
    aircraft: Aircraft,
    country_id: int,
) -> None:
    ...