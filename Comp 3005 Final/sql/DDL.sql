-- Members
CREATE TABLE IF NOT EXISTS members (
  member_id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  date_of_birth DATE,
  gender VARCHAR(10),
  phone VARCHAR(20),
  email VARCHAR(100) UNIQUE NOT NULL,
  address TEXT,
  join_date DATE DEFAULT CURRENT_DATE,
  membership_status VARCHAR(20),
  attendance INTEGER
);

-- Trainers
CREATE TABLE IF NOT EXISTS trainers (
  trainer_id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  phone VARCHAR(20)
);

--Admins
CREATE TABLE IF NOT EXISTS admins (
  admin_id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  phone VARCHAR(20)
);

-- Rooms
CREATE TABLE IF NOT EXISTS rooms (
  room_id SERIAL PRIMARY KEY,
  room_type VARCHAR(50),
  status VARCHAR(20),
  capacity INTEGER
);

-- PT sessions
CREATE TABLE IF NOT EXISTS pt_sessions (
  session_id SERIAL PRIMARY KEY,
  member_id INTEGER REFERENCES members(member_id) ON DELETE CASCADE,
  trainer_id INTEGER REFERENCES trainers(trainer_id),
  room_id INTEGER REFERENCES rooms(room_id),
  date DATE,
  start_time TIME,
  end_time TIME,
  status VARCHAR(20) DEFAULT 'open'
);

-- Group classes
CREATE TABLE IF NOT EXISTS group_classes (
  class_id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  trainer_id INTEGER REFERENCES trainers(trainer_id),
  room_id INTEGER REFERENCES rooms(room_id),
  capacity INTEGER,
  max_capacity INTEGER,
  date DATE,
  start_time TIME,
  end_time TIME,
  status VARCHAR(20) DEFAULT 'scheduled'
);


-- Class attendance
CREATE TABLE IF NOT EXISTS class_attendance (
  class_attendance SERIAL PRIMARY KEY,
  class_id INTEGER REFERENCES group_classes(class_id),
  member_id INTEGER REFERENCES members(member_id)
);

-- Health metrics
CREATE TABLE IF NOT EXISTS health_metrics (
  metric_id SERIAL PRIMARY KEY,
  member_id INTEGER REFERENCES members(member_id),
  status VARCHAR(20),
  date_recorded DATE,
  height NUMERIC,
  weight NUMERIC,
  heart_rate INTEGER,
  body_fat_percentage NUMERIC
);

-- Equipment
CREATE TABLE IF NOT EXISTS equipment (
  machine_id SERIAL PRIMARY KEY,
  room_id INTEGER REFERENCES rooms(room_id),
  name VARCHAR(100),
  status VARCHAR(20),
  last_maintenance_date DATE
);

-- Repairs
CREATE TABLE IF NOT EXISTS repairs (
  repair_id SERIAL PRIMARY KEY,
  machine_id INTEGER REFERENCES equipment(machine_id),
  assigned_to INTEGER REFERENCES trainers (trainer_id),
  reported_by INTEGER, 
  issue_description TEXT,
  status VARCHAR(20),
  date_reported DATE,
  completion_date DATE
);

-- Availability
CREATE TABLE IF NOT EXISTS availability (
  availability_id SERIAL PRIMARY KEY,
  trainer_id INTEGER REFERENCES trainers(trainer_id),
  type VARCHAR(10) NOT NULL CHECK (type IN ('recurring','oneoff')),
  day_of_week SMALLINT CHECK (day_of_week BETWEEN 0 AND 6),
  date DATE, -- used when type='oneoff'
  start_time TIME NOT NULL,
  end_time TIME NOT NULL,
  CHECK (
    (type = 'recurring' AND day_of_week IS NOT NULL AND date IS NULL)
    OR
    (type = 'oneoff' AND date IS NOT NULL AND day_of_week IS NULL)
  ),
  CHECK (start_time < end_time)
);


-- Invoices
CREATE TABLE IF NOT EXISTS invoices (
  invoice_id SERIAL PRIMARY KEY,
  member_id INTEGER REFERENCES members(member_id),
  service VARCHAR(100),
  amount_due NUMERIC,
  status VARCHAR(20),
  billing_date DATE,
  paid_date DATE
);

