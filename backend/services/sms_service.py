import requests


class SMSService:
    def __init__(self, api_key: str, from_number: str):
        self.api_key = api_key
        self.from_number = from_number

    def send_sms(self, to: str, message: str):
        try:
            response = requests.post(
                "https://api.httpsms.com/v1/messages/send",
                headers={
                    "x-api-key": self.api_key,
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
                json={
                    "content": message,
                    "from": self.from_number,
                    "to": to
                },
            )
            print(f"[SMS] To {to} | Status {response.status_code}")
            print(f"[SMS Response] {response.json()}")
        except Exception as e:
            print(f"[SMS Error] {e}")
