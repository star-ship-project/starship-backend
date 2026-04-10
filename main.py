import os, sqlite3
from dotenv import load_dotenv
from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from database import DatabaseManager
from sms_service import SMSService
from survey_service import SurveyService


load_dotenv()

HTTPSMS_API_KEY = os.getenv("HTTPSMS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FROM_NUMBER = os.getenv("FROM_NUMBER")

# Change database file here
DB_FILE = "star.db"

DISPLAY_MESSAGES = {
    1: "Good Day! This is the STAR's data collection system!",
    2: "Identity confirmed!"
}

SURVEY_QUESTIONS = {
    1: "Ilagay ang DepEd ID: ",
    2: "Ilagay ang School ID (isulat ang N/A kung wala):  ",
    3: "Buong Pangalan [Apilyido],[Unang Pangalan],[Gitnang Pangalan],[Suffix/Hulapi]",
    4: "Edad (Ex: 30): ",
    5: "Kasarian (Ex: Lalake): ",
    6: "Tagal ng Pagtuturo: ",
    7: "Posisyon: ",
    8: "Ispesyalisasiyon: ",
    9: "May access ka ba sa internet?: ",
    10: "Gaano karami ang iyong device?: "
}

db = DatabaseManager(DB_FILE)
db.init_db()

sms_service = SMSService(HTTPSMS_API_KEY, FROM_NUMBER)
survey_service = SurveyService(db, sms_service, DISPLAY_MESSAGES, SURVEY_QUESTIONS)

app = FastAPI()

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

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("frontend/login_page.html", encoding="utf-8") as f:
        return f.read()

@app.get("/login.js")
async def login_js():
    with open("frontend/login.js", encoding="utf-8") as f:
        return f.read()


# --- Database Helper Function ---
def get_db_connection():
    # Check if DB exists, if not, print a warning
    if not os.path.exists(DB_FILE):
        raise HTTPException(status_code=500, detail="Database not found. Please run schema and seed files.")

    conn = sqlite3.connect(DB_FILE)
    # This row_factory allows us to access columns by name (like a dictionary),
    # which makes converting to JSON seamless.
    conn.row_factory = sqlite3.Row
    return conn


@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()

    # Ignore messages from self
    event_type = payload.get("type", "")
    if event_type != "message.phone.received":
        return {"status": "ignored"}

    data = payload.get("data", {})
    phone = data.get("contact")
    text = data.get("content")

    print("\n--- INCOMING WEBHOOK ---")
    print(f"[DEBUG] Phone: {phone}, Text: {text}")

    if not phone or not text:
        return {"status": "error", "message": "Missing contact or content"}

    background_tasks.add_task(survey_service.process_sms, phone, text)
    return {"status": "success"}

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
