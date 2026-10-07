
import json
import os

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
PARKING_PRICE = 20


class Event:
    def __init__(self, name, price, location, time, date, parking_capacity=50, tickets_available=100):
        self.name = name
        self.price = price
        self.location = location
        self.time = time
        self.date = date
        self.parking_capacity = parking_capacity
        self.parking_reserved = 0
        self.tickets_available = tickets_available
        self.tickets_total = tickets_available  # new: lets the UI draw a "sold" progress bar

    def parking_available(self):
        return self.parking_capacity - self.parking_reserved


class CartItem:
    def __init__(self, event, tickets=1):
        self.event = event
        self.tickets = tickets

    def total_price(self):
        return self.event.price * self.tickets


class ParkingReservation:
    def __init__(self, event, spots):
        self.event = event
        self.spots = spots

    def total_price(self):
        return self.spots * PARKING_PRICE


def _find(items, event):
    return next((i for i in items if i.event is event), None)


def _merge(items, event, amount, kind):
    item = _find(items, event)
    if item is None:
        items.append(CartItem(event, amount) if kind == "ticket" else ParkingReservation(event, amount))
    elif kind == "ticket":
        item.tickets += amount
    else:
        item.spots += amount
class Store:
    """Holds all state. The UI creates ONE of these and keeps it in st.session_state."""

    def __init__(self):
        self.events = [
            Event("Boulevard World", 250, "Riyadh", "8:00 PM", "2026-10-10", tickets_available=100),
            Event("Comedy Show", 100, "Riyadh", "9:00 PM", "2026-10-15", tickets_available=60),
            Event("Kingdom Arena Boxing Night", 80, "Riyadh", "7:30 PM", "2026-10-20", tickets_available=80),
            Event("Winter Wonderland", 200, "Riyadh", "6:00 PM", "2026-10-25", tickets_available=40),
        ]
        self.cart = []
        self.parking_cart = []
        self.my_tickets = []
        self.parking_reservations = []
        self.load()

    def cart_total(self):
        return sum(i.total_price() for i in self.cart + self.parking_cart)

    def add_ticket(self, event):
        item = _find(self.cart, event)
        in_cart = item.tickets if item else 0
        if in_cart + 1 > event.tickets_available:
            return False, f"No more tickets left for {event.name}."
        _merge(self.cart, event, 1, "ticket")
        return True, f"{event.name} added to your cart."

    def change_tickets(self, event, delta):
        item = _find(self.cart, event)
        if item is None:
            return False, "That ticket is not in your cart."
        new = item.tickets + delta
        if new <= 0:
            self.cart.remove(item)
            return True, f"{event.name} removed from your cart."
        if new > event.tickets_available:
            return False, f"Only {event.tickets_available} tickets left for {event.name}."
        item.tickets = new
        return True, "Quantity updated."

    def remove_ticket(self, event):
        item = _find(self.cart, event)
        if item:
            self.cart.remove(item)
        return True, f"{event.name} removed from your cart."

    # ---------- cart: parking ----------
    def add_parking(self, event, spots):
        item = _find(self.parking_cart, event)
        in_cart = item.spots if item else 0
        if spots < 1 or in_cart + spots > event.parking_available():
            return False, f"Not enough parking left for {event.name}."
        _merge(self.parking_cart, event, spots, "parking")
        return True, f"{spots} parking spot(s) for {event.name} added to your cart."

    def remove_parking(self, event):
        item = _find(self.parking_cart, event)
        if item:
            self.parking_cart.remove(item)
        return True, f"Parking for {event.name} removed from your cart."
