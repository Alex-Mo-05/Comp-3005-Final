from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from datetime import datetime


def manage_rooms(conn, admin_id):
# show a list of all rooms and their current bookings, join tables room and pt sessions, room and group classes, show room id, type of room, type of activity, capacity of room, capacity of class, date, time, option to rebook
    while True:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT room_id, room_type, status, capacity FROM rooms;")
                rows = cur.fetchall()
                print("\nDisplaying all rooms\n")
                for r in rows:
                    print(f"  - Room ID {r['room_id']}: Room Type: {r['room_type']} | Status: {r['status']} | Room Capacity: {r['capacity']} \n")
        except Exception as e:
            print(f"[ERROR] Failed to get rooms: {e}")

        print("\n=== Room Dashboard ===")
        print("1. Assign Classes to rooms")
        print("2. Assign Repairs")
        print("3. Mark Repair as Comlete")
        print("4. Exit")
        choice = input("Select option: ").strip()
        if choice == "1":
            try:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("SELECT class_id, name, trainer_id, room_id, capacity, date, start_time, end_time FROM group_classes;")
                    rows = cur.fetchall()
                    print("\nDisplaying all classes\n")
                    for r in rows:
                        print(f"  - Class ID {r['class_id']}: Room Name: {r['name']} | Trainer ID: {r['trainer_id']} | Room ID: {r['room_id']} | Class Capacity: {r['capacity']} | Date: {r['date']} |  Start Time: {r['start_time']} | End Time: {r['end_time']} \n")
            except Exception as ed:
                print(f"[ERROR] Failed to get class list: {ed}")
            

        elif choice == "2":
            # assign
            rid = input("Input the ID for the room that requires repair: ")
            try:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("SELECT room_id FROM equipment WHERE room_id = %s;", (rid))
                    if cur.fetchone() is not None:
                        try:
                            with conn.cursor() as cur:
                                cur.execute("""
                                    UPDATE rooms SET status = 'closed'""")
                                conn.commit()
                                print("[Success] Room status updated to 'closed'.")
                        except Exception as ef:
                            conn.rollback()
                            print(f"[ERROR] Failed to update room: {ef}")
                        
            except Exception as d:
                print(f"[ERROR] Failed to find room with that ID: {d}")
        elif choice == "3":
            # mark as complete
            try:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("SELECT repair_id, machine_id, assigned_to, reported_by, issue_description, status, date_reported FROM repairs WHERE status = 'reported';")
                    rows = cur.fetchall()
                    print("\nPrinting all Reported Repairs\n")
                    for r in rows:
                        print(f"  - Repair ID {r['repair_id']}: Machine ID: {r['machine_id']} | Currently Assigned to: {r['assigned_to']} | Reported By: {r['reported_by']} | Issue: {r['issue_description']} | Status: {r['status']} | Date Reported: {r['date_reported']}\n")
            except Exception as et:
                print(f"[ERROR] Failed to get repair list: {et}")
            
            fid = input("Which repair would you like to mark as complete: ")
            cur.execute("SELECT machine_id FROM repairs WHERE repair_id = %s;", (rid))
            mid = cur.fetchone()
            if mid is not None:
                try: 
                    cur.execute("""UPDATE repairs SET status = 'completed' WHERE repair_id = %s """, (fid))
                    conn.commit()
                    cur.execute("""UPDATE equipment SET status = 'operational' WHERE machine_id = %s """, (mid))
                    conn.commit()
                    print("[Success] Repair updated.")
                except Exception as ye:
                    conn.rollback()
                    print(f"[ERROR] Failed to update repair {ye}")

        elif choice == "4":
            break
        else:
            print("Invalid choice")


def manage_equipment(conn, admin_id):
    # display all operational status
#create repair - should change machine to operational down - should be able to leave assignment open or assigned
# assign repair should show all repairs, and allow admin to assign repairs to a trainer
# mark reapirs as compleye - this should change machines back to operational
    while True:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT machine_id, room_id, name, operational_status, last_maintenance_date FROM equipment;")
                rows = cur.fetchall()
                print("\nPrinting all Invoices\n")
                for r in rows:
                    print(f"  - Invoice ID {r['invoice_id']}: Member ID: {r['member_id']} | Service: {r['service']} | Amount Due: {r['amount_due']} | Status: {r['status']} | Billing Date: {r['billing_date']} | Paid Date: {r['paid_date']}\n")
        except Exception as e:
            print(f"[ERROR] Failed to get invoices: {e}")
        
            print("\n=== Equipment Dashboard ===")
            print("1. Create Repair")
            print("2. Assign Repairs")
            print("3. Mark Repair as Comlete")
            print("4. Exit")
            choice = input("Select option: ").strip()
            if choice == "1":
                mid = input("Input the ID for the broken machine: ")
                try:
                    with conn.cursor(cursor_factory=RealDictCursor) as cur:
                        cur.execute("SELECT machine_id FROM equipment WHERE machine_id = %s;", (mid))
                        if cur.fetchone() is not None:
                            desc = input("Describe the issue: ")
                            try:
                                with conn.cursor() as cur:
                                    cur.execute("""
                                        INSERT INTO repairs (machine_id, assigned_to, reported_by, issue_description, status, date_reported)
                                        VALUES ( %s, %s, %s, %s, %s, %s)
                                    """, (mid, "", admin_id, desc, "reported", datetime.now()))
                                    conn.commit()
                                    print("[Success] Repair added.")
                            except Exception as y:
                                conn.rollback()
                                print(f"[ERROR] Failed to add repair: {y}")
                            try:
                                with conn.cursor() as cur:
                                    cur.execute("""
                                        UPDATE equipment SET status = 'down' WHERE machine_id = %s """, (mid))
                                    conn.commit()
                                    print("[Success] Repair added.")
                            except Exception as u:
                                conn.rollback()
                                print(f"[ERROR] Failed to add repair: {u}")
                except Exception as d:
                    print(f"[ERROR] Failed to find machine with that ID: {d}")
                

            elif choice == "2":
                # assign
                try:
                    with conn.cursor(cursor_factory=RealDictCursor) as cur:
                        cur.execute("SELECT repair_id, machine_id, assigned_to, reported_by, issue_description, status, date_reported FROM repairs WHERE status = 'reported';")
                        rows = cur.fetchall()
                        print("\nPrinting all Reported Repairs\n")
                        for r in rows:
                            print(f"  - Repair ID {r['repair_id']}: Machine ID: {r['machine_id']} | Currently Assigned to: {r['assigned_to']} | Reported By: {r['reported_by']} | Issue: {r['issue_description']} | Status: {r['status']} | Date Reported: {r['date_reported']}\n")
                except Exception as i:
                    print(f"[ERROR] Failed to get repair list: {i}")

                try:
                    with conn.cursor(cursor_factory=RealDictCursor) as cur:
                        cur.execute("SELECT trainer_id, name, FROM trainers;")
                        rows = cur.fetchall()
                        print("\nPrinting all Reported Repairs\n")
                        for r in rows:
                            print(f"  - Trainer ID {r['trainer_id']}: Name: {r['name']}\n")
                except Exception as k:
                    print(f"[ERROR] Failed to get trainer list: {k}")

                rid = input("Which repair id would you like to assign: ")
                try:
                    with conn.cursor(cursor_factory=RealDictCursor) as cur:
                        cur.execute("SELECT repair_id FROM repairs WHERE repair_id = %s;", (rid))
                        if cur.fetchone() is not None:
                            tid = input("Which trainer would you like to assign to it: ")
                            cur.execute("SELECT trainer_id FROM trainers WHERE trainer_id = %s;", (tid))
                            if cur.fetchone() is not None:
                                try: 
                                    cur.execute("""UPDATE repairs SET assigned_to = %s WHERE machine_id = %s """, (tid, mid))
                                    conn.commit()
                                    print("[Success] Repair assigned.")
                                except Exception as o:
                                    conn.rollback()
                                    print(f"[ERROR] Failed to Assign repair {o}")


                except Exception as l:
                    print(f"[ERROR] Failed to Assign repair {l}")

            elif choice == "3":
                # mark as complete
                try:
                    with conn.cursor(cursor_factory=RealDictCursor) as cur:
                        cur.execute("SELECT repair_id, machine_id, assigned_to, reported_by, issue_description, status, date_reported FROM repairs WHERE status = 'reported';")
                        rows = cur.fetchall()
                        print("\nPrinting all Reported Repairs\n")
                        for r in rows:
                            print(f"  - Repair ID {r['repair_id']}: Machine ID: {r['machine_id']} | Currently Assigned to: {r['assigned_to']} | Reported By: {r['reported_by']} | Issue: {r['issue_description']} | Status: {r['status']} | Date Reported: {r['date_reported']}\n")
                except Exception as g:
                    print(f"[ERROR] Failed to get repair list: {g}")
                
                fid = input("Which repair would you like to mark as complete: ")
                cur.execute("SELECT machine_id FROM repairs WHERE repair_id = %s;", (rid))
                mid = cur.fetchone()
                if mid is not None:
                    try: 
                        cur.execute("""UPDATE repairs SET status = 'completed' WHERE repair_id = %s """, (fid))
                        conn.commit()
                        cur.execute("""UPDATE equipment SET status = 'operational' WHERE machine_id = %s """, (mid))
                        conn.commit()
                        print("[Success] Repair updated.")
                    except Exception as eu:
                        conn.rollback()
                        print(f"[ERROR] Failed to update repair {eu}")

            elif choice == "4":
                break
            else:
                print("Invalid choice")


def manage_classes(conn, admin_id):
    print("")


def manage_billing(conn, admin_id):
    # display all invoices
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT invoice_id, member_id, service, amount_due, status, billing_date, paid_date FROM invoices;")
            rows = cur.fetchall()
            print("\nPrinting all Invoices\n")
            for r in rows:
                print(f"  - Invoice ID {r['invoice_id']}: Member ID: {r['member_id']} | Service: {r['service']} | Amount Due: {r['amount_due']} | Status: {r['status']} | Billing Date: {r['billing_date']} | Paid Date: {r['paid_date']}\n")
    except Exception as e:
        print(f"[ERROR] Failed to get invoices: {e}")

    ad = input("Would you like to create a new invoice (y/n): ")
    if ad == "y":
        mid = input("Please enter member ID for invoice: ")
        ser = input("Please write down the service provided: ")
        amt = input("Please enter the amount due: ")
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("INSERT INTO invoices (member_id, service, amount_due, status, billing_date) VALUES (%s, %s, %s, %s, %s)" , (mid, ser, amt, "unpaid", datetime.now()))
                conn.commit()
        except Exception as e:
            print(f"[ERROR] Failed to create invoice: {e}")
    else:
        return
    


def menu(conn, admin_id):
    while True:
        print("\n=== Admin Dashboard ===")
        print("1. Manage Rooms")
        print("2. Manage Equipment and Repairs")
        print("3. Manage Classes")
        print("4. Billing & Payments")
        print("5. Exit")
        choice = input("Select option: ").strip()
        if choice == "1":
            manage_rooms(conn, admin_id)
        elif choice == "2":
            manage_equipment(conn, admin_id)
        elif choice == "3":
            manage_classes(conn, admin_id)
        elif choice == "4":
            manage_billing(conn, admin_id)
        elif choice == "5":
            break
        else:
            print("Invalid choice")

