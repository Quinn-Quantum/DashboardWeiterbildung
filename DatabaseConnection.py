import sqlite3
import os




class DatabaseConnection:
    def __init__(self, db_name="coursesData.db"):
        self.db_name = db_name
        # Check if the database already exists at startup
        db_exists = os.path.exists(self.db_name)

        # Connect (creates the file if it's not there)
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

        # If the DB is new, create tables
        if not db_exists:
            self.create_db()

    def create_db(self):
        """create the DB at the first start"""
        # Table for courses
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                time INTEGER,
                test_id INTEGER,
                is_active INTEGER DEFAULT 0,
                FOREIGN KEY (test_id) REFERENCES courses (id)
            )
        """)

        # Table for tests (with link to the course via course_id, if desired)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type_of_examination TEXT NOT NULL,
                is_mandatory BOOLEAN                
            )
        """)
        self.connection.commit()
        print("Datenbank und Tabellen wurden erfolgreich erstellt!")

    def close(self):
        self.connection.close()

    def store_in_db(self, name_course, name_test, is_mandatory):
        try:
            self.cursor.execute(
                "INSERT INTO tests (type_of_examination, is_mandatory) VALUES (?, ?)",
                (name_test, 1 if is_mandatory else 0)
            )
            test_id = self.cursor.lastrowid

            self.cursor.execute(
                "INSERT INTO courses (name, time, test_id) VALUES (?, ?, ?)",
                (name_course, 4, test_id)
            )
            self.connection.commit()
            print(f"Erfolgreich gespeichert! Kurs: '{name_course}', Test-ID: {test_id}, Dauer: 4 Wochen")
        except Exception as e:
            print(f"Fehler beim Speichern in die Datenbank: {e}")

    def set_active_course_in_db(self, course_id):
        """Set all courses to inactive (0) and the selected course to active (1)"""
        try:
            self.cursor.execute("UPDATE courses SET is_active = 0")
            self.cursor.execute("UPDATE courses SET is_active = 1 WHERE id = ?", (course_id,))
            self.connection.commit()
        except Exception as e:
            print(f"Fehler beim Aktualisieren des aktiven Kurses: {e}")

    def get_all_courses(self):
        """lode all Courses"""
        self.cursor.execute("""SELECT c.id, c.name, c.time, t.type_of_examination, t.is_mandatory, c.is_active
                                FROM courses c
                                LEFT JOIN tests t ON c.test_id = t.id""")

        return self.cursor.fetchall()