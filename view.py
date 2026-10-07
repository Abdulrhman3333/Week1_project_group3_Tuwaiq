
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
