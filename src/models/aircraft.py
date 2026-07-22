from dataclasses import dataclass

from mypy.nodes import Any


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
    def from_opensky(cls, state: list[Any]) -> Aircraft:
        EXPECTED_STATE_LENGTH = 11

        if len(state) < EXPECTED_STATE_LENGTH:
            raise ValueError("Неккоректные данные OpenSky")

        callsign = state[1]
        if isinstance(callsign, str):
            callsign = callsign.strip() or None

        return cls(
            icao24=state[0],
            callsign=callsign,
            longitude=state[5],
            latitude=state[6],
            altitude=state[7],
            on_ground=state[8],
            velocity=state[9],
            heading=state[10],
        )
