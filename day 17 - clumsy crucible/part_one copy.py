from copy import deepcopy
import math
import statistics
import time

with open("input.txt", "r") as file:
    city_blocks = [[int(block) for block in row] for row in file.read().splitlines()]

all_heats = []
for block in city_blocks:
    all_heats.extend(block)
AVG_HL = statistics.mean(all_heats)
# 658 best so far. TOO HIGH
WIDTH = len(city_blocks) - 1
DESTINATION = (WIDTH, WIDTH)
MAX_HEAT_LOSS =1
SLEEP_STEP = 0
N_DEPTH = 1

class Node:
    connected_to: "Node" = None
    bearing = None
    unwalkable_direction = None
    def __init__(self, point: tuple[int,int], heat_loss: int):
        self.point = point
        self.key = f"{point[0]},{point[1]}"
        self.heat_loss = heat_loss
        self.X = point[0]
        self.Y = point[1]
        self.H = None
        self.G = None
        self.F = 0

    def __repr__(self) -> str:
        return self.key
    def __str__(self) -> str:
        return self.key
    
    def connect_to(self, other_node: "Node"):
        # bearing based on coming FROM the other node
        self.connected_to = other_node
        if self.X == other_node.X and self.Y < other_node.Y:
            self.bearing = "u" # up
        elif self.X > other_node.X and self.Y == other_node.Y:
            self.bearing = "r" # right
        elif self.X == other_node.X and self.Y > other_node.Y:
            self.bearing = "d" # down
        elif self.X < other_node.X and self.Y == other_node.Y:
            self.bearing = "l" # left
        self.unwalkable_direction = None
        if self.connected_to.bearing == self.bearing:
            if self.connected_to.connected_to is not None and self.connected_to.connected_to.bearing == self.bearing:
                self.unwalkable_direction = self.bearing
    
    def neighbors(self, city: list[list["Node"]]) -> list["Node"]:
        # unwalkable_direction, 1,2,3,4 == u,r,d,l
        neighbors = []
        if self.Y > 0 and self.unwalkable_direction != "u" and self.bearing != "d":
            neighbors.append(city[self.Y - 1][self.X])
        if self.Y < WIDTH and self.unwalkable_direction != "d" and self.bearing != "u":
            neighbors.append(city[self.Y + 1][self.X])
        if self.X > 0 and self.unwalkable_direction != "l" and self.bearing != "r":
            neighbors.append(city[self.Y][self.X - 1])
        if self.X < WIDTH and self.unwalkable_direction != "r" and self.bearing != "l":
            neighbors.append(city[self.Y][self.X + 1])
        return neighbors
    
    def distance_to(self, destination: "Node"):
        distance_x = abs(destination.point[0] - self.point[0])
        distance_y = abs(destination.point[1] - self.point[1])
        furthest = max(distance_x, distance_y)
        nearest = min(distance_x, distance_y)
        jumps_needed = math.floor((furthest - nearest) / 3) * 2
        total_moves_to_destination = distance_x + distance_y + jumps_needed

        if total_moves_to_destination > 1:
            # MAGIC HEURISTIC SHIZZ
            prev_neighbors = []
            next_neighbors = self.neighbors(city_nodes)
            neighborz = next_neighbors
            for _ in range(N_DEPTH):
                prev_neighbors = deepcopy(next_neighbors)
                next_neighbors = []
                [next_neighbors.extend(n.neighbors(city_blocks)) for n in prev_neighbors]
                [neighborz.append(n) for n in next_neighbors]
            neighbor_hl = [n.heat_loss for n in neighborz]
            [neighbor_hl.append(self.heat_loss) for i in range(N_DEPTH)]
            neighbor_hl_avg = statistics.mean(neighbor_hl)
        else:
            neighbor_hl_avg = 1

        distance_without_first_step = max(0, total_moves_to_destination - 1) * neighbor_hl_avg
        return round(distance_without_first_step, 2) + self.heat_loss
    
city_nodes: list[list[Node]] = city_blocks.copy()
for y, row in enumerate(city_blocks):
    for x, col in enumerate(row):
        city_nodes[y][x] = Node(point=(x, y), heat_loss=col)


start_node: Node = city_nodes[0][0]
target_node: Node = city_nodes[WIDTH][WIDTH]
for row in city_nodes:
    for node in row:
        node.G = 0#start_node.distance_to(node)
        node.H = node.distance_to(target_node)


for row in city_nodes:
    hs = [node.H for node in row]
    print(hs)

to_search: list[Node] = [start_node]
processed: dict[str, Node] = {}
shortest_path = []
while len(to_search) > 0:
    current_i = 0
    current = to_search[current_i]
    for i, node in enumerate(to_search):
        #print(f"Current: {current} F:{current.F} H: {current.H} | Search: {node} F: {node.F} H: {node.H}")
        if node.F < current.F or (node.F == current.F and node.H < current.H):
            current = node
            current_i = i
    #print(f"{current} F score is lowest. Starting from there")
    to_search.pop(current_i)

    neighbors = current.neighbors(city=deepcopy(city_nodes))

    for neighbor in neighbors:
        neighbor.connect_to(current)
    for neighbor in neighbors:
        # End Logic
        if neighbor.key == target_node.key:
            current_path_tile = neighbor
            total_heat_loss = 0
            while current_path_tile != start_node:
                print(current_path_tile.key)
                shortest_path.append(current_path_tile)
                total_heat_loss += current_path_tile.heat_loss
                current_path_tile = current_path_tile.connected_to
            print(start_node.key)
            print(total_heat_loss)
            to_search = []
            print("Path found. Probably not the smallest tho...")
            break

        # Get distance to start node
        neighbor.G = current.G + neighbor.distance_to(current)
        neighbor.F = neighbor.G + neighbor.H
        #print(f"{neighbor}'s F score is {neighbor.F} from {current}")
        time.sleep(SLEEP_STEP)

        search_node = None
        d_key = neighbor.key# + f",{neighbor.bearing}"
        for n in to_search:
            if n.key == neighbor.key:
                search_node = n
                break
        if search_node is not None and search_node.F < neighbor.F:
            # if search_node.F < neighbor.F:
            #     print(f"Skipping {neighbor} since we're planning to search for it at a shorter path.")
            # else:
            #     print(f"Already searching for {neighbor}")
            continue
        if d_key not in processed.keys():
            #print(f"Adding {neighbor},{neighbor.bearing} to search")
            city_nodes[neighbor.Y][neighbor.X] = neighbor
            to_search.append(neighbor)
        if d_key in processed.keys() and processed[d_key].F > neighbor.F:
            #print(f"Found that {d_key} is further than {neighbor},{neighbor.bearing}.")
            city_nodes[neighbor.Y][neighbor.X] = neighbor
            to_search.append(neighbor)
        time.sleep(SLEEP_STEP)
    #print(f"Adding {current_d_key} to processed")
    processed[current.key] = current
    time.sleep(SLEEP_STEP)

