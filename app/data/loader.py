from dataclasses import dataclass
from pathlib import Path
import csv

_CSV_PATH = Path(__file__).resolve().parent.parent.parent / 'data' / 'precincts_merged.csv'


@dataclass
class Precinct:
    id: int
    lat: float
    lon: float
    left: int
    right: int
    arab: int
    population: int
    name: str


def load_precincts() -> list[Precinct]:
    precincts = []
    with open(_CSV_PATH, encoding='utf-8') as f:
        for i, row in enumerate(csv.DictReader(f)):
            try:
                precincts.append(Precinct(
                    id=i,
                    lat=float(row['lat']),
                    lon=float(row['lon']),
                    left=int(float(row['left'])),
                    right=int(float(row['right'])),
                    arab=int(float(row['arab'])),
                    population=int(float(row['population'])),
                    name=row['yisuv name'],
                ))
            except (ValueError, KeyError):
                continue
    return precincts
