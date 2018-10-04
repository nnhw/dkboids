import dronekit

class boid(Vehicle):
    def __init__(self, id):
        super(boid, self).__init__()
        
        self._id = id

        self._buddy_1 = self
        self._buddy_2 = self

        # self._buddy_1_location = LocationGlobalRelative(0,0,0)
        # self._buddy_2_location = LocationGlobalRelative(0,0,0)
        # self._buddy_3_location = LocationGlobalRelative(0,0,0)    