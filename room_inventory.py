import csv
import logging
from exceptions import RulesVoilationError
#Reading csv file
import csv
file=open("rooms.csv","r")
file=csv.DictReader(file)
rooms_data=[]
for i in file:
    rooms_data.append(i)
# print(rooms_data)
# [{'room_no': '101', 'room_type': 'Standard', 'floor': '1'}, 
# {'room_no': '102', 'room_type': 'Standard', 'floor': '1'},
#  {'room_no': '103', 'room_type': 'Standard', 'floor': '1'},
#  {'room_no': '106', 'room_type': 'Premium', 'floor': '1'}, 
# {'room_no': '104', 'room_type': 'Standard', 'floor': '1'},
#  {'room_no': '105', 'room_type': 'Standard', 'floor': '1'},
#  {'room_no': '201', 'room_type': 'Deluxe', 'floor': '2'}, 
# {'room_no': '202', 'room_type': 'Deluxe', 'floor': '2'}, {'room_no': '203', 'room_type': 'Deluxe', 'floor': '2'}, {'room_no': '204', 'room_type': 'Deluxe', 'floor': '2'}, {'room_no': '301', 'room_type': 'Suite', 'floor': '3'}, {'room_no': '302', 'room_type': 'Suite', 'floor': '3'}, {'room_no': '303', 'room_type': 'Suite', 'floor': '3'}]

#rooms data validation
room_number_seen=set()
valid_rooms=[]
def validate_rooms_data():
    for i in rooms_data:
        try:
            if i["room_no"].strip() in room_number_seen:
                raise RulesVoilationError("Room number cannot be duplicated")
            if not i["room_no"].strip().isdigit():
                raise RulesVoilationError("Room number should be a number")
            if i["room_no"].strip()=="":
                raise RulesVoilationError("Room number cannot be empty")
            if int(i["room_no"].strip())<=0:
                raise RulesVoilationError("Room number cannot be negative")
            if i["room_type"].strip()=="":
                raise RulesVoilationError("Room type cannot be empty")
            if i["room_type"].strip().lower() not in ["standard","deluxe","suite"]:
                raise RulesVoilationError("Room type should be standard,deluxe,suite")
            floor = i["floor"].strip()

            if floor == "":
                raise RulesVoilationError("Floor number cannot be empty")

            if not floor.isdigit():
                raise RulesVoilationError("Floor number should be a number")

            if int(floor) <= 0:
                raise RulesVoilationError("Floor number must be positive")
            valid_rooms.append(i)
            room_number_seen.add(i["room_no"])
        except RulesVoilationError as r:
            logging.error(str(r))
room_types = [
    {
        "room_type": "Standard",
        "base_rate": 2500,
        "max_guests": 2,
        "breakfast": False,
        "breakfast_charge": 350
    },
    {
        "room_type": "Deluxe",
        "base_rate": 4000,
        "max_guests": 3,
        "breakfast": True,
        "breakfast_charge": 0
    },
    {
        "room_type": "Suite",
        "base_rate": 7500,
        "max_guests": 4,
        "breakfast": True,
        "breakfast_charge": 0
    }
]
 