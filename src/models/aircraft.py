from dataclasses import dataclass


@dataclass(slots=True)
class Aircraft:
    icao24: str
    callsign: str | None
    latitude: float | None
    longitude: float | None
    altitude: float | None
    velocity: float | None
    heading: float | None
    on_ground: bool

    @classmethod
    def from_opensky(cls, state: list) -> Aircraft:
        return cls(
            icao24=state[0],
            callsign=state[1].strip() if state[1] else None,
            longitude=state[5],
            latitude=state[6],
            altitude=state[7],
            on_ground=state[8],
            velocity=state[9],
            heading=state[10],
        )
