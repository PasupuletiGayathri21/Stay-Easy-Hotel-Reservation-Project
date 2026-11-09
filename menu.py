from models import Guest, Booking, Room, StandardRoom, DeluxeRoom, SuiteRoom
from exceptions import (
    RoomUnavailable,
    InvalidDate,
    InvalidStatusChange,
    BookingNotFound,
    RulesVoilationError,
    
)
from database import (
    insert_into_guest_table,
    get_booked_rooms,
    insert_into_booking,
    generate_booking_id,
    get_booking_details,
    get_bookingid,
    set_checkin_status,
    get_bookingid_checkout,
    set_checkout_status,
    get_invoice_details,
    cancel_booking_status,
    get_occupancy_data,
    get_revenue_data,
    get_all_bookings_for_export,
    get_guest_history
)
import csv
from room_inventory import valid_rooms,room_types
from datetime import date ,datetime
import os

def take_guest_data():
    while True:
        try:
            name=input("enter the name of the guest").lower().strip()
            if name=="":
                raise RulesVoilationError("guest name cannot be empty")
            break
        except RulesVoilationError as r:
            print(r)
            # logging.error(str(r))
    while True:
        try:
            mobile_number=input("enter the mobile number").strip()
            if mobile_number=="":
                raise RulesVoilationError("mobile number cannot be empty")
            if len(mobile_number)!=10:
                raise RulesVoilationError("mobile number should consist of 10 digits ")
            if not mobile_number.isdigit():
                raise RulesVoilationError("Mobile number must contain only digits")
            if not mobile_number.startswith(('6', '7', '8', '9')):
                raise RulesVoilationError("Mobile number must start with 6, 7, 8 or 9")
            
            break
        except RulesVoilationError as r:
            print(r)
            # logging.error(str(r))  
    while True:
        try: 
            email_id=input("enter the email id")
            if email_id.count('@')>1:
                raise RulesVoilationError("email id is not in correct format")
            if '@' not in email_id:
                raise RulesVoilationError("email id is not in correct format")
            fist_part,second_part=email_id.split('@')
            if '.' not in second_part:
                raise RulesVoilationError("email id is not in correct format")
            if '.' in fist_part:
                raise RulesVoilationError("email id is not in correct format")
            if second_part.count('.')>1:
                raise RulesVoilationError("email id is not in correct format")
            break
        except RulesVoilationError as r:
            print(r)
            # logging.error(str(r))
    guest=Guest(name,mobile_number,email_id)
    insert_into_guest_table(guest)
    return guest

room_types_avail=[]
for i in room_types:
    room_types_avail.append(i['room_type'].lower())



def available_rooms(guest):
    while True:
        print("Room types available and their capacities")
        try:
            room_type=input("enter room type").lower().strip()
            if room_type=="":
                raise RoomUnavailable("Empty room type is not available")
            if room_type not in room_types_avail:
                raise RoomUnavailable("Room with this room type is not available")
            break
        except RoomUnavailable as r:
            print(r)
            # logging.error(str(r))
    while True:
        try:
            number_of_guest=input("enter number of guest")
            if not number_of_guest.isdigit():
                raise RulesVoilationError("Number of guests should be a number")

            number_of_guest = int(number_of_guest)
            for i in room_types:
                    if i['room_type'].strip().lower()==room_type:
                        max_guest_capacity=i['max_guests']
            if max_guest_capacity<number_of_guest:
                raise RulesVoilationError(f"Room type capacity is exceeding ....please choose another or split and stay in different rooms")
            
            break
            
        except RulesVoilationError as r:
            print(r)
            # logging.error(str(r))
    while True:
        try:
            checkin = input("enter checkin date in dd-mm-yyyy format: ").strip()
            converted_checkin = datetime.strptime(checkin, "%d-%m-%Y").date()
            if (converted_checkin<date.today()):
                raise InvalidDate("Date is not valid")
            if (converted_checkin-date.today()).days>180:
                raise InvalidDate("checkin date is 180 days from today which is not accepted")
            break
        except InvalidDate as i:
            print(i)
        except ValueError:
            print("Please enter the date in DD-MM-YYYY format")
    while True:
        try:
            checkout = input("enter checkout date in dd-mm-yyyy format: ").strip()
            converted_checkout = datetime.strptime(checkout, "%d-%m-%Y").date()
            if (converted_checkout-converted_checkin).days>30:
                raise InvalidDate("stay cannot be more than 30 days ....enter valid checkout date")
            if converted_checkout<=converted_checkin:
                raise InvalidDate("Checkout must be after check-in")
            break
        except InvalidDate as i:
            print(i)
        except ValueError as v:
            print(v)
        
    booked_rooms_of_room_type = get_booked_rooms(room_type,converted_checkin.isoformat(),converted_checkout.isoformat())
    available_rooms_to_show = []
    for i in valid_rooms:
        if i["room_type"].strip().lower() == room_type:
            room_number = i["room_no"].strip()
            is_available = True
            for j in booked_rooms_of_room_type:
                if room_number == str(j[0]):
                    is_available = False
                    break
            if is_available:
                available_rooms_to_show.append(room_number)
    print("Available rooms:", available_rooms_to_show)

    if not available_rooms_to_show:
        raise RoomUnavailable("No rooms available for the selected dates")

    room_number = available_rooms_to_show[0]
    return room_type,number_of_guest,converted_checkin,converted_checkout,room_number


   























    # room_type = guest.room_type
    # number_of_guest = int(guest.number_of_guest)

    # cur.execute("""
    #     SELECT x.room_type, x.room_no, x.maximum_guests
    #     FROM (
    #         SELECT rt.room_type, r.room_no, rt.maximum_guests
    #         FROM room_types AS rt
    #         INNER JOIN rooms AS r
    #             ON rt.room_type = r.room_type
    #         WHERE rt.room_type = ?
    #           AND rt.maximum_guests >= ?
    #     ) AS x
    #     WHERE NOT EXISTS (
    #         SELECT 1
    #         FROM bookings AS b
    #         WHERE x.room_no = b.room_no
    #           AND b.status NOT IN ('CANCELLED', 'CHECKED_OUT')
    #     )
    #     ORDER BY x.room_no ASC
    # """, (room_type, number_of_guest))

    # temp = cur.fetchall()

    # if temp:
    #     print("Available rooms:")
    #     for i in temp:
    #         print(i)

    # else:
    #     print("Sorry... The requested room type is not available.")
    #     print("Checking alternative room types...")

    #     cur.execute("""
    #         SELECT x.room_type, x.room_no, x.maximum_guests
    #         FROM (
    #             SELECT rt.room_type, r.room_no, rt.maximum_guests
    #             FROM room_types AS rt
    #             INNER JOIN rooms AS r
    #                 ON rt.room_type = r.room_type
    #             WHERE rt.room_type != ?
    #               AND rt.maximum_guests >= ?
    #         ) AS x
    #         WHERE NOT EXISTS (
    #             SELECT 1
    #             FROM bookings AS b
    #             WHERE x.room_no = b.room_no
    #               AND b.status NOT IN ('CANCELLED', 'CHECKED_OUT')
    #         )
    #         ORDER BY x.room_no ASC
    #     """, (room_type, number_of_guest))

    #     alternative_rooms = cur.fetchall()

    #     if alternative_rooms:
    #         print("Alternative rooms available:")
    #         for i in alternative_rooms:
    #             print(i)
    #     else:
    #         print("No rooms are available.")
    pass


def create_booking(guest):

    room_type, number_of_guest, checkin, checkout, room_number = available_rooms(guest)

    if room_type == "standard":
        room = StandardRoom(room_type, number_of_guest, checkin, checkout, guest.mobile_number)

    elif room_type == "deluxe":
        room = DeluxeRoom(room_type, number_of_guest, checkin, checkout, guest.mobile_number)

    else:
        room = SuiteRoom(room_type, number_of_guest, checkin, checkout, guest.mobile_number)

    total_base_price, base_price = room.normal_room_charges()
    total_weekend_charge, normal_weekend_charge = room.weekends_charges()

    extra_guest_result = room.extra_guest_charge()

    if isinstance(extra_guest_result, tuple):
        total_extra_guest_charge = extra_guest_result[0]
    else:
        total_extra_guest_charge = extra_guest_result

    total_breakfast_charge, normal_breakfast_charge = room.breakfast()

    total_discount, normal_discount = room.discount_on_room_charges()
    total_loyalty_discount, normal_loyalty_discount = room.loyality_discount()

    total_gst = room.gst()

    total_pay = round(
        total_base_price
        + total_weekend_charge
        + total_extra_guest_charge
        + total_breakfast_charge
        - total_discount
        - total_loyalty_discount
        + total_gst
    )

    booking_id = generate_booking_id()
    booking_date = date.today().isoformat()
    status = "CONFIRMED"

    insert_into_booking(
        booking_id,
        guest.mobile_number,
        room_type,
        number_of_guest,
        booking_date,
        checkin.isoformat(),
        checkout.isoformat(),
        int(room_number),
        status,
        total_pay
    )

    print("------ BOOKING CONFIRMED ------")
    print("Booking ID:", booking_id)
    print("Guest:", guest.name)
    print("Room Type:", room_type)
    print("Room Number:", room_number)
    print("Check-in:", checkin)
    print("Check-out:", checkout)
    print("Total Payment:", total_pay)
    print("Status:", status)

    
#     room_no=selected_room
    
#     booking_date=date.today()
#     while True:
#             try:
#                 number_of_guest=input("enter the umber of guests").strip()
#                 if not number_of_guest.isdigit():
#                     raise RulesVoilationError("number of guests should be a number")
#                 if int(number_of_guest)<0:
#                     raise RulesVoilationError("number of guests cannot be negative")
#                 if number_of_guest=="":
#                     raise RulesVoilationError("number of guests cannot be empty")
#                 break
#             except RulesVoilationError as r:
#                 print(r)
#     while True:
#         room_type=input("enter room type").lower().strip()
#         break
#     while True:
#         try:
#             checkin=input("enter checkin date in dd-mm-yyyy format")
#             converted_checkin=datetime.strptime(checkin,"%d-%m-%Y")
#             if converted_checkin<date.today():
#                 raise InvalidDate("Date is not valid")
#             if converted_checkin-date.today()>=180:
#                 raise InvalidDate("checkin date is 180 days from today which is not accepted")
#             break
#         except InvalidDate as i:
#             print(i)
#     while True:
#         try:
#             checkout=input("enter checkout date")
#             converted_checkout=datetime.strptime(checkout,"%d-%m-%Y")
#             if converted_checkout-converted_checkin>30:
#                 raise InvalidDate("stay cannot be more than 30 days ....enter valid checkout date")
#             break
#         except InvalidDate as i:
#             print(i)
#     status='Confirmed'
#     total_pay=0




#     booking=Booking(guest,room_type,number_of_guest,booking_date,checkin,checkout,room_no,status,total_pay)
    pass
def view_booking_details():
    booking_id = input("Enter booking ID: ")

    if not booking_id.isdigit():
        print("Booking ID must be numeric")
        return

    booking = get_booking_details(int(booking_id))

    if booking is None:
        print("Booking not found")
        return

    print(" BOOKING DETAILS)
    print("Booking ID:", booking[0])
    print("Mobile Number:", booking[1])
    print("Room Type:", booking[2])
    print("Number of Guests:", booking[3])
    print("Booking Date:", booking[4])
    print("Check-in:", booking[5])
    print("Check-out:", booking[6])
    print("Room Number:", booking[7])
    print("Status:", booking[8])
    print("Total Payment:", booking[9])

    



def perform_checkin():
    user_mobile_number = input("Enter mobile number: ").strip()

    record = get_bookingid(user_mobile_number)

    if not record:
        print("No confirmed booking found for this mobile number today")
        return

    if len(record) > 1:
        print("Multiple bookings found. Please identify the correct booking.")
        return

    set_checkin_status(record[0])
    print("Check-in successful!")

def perform_checkout():
    user_mobile_number = input("Enter mobile number: ").strip()

    record = get_bookingid_checkout(user_mobile_number)

    if not record:
        print("No checked-in booking found for this mobile number today")
        return

    if len(record) > 1:
        print("Multiple bookings found. Please identify the correct booking.")
        return
    booking_id = record[0][0]
    set_checkout_status(record[0])
    print("Checkout successful!")
    generate_invoice(booking_id)
    
def generate_invoice(booking_id):
    record = get_invoice_details(booking_id)

    if record is None:
        print("Invoice details not found")
        return
    os.makedirs("invoices", exist_ok=True)
    invoice_path = os.path.join("invoices", f"BK{booking_id}.txt")
    checkin_date = datetime.strptime(record[7], "%Y-%m-%d").date()
    checkout_date = datetime.strptime(record[8], "%Y-%m-%d").date()
    nights = (checkout_date - checkin_date).days
    with open(invoice_path, "w") as file:
        file.write("STAYEASY HOTEL")
        file.write(" GUEST INVOICE")
        file.write(f"Invoice Number : BK{record[0]}\n")
        file.write(f"Guest Name     : {record[1]}\n")
        file.write(f"Mobile Number  : {record[2]}\n")
        file.write(f"Email          : {record[3]}\n")
        file.write(f"Room Type      : {record[4]}\n")
        file.write(f"Room Number    : {record[9]}\n")
        file.write(f"Number Guests  : {record[5]}\n")
        file.write(f"Booking Date   : {record[6]}\n")
        file.write(f"Check-in       : {record[7]}\n")
        file.write(f"Check-out      : {record[8]}\n")
        file.write(f"Total Nights   : {nights}\n")
        file.write(f"Total Amount   : Rs. {record[10]}\n")
        file.write("       THANK YOU FOR STAYING!\n")

    print("Invoice generated successfully!")
    print("Invoice saved at:", invoice_path)
def cancel_booking():
    booking_id = input("Enter booking ID: ").strip()
    if not booking_id.isdigit():
        print("Booking ID must be numeric")
        return
    booking = get_booking_details(int(booking_id))
    if booking is None:
        print("Booking not found")
        return
    if booking[8] != "CONFIRMED":
        print("Only confirmed bookings can be cancelled")
        return
    checkin_date = datetime.strptime(booking[5], "%Y-%m-%d").date()
    today = date.today()
    days_remaining = (checkin_date - today).days
    if days_remaining >= 7:
        refund_percentage = 100
    elif days_remaining >= 2:
        refund_percentage = 50
    else:
        refund_percentage = 0
    refund_amount = booking[9] * refund_percentage // 100
    cancel_booking_status(int(booking_id))
    print("Booking cancelled successfully!")
    print("Total Amount:", booking[9])
    print("Refund Percentage:", refund_percentage, "%")
    print("Refund Amount: Rs.", refund_amount)
def occupancy_report():
    total_rooms = len(valid_rooms)
    occupied_rooms = get_occupancy_data()
    available_rooms_count = total_rooms - occupied_rooms
    if total_rooms == 0:
        print("No valid rooms available")
        return
    occupancy_percentage = (occupied_rooms / total_rooms) * 100

    print("OCCUPANCY REPORT")
    print("Total Rooms:", total_rooms)
    print("Occupied Rooms:", occupied_rooms)
    print("Available Rooms:", available_rooms_count)
    print("Occupancy Percentage:", round(occupancy_percentage, 2), "%")
def revenue_report():
    total_bookings, total_revenue = get_revenue_data()

    print("REVENUE REPORT ")
    print("Total Bookings:", total_bookings)
    print("Total Booking Revenue: Rs.", total_revenue)
def export_bookings():
    bookings = get_all_bookings_for_export()

    if not bookings:
        print("No bookings available to export")
        return
    with open("bookings_export.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Booking ID",
            "Guest Name",
            "Mobile Number",
            "Room Type",
            "Number of Guests",
            "Booking Date",
            "Check-in",
            "Check-out",
            "Room Number",
            "Status",
            "Total Payment"
        ])

        writer.writerows(bookings)

    print("Bookings exported successfully!")
    print("File saved as bookings_export.csv")
def guest_stay_history():
    mobile_number = input("Enter mobile number: ").strip()

    if not mobile_number.isdigit() or len(mobile_number) != 10:
        print("Invalid mobile number")
        return

    history = get_guest_history(mobile_number)

    if not history:
        print("No booking history found")
        return
    print("GUEST STAY HISTORY ")
    for record in history:
        print("\nBooking ID:", record[0])
        print("Room Type:", record[1])
        print("Number of Guests:", record[2])
        print("Check-in:", record[3])
        print("Check-out:", record[4])
        print("Room Number:", record[5])
        print("Status:", record[6])
        print("Total Payment: Rs.", record[7])
def start_menu():
    while True:
        print("""
        1. Search room availability
        2. Create booking
        3. Check-in
        4. Check-out
        5. Cancel booking
        6. View booking details
        7. Guest stay history
        8. Occupancy report
        9. Revenue report
        10. Export bookings to CSV
        11. Exit
        """)

        choice = int(input("Enter your choice: "))
       
        match choice:
            case 1:
                guest = take_guest_data()
                mobile_number = guest.mobile_number

                room_type, number_of_guest, checkin, checkout, room_number = available_rooms(guest)
                
               
                if room_type=="standard":
                    room = StandardRoom(
                            room_type,
                            number_of_guest,
                            checkin,
                            checkout,
                            mobile_number
                        )
                elif room_type=="deluxe":
                    room = DeluxeRoom(
                            room_type,
                            number_of_guest,
                            checkin,
                            checkout,
                            mobile_number
                        )
                else:
                    room = SuiteRoom(
                            room_type,
                            number_of_guest,
                            checkin,
                            checkout,
                            mobile_number
                        )
                print("Selected available room:", room_number)

            case 2:
                guest = take_guest_data()
                create_booking(guest)
            case 3:
                perform_checkin()
            case 4:perform_checkout()
            case 5:
                cancel_booking()
            case 6:
                view_booking_details()
            case 7:
                guest_stay_history()
            case 8:
                occupancy_report()

            case 9:
                revenue_report()

            case 10:
                export_bookings()

                
            case 11:
                raise SystemExit

            case _:
                print("Please enter a valid option")
