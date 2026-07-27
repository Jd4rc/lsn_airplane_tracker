import argparse

import requests

from src.api.nominatim import NominaAPIClient
from src.api.opensky import OpenSkyAPIClient
from src.models.aircraft import Aircraft
from src.services.flight_service import FlightService
from src.storage.json_storage import JsonStorage

nominatim_client = NominaAPIClient()
opensky_client = OpenSkyAPIClient()

service = FlightService(
    nominatim_client=nominatim_client,
    opensky_client=opensky_client,
)


def print_aircraft(aircraft: Aircraft) -> None:
    altitude = aircraft.altitude if aircraft.altitude is not None else "unknown"
    velocity = aircraft.velocity if aircraft.velocity is not None else "unknown"
    heading = aircraft.heading if aircraft.heading is not None else "unknown"

    print(
        f"ICAO24: {aircraft.icao24}\n"
        f"Callsign: {aircraft.callsign or 'unknown'}\n"
        f"Altitude: {altitude} m\n"
        f"Velocity: {velocity} m/s\n"
        f"Heading: {heading}°\n"
        f"On ground: {'yes' if aircraft.on_ground else 'no'}\n"
    )


def handle_search(
    city: str,
    country: str | None = None,
    top_altitude: int | None = None,
) -> None:
    try:
        if country is not None:
            print(f"Поиск самолётов для {city} " f"по стране регистрации {country}...")
            aircraft_list = service.get_aircraft_by_country(city, country)
        elif top_altitude is not None:
            print(f"Поиск самолётов для {city}: " f"топ-{top_altitude} по высоте...")
            aircraft_list = service.get_top_aircraft_by_altitude(city, top_altitude)
        else:
            print(f"Поиск самолётов для {city}...")
            aircraft_list = service.get_aircraft_by_location(city)

    except requests.exceptions.Timeout:
        print("Сервис не ответил вовремя. " "Проверьте подключение и повторите запрос.")
        return

    if not aircraft_list:
        print(f"Самолётов поблизости от {city} не найдено")
        return

    print(f"Найдено самолётов поблизости от {city}: " f"{len(aircraft_list)}")

    storage = JsonStorage()

    file_path = storage.save(
        aircraft=aircraft_list,
        location=city,
    )

    print(f"Сохранено {len(aircraft_list)} самолетов в {file_path}\n")

    for aircraft in aircraft_list:
        print_aircraft(aircraft)


def main() -> None:
    parser = argparse.ArgumentParser(prog="airplane-tracker")

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    search = subparsers.add_parser("search")
    search.add_argument("city")

    filters = search.add_mutually_exclusive_group()

    filters.add_argument("--country", help="Фильтрация самолетов по стране происхождения")

    filters.add_argument(
        "--top-altitude",
        type=int,
        metavar="LIMIT",
        help="Показать самолет с наибольшей высотой полета",
    )

    args = parser.parse_args()

    if args.command == "search":
        handle_search(
            city=args.city,
            country=args.country,
            top_altitude=args.top_altitude,
        )


if __name__ == "__main__":
    main()
