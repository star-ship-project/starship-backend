from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os

app = FastAPI(title="STAR S.H.I.P API")

# --- CORS Configuration ---
# This is crucial. It allows your frontend (running on a different port or file path) 
# to request data from this backend without being blocked by the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend's exact URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "../star.db"

# --- Database Helper Function ---
def get_db_connection():
    # Check if DB exists, if not, print a warning
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=500, detail="Database not found. Please run schema and seed files.")
    
    conn = sqlite3.connect(DB_PATH)
    # This row_factory allows us to access columns by name (like a dictionary), 
    # which makes converting to JSON seamless.
    conn.row_factory = sqlite3.Row 
    return conn

# --- API Endpoints ---

@app.get("/api/schools")
def get_schools():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM schools")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/api/teachers-bio")
def get_teachers_bio():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teachers_bio")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/api/teachers-professional")
def get_teachers_professional():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Using a JOIN to swap deped_id for the actual teacher's full name
    query = """
        SELECT 
            t.first_name || ' ' || t.last_name AS teacher_name,
            p.years_experience, 
            p.teaching_level, 
            p.role_position, 
            p.specialization, 
            p.is_internet_access, 
            p.device_count
        FROM teachers_professional p
        JOIN teachers_bio t ON p.teacher_id = t.deped_id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/api/qualifications")
def get_qualifications():
    conn = get_db_connection()
    cursor = conn.cursor()
    # JOIN for teacher name
    query = """
        SELECT 
            t.first_name || ' ' || t.last_name AS teacher_name,
            q.cert_name, 
            q.category, 
            q.awarding_body, 
            q.date_obtained
        FROM qualifications q
        JOIN teachers_bio t ON q.teacher_id = t.deped_id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/api/star-events")
def get_star_events():
    conn = get_db_connection()
    cursor = conn.cursor()
    # JOIN for teacher name
    query = """
        SELECT 
            t.first_name || ' ' || t.last_name AS teacher_name,
            e.event_title, 
            e.event_type, 
            e.event_date
        FROM star_events e
        JOIN teachers_bio t ON e.teacher_id = t.deped_id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]