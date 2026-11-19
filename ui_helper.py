from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QLayout, QLabel, QListWidget, QListWidgetItem

from CourseTile import CourseTile


def clear_layout_widgets(layout: QLayout) -> None:
    """Removes and schedules all child widgets from the given layout for deletion."""
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()


def clear_active_course_banner(active_layout: QLayout, active_label: QLabel) -> None:
    """Clears the active course display at the top and resets its header label."""
    clear_layout_widgets(active_layout)
    active_label.setText("Aktiver Kurs")


def set_active_course_banner(
    active_layout: QLayout,
    active_label: QLabel,
    course_tile: CourseTile,
    start_date: QDate,
) -> None:
    """Renders the highlighted active course tile at the top of the UI."""
    clear_layout_widgets(active_layout)

    # Create a dedicated display copy for the active course banner
    active_display_tile = CourseTile(
        course_tile.course_id,
        course_tile.name,
        course_tile.test_name,
        course_tile.is_mandatory,
    )
    active_display_tile.setStyleSheet("""
        CourseTile {
            background-color: #6e35c9;
            border: 2px solid #522596;
            border-radius: 10px;
            padding: 15px;
        }
    """)
    active_display_tile.name_label.setStyleSheet("font-size: 20px; color: white;")
    active_display_tile.info_label.setStyleSheet("font-size: 15px; color: white;")

    active_layout.addWidget(active_display_tile)
    active_display_tile.show()

    active_label.setText(
        f"Aktiver Kurs: {course_tile.name} (Start: {start_date.toString('dd.MM.yyyy')})"
    )


def update_course_tile_styles(list_widget: QListWidget, active_course_id: int | None) -> None:
    """Updates active/inactive visual styling across all tiles in the list widget."""
    for i in range(list_widget.count()):
        item = list_widget.item(i)
        tile = list_widget.itemWidget(item)
        if tile:
            tile.set_active_style(tile.course_id == active_course_id)


def populate_course_list(
    list_widget: QListWidget,
    courses: list,
    on_delete_callback,
) -> tuple[CourseTile | None, int | None, QDate | None]:
    """Populates the course list widget and returns info about any active course."""
    list_widget.clear()

    active_tile_to_restore = None
    active_course_id = None
    active_start_date = None

    for course_data in courses:
        c_id, name, time, test_name, is_mandatory, is_active, start_date, is_complete = course_data
        tile = CourseTile(c_id, name, test_name, is_mandatory, is_complete)

        # Connect delete signal emitted by the tile
        tile.delete_requested.connect(on_delete_callback)

        item = QListWidgetItem(list_widget)
        item.setSizeHint(tile.sizeHint())
        list_widget.setItemWidget(item, tile)

        # Track active course to restore state after reload
        if is_active == 1:
            active_tile_to_restore = tile
            active_course_id = tile.course_id
            if start_date:
                active_start_date = QDate.fromString(start_date, "yyyy-MM-dd")
            else:
                active_start_date = QDate.currentDate()

    return active_tile_to_restore, active_course_id, active_start_date