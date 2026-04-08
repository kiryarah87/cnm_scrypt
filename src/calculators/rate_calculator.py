from ..models.settings import BasicSettings, DeviationCoeffRow


class RateCalculator:
    def __init__(
        self, settings: BasicSettings, deviation_table: list[DeviationCoeffRow]
    ) -> None:
        self._settings = settings
        self._table = deviation_table

    def calculate(self, deviation: float) -> tuple[float, float]:
        """Возвращает (итоговый_курс, использованный_коэффициент)."""
        coef = self._find_coef_rate(deviation)
        temp_rate = self._settings.base_rate * coef * self._settings.rate_multiplier
        return self._settings.clamp_rate(temp_rate), coef

    def _find_coef_rate(self, deviation: float) -> float:
        for row in self._table:
            if row.contains(deviation):
                return row.coef_rate
        if deviation < self._table[0].min_dev:
            return self._table[0].coef_rate
        return self._table[-1].coef_rate
