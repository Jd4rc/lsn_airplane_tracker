from src.database.connection import get_connection


class DBManager:
    """Предоставляет методы для получения данных о самолётах из БД."""
    def get_countries_and_aeroplanes_count(self) -> list[tuple[str, int]]:
        """Возвращает список стран и количество самолётов для каждой страны."""
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
        """Возвращает список всех самолётов из БД."""
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT *
                    FROM aeroplanes
                    ORDER BY id;
                    """)

                return cur.fetchall()

    def get_avg_velocity(self) -> float | None:
        """Возвращает среднюю скорость самолётов или None, если данных нет."""
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
        """Возвращает самолёты со скоростью выше средней."""
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
        """Возвращает самолёты, содержащие keyword в позывном."""
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
