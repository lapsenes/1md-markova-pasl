import random
import numpy as np
import src.shared_data as shared_data

layers = 4
directions = {
    'right': [1, 0],
    'up': [0, -1],
    'left': [-1, 0],
    'down': [0, 1]
}
"""
pārvietojuma modelis:
0.8: plānotā kustība notiek
0.2: layers paliek uz vietas
"""
movement_model = [0.8, 0.2]
"""
novērojumu modelis:
attālums līdz tuvākajam šķērslim pagrieziena virzienā
modelis:
0.8: korekts mērījums
0.15: nekorekts mērījums -/+ 1 solis
0.05: jebkurš cits nekorekts mērījums

"""
measurement_model = [0.8, 0.15, 0.05]

class layer:
    def __init__(self, width, height, theta, direction, grid_occupancy):
        self.occupancy = grid_occupancy
        initial_value = 1 / (height * width - np.count_nonzero(self.occupancy == 1)) / layers
        self.knowledge = np.zeros(grid_occupancy.shape) # last calculated knowledge
        self.measurement = np.zeros(grid_occupancy.shape) # current measurement
        self.knowledge[self.occupancy != 1] = initial_value
        self.num_layers = layers
        self.theta = theta
        self.direction = direction

    
    def __iter__(self):
        return iter(self.basics)

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

                # updated_measurements = np.copy(self.measurement)
        # for layer, direction in zip(layers, directions):
        #     dx, dy = direction
        #     for x in range(shared_data.grid_args["width"]):
        #         for y in range(shared_data.grid_args["height"]):
        #             # Skip cells with obstacles
        #             if shared_data.grid_args["grid_occupancy"][x, y] == 1:
        #                 continue
        #             # Determine the previous cell position based on the layer direction
        #             prev_x, prev_y = x - dx, y - dy
        #             # Check if the previous cell is out of bounds
        #             if prev_x < 0 or prev_x >= shared_data.grid_args["width"] or \
        #             prev_y < 0 or prev_y >= shared_data.grid_args["height"]:
        #                 updated_measurements[x, y] = measurement_model[0] * self.measurement[x, y]
        #                 continue

        #             # Check if the previous cell is occupied
        #             if shared_data.grid_args["grid_occupancy"][prev_x, prev_y] == 1:
        #                 updated_measurements[x, y] = x_factor * self.measurement[x, y]
        #                 continue

        #             # Apply the full formula if the previous cell is not occupied
        #             prev_value = self.measurement[prev_x, prev_y]
        #             current_value = self.measurement[x, y]
        #             updated_measurements[x, y] = x_factor * prev_value + y_factor * current_value

        # # Update the measurement attribute with the new values
        # self.measurement = updated_measurements
    
    def measure(self):
        print(f"\nMeasuring for layer with direction={self.direction}, theta={self.theta}")
        print(f"Using direction vector: {directions[self.direction]}")
        # Create a new measurement array
        new_measurement_np = np.zeros((shared_data.grid_args["width"], shared_data.grid_args["height"]))
        simulated_measurement = 7 # np.random.randint(1, 9)
        max_possible_distance = max(shared_data.grid_args["width"], shared_data.grid_args["height"])  # Maximum possible distance in the grid
        real_distance = max(shared_data.grid_args["width"], shared_data.grid_args["height"])
        # adapted_occupancy = np.flipud(shared_data.grid_args["grid_occupancy"])  # Invert the rows of the occupancy grid

        for x in range(shared_data.grid_args["width"]):
            for y in range(shared_data.grid_args["height"]):
                # Skip cells with obstacles
                if shared_data.grid_args["grid_occupancy"][y, x] == 1:
                    continue
                direction_values = directions[self.direction]  # Get the direction values from the dictionary
                for step in range(1, max_possible_distance + 1):  # Step through possible distances
                    
                    nx, ny = x + step * direction_values[0], y + step * direction_values[1]

                    # Check if we've reached the grid boundary
                    if nx < 0 or nx >= shared_data.grid_args["width"] or ny < 0 or ny >= shared_data.grid_args["height"]:
                        real_distance = step
                        break
                    # Check if an obstacle is found
                    if shared_data.grid_args["grid_occupancy"][ny, nx] == 1:
                        real_distance = step
                        break

                # Assign probabilities based on simulated and real distances
                if simulated_measurement == real_distance:
                    self.measurement[y, x] = 0.85
                elif abs(simulated_measurement - real_distance) == 1:
                    self.measurement[y, x] = 0.1
                else:
                    self.measurement[y, x] = 0.05

        # Perform element-wise multiplication and update knowledge
        self.knowledge *= self.measurement

    
    def print_knowledge():
        raise NotImplemented