from datetime import date, datetime


class DTDCalculator:
    @staticmethod
    def calculate(current_date: date, departure: datetime) -> int:
        dep_date = departure.date() if isinstance(departure, datetime) else departure
        dtd = (dep_date - current_date).days
        return max(dtd, 0)
