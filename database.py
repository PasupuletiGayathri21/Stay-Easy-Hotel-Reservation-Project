import sqlite3
import os

conn = None
cur = None
from datetime import date,datetime

def initialize_database():
    global conn,cur

    conn = sqlite3.connect("rooms.db")
    cur = conn.cursor()

    cur.execute("PRAGMA foreign_keys = ON")
    

    cur.execute("""
        CREATE TABLE IF NOT EXISTS guests (
            name NVARCHAR(40) NOT NULL,
            mobile_number TEXT PRIMARY KEY,
            email_id TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY,
            mobile_no TEXT NOT NULL,
            room_type NVARCHAR(30) NOT NULL,
            number_of_guest INTEGER NOT NULL,
            booking_date DATE NOT NULL,
            checkin DATE NOT NULL,
            checkout DATE NOT NULL,
            room_no INTEGER NOT NULL,
            status NVARCHAR(30) NOT NULL,
            total_pay INTEGER NOT NULL,
            FOREIGN KEY (mobile_no) REFERENCES guests(mobile_number)
        )
    """)

    conn.commit()


def insert_into_guest_table(guest):
    guest_mobile_number_list = []

    cur.execute("SELECT mobile_number FROM guests")

    for i in cur.fetchall():
        guest_mobile_number_list.append(i[0])

    if guest.mobile_number not in guest_mobile_number_list:
        cur.execute(
            "INSERT INTO guests VALUES (?, ?, ?)",
            (guest.name, guest.mobile_number, guest.email_id)
        )
        conn.commit()


def get_booked_rooms(room_type, requested_checkin, requested_checkout):
    cur.execute("""
        SELECT room_no, room_type, status
        FROM bookings
        WHERE room_type = ?
        AND status NOT IN ('CANCELLED', 'CHECKED_OUT')
        AND checkin < ?
        AND checkout > ?
    """, (room_type, requested_checkout, requested_checkin))

    return cur.fetchall()
def get_returning_guest(mobile_number):
    cur.execute("""
        SELECT mobile_no
        FROM bookings
        WHERE mobile_no = ?
        AND status = 'CHECKED_OUT'
    """, (mobile_number,))
    return cur.fetchall()
def insert_into_booking(booking_id, mobile_number, room_type,
                        number_of_guest, booking_date, checkin,
                        checkout, room_no, status, total_pay):

    cur.execute("""
        INSERT INTO bookings
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        booking_id, mobile_number, room_type, number_of_guest,
        booking_date, checkin, checkout, room_no, status, total_pay
    ))

    conn.commit()

def generate_booking_id():
    cur.execute("SELECT MAX(booking_id) FROM bookings")
    result = cur.fetchone()[0]

    if result is None:
        return 1

    return result + 1
def get_booking_details(booking_id):
    cur.execute("""
        SELECT *
        FROM bookings
        WHERE booking_id = ?
    """, (booking_id,))

    return cur.fetchone()
def get_bookingid(user_mobile_number):
    cur.execute("""
        SELECT booking_id
        FROM bookings
        WHERE mobile_no = ?
        AND status = 'CONFIRMED'
        AND checkin = ?
    """, (user_mobile_number,date.today().isoformat()))

    return cur.fetchall()
def set_checkin_status(record):
    cur.execute("""
        UPDATE bookings
        SET status = 'CHECKED_IN'
        WHERE booking_id = ?
    """, (record[0],))
    conn.commit()
def get_bookingid_checkout(user_mobile_number):
    cur.execute("""
        SELECT booking_id
        FROM bookings
        WHERE mobile_no = ?
        AND status = 'CHECKED_IN'
        AND checkout = ?
    """, (user_mobile_number, date.today().isoformat()))

    return cur.fetchall()


def set_checkout_status(record):
    cur.execute("""
        UPDATE bookings
        SET status = 'CHECKED_OUT'
        WHERE booking_id = ?
    """, (record[0],))
    conn.commit()
def get_invoice_details(booking_id):
    cur.execute("""
        SELECT b.booking_id, g.name, b.mobile_no, g.email_id,
               b.room_type, b.number_of_guest, b.booking_date,
               b.checkin, b.checkout, b.room_no, b.total_pay
        FROM bookings b
        JOIN guests g
        ON b.mobile_no = g.mobile_number
        WHERE b.booking_id = ?
    """, (booking_id,))

    return cur.fetchone()
def cancel_booking_status(booking_id):
    cur.execute("""
        UPDATE bookings
        SET status = 'CANCELLED'
        WHERE booking_id = ?
    """, (booking_id,))
    conn.commit()
def get_occupancy_data():
    cur.execute("""
        SELECT COUNT(DISTINCT room_no)
        FROM bookings
        WHERE status = 'CHECKED_IN'
    """)
    return cur.fetchone()[0]


def get_revenue_data():
    cur.execute("""
        SELECT
            COUNT(*),
            COALESCE(SUM(total_pay), 0)
        FROM bookings
        WHERE status != 'CANCELLED'
    """)
    return cur.fetchone()


def get_all_bookings_for_export():
    cur.execute("""
        SELECT b.booking_id, g.name, b.mobile_no,
               b.room_type, b.number_of_guest,
               b.booking_date, b.checkin, b.checkout,
               b.room_no, b.status, b.total_pay
        FROM bookings b
        JOIN guests g
        ON b.mobile_no = g.mobile_number
        ORDER BY b.booking_id
    """)
    return cur.fetchall()
def get_guest_history(mobile_number):
    cur.execute("""
        SELECT booking_id, room_type, number_of_guest,
               checkin, checkout, room_no, status, total_pay
        FROM bookings
        WHERE mobile_no = ?
        ORDER BY checkin DESC
    """, (mobile_number,))

    return cur.fetchall()