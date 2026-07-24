from dataclasses import asdict
import json
from datetime import datetime
from pathlib import Path

from src.models.aircraft import Aircraft


class JsonStorage:
    def __init__(
            self,
            data_directory: str | Path = 'data',
    ) -> None:
        self.data_directory = Path(data_directory)

    def save(
            self,
            aircraft: list[Aircraft],
            location: str,
    ) -> Path:
        self.data_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        aircraft_data = [asdict(item) for item in aircraft]

        data = {
            "location": location,
            "aircraft": aircraft_data,
        }

        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f'{location.lower().replace(" ", "_")}_{current_date}.json'
        file_path = self.data_directory / filename

        with file_path.open(
            'w',
            encoding="utf-8",
        ) as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return file_path


