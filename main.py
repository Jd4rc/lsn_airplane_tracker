from src.database.db_manager import DBManager
from loader import main as load_data
from src.database.schema import create_tables

def main() -> None:
    create_tables()
    load_data()

    manager = DBManager()


    print("\n=== COUNTRIES ===")

    countries = manager.get_countries_and_aeroplanes_count()

    for country, count in countries:
        print(f"{country}: {count}")


    print("\n=== ALL AIRCRAFT ===")

    aircraft = manager.get_all_aeroplanes()

    print(f"Всего самолётов: {len(aircraft)}")


    print("\n=== AVERAGE VELOCITY ===")

    avg_velocity = manager.get_avg_velocity()

    if avg_velocity is not None:
        print(f"Средняя скорость: {avg_velocity:.2f}")
    else:
        print("Нет данных о скорости")


    print("\n=== ABOVE AVERAGE VELOCITY ===")

    fast_aircraft = manager.get_aeroplanes_with_higher_velocity()

    print(f"Самолётов быстрее средней: {len(fast_aircraft)}")


    print("\n=== CALLSIGN SEARCH ===")

    aircraft_by_keyword = manager.get_aeroplanes_with_keyword("DLH")

    print(f"Найдено по 'DLH': {len(aircraft_by_keyword)}")

    for aircraft_item in aircraft_by_keyword[:10]:
        print(aircraft_item)

if __name__ == "__main__":
    main()