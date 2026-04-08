import os
from concurrent.futures import ThreadPoolExecutor
from datetime import date

from .calculators.deviation_calculator import DeviationCalculator
from .calculators.dtd_calculator import DTDCalculator
from .calculators.exception_resolver import ExceptionResolver
from .calculators.rate_calculator import RateCalculator
from .calculators.share_calculator import ShareCalculator
from .models.exception_rule import ExceptionRule
from .models.flight import FlightInventory, FlightResult
from .models.settings import BasicSettings, DeviationCoeffRow


class MilesEngine:
    def __init__(
        self,
        settings: BasicSettings,
        deviation_table: list[DeviationCoeffRow],
        line_models: dict[tuple[str, int], float],
        exceptions: list[ExceptionRule],
        current_date: date,
    ) -> None:
        self._current_date = current_date
        self._dtd_calc = DTDCalculator()
        self._dev_calc = DeviationCalculator(line_models)
        self._rate_calc = RateCalculator(settings, deviation_table)
        self._share_calc = ShareCalculator(settings, deviation_table)
        self._exc_resolver = ExceptionResolver(exceptions)

    def process_flight(self, flight: FlightInventory) -> FlightResult:
        dtd = self._dtd_calc.calculate(self._current_date, flight.departure_datetime)

        load_plan, line_key = self._dev_calc.get_load_plan(
            flight.origin, flight.destination, dtd, flight.flight_number
        )
        deviation = self._dev_calc.calculate_deviation(flight.load_fact, load_plan)

        ex_rate, coef_rate = self._rate_calc.calculate(deviation)
        max_share, coef_share = self._share_calc.calculate(deviation)

        exception = self._exc_resolver.resolve(
            flight.origin, flight.destination, flight.departure_datetime
        )
        exception_id = None
        if exception is not None:
            ex_rate = exception.fixed_rate
            max_share = exception.fixed_share
            exception_id = exception.rule_id

        return FlightResult(
            origin=flight.origin,
            destination=flight.destination,
            departure_datetime=flight.departure_datetime,
            flight_number=flight.flight_number,
            ex_rate=round(ex_rate, 4),
            max_share=round(max_share, 4),
            dtd=dtd,
            line_key=line_key,
            load_plan=round(load_plan, 4),
            load_fact=round(flight.load_fact, 4),
            deviation=round(deviation, 4),
            coef_rate=round(coef_rate, 4),
            coef_share=round(coef_share, 4),
            exception_id=exception_id,
        )

    def process_all(self, flights: list[FlightInventory]) -> list[FlightResult]:
        if len(flights) < 5000:
            return [self.process_flight(f) for f in flights]

        workers = min(os.cpu_count() or 4, 8)
        with ThreadPoolExecutor(max_workers=workers) as pool:
            return list(pool.map(self.process_flight, flights))
