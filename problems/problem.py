# problem.py

class FlightFinder:
    def __init__(self):

        self.flights = {
    'New York': {'Chicago': 22, 'London': 38, 'Los Angeles': 36, 'Toronto': 21},
    'Chicago': {'New York': 22, 'Denver': 23, 'Dallas': 24, 'Atlanta': 22},
    'Denver': {'Chicago': 23, 'San Francisco': 24, 'Seattle': 25, 'Phoenix': 23},
    'San Francisco': {'Denver': 24, 'Seattle': 22, 'Los Angeles': 21, 'Tokyo': 30},
    'London': {'New York': 38, 'Tokyo': 50},
    'Los Angeles': {'New York': 36, 'San Francisco': 21},
    'Toronto': {'New York': 21},
    'Dallas': {'Chicago': 24},
    'Atlanta': {'Chicago': 22},
    'Seattle': {'Denver': 25, 'San Francisco': 22},
    'Phoenix': {'Denver': 23},
    'Tokyo': {'San Francisco': 30, 'London': 50},
}



    def get_flights(self):
        return self.flights
