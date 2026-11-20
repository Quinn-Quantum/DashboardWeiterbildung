import sqlite3
import os

from PyQt6.QtCore import QDate


class DatabaseConnection:
    def __init__(self, db_name="coursesData.db"):
        self.db_name = db_name
        # Check if the database already exists at startup
        db_exists = os.path.exists(self.db_name)

        # Connect (creates the file if it's not there)
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")


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
                start_date TEXT,
                is_complete INTEGER DEFAULT 0,
                FOREIGN KEY (test_id) REFERENCES tests (id)
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
        print("Database and tables have been successfully created!")

    def close(self):
        self.connection.close()

    def store_in_db(self, name_course, name_test, is_mandatory):
        try:
            self.cursor.execute(
                "INSERT INTO tests (type_of_examination, is_mandatory) VALUES (?, ?)",
                (name_test, 1 if is_mandatory else 0)
            )
            test_id = self.cursor.lastrowid
            # 4 because my courses always last 4 weeks
            self.cursor.execute(
                "INSERT INTO courses (name, time, test_id) VALUES (?, ?, ?)",
                (name_course, 4, test_id)
            )
            self.connection.commit()
            print(f"Successfully saved! Course: '{name_course}', Test-ID: {test_id}, Duration: 4 weeks")
        except Exception as e:
            print(f"Failed to save to db: {e}")

    def set_active_course_in_db(self, course_id, start_date):
        """Set all courses to inactive (0) and the selected course to active (1)"""
        effective_date = (
            start_date if (start_date is not None and start_date.isValid()) else QDate.currentDate()
        )

        date_str = effective_date.toString("yyyy-MM-dd")

        try:
            self.cursor.execute("UPDATE courses SET is_active = 0, start_date = NULL")
            self.cursor.execute("UPDATE courses SET is_active = 1, start_date = ? WHERE id = ?",
                (date_str, course_id),
            )
            self.connection.commit()
            print(f"Active course {course_id} updated in database ")
        except Exception as e:
            print(f"Error updating active course: {e}")

    def get_all_courses(self):
        """lode all Courses"""
        self.cursor.execute("""SELECT c.id, c.name, c.time, t.type_of_examination, t.is_mandatory, c.is_active, c.start_date, c.is_complete
                                FROM courses c
                                LEFT JOIN tests t ON c.test_id = t.id""")

        return self.cursor.fetchall()

    def delete_course_from_db(self, course_id):
        """Deletes a course and the linked test from the db."""
        try:
            # Determine test ID to also clean up the test
            self.cursor.execute("SELECT test_id FROM courses WHERE id = ?", (course_id,))
            row = self.cursor.fetchone()
            # delete course
            self.cursor.execute("DELETE FROM courses WHERE id = ?", (course_id,))

            if row and row[0]:
                test_id = row[0]
                self.cursor.execute("DELETE FROM tests WHERE id = ?", (test_id,))


            self.connection.commit()
            print(f"Course with ID {course_id} successfully deleted.")
        except Exception as e:
            print(f"Error deleting the course: {e}")

    def mark_cours_as_complet(self,course_id):
        """Updates the completion status of a course"""
        try:
            self.cursor.execute("UPDATE courses SET is_complete = 1, is_active = 0 WHERE id = ?",
                                ( course_id,))
            self.connection.commit()
            print(f"Course ID {course_id} successfully marked as complete and set to inactive.")
        except Exception as e:
            print(f"Error updating complet course: {e}")