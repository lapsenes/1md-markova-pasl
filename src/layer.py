import random
import numpy as np
import src.shared_data as shared_data

layers = 4
"""
pārvietojuma modelis:
0.8: plānotā kustība notiek
0.2: layers paliek uz vietas
"""

"""
novērojumu modelis:
attālums līdz tuvākajam šķērslim pagrieziena virzienā
modelis:
0.8: korekts mērījums
0.15: nekorekts mērījums -/+ 1 solis
0.05: jebkurš cits nekorekts mērījums

"""

class layer:
    def __init__(self, width, height, theta_dict, grid_occupancy):
        self.occupancy = grid_occupancy
        self.theta_dict = theta_dict
        initial_value = 1 / (height * width - np.count_nonzero(self.occupancy == 1)) / layers
        self.knowledge = np.zeros(grid_occupancy.shape)
        self.knowledge[self.occupancy != 1] = initial_value
        self.num_layers = len(self.theta_dict)
        self.layers = []

        for direction, theta in self.theta_dict.items():
            if len(self.layers) < self.num_layers:
                self.layers.append({"theta": theta, "direction": direction, "knowledge": self.knowledge})

    
    def __iter__(self):
        return iter(self.layers)

    def draw_on_map(self):
        raise NotImplemented

    def move(self):
        movement_probability = 0.8
        moves = {
            'right': (self.x + 1, self.y),
            'up': (self.x, self.y + 1),
            'left': (self.x - 1, self.y),
            'down': (self.x, self.y - 1)
        }

        for direction, (new_x, new_y) in moves.items():
            # is the move in bounds of the grid
            if 0 <= new_x < self.occupancy.shape[0] and 0 <= new_y < self.occupancy.shape[1]:
                # is the next spot free
                if self.occupancy[new_x, new_y] == 0:
                    
                    if random.random() < movement_probability:
                        print(f"Moving {direction} to ({new_x}, {new_y})")
                        self.x, self.y = new_x, new_y
                        break
                    else:
                        print(f"Attempted to move {direction}, but failed due to probability")
                else:
                    print(f"Cannot move {direction}, cell ({new_x}, {new_y}) is occupied")
            else:
                print(f"Cannot move {direction}, out of bounds")
    
    def measure():
        raise NotImplemented
    
    def normalize():
        raise NotImplemented
    
    def print_knowledge():
        raise NotImplemented