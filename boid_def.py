import dronekit
import geopy.distance
import math
import guidance
from geographiclib.geodesic import Geodesic


class Boid(dronekit.Vehicle):
    def __init__(self, handler, id):
        super(Boid, self).__init__(handler)

        self._id = id
        self._flight_level = 0
        self._poi = dronekit.LocationGlobalRelative(0, 0, 0)
        self._groundspeed = 0

        self._global_poi = dronekit.LocationGlobalRelative(0, 0, 0)

        self._follow_target_id = 0

        # yes, it is better to have a class (buddy), but it's OK for now
        self._buddy_id = [0, 0, 0]
        self._buddy_location = [dronekit.LocationGlobalRelative(
            0, 0, 0), dronekit.LocationGlobalRelative(0, 0, 0), dronekit.LocationGlobalRelative(0, 0, 0)]
        self._buddy_distance = [100000, 100000, 100000]
        self._buddy_groundspeed = [0, 0, 0]

        self._buddy_flight_level = [0, 0, 0]
        self._buddy_poi = [dronekit.LocationGlobalRelative(0, 0, 0), dronekit.LocationGlobalRelative(
            0, 0, 0), dronekit.LocationGlobalRelative(0, 0, 0)]

    def _calculate_distance_fine(self, lat, lon, alt):
        me = (self.location.global_relative_frame.lat,
              self.location.global_relative_frame.lon)
        target = (lat, lon)
        horizontal_distance = geopy.distance.geodesic(me, target).m
        vertical_distance = abs(self.location.global_relative_frame.alt - alt)
        distance = math.sqrt(pow(horizontal_distance, 2) +
                             pow(vertical_distance, 2))
        return distance, horizontal_distance, vertical_distance

    def _calculate_angle(self, l_location):
        me = (self.location.global_relative_frame.lat,
              self.location.global_relative_frame.lon)
        target = (l_location[0], l_location[1])
        result = Geodesic.WGS84.Inverse(me[0], me[1], target[0], target[1])
        azimuth = result['azi1']
        if azimuth > 0:
            angle = azimuth
        elif azimuth < 0:
            angle = 360 + azimuth
        print("azi1 is ", azimuth)
        print("angle is ", angle)
        return angle

    def analyze_data(self, l_data):
        if l_data[0] == self._id:
            return

        if l_data[0] == 200:
            self._global_poi = dronekit.LocationGlobalRelative(
                l_data[3], l_data[4], l_data[5])
            self.mode = dronekit.VehicleMode("GUIDED")
            print("new poi set")
            return

        if self._follow_target_id != 0:
            if l_data[0] == self._follow_target_id:
                self._global_poi = dronekit.LocationGlobalRelative(
                    l_data[3], l_data[4], l_data[5])

        distance = self._calculate_distance_fine(
            l_data[3], l_data[4], l_data[5])[0]
        new_id = l_data[0] != self._buddy_id[0] and l_data[0] != self._buddy_id[1] and l_data[0] != self._buddy_id[2]
        for n in range(len(self._buddy_distance)):
            if distance < self._buddy_distance[n] and new_id is True:
                self._buddy_id[n] = l_data[0]
        self.update_buddy_data(l_data, distance)

    def update_buddy_data(self, l_data, distance):
        if l_data[0] == self._id:
            return
        elif l_data[0] == self._buddy_id[0]:
            self._buddy_flight_level[0] = l_data[2]
            self._buddy_location[0].lat = l_data[3]
            self._buddy_location[0].lon = l_data[4]
            self._buddy_location[0].alt = l_data[5]
            self._buddy_groundspeed[0] = l_data[6]
            self._buddy_distance[0] = distance
        elif l_data[0] == self._buddy_id[1]:
            self._buddy_flight_level[1] = l_data[2]
            self._buddy_location[1].lat = l_data[3]
            self._buddy_location[1].lon = l_data[4]
            self._buddy_location[1].alt = l_data[5]
            self._buddy_groundspeed[1] = l_data[6]
            self._buddy_distance[1] = distance
        elif l_data[0] == self._buddy_id[2]:
            self._buddy_flight_level[2] = l_data[2]
            self._buddy_location[2].lat = l_data[3]
            self._buddy_location[2].lon = l_data[4]
            self._buddy_location[2].alt = l_data[5]
            self._buddy_groundspeed[2] = l_data[6]
            self._buddy_distance[2] = distance

    def get_buddy(self, n):
        return self._buddy_id[n-1], self._buddy_flight_level[n-1], self._buddy_location[n-1].lat, self._buddy_location[n-1].lon, self._buddy_location[n-1].alt, self._buddy_distance[n-1], self._buddy_groundspeed[n-1]

    def separation(self):
        NotImplemented

    def alignment(self):
        buddies_average_groundspeed = 0
        for speed in self._buddy_groundspeed:
            buddies_average_groundspeed += speed
        buddies_average_groundspeed = buddies_average_groundspeed/3
        return buddies_average_groundspeed

    def cohesion(self):
        lat_summ = 0
        lon_summ = 0
        alt_summ = 0
        for loc in self._buddy_location:
            lat_summ += loc.lat
            lon_summ += loc.lon
            alt_summ += loc.alt
        lat_mean = lat_summ/3
        lon_mean = lon_summ/3
        alt_mean = alt_summ/3
        buddies_center = dronekit.LocationGlobalRelative(
            lat_mean, lon_mean, alt_mean)
        distance = self._calculate_distance_fine(
            buddies_center.lat, buddies_center.lon, buddies_center.alt)
        return buddies_center, distance

    def implement_corrections(self):
        cohesion_point = self.cohesion()[0]
        cohesion_distance = self.cohesion()[1]

        correction_poi = cohesion_point

        if correction_poi.lat == 0:
            self._poi = self._global_poi
        else:
            self._poi.lat = (self._global_poi.lat + correction_poi.lat)/2
            self._poi.lon = (self._global_poi.lon + correction_poi.lon)/2
            self._poi.alt = self._flight_level

        alignment_speed = self.alignment()
        if alignment_speed != 0:
            self.groundspeed = alignment_speed

    def goto_poi(self):
        self.simple_goto(self._poi)
