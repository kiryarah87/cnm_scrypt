from datetime import datetime
from typing import Optional

from ..models.exception_rule import ExceptionRule


class ExceptionResolver:
    def __init__(self, rules: list[ExceptionRule]) -> None:
        self._rules = sorted(rules, key=lambda r: r.priority)

    def resolve(
        self, origin: str, destination: str, departure: datetime
    ) -> Optional[ExceptionRule]:
        best: Optional[ExceptionRule] = None
        for rule in self._rules:
            if rule.matches(origin, destination, departure):
                if best is None or rule.priority < best.priority:
                    best = rule
                    if best.priority == 1:
                        break
        return best
