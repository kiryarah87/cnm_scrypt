import pandas as pd

from ..config import MAX_DTD
from .base_reader import BaseReader


class LineModelsReader(BaseReader):
    def read(self) -> dict[tuple[str, int], float]:
        df = pd.read_excel(self.filepath, header=0, engine="calamine")
        line_col = df.columns[0]
        dtd_columns = [c for c in df.columns[1:] if 0 <= int(c) <= MAX_DTD]

        df_long = df[[line_col] + dtd_columns].melt(
            id_vars=line_col, var_name="dtd", value_name="load_plan"
        )
        df_long[line_col] = df_long[line_col].astype(str).str.strip()
        df_long["dtd"] = df_long["dtd"].astype(int)
        df_long["load_plan"] = df_long["load_plan"].apply(self._parse_pct)

        return dict(
            zip(
                zip(df_long[line_col], df_long["dtd"]),
                df_long["load_plan"],
            )
        )

    @staticmethod
    def _parse_pct(value) -> float:
        if isinstance(value, (int, float)):
            v = float(value)
            return v if v <= 1.0 else v / 100.0
        s = str(value).replace(",", ".").replace("%", "").strip()
        try:
            v = float(s)
            return v / 100.0 if v > 1.0 else v
        except ValueError:
            return 0.0
