CREATE TABLE IF NOT EXISTS schools (
  school_id VARCHAR(10) PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  region VARCHAR(50) NOT NULL,
  division VARCHAR(100),
  total_enrollment INTEGER
);

CREATE TABLE IF NOT EXISTS teachers_bio (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  deped_id VARCHAR(50),
  school_id VARCHAR(10) REFERENCES schools (school_id),
  first_name VARCHAR(100),
  middle_name VARCHAR(100),
  last_name VARCHAR(100),
  suffix_name VARCHAR(100),
  sex VARCHAR(20),
  age INTEGER,
  phone_number VARCHAR(13)
);

CREATE TABLE IF NOT EXISTS teachers_professional (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  teacher_id VARCHAR(50) REFERENCES teachers_bio (deped_id),
  years_experience INTEGER,
  teaching_level VARCHAR(50), -- 'Elementary', 'JHS', 'SHS'
  role_position VARCHAR(100), -- 'Teacher III', 'Master Teacher II'
  specialization VARCHAR(50), -- 'Science', 'Math'
  is_internet_access BOOLEAN,
  device_count INTEGER
);

CREATE TABLE IF NOT EXISTS qualifications (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  teacher_id VARCHAR(50) REFERENCES teachers_bio (deped_id),
  cert_name VARCHAR(255),
  category VARCHAR(50), -- 'Technical', 'Pedagogical', 'Leadership'
  awarding_body VARCHAR(150),
  date_obtained DATETIME
);

CREATE TABLE IF NOT EXISTS star_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  teacher_id VARCHAR(50) REFERENCES teachers_bio(deped_id),
  event_title VARCHAR(100),
  event_type VARCHAR(50), -- 'International Conference', 'Nuclear Camp', 'ISLA', 'STAR Fest'
  event_date date
);
