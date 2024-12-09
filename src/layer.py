import random
import numpy as np
import src.shared_data as shared_data

layers = 4
directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]
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
        new_measurement_np = np.zeros((layers, shared_data.grid_args["width"], shared_data.grid_args["height"]))
        simulated_measurement = np.random.randint(1, 9)
        max_possible_distance = max(shared_data.grid_args["width"], shared_data.grid_args["height"])  # Maximum possible distance in the grid

        for layer, (dx, dy) in zip(layers, directions):
            for x in range(shared_data.grid_args["width"]):
                for y in range(shared_data.grid_args["height"]):
                    # Skip cells with obstacles
                    if shared_data.grid_args["grid_occupancy"][x, y] == 1:
                        continue

            for step in range(1, real_distance + 1):  # Step through possible distances
                nx, ny = x + step * dx, y + step * dy

                # Check if we've reached the grid boundary
                if nx < 0 or nx >= shared_data.grid_args["width"] or ny < 0 or ny >= shared_data.grid_args["height"]:
                    real_distance = step
                    break
                # Check if an obstacle is found
                if shared_data.grid_args["grid_occupancy"][nx, ny] == 1:
                    real_distance = step
                    break
                    
            # Assign probabilities based on simulated and real distances
            if simulated_measurement == real_distance:
                new_measurement_np[layer, x, y] = 0.85
            elif abs(simulated_measurement - real_distance) == 1:
                new_measurement_np[layer, x, y] = 0.1
            else:
                new_measurement_np[layer, x, y] = 0.05
        
        return new_measurement_np
    
    def normalize():
        raise NotImplemented
    
    def print_knowledge():
        raise NotImplemented