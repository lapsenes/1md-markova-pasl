import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk
from src.layer import *
import src.shared_data as shared_data
import matplotlib.colors as mcolors
import logging

logging.basicConfig(level=logging.INFO)

def rand_grid(width, height):
    logging.info("Generating random grid.")
    occupancy_array = np.zeros((width, height), dtype=int)
    indices = np.random.choice(width*height, 20, replace=False)
    occupancy_array[np.unravel_index(indices, (width, height))] = 1
    return occupancy_array

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

def make_grid(width, height, layers, theta_dict, grid_occupancy):
    logging.info("Creating grid visualization.")
    if grid_occupancy is None:
        shared_data.grid_args["grid_occupancy"] = rand_grid(shared_data.grid_args["width"], shared_data.grid_args["height"])
        grid_occupancy = shared_data.grid_args["grid_occupancy"]

    # Create a custom red-to-green colormap
    colors = [(1, 0, 0, 0.3), (0, 1, 0, 0.3)]  # Red to Green
    cmap = mcolors.LinearSegmentedColormap.from_list("RedGreen", colors, N=256)
    
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    axes = axes.flatten()

    # Create subplot mapping for clockwise arrangement
    direction_to_subplot = {
        'up': 1,     # top left
        'right': 0,  # top right
        'down': 3,   # bottom left
        'left': 2    # bottom right
    }

    if layers is not None:
        # Find the global min and max knowledge values across all layers
        min_val = min(layer.knowledge.min() for layer in layers)
        max_val = max(layer.knowledge.max() for layer in layers)

        # Sort layers by their intended subplot position
        sorted_layers = sorted(layers, key=lambda x: direction_to_subplot[x.direction])
        
        # Iterate over each subplot and layer
        for ax, layer in zip(axes, sorted_layers):
            # Display the grid
            ax.imshow(grid_occupancy, cmap='gray_r', origin='upper', extent=(0, width, height, 0))
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_aspect('equal')
            ax.grid(True)
            ax.set_xticks(np.arange(0, width + 1, 1))
            ax.set_yticks(np.arange(0, height + 1, 1))
            ax.tick_params(which='both', length=0)

            # Add headline for each graph
            ax.set_title(f"Layer Direction: {layer.direction}")

            knowledge = layer.knowledge

            for i in range(knowledge.shape[0]):
                for j in range(knowledge.shape[1]):
                    # Skip if the grid_occupancy cell is 1 (occupied)
                    if grid_occupancy[i, j] == 1:
                        continue

                    if knowledge[i, j] != 0:
                        # Normalize the knowledge value to the range [0, 1] for colormap
                        norm_value = (knowledge[i, j] - min_val) / (max_val - min_val)
                        color = cmap(norm_value)
                        ax.add_patch(plt.Rectangle((j, i), 1, 1, color=color))
                        ax.text(j + 0.5, i + 0.5, f'{knowledge[i, j]:.2f}', ha='center', va='center', color='black', fontsize=5)

            # Plot the robot position and orientation if it is the right layer
            if shared_data.grid_args["rot"] == layer.theta:
                center_x = shared_data.grid_args['x'] - 0.5
                center_y = shared_data.grid_args['y'] - 0.5
                ax.plot(center_x, center_y, marker='o', color='red', markersize=6)
                theta = theta_dict[layer.direction]
                ax.arrow(center_x, center_y, 0.5 * np.cos(np.radians(theta)), 
                            0.5 * np.sin(np.radians(theta)), head_width=0.2, head_length=0.3, 
                            fc='blue', ec='blue')
                
    else:
        for idx, ax in enumerate(axes):
            # Display the grid
            ax.imshow(grid_occupancy.reshape(height, width), cmap='gray_r', origin='upper', extent=(0, width, height, 0))
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_aspect('equal')
            ax.grid(True)
            ax.set_xticks(np.arange(0, width + 1, 1))
            ax.set_yticks(np.arange(0, height + 1, 1))
            ax.tick_params(which='both', length=0)

    plt.tight_layout()
    if layers is not None:
        print("Layer directions:", [layer.direction for layer in layers])
        print("Axes order:", [i for i in range(len(axes))])
    logging.info("Grid visualization created.")
    return fig

def visualize_grid(width, height, theta_dict, grid_occupancy, widgets, layers=None):
    global canvas
    plt.close('all')
    fig = make_grid(shared_data.grid_args["width"], shared_data.grid_args["height"], layers, shared_data.grid_args["theta_dict"], shared_data.grid_args["grid_occupancy"])
    if 'canvas' in globals() and canvas is not None:
        canvas.get_tk_widget().destroy()
    canvas = FigureCanvasTkAgg(fig, master=widgets['action_frame'])
    canvas.draw()
    canvas.get_tk_widget().pack()
    logging.info("Grid visualization displayed.")

def export_grid():
    logging.info("Exporting grid state.")
    grid_state = []
    grid_array = np.array(grid_state)

def ask_location(window, width, height, location_entries, widgets, grid_occupancy, theta_dict):
    if "x_loc_entry" not in location_entries and "y_loc_entry" not in location_entries:
        widgets['x_loc_label'] = tk.Label(master=widgets['side_frame'], text="robota sākuma pozīcija x")
        widgets['x_loc_entry'] = tk.Entry(master=widgets['side_frame'])
        widgets['y_loc_label'] = tk.Label(master=widgets['side_frame'], text="robota sākuma pozīcija y")
        widgets['y_loc_entry'] = tk.Entry(master=widgets['side_frame'])
        widgets['rot_label'] = tk.Label(master=widgets['side_frame'], text="robota sākuma pagrieziens")
        widgets['rot_entry'] = tk.Entry(master=widgets['side_frame'])
        widgets['submit_location_button'] = tk.Button(master=widgets['side_frame'], text="Inicializēt layeru", width=15, height=2)

        widgets['x_loc_label'].pack()
        widgets['x_loc_entry'].pack()
        widgets['y_loc_label'].pack()
        widgets['y_loc_entry'].pack()
        widgets['rot_label'].pack()
        widgets['rot_entry'].pack()
        widgets['submit_location_button'].pack()

        location_entries["x_loc_entry"] = widgets['x_loc_entry']
        location_entries["y_loc_entry"] = widgets['y_loc_entry']
        location_entries["rot_entry"] = widgets['rot_entry']
        logging.info("Entry widgets created.")
        widgets['submit_location_button'].bind("<Button-1>", lambda event: initialize_layer(window, shared_data.grid_args["width"], shared_data.grid_args["height"], shared_data.grid_args["theta_dict"], shared_data.grid_args["grid_occupancy"], shared_data.grid_args["widgets"]))
        
    else:
        location_entries["x_loc_entry"].delete(0, tk.END)
        location_entries["y_loc_entry"].delete(0, tk.END)
        logging.info("Entry widgets already exist, clearing content.")


def initialize_layer(window, height, width, theta_dict, grid_occupancy, widgets):
    try:
        # Commented out the original code for setting the robot's initial position and rotation
        # shared_data.grid_args["x"] = int(widgets['x_loc_entry'].get())
        # shared_data.grid_args["y"] = int(widgets['y_loc_entry'].get())
        # shared_data.grid_args["rot"] = int(widgets['rot_entry'].get())

        # Overwrite the robot's initial position and rotation
        shared_data.grid_args["x"] = 3
        shared_data.grid_args["y"] = 3
        shared_data.grid_args["rot"] = 0

        # Commented out the original code for generating a random grid
        # if shared_data.grid_args["grid_occupancy"] is None:
        #     shared_data.grid_args["grid_occupancy"] = rand_grid(shared_data.grid_args["width"], shared_data.grid_args["height"])

        # Use a more random occupancy array that is not occupied in (3, 3)
        np.random.seed(42)  # For reproducibility
        shared_data.grid_args["grid_occupancy"] = np.random.choice([0, 1], size=(12, 12), p=[0.8, 0.2])
        shared_data.grid_args["grid_occupancy"][3, 3] = 0  # Ensure (3, 3) is not occupied
        grid_occupancy = shared_data.grid_args["grid_occupancy"]

        shared_data.grid_args["widgets"]['x_loc_entry'].config(state='disabled')
        shared_data.grid_args["widgets"]['y_loc_entry'].config(state='disabled')
        shared_data.grid_args["widgets"]['submit_location_button'].config(state='disabled')

        layers = []
        print("Initializing layers in order:")
        for direction, theta in theta_dict.items():
            print(f"Creating layer: direction={direction}, theta={theta}")
            new_layer = layer(shared_data.grid_args["width"], shared_data.grid_args["height"], theta, direction, shared_data.grid_args["grid_occupancy"])
            layers.append(new_layer)
        visualize_grid(shared_data.grid_args["width"], shared_data.grid_args["height"], shared_data.grid_args["theta_dict"], shared_data.grid_args["grid_occupancy"], shared_data.grid_args["widgets"], layers)
        setup_screen(shared_data.grid_args["widgets"], layers)
        logging.info("Layer initialized.")
    except ValueError as e:
        widgets['error_label'].config(text=f"Error: {e}")
        logging.error(f"Error initializing layer: {e}")

def setup_screen(widgets, layers):
    # Add measurement value entry
    widgets['measurement_label'] = tk.Label(master=widgets['side_frame'], text="Mērījuma vērtība:")
    widgets['measurement_entry'] = tk.Entry(master=widgets['side_frame'])
    widgets['measurement_label'].pack()
    widgets['measurement_entry'].pack()

    widgets['submit_measure_button'] = tk.Button(master=widgets['side_frame'], text="Veikt mērījumu", width=15, height=2)
    widgets['submit_mov_button'] = tk.Button(master=widgets['side_frame'], text="Veikt kustību 1 soli", width=15, height=2)

    widgets['submit_measure_button'].pack()
    widgets['submit_mov_button'].pack()

    widgets['submit_mov_button'].bind("<Button-1>", lambda event: movement(layers))
    widgets['submit_measure_button'].bind("<Button-1>", lambda event: measurement(layers, widgets))
    logging.info("Screen setup with movement and measurement buttons.")

def movement(layers):
    logging.info("Movement function called.")
    
    # Get current robot orientation and update position accordingly
    current_rot = shared_data.grid_args["rot"]
    # Find the layer that matches current rotation
    current_layer = next(layer for layer in layers if layer.theta == current_rot)
    move_direction = directions[current_layer.direction]
    
    # Calculate new position
    new_x = shared_data.grid_args["x"] + move_direction[0]
    new_y = shared_data.grid_args["y"] + move_direction[1]
    
    # Check if new position is valid (within bounds and not occupied)
    if (0 <= new_x < shared_data.grid_args["width"] and 
        0 <= new_y < shared_data.grid_args["height"] and 
        shared_data.grid_args["grid_occupancy"][new_y, new_x] == 0):
        
        # Update robot position
        shared_data.grid_args["x"] = new_x
        shared_data.grid_args["y"] = new_y
        logging.info(f"Robot moved to position ({new_x}, {new_y})")
    else:
        logging.info("Robot cannot move - blocked by obstacle or boundary")
    
    # Update knowledge for all layers
    for layer in layers:
        layer.move()
    normalize(layers)

def measurement(layers, widgets):
    try:
        measurement_value = int(widgets['measurement_entry'].get())
        logging.info(f"Measurement function called with value: {measurement_value}")
        for layer in layers:
            layer.measure(measurement_value)
        normalize(layers)
    except ValueError:
        logging.error("Invalid measurement value entered")

def normalize(layers):
    logging.info("Normalizing knowledge across layers.")
    # Sum the knowledge across all layers
    total_sum = np.sum([layer.knowledge for layer in layers])
    # Avoid division by zero
    if total_sum != 0:
        for layer in layers:
            # Normalize each layer's knowledge
            layer.knowledge /= total_sum
            # Print the normalized knowledge array
            logging.info(f"Normalized knowledge for layer with direction {layer.direction}:")
            logging.info(layer.knowledge)
    new_total_sum = np.sum([layer.knowledge for layer in layers])
    logging.info(f"New total sum: {new_total_sum}")
    # and then re-visualize
    visualize_grid(shared_data.grid_args["width"], shared_data.grid_args["height"], shared_data.grid_args["theta_dict"], shared_data.grid_args["grid_occupancy"], shared_data.grid_args["widgets"], layers)
    logging.info("Normalized knowledge.")