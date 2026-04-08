from ..models.settings import BasicSettings, DeviationCoeffRow


class ShareCalculator:
    def __init__(
        self, settings: BasicSettings, deviation_table: list[DeviationCoeffRow]
    ) -> None:
        self._settings = settings
        self._table = deviation_table

    def calculate(self, deviation: float) -> tuple[float, float]:
        """Возвращает (итоговая_доля, использованный_коэффициент)."""
        coef = self._find_coef_share(deviation)
        temp_share = self._settings.base_share * coef * self._settings.share_multiplier
        return self._settings.clamp_share(temp_share), coef

    def _find_coef_share(self, deviation: float) -> float:
        for row in self._table:
            if row.contains(deviation):
                return row.coef_share
        if deviation < self._table[0].min_dev:
            return self._table[0].coef_share
        return self._table[-1].coef_share
