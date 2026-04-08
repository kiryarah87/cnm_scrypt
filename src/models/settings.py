from dataclasses import dataclass


@dataclass(frozen=True)
class BasicSettings:
    base_rate: float
    base_share: float
    min_rate: float
    max_rate: float
    min_share: float
    max_share: float
    rate_multiplier: float
    share_multiplier: float

    def clamp_rate(self, value: float) -> float:
        return max(self.min_rate, min(value, self.max_rate))

    def clamp_share(self, value: float) -> float:
        return max(self.min_share, min(value, self.max_share))


@dataclass(frozen=True)
class DeviationCoeffRow:
    load_label: str
    min_dev: float
    max_dev: float
    coef_rate: float
    coef_share: float

    def contains(self, deviation: float) -> bool:
        return self.min_dev <= deviation < self.max_dev
