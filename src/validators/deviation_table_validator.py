from ..models.settings import DeviationCoeffRow


class DeviationTableValidator:
    """Валидация таблицы коэффициентов отклонений."""

    @staticmethod
    def _try_parse_float(value) -> tuple[float, bool]:
        if value is None:
            return 0.0, True
        if isinstance(value, (int, float)):
            return float(value), True
        s = str(value).replace(",", ".").replace("%", "").strip()
        try:
            return float(s), True
        except ValueError:
            return 0.0, False

    def validate_raw(self, raw_rows: list[dict[str, object]]) -> list[str]:
        """Валидация сырых значений строк до построения модели."""
        errors: list[str] = []

        if not raw_rows:
            errors.append("Таблица отклонений пуста")
            return errors

        numeric_fields = ["min_dev", "max_dev", "coef_rate", "coef_share"]

        for i, row in enumerate(raw_rows):
            label = row.get("label", f"#{i + 1}")
            for field in numeric_fields:
                _, ok = self._try_parse_float(row.get(field))
                if not ok:
                    errors.append(
                        f"DeviationTable строка {i + 1} ({label!r}), {field}: "
                        f"некорректное значение {row.get(field)!r}"
                    )

        return errors

    def validate(self, rows: list[DeviationCoeffRow]) -> list[str]:
        """Логическая валидация уже распарсенных строк."""
        errors: list[str] = []

        if not rows:
            errors.append("Таблица отклонений пуста")
            return errors

        for i, row in enumerate(rows):
            if row.min_dev >= row.max_dev:
                errors.append(
                    f"Строка {i + 1} ({row.load_label!r}): "
                    f"min_dev ({row.min_dev}) >= max_dev ({row.max_dev})"
                )
            if row.coef_rate < 0:
                errors.append(
                    f"Строка {i + 1} ({row.load_label!r}): "
                    f"coef_rate ({row.coef_rate}) отрицательный"
                )
            if row.coef_share < 0:
                errors.append(
                    f"Строка {i + 1} ({row.load_label!r}): "
                    f"coef_share ({row.coef_share}) отрицательный"
                )

        sorted_rows = sorted(rows, key=lambda r: r.min_dev)
        for prev, curr in zip(sorted_rows, sorted_rows[1:]):
            if prev.max_dev != curr.min_dev:
                errors.append(
                    f"Разрыв или перекрытие диапазонов между "
                    f"{prev.load_label!r} (max={prev.max_dev}) "
                    f"и {curr.load_label!r} (min={curr.min_dev})"
                )

        return errors
