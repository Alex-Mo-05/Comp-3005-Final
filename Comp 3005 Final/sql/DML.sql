
BEGIN;

-- === Trainers (6) ===
INSERT INTO trainers (name, email, phone) VALUES
  ('Ava Morgan', 'ava.morgan@example.com', '555-0101'),
  ('Liam Carter', 'liam.carter@example.com', '555-0102'),
  ('Maya Patel', 'maya.patel@example.com', '555-0103'),
  ('Noah Kim', 'noah.kim@example.com', '555-0104'),
  ('Olivia Chen', 'olivia.chen@example.com', '555-0105'),
  ('Ethan Brown', 'ethan.brown@example.com', '555-0106');

-- === Admins (3) ===
INSERT INTO admins (name, email, phone) VALUES
  ('Grace Hall', 'grace.hall@example.com', '555-0201'),
  ('Marcus Lee', 'marcus.lee@example.com', '555-0202'),
  ('Sofia Rivera', 'sofia.rivera@example.com', '555-0203');

-- === Rooms (10) ===
INSERT INTO rooms (room_type, status, capacity) VALUES
  ('Studio A', 'available', 20),
  ('Studio B', 'available', 18),
  ('Weight Room', 'available', 30),
  ('Cardio Room', 'available', 25),
  ('Spin Room', 'available', 22),
  ('Yoga Room', 'available', 16),
  ('Pilates Room', 'available', 12),
  ('Functional Area', 'available', 28),
  ('Poolside', 'maintenance', 10),
  ('Outdoor Court', 'available', 40);

-- === Availability (5 different trainer availability rows) ===
-- Use trainer email to find trainer_id
INSERT INTO availability (trainer_id, type, day_of_week, date, start_time, end_time)
VALUES
  ((SELECT trainer_id FROM trainers WHERE email='ava.morgan@example.com'), 'recurring', 1, NULL, '08:00', '10:00'),
  ((SELECT trainer_id FROM trainers WHERE email='liam.carter@example.com'), 'recurring', 2, NULL, '12:00', '14:00'),
  ((SELECT trainer_id FROM trainers WHERE email='maya.patel@example.com'), 'recurring', 4, NULL, '17:00', '19:00'),
  ((SELECT trainer_id FROM trainers WHERE email='noah.kim@example.com'), 'oneoff', NULL, CURRENT_DATE + INTERVAL '3 days', '09:00', '11:00'),
  ((SELECT trainer_id FROM trainers WHERE email='olivia.chen@example.com'), 'oneoff', NULL, CURRENT_DATE + INTERVAL '7 days', '18:00', '20:00');

-- === Equipment (10 machines) ===
INSERT INTO equipment (room_id, name, status, last_maintenance_date) VALUES
  ((SELECT room_id FROM rooms WHERE room_type='Weight Room'), 'Treadmill A', 'operational', CURRENT_DATE - INTERVAL '30 days'),
  ((SELECT room_id FROM rooms WHERE room_type='Weight Room'), 'Treadmill B', 'operational', CURRENT_DATE - INTERVAL '45 days'),
  ((SELECT room_id FROM rooms WHERE room_type='Cardio Room'), 'Elliptical A', 'operational', CURRENT_DATE - INTERVAL '20 days'),
  ((SELECT room_id FROM rooms WHERE room_type='Cardio Room'), 'Rowing Machine', 'operational', CURRENT_DATE - INTERVAL '60 days'),
  ((SELECT room_id FROM rooms WHERE room_type='Weight Room'), 'Squat Rack', 'operational', CURRENT_DATE - INTERVAL '90 days'),
  ((SELECT room_id FROM rooms WHERE room_type='Functional Area'), 'Kettlebell Set', 'operational', CURRENT_DATE - INTERVAL '15 days'),
  ((SELECT room_id FROM rooms WHERE room_type='Spin Room'), 'Spin Bike A', 'operational', CURRENT_DATE - INTERVAL '10 days'),
  ((SELECT room_id FROM rooms WHERE room_type='Spin Room'), 'Spin Bike B', 'operational', CURRENT_DATE - INTERVAL '10 days'),
  ((SELECT room_id FROM rooms WHERE room_type='Yoga Room'), 'Yoga Mats (set)', 'operational', CURRENT_DATE - INTERVAL '5 days'),
  ((SELECT room_id FROM rooms WHERE room_type='Outdoor Court'), 'Outdoor Nets', 'operational', CURRENT_DATE - INTERVAL '120 days');

-- === Repairs (2) ===
-- assigned_to uses trainer email lookup; reported_by left NULL
INSERT INTO repairs (machine_id, assigned_to, reported_by, issue_description, status, date_reported, completion_date) VALUES
  ((SELECT machine_id FROM equipment WHERE name='Treadmill B' LIMIT 1),
   (SELECT trainer_id FROM trainers WHERE email='liam.carter@example.com'),
   NULL,
   'Treadmill belt slipping intermittently',
   'open',
   CURRENT_DATE - INTERVAL '2 days',
   NULL),
  ((SELECT machine_id FROM equipment WHERE name='Squat Rack' LIMIT 1),
   (SELECT trainer_id FROM trainers WHERE email='noah.kim@example.com'),
   NULL,
   'Squat rack safety pin bent',
   'in_progress',
   CURRENT_DATE - INTERVAL '5 days',
   NULL);

-- === Members (10) ===
INSERT INTO members (name, date_of_birth, gender, phone, email, address, join_date, membership_status, attendance) VALUES
  ('Alex Turner', '1990-06-15', 'male', '555-0301', 'alex.turner@example.com', '101 Main St', CURRENT_DATE - INTERVAL '120 days', 'active', 12),
  ('Bella Stone', '1985-09-02', 'female', '555-0302', 'bella.stone@example.com', '202 Oak Ave', CURRENT_DATE - INTERVAL '200 days', 'active', 20),
  ('Carlos Diaz', '1992-11-20', 'male', '555-0303', 'carlos.diaz@example.com', '303 Pine Rd', CURRENT_DATE - INTERVAL '60 days', 'active', 8),
  ('Diana Ross', '1978-03-10', 'female', '555-0304', 'diana.ross@example.com', '404 Maple Ln', CURRENT_DATE - INTERVAL '400 days', 'active', 45),
  ('Evan Scott', '2000-01-05', 'male', '555-0305', 'evan.scott@example.com', '505 Birch Blvd', CURRENT_DATE - INTERVAL '30 days', 'trial', 3),
  ('Fiona Green', '1995-07-22', 'female', '555-0306', 'fiona.green@example.com', '606 Cedar Ct', CURRENT_DATE - INTERVAL '90 days', 'active', 15),
  ('George King', '1988-12-12', 'male', '555-0307', 'george.king@example.com', '707 Spruce St', CURRENT_DATE - INTERVAL '10 days', 'trial', 1),
  ('Hannah White', '1993-05-30', 'female', '555-0308', 'hannah.white@example.com', '808 Elm Dr', CURRENT_DATE - INTERVAL '250 days', 'active', 30),
  ('Ian Black', '1982-08-08', 'male', '555-0309', 'ian.black@example.com', '909 Willow Way', CURRENT_DATE - INTERVAL '500 days', 'active', 60),
  ('Jade Liu', '1997-04-18', 'female', '555-0310', 'jade.liu@example.com', '1001 Aspen Pl', CURRENT_DATE - INTERVAL '14 days', 'trial', 2);

-- === PT sessions (5) ===
-- Two sessions assigned to members (lookup by member email), others open
INSERT INTO pt_sessions (member_id, trainer_id, room_id, date, start_time, end_time, status) VALUES
  (
    (SELECT member_id FROM members WHERE email='alex.turner@example.com'),
    (SELECT trainer_id FROM trainers WHERE email='ava.morgan@example.com'),
    (SELECT room_id FROM rooms WHERE room_type='Studio A'),
    CURRENT_DATE + INTERVAL '1 day', '08:00', '08:45', 'booked'
  ),
  (
    (SELECT member_id FROM members WHERE email='bella.stone@example.com'),
    (SELECT trainer_id FROM trainers WHERE email='liam.carter@example.com'),
    (SELECT room_id FROM rooms WHERE room_type='Studio B'),
    CURRENT_DATE + INTERVAL '1 day', '12:00', '12:45', 'booked'
  ),
  (
    NULL,
    (SELECT trainer_id FROM trainers WHERE email='maya.patel@example.com'),
    (SELECT room_id FROM rooms WHERE room_type='Weight Room'),
    CURRENT_DATE + INTERVAL '2 days', '17:00', '17:45', 'open'
  ),
  (
    NULL,
    (SELECT trainer_id FROM trainers WHERE email='noah.kim@example.com'),
    (SELECT room_id FROM rooms WHERE room_type='Cardio Room'),
    CURRENT_DATE + INTERVAL '3 days', '09:00', '09:45', 'open'
  ),
  (
    NULL,
    (SELECT trainer_id FROM trainers WHERE email='olivia.chen@example.com'),
    (SELECT room_id FROM rooms WHERE room_type='Spin Room'),
    CURRENT_DATE + INTERVAL '7 days', '18:00', '18:45', 'open'
  );

-- === Health metrics (one record per member) ===
INSERT INTO health_metrics (member_id, status, date_recorded, height, weight, heart_rate, body_fat_percentage) VALUES
  ((SELECT member_id FROM members WHERE email='alex.turner@example.com'), 'current', CURRENT_DATE - INTERVAL '7 days', 70.0, 180.0, 68, 0.18),
  ((SELECT member_id FROM members WHERE email='bella.stone@example.com'), 'current', CURRENT_DATE - INTERVAL '10 days', 65.0, 150.0, 72, 0.22),
  ((SELECT member_id FROM members WHERE email='carlos.diaz@example.com'), 'current', CURRENT_DATE - INTERVAL '5 days', 72.0, 200.0, 75, 0.20),
  ((SELECT member_id FROM members WHERE email='diana.ross@example.com'), 'current', CURRENT_DATE - INTERVAL '30 days', 64.0, 140.0, 66, 0.24),
  ((SELECT member_id FROM members WHERE email='evan.scott@example.com'), 'current', CURRENT_DATE - INTERVAL '2 days', 69.0, 170.0, 80, 0.19),
  ((SELECT member_id FROM members WHERE email='fiona.green@example.com'), 'current', CURRENT_DATE - INTERVAL '12 days', 62.0, 135.0, 70, 0.21),
  ((SELECT member_id FROM members WHERE email='george.king@example.com'), 'current', CURRENT_DATE - INTERVAL '1 day', 71.0, 190.0, 78, 0.23),
  ((SELECT member_id FROM members WHERE email='hannah.white@example.com'), 'current', CURRENT_DATE - INTERVAL '20 days', 66.0, 155.0, 65, 0.17),
  ((SELECT member_id FROM members WHERE email='ian.black@example.com'), 'current', CURRENT_DATE - INTERVAL '40 days', 68.0, 175.0, 69, 0.16),
  ((SELECT member_id FROM members WHERE email='jade.liu@example.com'), 'current', CURRENT_DATE - INTERVAL '3 days', 63.0, 145.0, 74, 0.20);

-- === Goals table (create if you want to store goals) ===
CREATE TABLE IF NOT EXISTS goals (
  goal_id SERIAL PRIMARY KEY,
  member_id INTEGER REFERENCES members(member_id),
  description TEXT,
  target_date DATE,
  status VARCHAR(20) DEFAULT 'open'
);

-- Insert a goal for each member (optional)
INSERT INTO goals (member_id, description, target_date, status) VALUES
  ((SELECT member_id FROM members WHERE email='alex.turner@example.com'), 'Lose 10 lbs', CURRENT_DATE + INTERVAL '90 days', 'open'),
  ((SELECT member_id FROM members WHERE email='bella.stone@example.com'), 'Improve 5k time by 2 minutes', CURRENT_DATE + INTERVAL '60 days', 'open'),
  ((SELECT member_id FROM members WHERE email='carlos.diaz@example.com'), 'Increase bench press by 20 lbs', CURRENT_DATE + INTERVAL '120 days', 'open'),
  ((SELECT member_id FROM members WHERE email='diana.ross@example.com'), 'Attend 3x weekly for 3 months', CURRENT_DATE + INTERVAL '90 days', 'open'),
  ((SELECT member_id FROM members WHERE email='evan.scott@example.com'), 'Complete introductory PT program', CURRENT_DATE + INTERVAL '30 days', 'open'),
  ((SELECT member_id FROM members WHERE email='fiona.green@example.com'), 'Reduce resting heart rate to 65', CURRENT_DATE + INTERVAL '90 days', 'open'),
  ((SELECT member_id FROM members WHERE email='george.king@example.com'), 'Gain 8 lbs muscle mass', CURRENT_DATE + INTERVAL '120 days', 'open'),
  ((SELECT member_id FROM members WHERE email='hannah.white@example.com'), 'Improve flexibility with weekly yoga', CURRENT_DATE + INTERVAL '60 days', 'open'),
  ((SELECT member_id FROM members WHERE email='ian.black@example.com'), 'Maintain weight and reduce body fat by 1%', CURRENT_DATE + INTERVAL '90 days', 'open'),
  ((SELECT member_id FROM members WHERE email='jade.liu@example.com'), 'Build consistent workout habit (12 weeks)', CURRENT_DATE + INTERVAL '84 days', 'open');

-- === Invoices (a few dummy invoices) ===
INSERT INTO invoices (member_id, service, amount_due, status, billing_date, paid_date) VALUES
  ((SELECT member_id FROM members WHERE email='alex.turner@example.com'), 'Monthly membership', 49.99, 'paid', CURRENT_DATE - INTERVAL '15 days', CURRENT_DATE - INTERVAL '10 days'),
  ((SELECT member_id FROM members WHERE email='bella.stone@example.com'), 'Personal training (1 session)', 35.00, 'unpaid', CURRENT_DATE - INTERVAL '3 days', NULL),
  ((SELECT member_id FROM members WHERE email='diana.ross@example.com'), 'Equipment rental', 12.50, 'paid', CURRENT_DATE - INTERVAL '40 days', CURRENT_DATE - INTERVAL '35 days'),
  ((SELECT member_id FROM members WHERE email='hannah.white@example.com'), 'Monthly membership', 49.99, 'unpaid', CURRENT_DATE - INTERVAL '5 days', NULL);

COMMIT;
