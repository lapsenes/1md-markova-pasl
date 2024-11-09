import tkinter as tk
from tkinter import ttk
import threading
import numpy as np
from functools import partial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from robot import * 

buttons = []

def toggle_color(button):
    current_color = button.cget("background") #TODO
    new_color = "blue" if current_color == "white" else "white"
    button.config(background=new_color)
    button.update_idletasks()

def rand_grid(width, height):
    occupancy_array = np.zeros((width, height), dtype=int)

    indices = np.random.choice(width*height, 20, replace=False)
    occupancy_array[np.unravel_index(indices, (width, height))] = 1
    return occupancy_array

def make_grid(width, height):
    occupancy = rand_grid(width, height)
    cmap = plt.cm.get_cmap('gray_r', 2)

    directions = ['Right', 'Up', 'Left', 'Down']
    theta_values = [0, 90, 180, 270]
    
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    axes = axes.flatten()
    
    for idx, theta in enumerate(theta_values):
        ax = axes[idx]
        ax.imshow(occupancy, cmap=cmap, origin='upper', extent=(0, occupancy.shape[1], 0, occupancy.shape[0]))

        dx, dy = 0, 0
        if theta == 0:     # Right
            dx, dy = 0.5, 0
        elif theta == 90:  # Up
            dx, dy = 0, -0.5
        elif theta == 180: # Left
            dx, dy = -0.5, 0
        elif theta == 270: # Down
            dx, dy = 0, 0.5
        
        ax.arrow(1.5, 1.5, dx, dy, head_width=0.3, head_length=0.3, fc='red', ec='red') # TODO specific location of the robot
        
        ax.set_title(f'Robot Facing {directions[idx]}')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.grid(False)
    plt.tight_layout()
    return fig

def visualize_grid(width, height):
        # Generate the Matplotlib figure
    fig = make_grid(width, height)
    canvas = FigureCanvasTkAgg(fig, master=action_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def handle_submit_size(event):
    try:
        width = int(width_entry.get())
        height = int(height_entry.get())
        
        if width < 10 or width > 20 or height < 10 or height > 20:
            raise ValueError("Width and height must be between 10 and 20")

        threading.Thread(target=create_grid_thread, args=(width, height), daemon=True).start()

    except ValueError as e:
        error_label.config(text=f"Error: {e}")

def create_grid_thread(width, height):
    window.after(0, visualize_grid, width, height)

def export_grid():
    grid_state = []
    for row in buttons:
        row_state = []
        for button in row:
            # 0 (white) or 1 (blue)
            current_color = button.cget("background")
            row_state.append(1 if current_color == "blue" else 0)
        grid_state.append(row_state)
    
    grid_array = np.array(grid_state)










window = tk.Tk()
window.title("Markova pašlokalizācija")

greeting = tk.Label(text="Markova pašlokalizācija")
greeting.pack()

side_frame = tk.Frame(window, bd=2, relief="solid", width=2000, height=3000)
action_frame = tk.Frame(window, bd=2, relief="solid", width=5000)
side_frame.pack(fill=tk.Y, side=tk.LEFT)
action_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

width_label = tk.Label(master=side_frame, text="Laukuma platums (no 10 līdz 20)")
width_entry = tk.Entry(master=side_frame)
width_label.pack()
width_entry.pack()

height_label = tk.Label(master=side_frame, text="Laukuma augstums (no 10 līdz 20)")
height_entry = tk.Entry(master=side_frame)
height_label.pack()
height_entry.pack()

submit_size = tk.Button(master=side_frame, text="Ģenerēt laukumu", width=15, height=2)
submit_size.pack()

# Error message label
error_label = tk.Label(master=side_frame, text="", fg="red")
error_label.pack()

# Bind actions
window.bind("<Escape>", lambda event: window.attributes('-fullscreen', False))
submit_size.bind("<Button-1>", handle_submit_size)

# Start the Tkinter event loop
window.mainloop()
