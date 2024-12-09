import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk
from src.layer import *
import src.shared_data as shared_data
import matplotlib.colors as mcolors


def rand_grid(width, height):
    occupancy_array = np.zeros((width, height), dtype=int)
    indices = np.random.choice(width*height, 20, replace=False)
    occupancy_array[np.unravel_index(indices, (width, height))] = 1
    return occupancy_array

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

def make_grid(width, height, layers, theta_dict, grid_occupancy):
    if grid_occupancy is None:
        shared_data.grid_args["grid_occupancy"] = rand_grid(shared_data.grid_args["width"], shared_data.grid_args["height"])
        grid_occupancy = shared_data.grid_args["grid_occupancy"]

    # Create a custom red-to-green colormap
    colors = [(1, 0, 0, 0.3), (0, 1, 0, 0.3)]  # Red to Green
    cmap = mcolors.LinearSegmentedColormap.from_list("RedGreen", colors, N=256)
    
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    axes = axes.flatten()

    if layers is not None:
        # Iterate over each subplot and layer (up to the number of layers)
        for ax, layer in zip(axes, layers):
            # Display the grid
            ax.imshow(grid_occupancy, cmap='gray_r', origin='upper', extent=(0, width, 0, height))
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_aspect('equal')
            ax.grid(True)
            ax.set_xticks(np.arange(0, width + 1, 1))
            ax.set_yticks(np.arange(0, height + 1, 1))
            ax.tick_params(which='both', length=0)

            knowledge = layer.get("knowledge")

            for i in range(knowledge.shape[0]):
                for j in range(knowledge.shape[1]):
                    # Skip if the grid_occupancy cell is 1 (occupied)
                    if grid_occupancy[i, j] == 1:
                        continue

                    if knowledge[i, j] != 0:
                        # Apply color grading to the knowledge value using the colormap
                        color = cmap(knowledge[i, j])
                        ax.add_patch(plt.Rectangle((j, height - (i + 1)), 1, 1, color=color))
                        ax.text(j + 0.5, height - (i + 0.5), f'{knowledge[i, j]:.2f}', ha='center', va='center', color='black', fontsize=5)

            # Plot the robot position and orientation if it is the right layer
            if shared_data.grid_args["rot"] == layer['theta']:
                center_x = shared_data.grid_args['x'] - 0.5
                center_y = shared_data.grid_args['y'] - 0.5
                ax.plot(center_x, center_y, marker='o', color='red', markersize=6)
                theta = theta_dict[layer['direction']]
                ax.arrow(center_x, center_y, 0.5 * np.cos(np.radians(theta)), 
                            0.5 * np.sin(np.radians(theta)), head_width=0.2, head_length=0.3, 
                            fc='blue', ec='blue')
                
    else:
        for idx, ax in enumerate(axes):
            # Display the grid
            ax.imshow(grid_occupancy, cmap='gray_r', origin='upper', extent=(0, width, 0, height))
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_aspect('equal')
            ax.grid(True)
            ax.set_xticks(np.arange(0, width + 1, 1))
            ax.set_yticks(np.arange(0, height + 1, 1))
            ax.tick_params(which='both', length=0)

    plt.tight_layout()
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

def export_grid():
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
        print("Entry widgets created.")
        widgets['submit_location_button'].bind("<Button-1>", lambda event: initialize_layer(window, shared_data.grid_args["width"], shared_data.grid_args["height"], shared_data.grid_args["theta_dict"], shared_data.grid_args["grid_occupancy"], shared_data.grid_args["widgets"]))
        
    else:
        location_entries["x_loc_entry"].delete(0, tk.END)
        location_entries["y_loc_entry"].delete(0, tk.END)
        print("Entry widgets already exist, clearing content.")

def initialize_layer(window, height, width, theta_dict, grid_occupancy, widgets):
    try:
        shared_data.grid_args["x"] = int(widgets['x_loc_entry'].get())
        shared_data.grid_args["y"] = int(widgets['y_loc_entry'].get())
        shared_data.grid_args["rot"] = int(widgets['rot_entry'].get())

        shared_data.grid_args["widgets"]['x_loc_entry'].config(state='disabled')
        shared_data.grid_args["widgets"]['y_loc_entry'].config(state='disabled')
        shared_data.grid_args["widgets"]['submit_location_button'].config(state='disabled')

        layers = layer(shared_data.grid_args["width"], shared_data.grid_args["height"], shared_data.grid_args["theta_dict"], shared_data.grid_args["grid_occupancy"])
        visualize_grid(shared_data.grid_args["width"], shared_data.grid_args["height"], shared_data.grid_args["theta_dict"], shared_data.grid_args["grid_occupancy"], shared_data.grid_args["widgets"], layers)
        setup_screen(shared_data.grid_args["widgets"])
    except ValueError as e:
        widgets['error_label'].config(text=f"Error: {e}")

def setup_screen(widgets):
    widgets['submit_mov_button'] = tk.Button(master=widgets['side_frame'], text="Veikt kustību 1 soli", width=15, height=2)
    widgets['submit_measure_button'] = tk.Button(master=widgets['side_frame'], text="Veikt mērījumu", width=15, height=2)
    widgets['submit_mov_button'].pack()
    widgets['submit_measure_button'].pack()
