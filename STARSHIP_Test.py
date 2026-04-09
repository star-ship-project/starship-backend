import os
import sqlite3
from dotenv import load_dotenv
import requests
from fastapi import FastAPI, Request, BackgroundTasks
from google import genai

# ==========================================
# CONFIGURATION 
# ==========================================
load_dotenv()
HTTPSMS_API_KEY = os.getenv("HTTPSMS_API_KEY")
GEMINI_API_KEY  = os.getenv("GEMINI_API_KEY")
FROM_NUMBER     = os.getenv("FROM_NUMBER")

# ==========================================
# DATABASE INIT
# ==========================================
DB_FILE = "teachers.db"

def init_db():
    """Creates the SQLite database and table if they don't exist."""
    with sqlite3.connect(DB_FILE) as db_file:
        cursor = db_file.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS survey_data (
                phone TEXT PRIMARY KEY,
                step INTEGER DEFAULT 1,
                errors INTEGER DEFAULT 0,
                q1_total_students INTEGER,
                q2_no_internet INTEGER
            )
        """)
        db_file.commit()
    print("[DB] SQLite Database Initialized.")

init_db() # Run this when the script starts


# ==========================================
# APP INIT
# ==========================================
client = genai.Client(api_key=GEMINI_API_KEY)
print(f"[DEBUG] Using API key: {HTTPSMS_API_KEY}")

app = FastAPI()

# In-memory state (resets on restart — fine for a prototype)
user_states = {}

SURVEY_QUESTIONS = {
    1: "Hello Teacher! Please reply with the TOTAL NUMBER of students enrolled in your advisory class.",
    2: "Thank you. Now, please reply with the number of students who DO NOT have internet access at home.",
}
THANK_YOU_MSG = "Data saved successfully. Thank you for your submission!"


# ==========================================
# HELPERS
# ==========================================
def send_sms(to: str, message: str):
    try:
        response = requests.post(
            "https://api.httpsms.com/v1/messages/send",
            headers={
                "x-api-key": HTTPSMS_API_KEY,
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            json={"content": message, "from": FROM_NUMBER, "to": to},
        )
        print(f"[SMS] To {to} | Status {response.status_code}")
        print(f"[SMS Response] {response.json()}")  # ← add this line
    except Exception as e:
        print(f"[SMS Error] {e}")

def extract_number_with_ai(user_text: str, step: int) -> str:
    prompt = f"""
You are a strict data collection assistant for the Department of Education.
The user was asked: "{SURVEY_QUESTIONS[step]}"
User replied: "{user_text}"

Rules:
1. If the reply contains a valid whole number, respond with ONLY that number. Nothing else.
2. If the reply is invalid or off-topic, respond EXACTLY with:
   "I cannot answer that. Please just provide the number for: {SURVEY_QUESTIONS[step]}"
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"[AI Error] {e}")  # ← check what this prints
        return "System error. Please try sending your number again."


def process_sms(phone: str, text: str):
    # Connect to DB securely within the background task thread
    with sqlite3.connect(DB_FILE) as db_file:
        cursor = db_file.cursor()

        # 1. Check if user exists in database
        cursor.execute("SELECT step, errors FROM survey_data WHERE phone = ?", (phone,))
        row = cursor.fetchone()

        if not row:
            # New User: Insert them into DB and send Question 1
            cursor.execute("INSERT INTO survey_data (phone, step, errors) VALUES (?, 1, 0)", (phone,))
            db_file.commit()
            print(f"[DB] New user {phone} added to database.")
            send_sms(phone, SURVEY_QUESTIONS[1])
            return

        step, errors = row

        if step > len(SURVEY_QUESTIONS):
            send_sms(phone, "You have already completed the survey. Thank you!")
            return

        # 2. Run AI Extraction
        ai_response = extract_number_with_ai(text, step)

        try:
            # 3. Successful extraction (it's a number!)
            number = int(ai_response)

            # Map the current step to the correct database column
            column_name = "q1_total_students" if step == 1 else "q2_no_internet"
            next_step = step + 1

            # Update the specific column, increment step, and reset errors
            cursor.execute(f"""
                    UPDATE survey_data 
                    SET {column_name} = ?, step = ?, errors = 0 
                    WHERE phone = ?
                """, (number, next_step, phone))
            db_file.commit()

            print(f"[DB] Saved {column_name} = {number} for {phone}.")

            if next_step > len(SURVEY_QUESTIONS):
                send_sms(phone, THANK_YOU_MSG)
            else:
                send_sms(phone, SURVEY_QUESTIONS[next_step])

        except ValueError:
            # 4. Failed extraction (AI couldn't find a number)
            if errors < 1:
                cursor.execute("UPDATE survey_data SET errors = errors + 1 WHERE phone = ?", (phone,))
                db_file.commit()
                send_sms(phone, ai_response)
            else:
                print(f"[SKIP] Error limit reached for {phone}, not sending.")


# ==========================================
# WEBHOOK
# ==========================================
@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()

    data  = payload.get("data", {})
    phone = data.get("contact")
    text  = data.get("content")

    print(f"\n--- INCOMING WEBHOOK ---")
    print(f"[DEBUG] Phone: {phone}, Text: {text}")

    if not phone or not text:
        return {"status": "error", "message": "Missing contact or content"}

    background_tasks.add_task(process_sms, phone, text)
    return {"status": "success"}