PRAGMA foreign_keys = ON;

-- 2. SCHOOLS DATA
INSERT INTO schools (school_id, name, region, division, total_enrollment) VALUES 
('SCH001', 'PUP Laboratory High School', 'NCR', 'Manila', 500),
('SCH002', 'Manila Science High School', 'NCR', 'Manila', 800),
('SCH003', 'Quezon City Science High School', 'NCR', 'QC', 750);

-- 3. TEACHERS BIO (The "Parent" Table)
INSERT INTO teachers_bio (deped_id, school_id, first_name, middle_name, last_name, sex, age, phone_number) VALUES 
('DEPED-101', 'SCH001', 'Maria', 'Santos', 'Reyes', 'Female', 34, '+639171234567'),
('DEPED-102', 'SCH001', 'Juan', 'Perez', 'Dela Cruz', 'Male', 42, '+639189876543'),
('DEPED-103', 'SCH002', 'Elena', 'Gomez', 'Bautista', 'Female', 29, '+639195554433');

-- 4. TEACHERS PROFESSIONAL
INSERT INTO teachers_professional (teacher_id, years_experience, teaching_level, role_position, specialization, is_internet_access, device_count) VALUES 
('DEPED-101', 10, 'SHS', 'Master Teacher II', 'Science', 1, 2),
('DEPED-102', 15, 'JHS', 'Teacher III', 'Math', 1, 1),
('DEPED-103', 5, 'Elementary', 'Teacher I', 'General Education', 0, 1);

-- 5. QUALIFICATIONS
INSERT INTO qualifications (teacher_id, cert_name, category, awarding_body, date_obtained) VALUES 
('DEPED-101', 'Advanced Physics Certification', 'Technical', 'DOST', '2023-05-20'),
('DEPED-101', 'LMS Management Training', 'Pedagogical', 'DepEd Central', '2024-02-15'),
('DEPED-103', 'Early Childhood Dev Certificate', 'Pedagogical', 'UP Diliman', '2025-01-10');

-- 6. STAR EVENTS
INSERT INTO star_events (teacher_id, event_title, event_type, event_date) VALUES 
('DEPED-101', 'International Nuclear Camp 2026', 'Nuclear Camp', '2026-03-15'),
('DEPED-102', 'STAR Fest 2025', 'STAR Fest', '2025-11-10'),
('DEPED-101', 'ISLA Conference', 'ISLA', '2026-01-20');