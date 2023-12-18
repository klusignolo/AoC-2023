import math

with open("input.txt", "r") as file:
    city_blocks = [[int(block) for block in row] for row in file.read().splitlines()]
# 658 best so far. TOO HIGH
WIDTH = len(city_blocks) - 1
DESTINATION = (WIDTH, WIDTH)
MAX_HEAT_LOSS =1

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

    def __repr__(self) -> str:
        return self.key
    
    def F(self) -> int:
        return self.G + self.H + self.heat_loss
    
    def connect_to(self, other_node: "Node"):
        # bearing based on coming FROM the other node
        self.connected_to = other_node
        if self.X == other_node.X and self.Y < other_node.Y:
            self.bearing = 1 # up
        elif self.X > other_node.X and self.Y == other_node.Y:
            self.bearing = 2 # right
        elif self.X == other_node.X and self.Y > other_node.Y:
            self.bearing = 3 # down
        elif self.X < other_node.X and self.Y == other_node.Y:
            self.bearing = 4 # left
        self.unwalkable_direction = None
        if self.connected_to.bearing == self.bearing:
            if self.connected_to.connected_to is not None and self.connected_to.connected_to.bearing == self.bearing:
                self.unwalkable_direction = self.bearing
    
    def neighbors(self, city: list[list["Node"]]) -> list["Node"]:
        # unwalkable_direction, 1,2,3,4 == u,r,d,l
        neighbors = []
        if self.Y > 0 and self.unwalkable_direction != 1 and self.bearing != 3:
            neighbors.append(city[self.Y - 1][self.X])
        if self.Y < WIDTH and self.unwalkable_direction != 3 and self.bearing != 1:
            neighbors.append(city[self.Y + 1][self.X])
        if self.X > 0 and self.unwalkable_direction != 4 and self.bearing != 2:
            neighbors.append(city[self.Y][self.X - 1])
        if self.X < WIDTH and self.unwalkable_direction != 2 and self.bearing != 4:
            neighbors.append(city[self.Y][self.X + 1])
        return neighbors
    
    def distance_to(self, destination: "Node"):
        distance_x = destination.point[0] - self.point[0]
        distance_y = destination.point[1] - self.point[1]
        furthest = max(distance_x, distance_y)
        nearest = min(distance_x, distance_y)
        jumps_needed = math.floor((furthest - nearest) / 3) * 2
        return distance_x + distance_y + jumps_needed
    
city_nodes: list[list[Node]] = city_blocks.copy()
for y, row in enumerate(city_blocks):
    for x, col in enumerate(row):
        city_nodes[y][x] = Node(point=(x, y), heat_loss=col)

start_node: Node = city_nodes[0][0]
target_node: Node = city_nodes[WIDTH][WIDTH]
for row in city_nodes:
    for node in row:
        node.G = start_node.distance_to(node)
        node.H = node.distance_to(target_node)
to_search: list[Node] = [start_node]
processed: list[str] = []
while len(to_search) > 0:
    current_i = 0
    current = to_search[current_i]
    for i, node in enumerate(to_search):
        if node.F() < current.F() or (node.F() == current.F() and node.H < current.H):
            current = node
            current_i = i
    processed.append(current.key)
    to_search.pop(current_i)

    if current == target_node:
        current_path_tile = target_node
        shortest_path = []
        total_heat_loss = 0
        while current_path_tile != start_node:
            print(current_path_tile.key)
            shortest_path.append(current_path_tile)
            total_heat_loss += current_path_tile.heat_loss
            current_path_tile = current_path_tile.connected_to
        print(start_node.key)
        print(total_heat_loss)
        print("Path found. Probably not the smallest tho...")

    for neighbor in current.neighbors(city=city_nodes):
        if neighbor.key in processed: continue
        is_in_search = neighbor in to_search
        cost_to_neighbor = current.G + neighbor.heat_loss
        if not is_in_search or cost_to_neighbor < neighbor.G:
            neighbor.G = cost_to_neighbor
            neighbor.connect_to(current)

            if not is_in_search:
                to_search.append(neighbor)

