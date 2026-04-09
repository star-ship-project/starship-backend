import sqlite3

class DatabaseManager:
    def __init__(self, db_file: str):
        self.db_file = db_file

    def init_db(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS schools (
                    school_id VARCHAR(10) PRIMARY KEY,
                    name VARCHAR(150) NOT NULL,
                    region VARCHAR(50) NOT NULL,
                    division VARCHAR(100),
                    total_enrollment INTEGER
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS teachers_bio (
                    deped_id VARCHAR(50) PRIMARY KEY,
                    school_id VARCHAR(10) REFERENCES schools (school_id),
                    first_name VARCHAR(100),
                    middle_name VARCHAR(100),
                    last_name VARCHAR(100),
                    suffix_name VARCHAR(100),
                    sex VARCHAR(20),
                    age INTEGER,
                    phone_number VARCHAR(13),
                    step INTEGER DEFAULT 0,
                    errors INTEGER DEFAULT 0
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS teachers_professional (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    teacher_id VARCHAR(50) REFERENCES teachers_bio (deped_id),
                    years_experience INTEGER,
                    teaching_level VARCHAR(50),
                    role_position VARCHAR(100),
                    specialization VARCHAR(50),
                    is_internet_access BOOLEAN,
                    device_count INTEGER
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS qualifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    teacher_id VARCHAR(50) REFERENCES teachers_bio (deped_id),
                    cert_name VARCHAR(255),
                    category VARCHAR(50),
                    awarding_body VARCHAR(150),
                    date_obtained DATETIME
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS star_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    teacher_id VARCHAR(50) REFERENCES teachers_bio(deped_id),
                    event_title VARCHAR(100),
                    event_type VARCHAR(50),
                    event_date date
                )
            """)
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
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO teachers_bio (deped_id, phone_number, step, errors) VALUES (?, ?, 1, 0)",
                (deped_id, phone)
            )
            conn.commit()

    def get_user_by_deped_id(self, deped_id: str):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT deped_id, school_id, first_name, middle_name, last_name, suffix_name, sex, age, phone_number, step, errors FROM teachers_bio WHERE deped_id = ?",
                (deped_id,)
            )
            return cursor.fetchone()

    def get_user_by_phone(self, phone: str):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT deped_id, school_id, first_name, middle_name, last_name, suffix_name, sex, age, phone_number, step, errors FROM teachers_bio WHERE phone_number = ?",
                (phone,)
            )
            return cursor.fetchone()

    def update_bio(self, deped_id: str, field: str, value, next_step: int):
        allowed_fields = {
            "school_id", "first_name", "middle_name", "last_name", 
            "suffix_name", "sex", "age"
        }
        if field not in allowed_fields:
            raise ValueError(f"Invalid field: {field}")

        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE teachers_bio
                SET {field} = ?, step = ?, errors = 0
                WHERE deped_id = ?
            """, (value, next_step, deped_id))
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

    def create_professional_record(self, deped_id: str):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO teachers_professional (teacher_id) VALUES (?)",
                (deped_id,)
            )
            conn.commit()

    def increment_error(self, deped_id: str):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE teachers_bio SET errors = errors + 1 WHERE deped_id = ?",
                (deped_id,)
            )
            conn.commit()
