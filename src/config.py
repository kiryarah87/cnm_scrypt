import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    # Запуск из .exe
    BASE_DIR = Path(sys.executable).parent
else:
    # Обычный запуск через Python
    BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# Создать папку output если не существует
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

UI_FILE = DATA_DIR / "UI_with_input_cells.xlsx"
LINE_MODELS_FILE = DATA_DIR / "line_models_dusid.xlsx"
INVENTORY_FILE = DATA_DIR / "inventory_soda.xlsx"
OUTPUT_FILE = OUTPUT_DIR / "flights_with_data.xlsx"

# ...existing code...
SHEET_BASIC_SETTINGS = "Basic settings"
SHEET_EXCEPTIONS = "Exceptions"

MOSCOW_AIRPORTS = {"SVO": "MOW", "DME": "MOW", "VKO": "MOW"}
MAX_DTD = 100

DEFAULT_LINE_KEY = "default"
NOT_FOUND_LOAD_PLAN = (0.0, "NOT_FOUND")

CARRIER_PREFIXES = ["SU", "FV"]
DEFAULT_CARRIER_PREFIX = "SU"

BASIC_PARAM_RANGES = [(4, 10), (12, 14)]
BASIC_PARAM_NAME_COL = 2
BASIC_PARAM_VALUE_COL = 3

CURRENT_DATE_ROW = 2
CURRENT_DATE_COL = 6

DEVIATION_START_ROW = 19
DEVIATION_COLUMNS = {
    "label": 2,
    "min_dev": 3,
    "max_dev": 4,
    "coef_rate": 5,
    "coef_share": 6,
}

EXCEPTION_COUNT_ROW = 2
EXCEPTION_COUNT_COL = 10
EXCEPTION_START_ROW = 4
EXCEPTION_COLUMNS = {
    "rule_id": 2,
    "origin": 3,
    "destination": 4,
    "date_from": 5,
    "date_to": 6,
    "fixed_rate": 7,
    "fixed_share": 8,
    "reason": 9,
    "priority": 10,
}
