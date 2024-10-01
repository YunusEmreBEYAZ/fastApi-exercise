import enum


class BookingStatusEnum(enum.Enum):
    draft = "draft"
    canceled = "canceled"
    confirmed = "confirmed"
