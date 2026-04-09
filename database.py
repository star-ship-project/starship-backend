import sqlite3

class DatabaseManager:
    def __init__(self, db_file: str):
        self.db_file = db_file

    def init_db(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS teachers (
                    deped_id TEXT PRIMARY KEY,
                    school_id TEXT,
                    first_name TEXT,
                    middle_name TEXT,
                    last_name TEXT,
                    suffix_name TEXT,
                    sex TEXT,
                    age INTEGER,
                    contact_number TEXT,
                    step INTEGER DEFAULT 0,
                    errors INTEGER DEFAULT 0
                )
            """)
            conn.commit()
        print("[DB] SQLite Database Initialized.")

    def track_user(self, phone: str):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT step, errors FROM teachers WHERE phone = ?",
                (phone,)
            )
            return cursor.fetchone()

    def create_user(self, phone: str):
        # TODO: Parse full name of teacher's entry
        # TODO: Insert into database after parsing
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO teachers (phone, step, errors) VALUES (?, 1, 0)",
                (phone,)
            )
            conn.commit()

    def update_answer(self, phone: str, column_name: str, number: int, next_step: int):
        allowed_columns = {"q1_total_students", "q2_no_internet"}
        if column_name not in allowed_columns:
            raise ValueError(f"Invalid column name: {column_name}")

        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE teachers
                SET {column_name} = ?, step = ?, errors = 0
                WHERE phone = ?
            """, (number, next_step, phone))
            conn.commit()

    def increment_error(self, phone: str):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE teachers SET errors = errors + 1 WHERE phone = ?",
                (phone,)
            )
            conn.commit()
