import argparse

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
    altitude = aircraft.altitude if aircraft.altitude is not None else 'unknown'
    velocity = aircraft.velocity if aircraft.velocity is not None else 'unknown'
    heading = aircraft.heading if aircraft.heading is not None else 'unknown'

    print(
        f'ICAO24: {aircraft.icao24}\n'
        f'Callsign: {aircraft.callsign or 'unknown'}\n'
        f'Altitude: {altitude} m\n'
        f'Velocity: {velocity} m/s\n'
        f'Heading: {heading}°\n'
        f'On ground: {'yes' if aircraft.on_ground else 'no'}\n'
    )


def handle_search(city: str) -> None:
    print(f'Searching flights for {city}...')

    aircraft_list = service.get_aircraft_by_location(city)

    if not aircraft_list:
        print(f'No aircraft found near {city}')
        return

    storage = JsonStorage()

    file_path = storage.save(
        aircraft=aircraft_list,
        location=city,
    )

    print(f'Found {len(aircraft_list)} aircraft near {city}')
    print(f'Saved {len(aircraft_list)} aircraft to {file_path}')

    for aircraft in aircraft_list:
        print_aircraft(aircraft)


def main() -> None:
    parser = argparse.ArgumentParser(prog='airplane-tracker')

    subparsers = parser.add_subparsers(
        dest='command',
        required=True,
    )

    search = subparsers.add_parser('search')
    search.add_argument('city')

    args = parser.parse_args()

    if args.command == 'search':
        handle_search(args.city)


if __name__ == '__main__':
    main()
