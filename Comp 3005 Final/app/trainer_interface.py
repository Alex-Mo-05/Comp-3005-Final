from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from datetime import datetime

def set_availability(conn, trainer_id):
    type = input("Will this schedule be recurring or a oneoff: ")
    if type == "oneoff":
        date = input("Please enter the date you will be working (YYYY-MM-DD): ")
        date = datetime.strptime(date, "%Y-%m-%d")
        stime = input("Please enter start time (9:00): ")
        etime = input("Please enter end time (17:30): ")
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO availability (trainer_id, type, date, start_time, end_time)
                    VALUES (%s, %s, %s, %s, %s)
                """, (trainer_id, type, date, stime, etime))
                conn.commit()
                print("[Success] Schedule added.")
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Failed to add schedule: {e}")
    elif type == "recurring":
        dow = input("Please select the weekday you wish to set a schedule for (0-6, 0 = Sunday, 6 = Saturday): ")
        stime = input("Please enter start time (9:00): ")
        etime = input("Please enter end time (17:30): ")
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO availability (trainer_id, type, day_of_week, start_time, end_time)
                    VALUES (%s, %s, %s, %s, %s)
                """, (trainer_id, type, dow, stime, etime))
                conn.commit()
                print("[Success] Schedule added.")
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Failed to add schedule: {e}")
    else:
        print("[Error] Non valid schedule type selected \n")
        return
    

    if type == "oneoff":
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO pt_sessions (trainer_id, date, start_time, end_time)
                    VALUES (%s, %s, %s, %s)
                """, (trainer_id, date, stime, etime))
                conn.commit()
                print("[Success] Physical Training Session added.")
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Failed to add Physical Training Session: {e}")
    
    else:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO group_classes (trainer_id, capacity, max_capacity, date, start_time, end_time)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (trainer_id, 0, 30, date, stime, etime))
                conn.commit()
                print("[Success] Group Class added.")
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Failed to add Group Class: {e}")


def view_schedule(conn, trainer_id):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            sql = """
            SELECT member_id, room_id, date, start_time, end_time
            FROM pt_sessions
            WHERE trainer_id = %s AND status = 'booked'
            ORDER BY date DESC, start_time DESC;
            """
            params = (trainer_id,)        
            cur.execute(sql, params)
            rows = cur.fetchall()

            print("\nCurrently Booked Physical Training Sessions:")
            if not rows:
                print("  (no booked sessions found)\n")
                return

            for r in rows:
                print(f"  - Member ID: {r['member_id']}; Room ID: {r['room_id']} {r['date']} | {r['start_time']} | {r['end_time']}\n")
    except Exception as e:
        print(f"[ERROR] Failed to get booked pt sessions: {repr(e)}")
        conn.rollback()
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT room_id, date, start_time, end_time, capacity FROM group_classes WHERE trainer_id = %s AND status = 'scheduled' ORDER BY date DESC;", (trainer_id))
            rows = cur.fetchall()
            print("\nCurrently Scheduled Group Classes:")
            for r in rows:
                print(f"  - Room ID: {r['room_id']} | Date: {r['date']} | Start-time: {r['start_time']} | End-time: {r['end_time']} | Number of Participants: {r['capacity']}\n")
    except Exception as e:
        print(f"[ERROR] Failed to get scheduled group classes: {e}")

def lookup_member(conn, trainer_id):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT DISTINCT m.member_id, m.name, m.attendance, hm.height, hm.weight, hm.heart_rate, hm.body_fat_percentage FROM members m JOIN pt_sessions s ON s.member_id = m.member_id JOIN health_metrics hm ON hm.member_id = m.member_id WHERE s.trainer_id = %s ORDER BY m.name ASC;", (trainer_id))
            rows = cur.fetchall()
            for r in rows:
                print(f"  - ID {r['m.member_id']}: Name: {r['m.name']} | Attendance Rate: {r['m.attendance']} | Height: {r['hm.height']} | Weight: {r['hm.weight']} | Heart Rate: {r['hm.heart_rate']} | Body Fat Percentage: {r['hm.body_fat_percentage']}\n")
    except Exception as e:
        print(f"[ERROR] Failed to get member information: {e}")

    # try:
    #     with conn.cursor(cursor_factory=RealDictCursor) as cur:
    #         cur.execute("SELECT DISTINCT m.member_id, m.name, m.attendance, hm.height, hm.weight, hm.heart_rate, hm.body_fat_percentage FROM members m JOIN group_classes s ON m.member_id = s.member_id JOIN health_metrics hm ON hm.member_id = m.member_id WHERE trainer_id = %s ORDER BY m.name ASC", (trainer_id))
    #         rows = cur.fetchall()
    #         for r in rows:
    #             print(f"  - ID {r['m.member_id']}: Name: {r['m.name']} | Attendance Rate: {r['m.attendance']} | Height: {r['hm.height']} | Weight: {r['hm.weight']} | Heart Rate: {r['hm.heart_rate']} | Body Fat Percentage: {r['hm.body_fat_percentage']}\n")
    # except Exception as e:
    #     print(f"[ERROR] Failed to get member information: {e}")



def menu(conn, trainer_id):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("CREATE INDEX IF NOT EXISTS idx_pt_trainer ON pt_sessions(trainer_id);")
            conn.commit()
    except Exception as e:
        print(f"[ERROR] Failed to create index: {e}")
    while True:
        print("\n=== Trainer Dashboard ===")
        print("1. Set Availability")
        print("2. View Schedule")
        print("3. Lookup Member")
        print("4. Exit")

        choice = input("Select option: ")
        if choice == "1":
            set_availability(conn, trainer_id)
        elif choice == "2":
            view_schedule(conn, trainer_id)
        elif choice == "3":
            lookup_member(conn, trainer_id)
        elif choice == "4":
            try:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("DROP INDEX CONCURRENTLY idx_pt_trainer;")
                    conn.commit()
            except Exception as e:
                print(f"[ERROR] Failed to drop index: {e}")
            break
