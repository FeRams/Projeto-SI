import random
class Order():
    def __init__ (self):
        self.load = random.randint (0,100)
        self.travel_time = random.randint (150,300)
        self.urgency = random.randint (0,10)