from src.api.nominatim import NominaAPIClient
from src.api.opensky import OpenSkyAPIClient
from src.database.data_loader import insert_aircraft_list, insert_country
from src.services.flight_service import FlightService


def main() -> None:

    countries = [
        'Germany',
        "France",
        "Poland",
        "Italy",
    ]

    nominatim_client = NominaAPIClient()
    opensky_client = OpenSkyAPIClient()

    flight_service = FlightService(
        nominatim_client=nominatim_client,
        opensky_client=opensky_client,
    )


    for country_name in countries:
        print(f"\nЗагрузка {country_name}...")

        location_data = nominatim_client.search(country_name)

        if not location_data:
            print(f"Не удалось получить координаты {country_name}")
            continue

        bounding_box = location_data[0]["boundingbox"]

        south_lat = float(bounding_box[0])
        north_lat = float(bounding_box[1])
        west_lon = float(bounding_box[2])
        east_lon = float(bounding_box[3])

        country_id = insert_country(
            name=country_name,
            south_lat=south_lat,
            north_lat=north_lat,
            west_lon=west_lon,
            east_lon=east_lon,
        )

        aircraft_list = flight_service.get_aircraft_by_location(country_name)

        print(f"Получено самолётов: {len(aircraft_list)}")

        insert_aircraft_list(
            aircraft_list=aircraft_list,
            country_id=country_id,
        )

        print(f"{country_name} сохранена в БД")


    print("\nЗагрузка завершена.")


if __name__ == "__main__":
    main()