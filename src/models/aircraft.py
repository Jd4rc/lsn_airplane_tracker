from dataclasses import dataclass

@dataclass(slots=True)
class Aircraft:
    icao24: str
    callsign: str
    latitude: float
    longitude: float
    altitude: float
    velocity: float
    heading: float
    on_ground: bool