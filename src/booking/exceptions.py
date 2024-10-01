class BookingStatusException(Exception):
 def __init__(self, message: str):
    self.message = message


class BookingNotFoundException(Exception):
 def __init__(self, message: str):
    self.message = message


class BookingException(Exception):
 def __init__(self, message: str):
    self.message = message
