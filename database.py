import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_file: str):
        self.db_file = db_file

    def init_db(self):
        schema_path = os.path.join(os.path.dirname(__file__), "database", "schema.sql")
        with open(schema_path, "r") as f:
            schema = f.read()

        with sqlite3.connect(self.db_file) as conn:
            conn.executescript(schema)

            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(teachers_bio)")
            columns = [row[1] for row in cursor.fetchall()]
            if "step" not in columns:
                cursor.execute("ALTER TABLE teachers_bio ADD COLUMN step INTEGER DEFAULT 0")
            if "errors" not in columns:
                cursor.execute("ALTER TABLE teachers_bio ADD COLUMN errors INTEGER DEFAULT 0")
            if "id" not in columns:
                cursor.execute("ALTER TABLE teachers_bio ADD COLUMN id INTEGER PRIMARY KEY AUTOINCREMENT")
            conn.commit()
        print("[DB] SQLite Database Initialized.")

    def get_user(self, phone: str):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT step, errors FROM teachers_bio WHERE phone_number = ?",
                (phone,)
            )
            return cursor.fetchone()

    def create_user(self, deped_id: str, phone: str):
        existing = self.get_user_by_phone(phone)
        if existing:
            return
        
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO teachers_bio (deped_id, phone_number, step, errors) VALUES (?, ?, 1, 0)",
                (deped_id if deped_id else None, phone)
            )
            conn.commit()

    def get_user_by_deped_id(self, deped_id: str):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, deped_id, school_id, first_name, middle_name, last_name, suffix_name, sex, age, phone_number, step, errors FROM teachers_bio WHERE deped_id = ?",
                (deped_id,)
            )
            return cursor.fetchone()

    def get_user_by_phone(self, phone: str):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, deped_id, school_id, first_name, middle_name, last_name, suffix_name, sex, age, phone_number, step, errors FROM teachers_bio WHERE phone_number = ?",
                (phone,)
            )
            return cursor.fetchone()

    def update_bio(self, user_id: int, field: str, value, next_step: int):
        allowed_fields = {
            "deped_id", "school_id", "first_name", "middle_name", "last_name", 
            "suffix_name", "sex", "age"
        }
        if field not in allowed_fields:
            raise ValueError(f"Invalid field: {field}")

        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE teachers_bio
                SET {field} = ?, step = ?, errors = 0
                WHERE id = ?
            """, (value, next_step, user_id))
            conn.commit()

    def update_professional(self, deped_id: str, field: str, value):
        allowed_fields = {
            "years_experience", "teaching_level", "role_position", 
            "specialization", "is_internet_access", "device_count"
        }
        if field not in allowed_fields:
            raise ValueError(f"Invalid field: {field}")

        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE teachers_professional
                SET {field} = ?
                WHERE teacher_id = ?
            """, (value, deped_id))
            conn.commit()

    def update_step(self, user_id: int, step: int):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE teachers_bio SET step = ?, errors = 0 WHERE id = ?
            """, (step, user_id))
            conn.commit()

    def create_professional_record(self, user_id: int, deped_id: str):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO teachers_professional (teacher_id) VALUES (?)",
                (deped_id,)
            )
            conn.commit()

    def increment_error(self, user_id: int):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE teachers_bio SET errors = errors + 1 WHERE id = ?",
                (user_id,)
            )
            conn.commit()
