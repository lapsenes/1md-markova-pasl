import tkinter as tk
from tkinter import ttk
import numpy as np
from functools import partial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.layer import * 
from src.helpers import *
import src.shared_data as shared_data

def handle_submit_size(event):
    try:
        width = shared_data.grid_args["width"] # = int(shared_data.grid_args["widgets"]['width_entry'].get())
        height = shared_data.grid_args["height"] # = int(shared_data.grid_args["widgets"]['height_entry'].get())
        shared_data.grid_args["widgets"]['width_entry'].config(state='disabled')
        shared_data.grid_args["widgets"]['height_entry'].config(state='disabled')
        shared_data.grid_args["widgets"]['submit_size'].config(state='disabled')
        if width < 10 or width > 20 or height < 10 or height > 20:
            raise ValueError("Width and height must be between 10 and 20")
        
        visualize_grid(shared_data.grid_args["width"], shared_data.grid_args["height"], shared_data.grid_args["theta_dict"], shared_data.grid_args["grid_occupancy"], shared_data.grid_args["widgets"])
        ask_location(window, shared_data.grid_args["width"], shared_data.grid_args["height"], shared_data.grid_args["location_entries"], shared_data.grid_args["widgets"], shared_data.grid_args["grid_occupancy"], shared_data.grid_args["theta_dict"])

    except ValueError as e:
        shared_data.grid_args["widgets"]['error_label'].config(text=f"Error: {e}")

# Create the main Tkinter window
window = tk.Tk()
window.title("Markova pašlokalizācija")

# Initialize frames and store in the widgets dictionary
shared_data.grid_args["widgets"]['side_frame'] = tk.Frame(window, bd=2, relief="solid", width=2000, height=3000)
shared_data.grid_args["widgets"]['action_frame'] = tk.Frame(window, bd=2, relief="solid", width=5000)
shared_data.grid_args["widgets"]['side_frame'].pack(fill=tk.Y, side=tk.LEFT)
shared_data.grid_args["widgets"]['action_frame'].pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

# Widgets for grid dimensions input
shared_data.grid_args["widgets"]['width_label'] = tk.Label(master=shared_data.grid_args["widgets"]['side_frame'], text="Laukuma platums (no 10 līdz 20)")
shared_data.grid_args["widgets"]['width_entry'] = tk.Entry(master=shared_data.grid_args["widgets"]['side_frame'])
shared_data.grid_args["widgets"]['width_label'].pack()
shared_data.grid_args["widgets"]['width_entry'].pack()

shared_data.grid_args["widgets"]['height_label'] = tk.Label(master=shared_data.grid_args["widgets"]['side_frame'], text="Laukuma augstums (no 10 līdz 20)")
shared_data.grid_args["widgets"]['height_entry'] = tk.Entry(master=shared_data.grid_args["widgets"]['side_frame'])
shared_data.grid_args["widgets"]['height_label'].pack()
shared_data.grid_args["widgets"]['height_entry'].pack()

# Button to generate grid and error label
shared_data.grid_args["widgets"]['submit_size'] = tk.Button(master=shared_data.grid_args["widgets"]['side_frame'], text="Ģenerēt laukumu", width=15, height=2)
shared_data.grid_args["widgets"]['submit_size'].pack()
shared_data.grid_args["widgets"]['error_label'] = tk.Label(master=shared_data.grid_args["widgets"]['side_frame'], text="", fg="red")
shared_data.grid_args["widgets"]['error_label'].pack()

# Bind actions
window.bind("<Escape>", lambda event: window.attributes('-fullscreen', False))
shared_data.grid_args["widgets"]['submit_size'].bind("<Button-1>", handle_submit_size)

# Start the Tkinter event loop
window.mainloop()
