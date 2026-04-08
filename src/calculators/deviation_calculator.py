from collections.abc import Iterator

from ..config import CARRIER_PREFIXES, DEFAULT_CARRIER_PREFIX, DEFAULT_LINE_KEY, MAX_DTD, MOSCOW_AIRPORTS, NOT_FOUND_LOAD_PLAN


class DeviationCalculator:

    def __init__(self, line_models: dict[tuple[str, int], float]) -> None:
        self._models = line_models

    def get_load_plan(
        self, origin: str, destination: str, dtd: int, flight_number: str
    ) -> tuple[float, str]:
        """Возвращает (load_plan, использованный line_key)."""
        dtd_clamped = min(dtd, MAX_DTD)

        for line_key in self._candidate_keys(origin, destination, flight_number):
            plan = self._models.get((line_key, dtd_clamped))
            if plan is not None:
                return plan, line_key

        return NOT_FOUND_LOAD_PLAN

    def _candidate_keys(
        self, origin: str, destination: str, flight_number: str
    ) -> Iterator[str]:
        """Генерирует ключи-кандидаты в порядке приоритета."""
        o = self._normalize_airport(origin)
        d = self._normalize_airport(destination)
        primary_prefix = self._carrier_prefix(flight_number)

        ordered_prefixes = [primary_prefix] + [
            pfx for pfx in CARRIER_PREFIXES if pfx != primary_prefix
        ]

        for pfx in ordered_prefixes:
            yield f"{pfx}_{o}-{d}"
            yield f"{pfx}_{d}-{o}"

        yield DEFAULT_LINE_KEY

    def calculate_deviation(self, load_fact: float, load_plan: float) -> float:
        return load_fact - load_plan

    @staticmethod
    def _normalize_airport(code: str) -> str:
        return MOSCOW_AIRPORTS.get(code, code)

    @staticmethod
    def _carrier_prefix(flight_number: str) -> str:
        for pfx in CARRIER_PREFIXES:
            if flight_number.upper().startswith(pfx):
                return pfx
        return DEFAULT_CARRIER_PREFIX
