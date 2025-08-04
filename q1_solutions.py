import numpy as np
import heapq
import matplotlib.pyplot as plt

def dijkstra_min_bends2(grid, start, end):
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
    plt.title("Shortest Path with Minimal Bends")
    plt.show()