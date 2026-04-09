import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, BackgroundTasks

from database import DatabaseManager
from sms_service import SMSService
from ai_service import AIService
from survey_service import SurveyService


load_dotenv()

HTTPSMS_API_KEY = os.getenv("HTTPSMS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FROM_NUMBER = os.getenv("FROM_NUMBER")
DB_FILE = "teachers.db"

SURVEY_QUESTIONS = {
    1: "Hello Teacher! Please reply with the TOTAL NUMBER of students enrolled in your advisory class.",
    2: "Thank you. Now, please reply with the number of students who DO NOT have internet access at home.",
}

db = DatabaseManager(DB_FILE)
db.init_db()

sms_service = SMSService(HTTPSMS_API_KEY, FROM_NUMBER)
ai_service = AIService(GEMINI_API_KEY, SURVEY_QUESTIONS)
survey_service = SurveyService(db, sms_service, ai_service)

app = FastAPI()


@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()

    data = payload.get("data", {})
    phone = data.get("contact")
    text = data.get("content")

    print("\n--- INCOMING WEBHOOK ---")
    print(f"[DEBUG] Phone: {phone}, Text: {text}")

    if not phone or not text:
        return {"status": "error", "message": "Missing contact or content"}

    background_tasks.add_task(survey_service.process_sms, phone, text)
    return {"status": "success"}
