import random
import numpy as np

layers = 4

class robot:
    def __init__(self, height, width, grid_occupancy, theta_dict, x=None, y=None):

        self.occupancy = grid_occupancy
        initial_value = 1 / height * width / layers
        self.knowledge = np.full(grid_occupancy.shape, initial_value)
        self.num_robots = len(self.theta_dict)
        self.robots = []
        self.x = x 
        self.y = y 

        for direction, theta in self.theta_dict.items():
            if len(self.robots) < self.num_robots:
                if self.x is None or self.y is None or self.occupancy[self.x, self.y] == 1:
                    while True:
                        self.x = random.randint(0, self.occupancy.shape[0] - 1)
                        self.y = random.randint(0, self.occupancy.shape[1] - 1)
                        if self.occupancy[self.x, self.y] == 0:
                            print("random location allocated")
                            break
                self.robots.append({"x": x, "y": y, "theta": theta, "direction": direction})



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