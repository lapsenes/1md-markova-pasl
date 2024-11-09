import random
import numpy as np

layers = 4

class robot:
    def __init__(self, height, width, grid_occupancy, x=None, y=None, theta=None):

        self.occupancy = grid_occupancy
        initial_value = 1 / height * width / layers
        self.knowledge = np.full(grid_occupancy.shape, initial_value)
        self.x = x 
        self.y = y 

        if self.x is None or self.y is None or self.occupancy[self.x, self.y] == 1:
            while True:
                self.x = random.randint(0, self.occupancy.shape[0] - 1)
                self.y = random.randint(0, self.occupancy.shape[1] - 1)
                if self.occupancy[self.x, self.y] == 0:
                    break

        self.theta = theta if theta is not None else random.choice([0, 90, 180, 270]) # its right, up, left, down

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