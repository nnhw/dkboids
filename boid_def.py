import dronekit
import scipy.spatial
from osgeo import gdal

class Boid(dronekit.Vehicle):
    def __init__(self, handler, id):
        super(Boid, self).__init__(handler)
        
        self._id = id
        self._flight_level = 0

        #yes, it is better to have a class (buddy), but it's OK for now
        self._buddy_id = [0,0,0]
        self._buddy_location = [dronekit.LocationGlobalRelative(0,0,0),dronekit.LocationGlobalRelative(0,0,0),dronekit.LocationGlobalRelative(0,0,0)]
        self._buddy_distance = [100,100,100]
        self._buddy_flight_level = [0,0,0]

    def _calculate_distance_coarse(self,l_location):
        me = (self.location.global_relative_frame.lat,self.location.global_relative_frame.lon,self.location.global_relative_frame.alt)
        target = (l_location[2], l_location[3], l_location[4])
        distance = scipy.spatial.distance.euclidean(me,target)
        # print(distance)
        return distance

    def _calculate_distance_fine(self, l_location):
        return 0

    def analyze_data(self, l_data):
        if l_data[0] == self._id: 
            return
        distance = self._calculate_distance_coarse(l_data)

        new_id = l_data[0] != self._buddy_id[0] and l_data[0] != self._buddy_id[1] and l_data[0] != self._buddy_id[2]

        for n in range(len(self._buddy_distance)):
            if distance < self._buddy_distance[n] and new_id is True :
                self._buddy_id[n] = l_data[0]
        self.update_buddy_data(l_data,distance)


    def update_buddy_data(self, l_data,distance):
        if l_data[0] == self._id:
            return
        elif l_data[0] == self._buddy_id[0]:
            self._buddy_flight_level[0] = 0
            self._buddy_location[0].lat = l_data[2]
            self._buddy_location[0].lon = l_data[3]
            self._buddy_location[0].alt = l_data[4]
            self._buddy_distance[0] = distance
        elif l_data[0] == self._buddy_id[1]:
            self._buddy_flight_level[0] = 0
            self._buddy_location[1].lat = l_data[2]
            self._buddy_location[1].lon = l_data[3]
            self._buddy_location[1].alt = l_data[4]
            self._buddy_distance[1] = distance
        elif l_data[0] == self._buddy_id[2]:
            self._buddy_flight_level[0] = 0
            self._buddy_location[2].lat = l_data[2]
            self._buddy_location[2].lon = l_data[3]
            self._buddy_location[2].alt = l_data[4]
            self._buddy_distance[2] = distance

    def get_buddy(self,n):
        return self._buddy_id[n-1],self._buddy_flight_level[n-1], self._buddy_location[n-1].lat, self._buddy_location[n-1].lon, self._buddy_location[n-1].alt, self._buddy_distance[n-1]

