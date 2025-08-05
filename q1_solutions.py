import numpy as np
import heapq
import matplotlib.pyplot as plt
import csv
from pathlib import Path
import fluids
from fluids.vectorized import *
from fluids.units import *
from math import *

def dijkstra_distance_priority(grid, start, end):
    rows, cols = grid.shape
    visited = np.full((rows, cols), False)
    distance = np.full((rows, cols), np.inf)
    bend_count = np.full((rows, cols), np.inf)
    prev_direction = np.full((rows, cols), None)
    parent = {}

    distance[start] = 0
    bend_count[start] = 0

    # Priority queue: (distance, bends, x, y, direction)
    queue = [(0, 0, start[0], start[1], None)]

    directions = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }

    while queue:
        dist, bends, x, y, dir_from = heapq.heappop(queue)

        if visited[x, y]:
            continue
        visited[x, y] = True

        if (x, y) == end:
            break

        for dir_name, (dx, dy) in directions.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx, ny] == 0 and not visited[nx, ny]:
                new_dist = dist + 1
                new_bends = bends + (dir_from != dir_name and dir_from is not None)
                if new_dist < distance[nx, ny] or (new_dist == distance[nx, ny] and new_bends < bend_count[nx, ny]):
                    distance[nx, ny] = new_dist
                    bend_count[nx, ny] = new_bends
                    prev_direction[nx, ny] = dir_name
                    parent[(nx, ny)] = (x, y)
                    heapq.heappush(queue, (new_dist, new_bends, nx, ny, dir_name))

    # Reconstruct path
    path = []
    bends = []
    current = end
    last_dir = None
    while current != start:
        path.append(current)
        prev = parent.get(current)
        if prev is None:
            return [], []  # No path found
        dx, dy = current[0] - prev[0], current[1] - prev[1]
        for dir_name, (ddx, ddy) in directions.items():
            if (dx, dy) == (ddx, ddy):
                if dir_name != last_dir:
                    bends.append(current)
                last_dir = dir_name
                break
        current = prev
    path.append(start)
    path.reverse()
    bends.reverse()

    
    # Remove final point from bends if present
    if bends and bends[-1] == end:
        bends.pop()

    return path, bends

def plot_path(grid, path, bends):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(grid, cmap=plt.cm.Dark2)
    path_x, path_y = zip(*path)
    plt.plot(path_y, path_x, color='blue', linewidth=2, label='Path')
    if bends:
        bend_x, bend_y = zip(*bends)
        plt.scatter(bend_y, bend_x, color='red', label='Bends')
    plt.scatter(path_y[0], path_x[0], color='green', label='Start')
    plt.scatter(path_y[-1], path_x[-1], color='orange', label='End')
    plt.legend()
    plt.title("Shortest Path")
    plt.show()

def unit_conversion(length):
    """ Assume we are in units of decimetres in the grid"""
    return length/10

def pipe_lengths(path, bends):
    start = path[0]
    end = path[-1]
    nodes = [start] + bends +[end]
    distances = []

    for i, node in enumerate(nodes):
        if i == len(nodes)-1:
            break
        else:
            length = np.sqrt((nodes[i+1][0]-nodes[i][0])**2+(nodes[i+1][1]-nodes[i][1])**2)
            distances.append(unit_conversion(length))

    return distances

def pressure_drop_simple(path, bends, flow_rate, diameter):
    """
    flow rate in m**3/s
    diameter in m
    """
    d1=diameter*u.m
    velocity = flow_rate/(pi/4*diameter**2)*u.m/u.s
    rho = 1000*u.kg/u.m**3
    mu = 1E-3*u.Pa*u.s
    total_length = sum(pipe_lengths(path,bends))*u.m
    
    Re = Reynolds(V=velocity, D=d1, rho=rho, mu=mu)
    fd = friction_factor(Re, eD=1e-5/diameter)
    K = K_from_f(fd=fd, L=total_length, D=d1)
    K += entrance_sharp()
    K += exit_normal()
    K += len(bends)*bend_miter(angle=90*u.degrees)
    pressure_drop = dP_from_K(K, rho=rho,V=velocity)
    return round(pressure_drop)

if __name__ == "__main__":
    rows = list(csv.reader(Path("grid.tsv").open(encoding="utf-8"), delimiter="\t"))
    grid = np.array([[int(x) for x in row] for row in rows])
    start = (18, 40)
    goal = (92, 25)
    flow_rate = 0.01
    diameter=0.05
    
    path, bends = dijkstra_distance_priority(grid, start, goal)
    plot_path(grid, path, bends)
    dp = pressure_drop_simple(path, bends, flow_rate, diameter)
    print("Pressure drop of pipe of diameter {} m with flow rate of {} m^3/s is {}".format(diameter, flow_rate, dp))