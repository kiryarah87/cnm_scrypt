from dataclasses import dataclass


@dataclass(frozen=True)
class LineModel:
    line: str
    dtd: int
    load_plan: float
