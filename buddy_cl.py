from dronekit import LocationGlobalRelative
import sys


class Buddy(object):
    def __init__(self, id=0, flight_level=0, location=LocationGlobalRelative(0, 0, 0), distance=sys.maxint, groundspeed=0, poi=LocationGlobalRelative(0, 0, 0)):
        self.id = id
        self.flight_level = flight_level
        self.location = location
        self.distance = distance
        self.groundspeed = groundspeed
        self.poi = poi
