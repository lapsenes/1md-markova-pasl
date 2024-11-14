import tkinter as tk
from tkinter import ttk
import threading
import numpy as np
from functools import partial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from robot import * 

buttons = []
grid_occupancy = 0
location_entries = {}
theta_dict = {
    "right": 0,    # "up" corresponds to 0 degrees (north)
    "up": 90, # "right" corresponds to 90 degrees (east)
    "left": 180, # "down" corresponds to 180 degrees (south)
    "down": 270  # "left" corresponds to 270 degrees (west)
}
widgets = {}  # Dictionary to store widgets

def toggle_color(button):
    current_color = button.cget("background")
    new_color = "blue" if current_color == "white" else "white"
    button.config(background=new_color)
    button.update_idletasks()

def rand_grid(width, height):
    occupancy_array = np.zeros((width, height), dtype=int)
    indices = np.random.choice(width*height, 20, replace=False)
    occupancy_array[np.unravel_index(indices, (width, height))] = 1
    return occupancy_array

def make_grid(width, height):
    grid_occupancy = rand_grid(width, height)
    cmap = plt.cm.get_cmap('gray_r', 2)
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    axes = axes.flatten()
    
    for idx, _ in enumerate(theta_dict.items()):
        ax = axes[idx]
        ax.imshow(grid_occupancy, cmap=cmap, origin='upper', extent=(0, grid_occupancy.shape[1], 0, grid_occupancy.shape[0]))   
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_aspect('equal')
        ax.grid(True)
        ax.set_xticks(np.arange(0, width + 1, 1))
        ax.set_yticks(np.arange(0, height + 1, 1))
        ax.tick_params(which='both', length=0)
    plt.tight_layout()
    return fig

def visualize_grid(width, height):
    fig = make_grid(width, height)
    canvas = FigureCanvasTkAgg(fig, master=widgets['action_frame'])
    canvas.draw()
    canvas.get_tk_widget().pack()

def handle_submit_size(event):
    try:
        width = int(widgets['width_entry'].get())
        height = int(widgets['height_entry'].get())
        
        if width < 10 or width > 20 or height < 10 or height > 20:
            raise ValueError("Width and height must be between 10 and 20")

        threading.Thread(target=create_grid_thread, args=(width, height), daemon=True).start()
        threading.Thread(target=ask_robot_location_thread, args=(width, height), daemon=True).start()

    except ValueError as e:
        widgets['error_label'].config(text=f"Error: {e}")

def create_grid_thread(width, height):
    window.after(0, visualize_grid, width, height)

def ask_robot_location_thread(width, height):
    window.after(0, ask_robot_location, width, height)

def initialize_robot_thread(width, height, grid_occupancy, theta_dict):
    window.after(0, initialize_robot, width, height, grid_occupancy, theta_dict)

def ask_robot_location(width, height):
    if "x_loc_entry" not in location_entries and "y_loc_entry" not in location_entries:
        widgets['x_loc_label'] = tk.Label(master=widgets['side_frame'], text="Robota sākuma pozīcija x")
        widgets['x_loc_entry'] = tk.Entry(master=widgets['side_frame'])
        widgets['y_loc_label'] = tk.Label(master=widgets['side_frame'], text="Robota sākuma pozīcija y")
        widgets['y_loc_entry'] = tk.Entry(master=widgets['side_frame'])
        widgets['submit_location_button'] = tk.Button(master=widgets['side_frame'], text="Inicializēt robotu", width=15, height=2)

        widgets['x_loc_label'].pack()
        widgets['x_loc_entry'].pack()
        widgets['y_loc_label'].pack()
        widgets['y_loc_entry'].pack()
        widgets['submit_location_button'].pack()

        location_entries["x_loc_entry"] = widgets['x_loc_entry']
        location_entries["y_loc_entry"] = widgets['y_loc_entry']
        print("Entry widgets created.")
        widgets['submit_location_button'].bind("<Button-1>", initialize_robot_thread(width, height, grid_occupancy, theta_dict))
        
    else:
        location_entries["x_loc_entry"].delete(0, tk.END)
        location_entries["y_loc_entry"].delete(0, tk.END)
        print("Entry widgets already exist, clearing content.")

def initialize_robot(height, width, grid_occupancy, theta_dict):
    try:
        x = int(widgets['x_loc_entry'].get())
        y = int(widgets['y_loc_entry'].get())
        robots = robot.__init__(height, width, grid_occupancy, x, y, theta_dict)

    except ValueError as e:
        widgets['error_label'].config(text=f"Error: {e}")

def export_grid():
    grid_state = []
    for row in buttons:
        row_state = []
        for button in row:
            current_color = button.cget("background")
            row_state.append(1 if current_color == "blue" else 0)
        grid_state.append(row_state)
    
    grid_array = np.array(grid_state)

# Create the main Tkinter window
window = tk.Tk()
window.title("Markova pašlokalizācija")

# Initialize frames and store in the widgets dictionary
widgets['side_frame'] = tk.Frame(window, bd=2, relief="solid", width=2000, height=3000)
widgets['action_frame'] = tk.Frame(window, bd=2, relief="solid", width=5000)
widgets['side_frame'].pack(fill=tk.Y, side=tk.LEFT)
widgets['action_frame'].pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

# Widgets for grid dimensions input
widgets['width_label'] = tk.Label(master=widgets['side_frame'], text="Laukuma platums (no 10 līdz 20)")
widgets['width_entry'] = tk.Entry(master=widgets['side_frame'])
widgets['width_label'].pack()
widgets['width_entry'].pack()

widgets['height_label'] = tk.Label(master=widgets['side_frame'], text="Laukuma augstums (no 10 līdz 20)")
widgets['height_entry'] = tk.Entry(master=widgets['side_frame'])
widgets['height_label'].pack()
widgets['height_entry'].pack()

# Button to generate grid and error label
widgets['submit_size'] = tk.Button(master=widgets['side_frame'], text="Ģenerēt laukumu", width=15, height=2)
widgets['submit_size'].pack()
widgets['error_label'] = tk.Label(master=widgets['side_frame'], text="", fg="red")
widgets['error_label'].pack()

# Bind actions
window.bind("<Escape>", lambda event: window.attributes('-fullscreen', False))
widgets['submit_size'].bind("<Button-1>", handle_submit_size)

# Start the Tkinter event loop
window.mainloop()
