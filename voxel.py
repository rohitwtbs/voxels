import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_voxel_landscape(size=64):
    """Generates a voxel landscape with a mountain and trees."""

    landscape = np.zeros((size, size, size), dtype=int)

    # Mountain (simple cone shape)
    center_x, center_y = size // 2, size // 2
    mountain_height = size // 2

    for x in range(size):
        for y in range(size):
            distance = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            if distance < size // 3:
                height = int(mountain_height * (1 - distance / (size // 3)))
                for z in range(height):
                    landscape[x, y, z] = 1  # Mountain rock

    # Trees (randomly placed)
    num_trees = 20
    for _ in range(num_trees):
        tree_x = np.random.randint(0, size)
        tree_y = np.random.randint(0, size)
        # Ensure trees are on the ground (above the mountain)
        ground_z = 0
        for z in range(size):
            if landscape[tree_x, tree_y, z] == 1:
                ground_z = z + 1
        if ground_z < size-1:
            tree_height = np.random.randint(5, 15)
            for z in range(ground_z, min(ground_z + tree_height, size)):
                landscape[tree_x, tree_y, z] = 2  # Tree trunk
            # Add leaves (simple cube on top)
            leaf_size = 3
            leaf_offset = tree_height // 2
            for lx in range(max(0, tree_x - leaf_size), min(size, tree_x + leaf_size + 1)):
                for ly in range(max(0, tree_y - leaf_size), min(size, tree_y + leaf_size + 1)):
                    for lz in range(max(ground_z + tree_height - leaf_offset,0), min(ground_z + tree_height - leaf_offset + leaf_size, size)):
                        landscape[lx, ly, lz] = 3  # Tree leaves

    return landscape

def plot_voxel_landscape(landscape):
    """Plots the voxel landscape."""

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    colors = np.empty(landscape.shape, dtype=object)
    colors[landscape == 1] = 'gray'  # Mountain
    colors[landscape == 2] = 'brown' # Tree trunk
    colors[landscape == 3] = 'green' # Tree leaves

    ax.voxels(landscape, facecolors=colors, edgecolor='k')

    plt.show()

if __name__ == "__main__":
    landscape = generate_voxel_landscape()
    plot_voxel_landscape(landscape)