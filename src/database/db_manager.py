from src.database.connection import get_connection


class DBManager:
    def get_countries_and_aeroplanes_count(self) -> list[tuple[str, int]]:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        countries.name,
                        COUNT(aeroplanes.id)
                    FROM countries
                    LEFT JOIN aeroplanes
                        ON countries.id = aeroplanes.country_id
                    GROUP BY countries.id, countries.name
                    ORDER BY countries.name;
                    """)

                return cur.fetchall()

    def get_all_aeroplanes(self) -> list[tuple]:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT *
                    FROM aeroplanes
                    ORDER BY id;
                    """)

                return cur.fetchall()

    def get_avg_velocity(self) -> float | None:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT AVG(velocity)
                    FROM aeroplanes;
                    """)

                result = cur.fetchone()

                if result is None or result[0] is None:
                    return None

                return float(result[0])

    def get_aeroplanes_with_higher_velocity(self) -> list[tuple]:

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT *
                    FROM aeroplanes
                    WHERE velocity > (
                        SELECT AVG(velocity)
                        FROM aeroplanes
                    )
                    ORDER BY velocity DESC;
                    """)

                return cur.fetchall()

    def get_aeroplanes_with_keyword(self, keyword: str) -> list[tuple]:

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT *
                    FROM aeroplanes
                    WHERE callsign ILIKE %s;
                    """,
                    (f"%{keyword}%",),
                )

                return cur.fetchall()
