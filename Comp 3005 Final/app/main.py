
import os
import sys
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from datetime import datetime
from .member_interface import menu as member_menu
from .trainer_interface import menu as trainer_menu
from .admin_interface import menu as admin_menu


def get_connection():
    """
    Create and return a psycopg2 connection using environment variables.
    Required env vars:
      - PGHOST
      - PGPORT
      - PGDATABASE
      - PGUSER
      - PGPASSWORD
    """
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            dbname='fitness_club',
            user="postgres",
            password="12345",
        )
        return conn
    except Exception as e:
        print(f"[ERROR] Failed to connect to database: {e}")
        sys.exit(1)

def check_id(conn, type, login):
    with conn.cursor() as cur:

        if type == "1":
            try:
                cur.execute("SELECT 1 FROM members WHERE member_id = %s;", (login))
                if cur.fetchone() is not None:
                        if cur.rowcount == 0:
                            print(f"[WARN] There are no members with ID: {login}")
                            conn.rollback()
                            return False
                        conn.commit()
                        print(f"[OK] Login Successful for id: {login}\n")
                        member_menu(conn, login)
                        return True
            
    
                else:
                    print("Unable to find member please try again. \n")
                    return False
            except Exception as e:
                conn.rollback()
                print(f"[ERROR] Login failed: {e}\n")
                return False
            
        elif type == "2":
            try:

                cur.execute("SELECT 1 FROM trainers WHERE trainer_id = %s;", (login))
                if cur.fetchone() is not None:
                    if cur.rowcount == 0:
                        print(f"[WARN] There are no trainers with ID: {login}")
                        conn.rollback()
                        return False
                    conn.commit()
                    print(f"[OK] Login Successful for id: {login}\n")
                    trainer_menu(conn, login)
                    return True
                
                else:
                    print("Unable to find trainer please try again. \n")
                    return False
            except Exception as e:
                        conn.rollback()
                        print(f"[ERROR] Login failed: {e}\n")
                        return False
                
        elif type == "3":
            try:
                cur.execute("SELECT 1 FROM admins WHERE admin_id = %s;", (login))
                if cur.fetchone() is not None:
                    if cur.rowcount == 0:
                        print(f"[WARN] There are no admins with ID: {login}")
                        conn.rollback()
                        return False
                    conn.commit()
                    print(f"[OK] Login Successful for id: {login}\n")
                    admin_menu(conn, login)
                    return True
                else:
                    print("Unable to find admin please try again. \n")
                    return False
            except Exception as e:
                conn.rollback()
                print(f"[ERROR] Login failed: {e}\n")
                return False
    




def register_member(conn):
    name = input("Enter Name: ").strip()
    email = input("Enter Email: ").strip()
    phone = input("Enter Phone: ").strip()
    try:
        phone = int(phone)

    except Exception as e:
        while True:
            print(f"Please enter your phone number {e}")
            phone = input("Enter Phone: ").strip()
            try:
                phone = int(phone)
                break
            except Exception as j:
                print("\n")


                    



    gender = input("Enter Gender: ").strip()
    address = input("Enter Address: ").strip()
    dob = input("Enter Date of Birth (YYYY-mm-dd): ")
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO members (name, date_of_birth, gender, phone, email, address, join_date, membership_status, attendance)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING member_id;
                """,
                (name, dob, gender, phone, email, address, datetime.now(), "active", "100"),
            )
            new_id = cur.fetchone()[0]
            conn.commit()
            print(f"[OK] New member added: Please remember your ID: {new_id}, thanks for joining us: ({name})!\n")
            member_menu(conn, new_id)
            return new_id
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Adding member failed: {e}")
        return None



def main():
    conn = get_connection()
    while True:
        print("1. Login as member\n2. Login as trainer\n3. Login as admin\n4. Register member\n5. Exit")
        choice = input("Choice: ").strip()
        if choice == "4":
            register_member(conn)
        elif choice == "1" or choice == "2" or choice == "3":
            id = input("Please enter your ID: ").strip()
            check_id(conn, choice, id)
           
        elif choice == "5":
            conn.close()
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
