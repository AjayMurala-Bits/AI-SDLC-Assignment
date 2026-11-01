"""Constants for the fixed movie-ticket booking domain."""

SHOW_IDS = ("S1", "S2")
SEAT_IDS = tuple(f"A{number}" for number in range(1, 11))
TICKET_PRICE_INR = 200
STORE_VERSION = 1
ACTIVE = "active"
CANCELLED = "cancelled"
BOOKING_STATUSES = (ACTIVE, CANCELLED)
