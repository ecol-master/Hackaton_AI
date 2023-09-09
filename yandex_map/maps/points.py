from dataclasses import dataclass
from enum import Enum
import json


points_yandex_static = {
    "1": "pm2ywm",
    "2":"pm2orm",
    "3":"pm2dom",
    "4": "pm2rdm",
    "5": "pm2am"
}

@dataclass(frozen=True, slots=True)
class Point:
    letter: str
    latitude: float
    longitude: float

def get_points() -> list[Point]:
    with open("./files/data.json", "r") as file:
        data = json.load(file)
        return [
            Point(
                letter=points_yandex_static[d["level"]],
                latitude=d["latitude"],
                longitude=d["longitude"]
            ) for d in data["points"]
        ]


# // {
# //   "level": "5",
# //   "lalitude": 0,
# //   "longitude": ""
# // }