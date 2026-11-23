from PyQt6.QtCore import QDate
from PyQt6.QtGui import QColor, QTextCharFormat
from PyQt6.QtWidgets import QCalendarWidget



def highlight_period(
        calendar: QCalendarWidget,
        start_date: QDate,
        end_date: QDate,
        bg_color: str,
        fg_color: str | None = None,
) -> None:
    """Highlight entire period of further training"""
    fmt = QTextCharFormat()
    fmt.setBackground(QColor(bg_color))
    if fg_color:
        fmt.setForeground(QColor(fg_color))

    current = start_date
    while current <= end_date:
        calendar.setDateTextFormat(current, fmt)
        current = current.addDays(1)

def mark_study_period(calendar: QCalendarWidget, start_date: QDate, total_months: int) -> None:
    """calculates the end date of the training and then also refers to highlight_period()"""
    end_date = start_date.addMonths(total_months)
    highlight_period(calendar, start_date, end_date, bg_color="#e2e8f0")

def mark_active_course_duration(
        calendar: QCalendarWidget,
        study_start: QDate,
        total_months: int,
        course_start: QDate,
        duration_days: int = 28,
) -> None:
    """Mark current price in the calendar"""
    # First, reset the entire period so that old price markers disappear cleanly
    mark_study_period(calendar, study_start, total_months)
    course_end = course_start.addDays(duration_days)
    highlight_period(
        calendar,
        course_start,
        course_end,
        bg_color="#6e35c9",
        fg_color="white",
    )