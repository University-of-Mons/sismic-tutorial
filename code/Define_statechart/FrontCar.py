
class FrontCar:

    def __init__(self, lower_bound, upper_bound):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.distanceTo = upper_bound
        self.accelerating = False

    def update_distance(self):
        if not self.accelerating:
            self.distanceTo = self.distanceTo - 0.5
            if max(self.distanceTo, self.lower_bound) == self.lower_bound:
                self.distanceTo = self.lower_bound
                self.accelerating = True
        else:
            self.distanceTo = self.distanceTo + 0.5
            if min(self.distanceTo, self.upper_bound) == self.upper_bound:
                self.distanceTo = self.upper_bound
                self.accelerating = False


    def distance_to(self):
        return int(self.distanceTo)