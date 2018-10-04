import dronekit
import scipy.spatial

class Boid(dronekit.Vehicle):
    def __init__(self, handler, id):
        super(Boid, self).__init__(handler)
        
        self._id = id

        self._buddy_1_id = 0
        self._buddy_2_id = 0

        self._buddy_1_location = dronekit.LocationGlobalRelative(0,0,0)
        self._buddy_2_location = dronekit.LocationGlobalRelative(0,0,0)
        # self._buddy_3_location = LocationGlobalRelative(0,0,0)  

        self._buddy_1_distance = 100
        self._buddy_2_distance = 100
        
    def _calculate_distance(self,l_location):
        me = (self.location.global_relative_frame.lat,self.location.global_relative_frame.lon,self.location.global_relative_frame.alt)
        target = (l_location[2], l_location[3], l_location[4])
        distance = scipy.spatial.distance.euclidean(me,target)
        # print(distance)
        return distance


    def analyze_data(self, l_data):
        if l_data[0] == self._id: # or l_data[0] == self._buddy_1_id or l_data[0] == self._buddy_2_id:
            return
        distance = self._calculate_distance(l_data)
        if distance < self._buddy_1_distance and l_data[0] !=self._buddy_1_id and l_data[0] !=self._buddy_2_id:
            self._buddy_1_id = l_data[0]
        elif distance < self._buddy_2_distance and l_data[0] !=self._buddy_1_id and l_data[0] !=self._buddy_2_id:
            self._buddy_2_id = l_data[0]
        self.update_buddy_data(l_data,distance)


    def update_buddy_data(self, l_data,distance):
        if l_data[0] == self._id:
            return
        elif l_data[0] == self._buddy_1_id:
            self._buddy_1_location.lat = l_data[2]
            self._buddy_1_location.lon = l_data[3]
            self._buddy_1_location.alt = l_data[4]
            self._buddy_1_distance = distance
        elif l_data[0] == self._buddy_2_id:
            self._buddy_2_location.lat = l_data[2]
            self._buddy_2_location.lon = l_data[3]
            self._buddy_2_location.alt = l_data[4]
            self._buddy_2_distance = distance

    def get_buddy_1(self):
        return self._buddy_1_id, self._buddy_1_location.lat, self._buddy_1_location.lon, self._buddy_1_location.alt, self._buddy_1_distance

    def get_buddy_2(self):
        return self._buddy_2_id, self._buddy_2_location.lat, self._buddy_2_location.lon, self._buddy_2_location.alt, self._buddy_2_distance
