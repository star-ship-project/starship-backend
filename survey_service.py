class SurveyService:
    def __init__(self, db, sms_service, messages, questions):
        self.db = db
        self.sms = sms_service

        self.messages = messages
        self.questions = questions

    def process_sms(self, phone: str, text: str):
        user_row = self.db.get_user_by_phone(phone)

        if not user_row:
            self.db.create_user("", phone)
            print(f"[DB] New user created for phone {phone}")
            self.sms.send_sms(phone, self.messages[1])
            self.sms.send_sms(phone, self.questions[1])
            return

        deped_id, school_id, first_name, middle_name, last_name, suffix_name, sex, age, phone_number, step, errors = user_row

        if step > 10:
            self.sms.send_sms(phone, "You have already completed the survey. Thank you!")
            return

        user_text = text.strip()

        if step == 1:
            self.db.update_bio_by_phone(phone, "deped_id", user_text, 2)
            print(f"[DB] Saved deped_id = {user_text} for {phone}")
            self.sms.send_sms(phone, self.questions[2])
            return

        if step == 3:
            parts = [p.strip() for p in user_text.split(",")]
            if len(parts) >= 1:
                self.db.update_bio(deped_id, "last_name", parts[0], 4)
            if len(parts) >= 2:
                self.db.update_bio(deped_id, "first_name", parts[1], 4)
            if len(parts) >= 3:
                self.db.update_bio(deped_id, "middle_name", parts[2], 4)
            if len(parts) >= 4:
                self.db.update_bio(deped_id, "suffix_name", parts[3], 4)
            print(f"[DB] Saved name for {deped_id}: {user_text}")
            self.sms.send_sms(phone, self.questions[4])
            return

        try:
            value = int(user_text)
            is_number = True
        except ValueError:
            is_number = False

        if is_number:
            if step == 4:
                self.db.update_bio(deped_id, "age", value, 5)
                print(f"[DB] Saved age = {value} for {deped_id}")
                self.sms.send_sms(phone, self.questions[5])
                return
            elif step == 6:
                self.db.update_professional(deped_id, "years_experience", value)
                self.db.update_step(deped_id, 7)
                print(f"[DB] Saved years_experience = {value} for {deped_id}")
                self.sms.send_sms(phone, self.questions[7])
                return
            elif step == 10:
                self.db.update_professional(deped_id, "device_count", value)
                self.db.update_step(deped_id, 11)
                print(f"[DB] Saved device_count = {value} for {deped_id}")
                self.sms.send_sms(phone, "Salamat! Successfully completed the survey.")
                return
            else:
                self.sms.send_sms(phone, self.questions[step + 1])
                return
        else:
            if step == 2:
                self.db.update_bio(deped_id, "school_id", user_text, 3)
                print(f"[DB] Saved school_id = {user_text} for {deped_id}")
                self.sms.send_sms(phone, self.questions[3])
                return
            elif step == 5:
                self.db.update_bio(deped_id, "sex", user_text, 6)
                print(f"[DB] Saved sex = {user_text} for {deped_id}")
                self.db.create_professional_record(deped_id)
                self.sms.send_sms(phone, self.questions[6])
                return
            elif step == 7:
                self.db.update_professional(deped_id, "role_position", user_text)
                self.db.update_step(deped_id, 8)
                print(f"[DB] Saved role_position = {user_text} for {deped_id}")
                self.sms.send_sms(phone, self.questions[8])
                return
            elif step == 8:
                self.db.update_professional(deped_id, "specialization", user_text)
                self.db.update_step(deped_id, 9)
                print(f"[DB] Saved specialization = {user_text} for {deped_id}")
                self.sms.send_sms(phone, self.questions[9])
                return
            elif step == 9:
                user_lower = user_text.lower()
                if user_lower in ["yes", "oo", "oo naman", "yes po"]:
                    is_internet = 1
                elif user_lower in ["no", "hindi", "walang internet"]:
                    is_internet = 0
                else:
                    if errors < 1:
                        self.db.increment_error(deped_id)
                        self.sms.send_sms(phone, "Pakisagot lang ng 'yes' o 'no': ")
                    else:
                        print(f"[SKIP] Error limit reached for {deped_id}, not sending.")
                    return
                self.db.update_professional(deped_id, "is_internet_access", is_internet)
                self.db.update_step(deped_id, 10)
                print(f"[DB] Saved is_internet_access = {is_internet} for {deped_id}")
                self.sms.send_sms(phone, self.questions[10])
                return
            else:
                if errors < 1:
                    self.db.increment_error(deped_id)
                    self.sms.send_sms(phone, f"Invalid input. Please try again: {self.questions[step]}")
                else:
                    print(f"[SKIP] Error limit reached for {deped_id}, not sending.")
                return

        next_step = step + 1

        if next_step > len(self.questions):
            self.sms.send_sms(phone, "Salamat! Successfully completed the survey.")
        else:
            self.sms.send_sms(phone, self.questions[next_step])
