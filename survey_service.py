class SurveyService:
    def __init__(self, db, sms_service, ai_service):
        self.db = db
        self.sms = sms_service
        self.ai = ai_service

        self.questions = {
            1: "Hello Teacher! Please reply with the TOTAL NUMBER of students enrolled in your advisory class.",
            2: "Thank you. Now, please reply with the number of students who DO NOT have internet access at home.",
        }

        self.thank_you_msg = "Data saved successfully. Thank you for your submission!"

    def process_sms(self, phone: str, text: str):
        row = self.db.get_user(phone)

        if not row:
            self.db.create_user(phone)
            print(f"[DB] New user {phone} added to database.")
            self.sms.send_sms(phone, self.questions[1])
            return

        step, errors = row

        if step > len(self.questions):
            self.sms.send_sms(phone, "You have already completed the survey. Thank you!")
            return

        ai_response = self.ai.extract_number(text, step)

        try:
            number = int(ai_response)

            if step == 1:
                column_name = "q1_total_students"
            elif step == 2:
                column_name = "q2_no_internet"
            else:
                self.sms.send_sms(phone, "Invalid survey step.")
                return

            next_step = step + 1

            self.db.update_answer(phone, column_name, number, next_step)
            print(f"[DB] Saved {column_name} = {number} for {phone}.")

            if next_step > len(self.questions):
                self.sms.send_sms(phone, self.thank_you_msg)
            else:
                self.sms.send_sms(phone, self.questions[next_step])

        except ValueError:
            if errors < 1:
                self.db.increment_error(phone)
                self.sms.send_sms(phone, ai_response)
            else:
                print(f"[SKIP] Error limit reached for {phone}, not sending.")
