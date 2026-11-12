import sqlite3
import os


class DatabaseConnection:
    def __init__(self, db_name="coursedaten.db"):
        self.db_name = db_name
        # Prüfen, ob die Datenbank beim Start schon existiert
        db_exists = os.path.exists(self.db_name)

        # Verbindung herstellen (erstellt die Datei, falls sie nicht da ist)
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

        # Wenn die DB neu ist, Tabellen anlegen
        if not db_exists:
            self.create_tables()

    def create_tables(self):
        """create the Db at the first start"""
        # Tabelle für Kurse
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                time INTEGER
                test_id INTEGER
                FOREIGN KEY (test_id) REFERENCES courses (id)
            )
        """)

        # Tabelle für Tests (mit Verknüpfung zum Kurs über course_id, falls gewünscht)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type_of_examination TEXT NOT NULL,
                is_mandatory BOOLEAN,
                
            )
        """)
        self.connection.commit()
        print("Datenbank und Tabellen wurden erfolgreich erstellt!")

    def close(self):
        self.connection.close()