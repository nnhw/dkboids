import dronekit

class Boid(dronekit.Vehicle):
    def __init__(self, handler, id):
        super(Boid, self).__init__(handler)
        
        self._id = id

        self._buddy_1_id = 0
        self._buddy_2_id = 0

        self._buddy_1_location = dronekit.LocationGlobalRelative(0,0,0)
        self._buddy_2_location = dronekit.LocationGlobalRelative(0,0,0)
        # self._buddy_3_location = LocationGlobalRelative(0,0,0)  

    def parse_data(self, l_data):
        if l_data[0] == self._id:
            return
        elif self._buddy_1_id == 0:
            self._buddy_1_id = l_data[0]
        if l_data[0] == self._buddy_1_id:
            self._buddy_1_location.lat = l_data[2]
            self._buddy_1_location.lon = l_data[3]
            self._buddy_1_location.alt = l_data[4]
        elif self._buddy_2_id == 0:
            self._buddy_2_id = l_data[0]
        if l_data[0] == self._buddy_2_id:
            self._buddy_2_location.lat = l_data[2]
            self._buddy_2_location.lon = l_data[3]
            self._buddy_2_location.alt = l_data[4]

    def get_buddy_1(self):
        return self._buddy_1_id, self._buddy_1_location.lat, self._buddy_1_location.lon, self._buddy_1_location.alt

    def get_buddy_2(self):
        return self._buddy_2_id, self._buddy_2_location.lat, self._buddy_2_location.lon, self._buddy_2_location.alt
