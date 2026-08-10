from src.database.connection import get_connection


class DBManager:
    def get_countries_and_aeroplanes_count(self) -> list[tuple[str, int]]:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        countries.name,
                        COUNT(aeroplanes.id)
                    FROM countries
                    LEFT JOIN aeroplanes
                        ON countries.id = aeroplanes.country_id
                    GROUP BY countries.id, countries.name
                    ORDER BY countries.name;
                    """
                )

                return cur.fetchall()

    def get_all_aeroplanes(self) -> list[tuple]:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT *
                    FROM aeroplanes
                    ORDER BY id;
                    """
                )

                return cur.fetchall()
