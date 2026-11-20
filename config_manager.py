import os
from PyQt6.QtCore import QDate

class ConfigManager:
    def __init__(self, filepath: str = "time.txt", default_months: int = 6):
        self.filepath = filepath
        self.default_months = default_months

    def write(self, start_str: str, months: int) -> None:
        """Writes start, date, and time of the training in txt"""
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write(f"{start_str}\n{months}")

    def load_raw(self) -> tuple[str, int]:
        """Reads start date as string (YYYY-MM-DD) and months as int, with fallback."""
        default_date_str = QDate.currentDate().toString("yyyy-MM-dd")

        if not os.path.exists(self.filepath):
            return default_date_str, self.default_months

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
                if len(lines) >= 2:
                    start_str = lines[0].strip()
                    months = int(lines[1].strip())
                    if QDate.fromString(start_str, "yyyy-MM-dd").isValid():
                        return start_str, months
        except Exception as e:
            print(f"Error reading {self.filepath}: {e}")

        return default_date_str, self.default_months

    def load_or_default(self) -> tuple[QDate, int]:
        """returns default values"""
        default_date = QDate.currentDate()
        default_months = 6

        if not os.path.exists(self.filepath):
            self.write(default_date.toString("yyyy-MM-dd"), default_months)
            return default_date, default_months

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
                start_date = QDate.fromString(lines[0], "yyyy-MM-dd")
                months = int(lines[1])
                if not start_date.isValid():
                    raise ValueError("Ungültiges Startdatum")
                return start_date, months
        except Exception as e:
            print(f"Fehler bei {self.filepath}: {e} – nutze Standardwerte.")
            self.write(default_date.toString("yyyy-MM-dd"), default_months)
            return default_date, default_months