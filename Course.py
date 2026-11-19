from Test import Test
from dataclasses import dataclass, field
from PyQt6.QtCore import QDate
from typing import Optional

@dataclass
class Course:
    name: str
    test: Test
    duration_weeks: int = 4
    is_active: bool = False
    is_complete: bool = False
    start_date: Optional[QDate] = None


    def ensure_start_date(self) -> QDate:
        """Returns a valid QDate start date, defaulting to today if none is set."""
        if self.start_date is None or not self.start_date.isValid():
            self.start_date = QDate.currentDate()
        return self.start_date

    def end_date(self) -> QDate:
        """Calculates the end QDate based on start_date and duration in weeks."""
        start = self.ensure_start_date()
        return start.addDays(self.duration_weeks * 7)

    def remaining_days(self, reference_date: Optional[QDate] = None) -> int:
        """Returns remaining days until the course ends (minimum 0)."""
        today = reference_date if (reference_date and reference_date.isValid()) else QDate.currentDate()
        return max(0, today.daysTo(self.end_date()))