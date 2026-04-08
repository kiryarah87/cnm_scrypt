from datetime import datetime
from pathlib import Path

import xlsxwriter

from ..models.flight import FlightResult


class ResultWriter:
    def __init__(self, filepath: Path) -> None:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        self._filepath = filepath

    def write(self, results: list[FlightResult]) -> None:
        wb = xlsxwriter.Workbook(str(self._filepath), {"constant_memory": True})
        date_fmt = wb.add_format({"num_format": "yyyy-mm-dd hh:mm"})

        # ── Лист Results ──
        ws_main = wb.add_worksheet("Results")
        main_headers = [
            "Origin",
            "Destination",
            "Departure_DateTime",
            "Flight_Number",
            "Ex_Rate",
            "Max_Share",
        ]
        for col, h in enumerate(main_headers):
            ws_main.write(0, col, h)

        for i, r in enumerate(results, start=1):
            ws_main.write_string(i, 0, r.origin)
            ws_main.write_string(i, 1, r.destination)
            if isinstance(r.departure_datetime, datetime):
                ws_main.write_datetime(i, 2, r.departure_datetime, date_fmt)
            else:
                ws_main.write(i, 2, str(r.departure_datetime))
            ws_main.write_string(i, 3, r.flight_number)
            ws_main.write_number(i, 4, r.ex_rate)
            ws_main.write_number(i, 5, r.max_share)

        # ── Лист Debug ──
        ws_debug = wb.add_worksheet("Debug")
        debug_headers = [
            "Flight_Number",
            "Origin",
            "Destination",
            "Departure_DateTime",
            "DTD",
            "Line_Key",
            "Load_Plan",
            "Load_Fact",
            "Deviation",
            "Coef_Rate",
            "Coef_Share",
            "Ex_Rate",
            "Max_Share",
            "Exception_ID",
        ]
        for col, h in enumerate(debug_headers):
            ws_debug.write(0, col, h)

        for i, r in enumerate(results, start=1):
            ws_debug.write_string(i, 0, r.flight_number)
            ws_debug.write_string(i, 1, r.origin)
            ws_debug.write_string(i, 2, r.destination)
            if isinstance(r.departure_datetime, datetime):
                ws_debug.write_datetime(i, 3, r.departure_datetime, date_fmt)
            else:
                ws_debug.write(i, 3, str(r.departure_datetime))
            ws_debug.write_number(i, 4, r.dtd)
            ws_debug.write_string(i, 5, r.line_key)
            ws_debug.write_number(i, 6, r.load_plan)
            ws_debug.write_number(i, 7, r.load_fact)
            ws_debug.write_number(i, 8, r.deviation)
            ws_debug.write_number(i, 9, r.coef_rate)
            ws_debug.write_number(i, 10, r.coef_share)
            ws_debug.write_number(i, 11, r.ex_rate)
            ws_debug.write_number(i, 12, r.max_share)
            if r.exception_id is not None:
                ws_debug.write_number(i, 13, r.exception_id)
            else:
                ws_debug.write_blank(i, 13, None)

        wb.close()
        print(f"Результаты записаны: {self._filepath}  ({len(results)} рейсов)")
