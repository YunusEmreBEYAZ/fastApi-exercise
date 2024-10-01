class InconsistentDatesException(Exception):
    def __init__(self, message: str):
        self.message = message

class DatesException(Exception):
    def __init__(self, message: str):
        self.message = message