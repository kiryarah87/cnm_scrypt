from ..models.settings import BasicSettings


class BasicSettingsValidator:
    """Валидация основных настроек тарификации."""

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

    def validate_raw(self, raw_params: dict[str, object]) -> list[str]:
        """Валидация сырых значений из Excel до построения модели."""
        errors: list[str] = []

        required_fields = [
            "Base_Rate",
            "Base_Share",
            "Min_Rate",
            "Max_Rate",
            "Min_Share",
            "Max_Share",
            "Rate_Multiplier",
            "Share_Multiplier",
        ]

        for field in required_fields:
            if field not in raw_params:
                errors.append(f"Отсутствует обязательный параметр: {field!r}")
                continue
            _, ok = self._try_parse_float(raw_params[field])
            if not ok:
                errors.append(
                    f"Параметр {field!r} содержит некорректное значение: "
                    f"{raw_params[field]!r}"
                )

        return errors

    def validate(self, settings: BasicSettings) -> list[str]:
        """Логическая валидация уже распарсенных настроек."""
        errors: list[str] = []

        if settings.min_rate >= settings.max_rate:
            errors.append(
                f"Min_Rate ({settings.min_rate}) должен быть меньше "
                f"Max_Rate ({settings.max_rate})"
            )
        if settings.min_share >= settings.max_share:
            errors.append(
                f"Min_Share ({settings.min_share}) должен быть меньше "
                f"Max_Share ({settings.max_share})"
            )
        if not (settings.min_rate <= settings.base_rate <= settings.max_rate):
            errors.append(
                f"Base_Rate ({settings.base_rate}) должен быть в диапазоне "
                f"[{settings.min_rate}, {settings.max_rate}]"
            )
        if not (settings.min_share <= settings.base_share <= settings.max_share):
            errors.append(
                f"Base_Share ({settings.base_share}) должен быть в диапазоне "
                f"[{settings.min_share}, {settings.max_share}]"
            )
        if settings.rate_multiplier <= 0:
            errors.append(
                f"Rate_Multiplier ({settings.rate_multiplier}) "
                f"должен быть положительным"
            )
        if settings.share_multiplier <= 0:
            errors.append(
                f"Share_Multiplier ({settings.share_multiplier}) "
                f"должен быть положительным"
            )

        return errors
