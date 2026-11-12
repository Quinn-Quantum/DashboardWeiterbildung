import sys
from PyQt6.QtWidgets import QApplication, QMainWindow

from Dashboard import Dashboard
# Importieren Sie hier den Namen Ihrer generierten Datei (ohne .py) und die Klasse
from gui_main_window import Ui_Dialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. UI-Klasse initialisieren
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        dashboard = Dashboard()
        time_for_study = dashboard.lade_time()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())