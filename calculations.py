import numpy as np

def rand_grid(width=10, height=10):
    array = np.zeros((width, height), dtype=int)

    indices = np.random.choice(width*height, 20, replace=False)
    array[np.unravel_index(indices, (width, height))] = 1

    print(array)

