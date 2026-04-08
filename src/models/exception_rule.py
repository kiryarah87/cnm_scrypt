from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class ExceptionRule:
    rule_id: int
    origin: str
    destination: str
    date_from: date
    date_to: date
    fixed_rate: float
    fixed_share: float
    reason: str
    priority: int

    def matches(self, origin: str, destination: str, departure: datetime) -> bool:
        dep_date = departure.date() if isinstance(departure, datetime) else departure
        origin_ok = self.origin == "ALL" or self.origin == origin
        dest_ok = self.destination == "ALL" or self.destination == destination
        date_ok = self.date_from <= dep_date <= self.date_to
        return origin_ok and dest_ok and date_ok
