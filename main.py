import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, BackgroundTasks

from database import DatabaseManager
from sms_service import SMSService
from survey_service import SurveyService


load_dotenv()

HTTPSMS_API_KEY = os.getenv("HTTPSMS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FROM_NUMBER = os.getenv("FROM_NUMBER")

# Change database file here
DB_FILE = "education.db"

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
    9: "May access ka ba sa internet? ",
    10: "Gaano karami ang iyong device? "
}

db = DatabaseManager(DB_FILE)
db.init_db()

sms_service = SMSService(HTTPSMS_API_KEY, FROM_NUMBER)
survey_service = SurveyService(db, sms_service, DISPLAY_MESSAGES, SURVEY_QUESTIONS)

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
