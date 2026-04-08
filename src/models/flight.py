from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class FlightInventory:
    flight_number: str
    origin: str
    destination: str
    departure_datetime: datetime
    load_fact: float


@dataclass
class FlightResult:
    origin: str
    destination: str
    departure_datetime: datetime
    flight_number: str
    ex_rate: float
    max_share: float
    # отладочная информация
    dtd: int = 0
    line_key: str = ""
    load_plan: float = 0.0
    load_fact: float = 0.0
    deviation: float = 0.0
    coef_rate: float = 0.0
    coef_share: float = 0.0
    exception_id: int | None = None
