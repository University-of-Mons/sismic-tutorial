class Car:
    def __init__(self):
        self.speed = 0
        self.acceleration = 0
        self.deceleration = 0

    def evaluate_speed(self, mode):
        total_acceleration = 14 * (self.acceleration/100)
        deceleration_factor = 28 * (self.deceleration / 100)
        resistance = 0.015
        time_interval = 0.1

        match(mode):
            case 0:
                self.speed -= (self.speed * resistance * time_interval) 
            case 1:
                self.speed += (total_acceleration * time_interval) - (self.speed * resistance * time_interval)
            case 2:
                if self.speed >= 0:
                    self.speed -= (deceleration_factor * time_interval)
                    if self.speed < 0:
                        self.speed = 0

    def is_stationary(self):
        return self.speed == 0

    def get_speed(self):
        if self.speed - int(self.speed) >= 0.5:
            return int(self.speed) + 1
        else:
            return int(self.speed)

    def get_real_speed(self):
        return self.speed
    
    def set_acceleration(self, new_acceleration):
        self.acceleration = new_acceleration


    def set_deceleration(self, new_deceleration):
        self.deceleration = new_deceleration


    def compute_acceleration(self, target):
        delta = abs(target - self.speed)
        resistance = 0.015
        
        acceleration = delta * 3 + self.speed * resistance * 5

        if acceleration >= 100:
            acceleration = 99


        return acceleration


    def compute_deceleration(self, target): 
        delta = abs(target - self.speed)
        resistance = 0.015
        
        deceleration = delta * 8 + self.speed * resistance * 5
        
        if deceleration >= 100:
            deceleration = 99

        return deceleration
    
    
    def compute_target_speed(self, distance):
        reaction_time = 1.0
        deceleration = 5.0
        discriminant = reaction_time**2 + 2 * (deceleration) * distance

        if discriminant < 0:
            return 0 

        speed_mps = (-reaction_time + discriminant**0.5)

        speed_kph = speed_mps * 3.6

        return speed_kph




    def __str__(self):
        return f"Car : speed = {self.get_speed()}, real_speed = {self.get_real_speed()}"