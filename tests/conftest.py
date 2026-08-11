import os
from dotenv import load_dotenv
import pytest
import psycopg2

from src.database import db_manager, data_loader

load_dotenv()

def get_test_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_TEST_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

@pytest.fixture(autouse=True)
def use_test_database(monkeypatch):
    monkeypatch.setattr(
        db_manager,
        "get_connection",
        get_test_connection,
    )

    monkeypatch.setattr(
        data_loader,
        "get_connection",
        get_test_connection,
    )

    with get_test_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                TRUNCATE TABLE aeroplanes, countries
                RESTART IDENTITY CASCADE;
                """
            )

