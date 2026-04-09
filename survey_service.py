class SurveyService:
    def __init__(self, db, sms_service, ai_service, messages, questions):
        self.db = db
        self.sms = sms_service
        self.ai = ai_service

        self.messages = messages
        self.questions = questions

    def process_sms(self, phone: str, text: str):
        user_row = self.db.get_user_by_phone(phone)

        if not user_row:
            self.sms.send_sms(phone, self.questions[1])
            return

        deped_id, school_id, first_name, middle_name, last_name, suffix_name, sex, age, phone_number, step, errors = user_row

        if step > len(self.questions):
            self.sms.send_sms(phone, "You have already completed the survey. Thank you!")
            return

        ai_response = self.ai.extract_number(text, step)

        if step == 1:
            self.db.create_user(ai_response, phone)
            print(f"[DB] New user {ai_response} added to database.")
            self.sms.send_sms(phone, self.questions[2])
            return

        if step == 3:
            parts = [p.strip() for p in text.split(",")]
            if len(parts) >= 1:
                self.db.update_bio(deped_id, "last_name", parts[0], 4)
            if len(parts) >= 2:
                self.db.update_bio(deped_id, "suffix_name", parts[1], 4)
            if len(parts) >= 3:
                self.db.update_bio(deped_id, "first_name", parts[2], 4)
            if len(parts) >= 4:
                self.db.update_bio(deped_id, "middle_name", parts[3], 4)
            print(f"[DB] Saved name for {deped_id}: {text}")
            self.sms.send_sms(phone, self.questions[4])
            return

        try:
            value = int(ai_response)

            if step == 4:
                self.db.update_bio(deped_id, "age", value, 5)
                print(f"[DB] Saved age = {value} for {deped_id}")
            elif step == 6:
                self.db.update_professional(deped_id, "years_experience", value)
                self.db.update_bio(deped_id, "step", 7)
                print(f"[DB] Saved years_experience = {value} for {deped_id}")
                self.sms.send_sms(phone, self.questions[7])
                return
            elif step == 10:
                self.db.update_professional(deped_id, "device_count", value)
                print(f"[DB] Saved device_count = {value} for {deped_id}")
                self.sms.send_sms(phone, self.messages[-1])
                return
            else:
                self.sms.send_sms(phone, "Invalid survey step.")
                return

        except ValueError:
            if step == 2:
                self.db.update_bio(deped_id, "school_id", ai_response, 3)
                print(f"[DB] Saved school_id = {ai_response} for {deped_id}")
                self.sms.send_sms(phone, self.questions[3])
                return
            elif step == 5:
                self.db.update_bio(deped_id, "sex", ai_response, 6)
                print(f"[DB] Saved sex = {ai_response} for {deped_id}")
                self.db.create_professional_record(deped_id)
                self.sms.send_sms(phone, self.questions[6])
                return
            elif step == 7:
                self.db.update_professional(deped_id, "role_position", ai_response)
                self.db.update_bio(deped_id, "step", 8)
                print(f"[DB] Saved role_position = {ai_response} for {deped_id}")
                self.sms.send_sms(phone, self.questions[8])
                return
            elif step == 8:
                self.db.update_professional(deped_id, "specialization", ai_response)
                self.db.update_bio(deped_id, "step", 9)
                print(f"[DB] Saved specialization = {ai_response} for {deped_id}")
                self.sms.send_sms(phone, self.questions[9])
                return
            elif step == 9:
                self.db.update_professional(deped_id, "is_internet_access", ai_response)
                self.db.update_bio(deped_id, "step", 10)
                print(f"[DB] Saved is_internet_access = {ai_response} for {deped_id}")
                self.sms.send_sms(phone, self.questions[10])
                return

            if errors < 1:
                self.db.increment_error(deped_id)
                self.sms.send_sms(phone, ai_response)
            else:
                print(f"[SKIP] Error limit reached for {deped_id}, not sending.")
                return

        next_step = step + 1

        if next_step > len(self.questions):
            self.sms.send_sms(phone, self.messages[-1])
        else:
            self.sms.send_sms(phone, self.questions[next_step])
