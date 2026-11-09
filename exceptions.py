#Exceptions
class RoomUnavailable(Exception):
    pass
class InvalidDate(Exception):
    pass
class InvalidStatusChange(Exception):
    pass
class BookingNotFound(Exception):
    pass
class RulesVoilationError(Exception):
    pass