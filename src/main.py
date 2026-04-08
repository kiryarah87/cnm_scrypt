import time

from .config import INVENTORY_FILE, LINE_MODELS_FILE, OUTPUT_FILE, UI_FILE
from .engine import MilesEngine
from .readers import InventoryReader, LineModelsReader, SettingsReader
from .writers import ResultWriter


def main() -> None:
    t0 = time.perf_counter()
    print("=" * 60)
    print("  Движок расчёта миль — запуск")
    print("=" * 60)

    t = time.perf_counter()
    print("\nЧтение UI_with_input_cells ...")
    ui_data = SettingsReader(UI_FILE).read()
    settings = ui_data["basic_settings"]
    current_date = ui_data["current_date"]
    deviation_table = ui_data["deviation_table"]
    exceptions = ui_data["exceptions"]
    print(f"  current_date = {current_date}")
    print(f"  Исключений: {len(exceptions)}")
    print(f"  ⏱ {time.perf_counter() - t:.2f} с")

    t = time.perf_counter()
    print("\nЧтение line_models_dusid ...")
    line_models = LineModelsReader(LINE_MODELS_FILE).read()
    unique_lines = {k[0] for k in line_models}
    print(f"  Направлений: {len(unique_lines)}, записей: {len(line_models)}")
    print(f"  ⏱ {time.perf_counter() - t:.2f} с")

    t = time.perf_counter()
    print("\nЧтение inventory_soda ...")
    flights = InventoryReader(INVENTORY_FILE).read()
    print(f"  Рейсов: {len(flights)}")
    print(f"  ⏱ {time.perf_counter() - t:.2f} с")

    t = time.perf_counter()
    print("\nРасчёт ...")
    engine = MilesEngine(
        settings=settings,
        deviation_table=deviation_table,
        line_models=line_models,
        exceptions=exceptions,
        current_date=current_date,
    )
    results = engine.process_all(flights)
    print(f"  ⏱ {time.perf_counter() - t:.2f} с")

    t = time.perf_counter()
    print("\nЗапись результатов ...")
    ResultWriter(OUTPUT_FILE).write(results)
    print(f"  ⏱ {time.perf_counter() - t:.2f} с")

    elapsed = time.perf_counter() - t0
    print(f"\nОбщее время: {elapsed:.2f} с")
    print("=" * 60)


if __name__ == "__main__":
    main()
