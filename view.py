
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