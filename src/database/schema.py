from src.database.connection import get_connection


def create_tables() -> None:
    """Создает необходимые таблицы в PostgreSQL."""

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS countries (
                    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    name VARCHAR(100) NOT NULL UNIQUE,
                    south_lat DOUBLE PRECISION NOT NULL,
                    north_lat DOUBLE PRECISION NOT NULL,
                    west_lon DOUBLE PRECISION NOT NULL,
                    east_lon DOUBLE PRECISION NOT NULL
                );
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS aeroplanes (
                    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    icao24 VARCHAR(6) NOT NULL,
                    callsign VARCHAR(20),
                    origin_country VARCHAR(100),
                    longitude DOUBLE PRECISION,
                    latitude DOUBLE PRECISION,
                    baro_altitude DOUBLE PRECISION,
                    velocity DOUBLE PRECISION,
                    true_track DOUBLE PRECISION,
                    vertical_rate DOUBLE PRECISION,
                    on_ground BOOLEAN NOT NULL,
                    country_id INTEGER NOT NULL,

                    CONSTRAINT fk_aeroplanes_country
                        FOREIGN KEY (country_id)
                        REFERENCES countries(id)
                        ON DELETE CASCADE
                );
                """
            )
