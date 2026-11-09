#creating log file
import logging
logging.basicConfig(filename="app.log",
                    level=logging.ERROR,
                    format="%(asctime)s-%(levelname)s-%(message)s")


from database import initialize_database
from room_inventory import validate_rooms_data
from menu import start_menu

def main():
    initialize_database()
    validate_rooms_data()
    start_menu()
if __name__=="__main__":
    main()
    