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
        print(f"Moving layer with direction={self.direction}")
        # Create a new knowledge array to store updated values
        new_knowledge = np.zeros(self.knowledge.shape)
        move_direction = directions[self.direction]
        
        # Probability constants from movement_model
        p_move = movement_model[0]  # 0.8 probability of moving
        p_stay = movement_model[1]  # 0.2 probability of staying

        for x in range(self.knowledge.shape[0]):
            for y in range(self.knowledge.shape[1]):
                if self.occupancy[y, x] == 1:  # Skip obstacles
                    continue

                # Calculate the position this cell could have come from
                prev_x = x - move_direction[0]
                prev_y = y - move_direction[1]

                # Current position's contribution (not moving)
                new_knowledge[y, x] += self.knowledge[y, x] * p_stay

                # Add contribution from previous position (if it exists and is not an obstacle)
                if (0 <= prev_x < self.knowledge.shape[0] and 
                    0 <= prev_y < self.knowledge.shape[1] and 
                    self.occupancy[prev_y, prev_x] == 0):
                    new_knowledge[y, x] += self.knowledge[prev_y, prev_x] * p_move

        # Update knowledge with new values
        self.knowledge = new_knowledge
        
        # Normalize the knowledge (similar to measurement normalization)
        total = np.sum(self.knowledge)
        if total > 0:
            self.knowledge /= total

    
    def measure(self, simulated_measurement):
        print(f"\nMeasuring for layer with direction={self.direction}, theta={self.theta}")
        print(f"Using direction vector: {directions[self.direction]}")
        # Create a new measurement array
        new_measurement_np = np.zeros((shared_data.grid_args["width"], shared_data.grid_args["height"]))
        max_possible_distance = max(shared_data.grid_args["width"], shared_data.grid_args["height"])
        real_distance = max(shared_data.grid_args["width"], shared_data.grid_args["height"])

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