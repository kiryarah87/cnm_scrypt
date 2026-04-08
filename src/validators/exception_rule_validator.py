from datetime import date, datetime

from ..models.exception_rule import ExceptionRule


class ExceptionRuleValidator:
    """Валидация правил-исключений."""

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

    @staticmethod
    def _try_parse_int(value) -> tuple[int, bool]:
        if value is None:
            return 0, False
        if isinstance(value, int):
            return value, True
        if isinstance(value, float):
            return int(value), True
        try:
            return int(str(value).strip()), True
        except (ValueError, TypeError):
            return 0, False

    @staticmethod
    def _try_parse_date(value) -> tuple[date | None, bool]:
        if isinstance(value, datetime):
            return value.date(), True
        if isinstance(value, date):
            return value, True
        return None, False

    def validate_raw(self, raw_rows: list[dict[str, object]]) -> list[str]:
        """Валидация сырых значений строк до построения модели ExceptionRule."""
        errors: list[str] = []

        for i, row in enumerate(raw_rows):
            prefix = f"Exception строка {i + 1}"

            _, ok = self._try_parse_int(row.get("rule_id"))
            if not ok:
                errors.append(
                    f"{prefix}, rule_id: некорректное значение {row.get('rule_id')!r}"
                )

            for str_field in ("origin", "destination"):
                val = row.get(str_field)
                if val is None or str(val).strip() == "":
                    errors.append(f"{prefix}, {str_field}: пустое значение")

            for date_field in ("date_from", "date_to"):
                _, ok = self._try_parse_date(row.get(date_field))
                if not ok:
                    errors.append(
                        f"{prefix}, {date_field}: некорректное значение "
                        f"{row.get(date_field)!r}"
                    )

            for float_field in ("fixed_rate", "fixed_share"):
                _, ok = self._try_parse_float(row.get(float_field))
                if not ok:
                    errors.append(
                        f"{prefix}, {float_field}: некорректное значение "
                        f"{row.get(float_field)!r}"
                    )

            _, ok = self._try_parse_int(row.get("priority"))
            if not ok:
                errors.append(
                    f"{prefix}, priority: некорректное значение {row.get('priority')!r}"
                )

        return errors

    def validate(self, rules: list[ExceptionRule]) -> list[str]:
        """Логическая валидация уже построенных ExceptionRule."""
        errors: list[str] = []
        seen_ids: set[int] = set()

        for rule in rules:
            prefix = f"Rule #{rule.rule_id}"

            if rule.rule_id in seen_ids:
                errors.append(f"{prefix}: дублирующийся rule_id")
            seen_ids.add(rule.rule_id)

            if rule.date_from > rule.date_to:
                errors.append(
                    f"{prefix}: date_from ({rule.date_from}) > date_to ({rule.date_to})"
                )
            if rule.priority < 1:
                errors.append(f"{prefix}: priority ({rule.priority}) должен быть >= 1")
            if rule.fixed_rate < 0:
                errors.append(
                    f"{prefix}: fixed_rate ({rule.fixed_rate}) не может быть отрицательным"
                )
            if rule.fixed_share < 0:
                errors.append(
                    f"{prefix}: fixed_share ({rule.fixed_share}) не может быть отрицательным"
                )
            if not rule.origin:
                errors.append(f"{prefix}: origin не может быть пустым")
            if not rule.destination:
                errors.append(f"{prefix}: destination не может быть пустым")

        return errors
