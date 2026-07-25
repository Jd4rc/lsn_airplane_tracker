from src.api.base import JSONData
from src.api.nominatim import NominaAPIClient
from src.api.opensky import OpenSkyAPIClient
from src.models.aircraft import Aircraft


class FlightService:
    def __init__(
        self,
        nominatim_client: NominaAPIClient,
        opensky_client: OpenSkyAPIClient,
    ) -> None:
        self.nominatim_client = nominatim_client
        self.opensky_client = opensky_client

    def get_aircraft_by_location(
        self,
        location: str,
    ) -> list[Aircraft]:
        response = self.get_raw_flights(location)

        if not isinstance(response, dict):
            raise ValueError("OpenSky вернул некорректный ответ")

        states = response.get("states")

        if states is None:
            return []

        if not isinstance(states, list):
            raise ValueError("Поле states имеет некорректный формат")

        aircraft_list: list[Aircraft] = []

        for state in states:
            if not isinstance(state, list):
                continue

            aircraft_list.append(Aircraft.from_opensky(state))

        return aircraft_list

    def get_raw_flights(
        self,
        location: str,
    ) -> JSONData:
        south, north, west, east = self.get_area_bounds(location)

        return self.opensky_client.get_states(
            lamin=south,
            lamax=north,
            lomin=west,
            lomax=east,
        )

    def get_area_bounds(
        self,
        location: str,
    ) -> tuple[float, float, float, float]:
        search_result = self.nominatim_client.search(location)

        if not isinstance(search_result, list) or not search_result:
            raise ValueError(f"Место не найдено: {location}")

        place = search_result[0]

        if not isinstance(place, dict):
            raise ValueError("Nominatim вернул некорректный результат")

        bounding_box = place.get("boundingbox")

        if not isinstance(bounding_box, list) or len(bounding_box) != 4:
            raise ValueError("Nominatim вернул некорректный boundingbox")

        south = float(bounding_box[0])
        north = float(bounding_box[1])
        west = float(bounding_box[2])
        east = float(bounding_box[3])

        return south, north, west, east

    def get_top_aircraft_by_altitude(
        self,
        location: str,
        limit: int,
    ) -> list[Aircraft]:
        if limit <= 0:
            raise ValueError("Лимит должен быть больше нуля")

        aircraft = self.get_aircraft_by_location(location)

        aircraft_with_altitude = [item for item in aircraft if item.altitude is not None]

        sorted_aircraft = sorted(
            aircraft_with_altitude,
            key=lambda item: item.altitude or 0.0,
            reverse=True,
        )

        return sorted_aircraft[:limit]
