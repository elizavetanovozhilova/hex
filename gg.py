import numpy as np
import plotly.express as px
import random

N = 5
default= -1


def create_map(max_dist):
    N = 2 * max_dist + 1
    default_value = -1

    coordinates = np.array([[x, y, z] for x in range(N) for y in range(N) for z in range(N)])
    data = np.zeros((N**3, 4), dtype=int)
    data[:, :3] = coordinates
    data[:, 3] = default_value

    return data


def get_hex_idxs(coords_map, max_dist):
    c = max_dist
    condition = (coords_map[:, 0] + coords_map[:, 1] + coords_map[:, 2]) == 3 * c
    hexagon_idxs = np.where(condition)[0]
    return hexagon_idxs


ALL_MOVEMENTS = np.array([
    [0, 1, -1],
    [1, 0, -1],
    [1, -1, 0],
    [0, -1, 1],
    [-1, 0, 1],
    [-1, 1, 0]
])

def is_valid_hex(coords, max_dist):
    x, y, z = coords
    N = 2 * max_dist + 1
    return 0 <= x < N and 0 <= y < N and 0 <= z < N and (x + y + z) == 3 * max_dist


def generate_rivers(river_map, hex_idxs, river_movements, rivers_count, max_river_length, river_type, max_dist):
    for _ in range(rivers_count):
        river_length = random.randint(1, max_river_length)
        start_idx = random.choice(hex_idxs)
        start_point = river_map[start_idx, :3]

        current_point = start_point

        for _ in range(river_length):
            if river_map[start_idx, 3] == -1:
                river_map[start_idx, 3] = river_type

            move = random.choice(river_movements)
            next_point = current_point + move
            if is_valid_hex(next_point, max_dist):
                current_point = next_point
                next_idx = (current_point[0] * (2 * max_dist + 1) ** 2 +
                            current_point[1] * (2 * max_dist + 1) +
                            current_point[2])
                if river_map[next_idx, 3] == -1:
                    river_map[next_idx, 3] = river_type

def generate_hills(hills_map, hex_idxs, hills_count, hills_type, max_dist):
    for _ in range(hills_count):
        start_idx = random.choice(hex_idxs)
        hills_map[start_idx, 3] = hills_type
        for movement in ALL_MOVEMENTS:
            new_point = hills_map[start_idx, :3] + movement
            if is_valid_hex(new_point, max_dist):
                new_idx = (new_point[0] * (2 * max_dist + 1) ** 2 +
                           new_point[1] * (2 * max_dist + 1) +
                           new_point[2])
                if hills_map[new_idx, 3] == -1:
                    hills_map[new_idx, 3] = hills_type


MAX_DIST = 20
RIVERS_COUNT = 40
MAX_RIVER_LENGTH = 7
RIVER_TYPE = 100
HILLS_COUNT = 10
HILLS_TYPE = 10

new_map = create_map(MAX_DIST)
hex_idxs = get_hex_idxs(new_map, MAX_DIST)

generate_rivers(new_map, hex_idxs, ALL_MOVEMENTS[0:3], RIVERS_COUNT, MAX_RIVER_LENGTH, RIVER_TYPE, MAX_DIST)
generate_hills(new_map, hex_idxs, HILLS_COUNT, HILLS_TYPE, MAX_DIST)

hex_data = new_map[hex_idxs]

ROUTE_TYPE = 1000

def visualize_solve(route_path):
    route_map = np.copy(new_map)
    for cell_idx in route_path:
        route_map[cell_idx][-1] = ROUTE_TYPE
    hex_data = route_map[hex_idxs]
    types_map = {
        -1: "Plain",
        RIVER_TYPE: "River",
        HILLS_TYPE: "Hill",
        ROUTE_TYPE: "Route"
    }
    vfunc = np.vectorize(types_map.get)
    colors = vfunc(hex_data[:, 3])
    fig = px.scatter_3d(
        hex_data,
        x=hex_data[:, 0],
        y=hex_data[:, 1],
        z=hex_data[:, 2],
        hover_name=hex_idxs,
        color=colors,
        color_discrete_sequence=["#387C44", "#0000FF", "gray", "maroon"],
    )
    fig.show()

visualize_solve([59460, 57780, 57740, 56060, 54380])


