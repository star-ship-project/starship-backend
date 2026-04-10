from google import genai


class AIService:
    def __init__(self, api_key: str, survey_questions: dict[int, str]):
        self.client = genai.Client(api_key=api_key)
        self.survey_questions = survey_questions

    def extract_number(self, user_text: str, step: int) -> str:
        prompt = f"""
You are a strict data collection assistant for the Department of Education.
The user was asked: "{self.survey_questions[step]}"
User replied: "{user_text}"

Rules:
1. If the reply contains a valid whole number, respond with ONLY that number. Nothing else.
2. If the reply is invalid or off-topic, respond EXACTLY with:
"I cannot answer that. Please just provide the number for: {self.survey_questions[step]}"
"""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            print(f"[AI Error] {e}")
            return "System error. Please try sending your number again."
