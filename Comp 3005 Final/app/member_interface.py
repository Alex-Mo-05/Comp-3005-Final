from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from datetime import datetime

def group_class(conn, member_id):
    print("")

def pt(conn, member_id):
    print("\nPhysical Training Scheduler")
    print("1. Schedule another PT Session")
    print("2. Cancel PT Session")
    print("3. Close")
    choice = input("Select option: ").strip()

    if choice == "1":
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT session_id, trainer_id, date, start_time, end_time, status FROM pt_sessions WHERE status = 'open' ORDER BY date DESC ;")
                rows = cur.fetchall()
                if rows is not None:
                    print("\nDisplaying open training sessions:")
                    for r in rows:
                        print(f"  - Session ID: {r['session_id']} | Trainer ID: {r['trainer_id']} | Date: {r['date']} | Start Time: {r['start_time']} | End Time: {r['end_time']} | Status: {r['status']}\n")
                else:
                    print("No Physical Sessions Available")
        except Exception as e:
            print(f"[ERROR] Failed to get physical training sessions: {e}")

        sid = input("Which session would you like to book: ")
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT session_id, trainer_id, date, start_time, end_time, status FROM pt_sessions WHERE status = 'open' ORDER BY date ASC ;")
                rows = cur.fetchall()
                if rows is not None:
                    print("\nSession Booked:")
                    for r in rows:
                        print(f"  - Session ID: {r['session_id']} | Trainer ID: {r['trainer_id']} | Date: {r['date']} | Start Time: {r['start_time']} | End Time: {r['end_time']} | Status: booked\n")
                    cur.execute("""UPDATE pt_sessions SET status = 'booked', member_id = %s WHERE session_id = %s """, (member_id, sid,))
                    conn.commit()
                else:
                    print("No Physical Sessions Available")
        except Exception as e:
            print(f"[ERROR] Failed to get physical training sessions: {e}")
        
    if choice == "2":
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT session_id, trainer_id, date, start_time, end_time, status FROM pt_sessions WHERE status = 'booked' AND member_id = %s ORDER BY date ASC ;", (member_id))
                rows = cur.fetchall()
                if rows is not None:
                    print("\nDisplaying booked training sessions:")
                    for r in rows:
                        print(f"  - Session ID: {r['session_id']} | Trainer ID: {r['trainer_id']} | Date: {r['date']} | Start Time: {r['start_time']} | End Time: {r['end_time']} | Status: {r['status']}\n")
                else:
                    print("No Booked Physical Sessions Recorded")
        except Exception as e:
            print(f"[ERROR] Failed to get booked physical training sessions: {e}")

        sid = input("Which session would you like to cancel: ")
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT session_id, trainer_id, date, start_time, end_time, status FROM pt_sessions WHERE status = 'booked' AND member_id = %s ORDER BY date ASC ;", (member_id))
                rows = cur.fetchall()
                if rows is not None:
                    print("\nSession Cancled:")
                    for r in rows:
                        print(f"  - Session ID: {r['session_id']} | Trainer ID: {r['trainer_id']} | Date: {r['date']} | Start Time: {r['start_time']} | End Time: {r['end_time']} | Status: canceled\n")
                    cur.execute("""UPDATE pt_sessions SET status = 'open', member_id = null WHERE session_id = %s """, ( sid,))
                    conn.commit()
                else:
                    print("No Physical Sessions Available")
        except Exception as e:
            print(f"[ERROR] Failed to get physical training sessions: {e}")     
    if choice == "3":
        return
    


def goals(conn, member_id):
    date = datetime.now()
    height = float(input("Target Height (Inches): ").strip())
    weight = float(input("Target Weight (lb): ").strip())
    hr = int(input("Target Heart rate: ").strip())
    bf = float(input("Target Body fat percentage (Decimal): ").strip())
    status = "goals"
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO health_metrics (member_id, status, date_recorded, height, weight, heart_rate, body_fat_percentage)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (member_id, status, date, height, weight, hr, bf))
            conn.commit()
            print("[Success] Goal added.")
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Failed to add goal: {e}")


def update(conn, member_id): 
    date = datetime.now()
    height = float(input("Height (Inches): ").strip())
    weight = float(input("Weight (lb): ").strip())
    hr = int(input("Heart rate: ").strip())
    bf = float(input("Body fat percentage (Decimal): ").strip())
    status = "current"
    try:
        with conn.cursor() as cur:
            cur.execute("""UPDATE health_metrics SET status = 'previous' WHERE status = 'current' AND member_id = %s """, (member_id,))
            conn.commit()
            cur.execute("""
                INSERT INTO health_metrics (member_id, status, date_recorded, height, weight, heart_rate, body_fat_percentage)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (member_id, status, date, height, weight, hr, bf))
            conn.commit()
            print("[Success] Metric added.")

    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Failed to add metric: {e}")


def view_dashboard(conn, member_id):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT height, weight, heart_rate, body_fat_percentage FROM health_metrics WHERE member_id = %s AND status = 'current' ORDER BY metric_id DESC LIMIT 1;", (member_id,))
            rows = cur.fetchall()
            if rows is not None:
                print("\nCurrent Health Metrics:")
                for r in rows:
                    print(f"  - Height: {r['height']} | Weight: {r['weight']} | Heart Rate: {r['heart_rate']} | Body Fat Percentage: {r['body_fat_percentage']}\n")
            else:
                print("No Metrics Recorded")
    except Exception as e:
        print(f"[ERROR] Failed to get current health metrics: {e}")
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT height, weight, heart_rate, body_fat_percentage FROM health_metrics WHERE member_id = %s AND status = 'goals' ORDER BY metric_id DESC LIMIT 1;", (member_id,))
            rows = cur.fetchall()
            if rows is not None:
                print("\nCurrent Goal Metrics:")
                for r in rows:
                    print(f"  - Height: {r['height']} | Weight: {r['weight']} | Heart Rate: {r['heart_rate']} | Body Fat Percentage: {r['body_fat_percentage']}\n")
            else:
                print("No Goals Set")
    except Exception as e:
        print(f"[ERROR] Failed to get current goal metrics: {e}")

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT session_id, trainer_id, room_id, date, start_time, end_time FROM pt_sessions WHERE member_id = %s AND status = 'booked' ORDER BY date ASC", (member_id,))
            rows = cur.fetchall()
            if not rows:
                print("No Sessions Booked")
                return
            print("\nBooked PT Sessions:")
            for r in rows:
                print(f"  - Session ID: {r['session_id']} | Trainer ID: {r['trainer_id']} | Room ID: {r['room_id']} | Date: {r['date']} | Start Time: {r['start_time']} | End Time: {r['end_time']}\n")
            return rows
    except Exception as e:
        print(f"[ERROR] Failed to get upcomming pt sessions: {e}")
    
    

def menu(conn, member_id):
    while True:
        print("\n=== Member Dashboard ===")
        view_dashboard(conn, member_id)
        print("\n1. Register for Group Classes")
        print("2. Schedule Personal Training")
        print("3. Add Fitness Goals")
        print("4. Update Health Metrics")
        print("5. Exit")
        choice = input("Select option: ").strip()
        if choice == "1":
            group_class(conn, member_id)
        elif choice == "2":
            pt(conn, member_id)
        elif choice == "3":
            goals(conn, member_id)
        elif choice == "4":
            update(conn, member_id)
        elif choice == "5":
            break
        else:
            print("Invalid choice")