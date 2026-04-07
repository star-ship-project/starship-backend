import requests
from fastapi import FastAPI, Request, BackgroundTasks
from google import genai

# ==========================================
# CONFIGURATION — Fill these in
# ==========================================
HTTPSMS_API_KEY = "uk_tDiNLOO2x1h7RfzafgKkVan94FNuUKebua-mUjv25zIVFkPJyupSUK1OO-vs9Pdf"
GEMINI_API_KEY  = "AIzaSyB_-jSKfJW0jPiUf2JBT1QZPKx-khooqvM"
FROM_NUMBER     = "+639760732493"  # ← Replace with your actual Android number

# ==========================================
# INIT
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
    if phone not in user_states:
        user_states[phone] = {"step": 1, "data": {}, "errors": 0}
        send_sms(phone, SURVEY_QUESTIONS[1])
        return

    step = user_states[phone]["step"]

    if step > len(SURVEY_QUESTIONS):
        send_sms(phone, "You have already completed the survey. Thank you!")
        return

    ai_response = extract_number_with_ai(text, step)

    try:
        number = int(ai_response)
        user_states[phone]["errors"] = 0  # reset errors on success
        user_states[phone]["data"][f"step_{step}"] = number
        user_states[phone]["step"] += 1
        next_step = user_states[phone]["step"]

        print(f"[DB] {phone} → {user_states[phone]['data']}")

        if next_step > len(SURVEY_QUESTIONS):
            send_sms(phone, THANK_YOU_MSG)
        else:
            send_sms(phone, SURVEY_QUESTIONS[next_step])

    except ValueError:
        if user_states[phone]["errors"] < 1:
            user_states[phone]["errors"] += 1
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

    print(f"[DEBUG] Phone: {phone}, Text: {text}")

    if not phone or not text:
        return {"status": "error", "message": "Missing contact or content"}

    background_tasks.add_task(process_sms, phone, text)
    return {"status": "success"}