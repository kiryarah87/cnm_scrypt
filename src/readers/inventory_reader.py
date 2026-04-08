import pandas as pd

from ..models.flight import FlightInventory
from .base_reader import BaseReader


class InventoryReader(BaseReader):
    def read(self) -> list[FlightInventory]:
        df = pd.read_excel(
            self.filepath,
            header=0,
            dtype={
                "flight_number": str,
                "origin": str,
                "destination": str,
            },
            engine="calamine",
        )

        df["departure_datetime"] = pd.to_datetime(df["departure_datetime"])
        df["origin"] = df["origin"].str.strip().str.upper()
        df["destination"] = df["destination"].str.strip().str.upper()
        df["flight_number"] = df["flight_number"].str.strip()
        df["load_fact"] = df["load_fact"].astype(float)

        return [
            FlightInventory(fn, orig, dest, dep, lf)
            for fn, orig, dest, dep, lf in zip(
                df["flight_number"],
                df["origin"],
                df["destination"],
                df["departure_datetime"],
                df["load_fact"],
            )
        ]
