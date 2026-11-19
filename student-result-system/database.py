
import sqlite3
from pathlib import Path

# Location of the database folder
DATABASE_DIR = Path(__file__).parent / "database"

# Location of the database file
DATABASE_PATH = DATABASE_DIR / "school.db"


def get_connection():
    DATABASE_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    # Enable foreign-key enforcement
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teacher_classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id INTEGER NOT NULL,
            class_name TEXT NOT NULL,
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (teacher_id)
                REFERENCES users(id)
                ON DELETE CASCADE,

            UNIQUE(teacher_id, class_name)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            role TEXT NOT NULL
                CHECK(role IN ('student', 'teacher', 'admin'))
        )
    """)


    # Add password-change tracking to existing databases
    columns = [
        column["name"]
        for column in cursor.execute("PRAGMA table_info(users)").fetchall()
    ]

    if "must_change_password" not in columns:
        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN must_change_password INTEGER NOT NULL DEFAULT 0
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_accounts (
            user_id INTEGER PRIMARY KEY,
            reg_no TEXT UNIQUE NOT NULL,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reg_no TEXT NOT NULL,
            class_name TEXT NOT NULL,
            attendance_date TEXT NOT NULL,
            status TEXT NOT NULL
                CHECK(status IN ('Present', 'Absent', 'Late')),
            marked_by INTEGER NOT NULL,
            FOREIGN KEY (marked_by) REFERENCES users(id),
            UNIQUE(reg_no, attendance_date)
        )
    """)

    connection.commit()
    connection.close()
def get_teachers():
    connection = get_connection()

    teachers = connection.execute("""
        SELECT id, username
        FROM users
        WHERE role = 'teacher'
        ORDER BY username
    """).fetchall()

    connection.close()
    return teachers


def assign_teacher_to_class(teacher_id, class_name):
    connection = get_connection()

    try:
        connection.execute("""
            INSERT INTO teacher_classes (teacher_id, class_name)
            VALUES (?, ?)
        """, (teacher_id, class_name))

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


def get_teacher_classes(teacher_id):
    connection = get_connection()

    classes = connection.execute("""
        SELECT class_name
        FROM teacher_classes
        WHERE teacher_id = ?
        ORDER BY class_name
    """, (teacher_id,)).fetchall()

    connection.close()

    return [row["class_name"] for row in classes]

if __name__ == "__main__":
    initialize_database()
    print("School database created successfully!")


def get_student_reg_no(user_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT reg_no FROM student_accounts WHERE user_id = ?",
            (user_id,)
        )

        result = cursor.fetchone()

        if result:
            return result["reg_no"]

        return None

    finally:
        connection.close()