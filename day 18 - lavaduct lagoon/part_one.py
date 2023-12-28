import re
with open("dig_plan.txt", "r") as file:
    dig_plan = file.read().splitlines()

dig_site: list[list[str]] = [["#"]]
dig_instructions = []
max_right = 0
min_left = 0
min_up = 0
max_down = 0
X = 0
Y = 0
# start with empty matrix
# make it wider if exceed width
# make it taller if exceed abs(height)
for instruction in dig_plan:
    instructions = instruction.split()
    direction = instructions[0]
    moves = int(instructions[1])
    color = re.findall(r"\((#\S+)\)", instructions[2])[0]
    dig_instructions.append((direction, moves, color))
    if direction == "R":
        growth_needed = max(0, moves + X - max_right)
        for grow_right in range(growth_needed):
            [dig_site[row].append(".") for row in range(max_down - min_up + 1)]
        max_right += growth_needed
        for i in range(moves):
            X += 1
            dig_site[Y][X] = "#"
    elif direction == "L":
        growth_needed = abs(min(0, X - moves - min_left))
        for grow_left in range(growth_needed):
            [dig_site[row].insert(0,".") for row in range(max_down - min_up + 1)]
        max_right += growth_needed
        X += growth_needed
        for i in range(moves):
            X -= 1
            dig_site[Y][X] = "#"
    elif direction == "U":
        growth_needed = abs(min(0, Y - moves - min_up))
        for grow_up in range(growth_needed):
            dig_site.insert(0,["." for _ in range(max_right - min_left + 1)])
        max_down += growth_needed
        Y += growth_needed
        for i in range(moves):
            Y -= 1
            dig_site[Y][X] = "#"
    elif direction == "D":
        growth_needed = max(0, moves + Y - max_down)
        for grow_down in range(growth_needed):
            dig_site.append(["." for _ in range(max_right - min_left + 1)])
        max_down += growth_needed
        for i in range(moves):
            Y += 1
            dig_site[Y][X] = "#"
area = 0
visited_nodes = {"0,0": True}
nodes_to_infect = [(0,0)]
[dig_site[row].insert(0,".") for row in range(len(dig_site))]
[dig_site[row].append(".") for row in range(len(dig_site))]
dig_site.insert(0,["." for _ in range(len(dig_site[0]))])
dig_site.append(["." for _ in range(len(dig_site[0]))])
while len(nodes_to_infect) > 0:
    next_node = nodes_to_infect.pop(0)
    x = next_node[0]
    y = next_node[1]
    dig_site[y][x] = "X"
    top = None if y == 0 else (x, y-1) if dig_site[y-1][x] == "." else None
    right = None if x == len(dig_site[y]) - 1 else (x+1, y) if dig_site[y][x+1] == "." else None
    bot = None if y == len(dig_site) - 1 else (x, y+1) if dig_site[y+1][x] == "." else None
    left = None if x == 0 else (x-1, y) if dig_site[y][x-1] == "." else None
    if top and f"{top[0]},{top[1]}" not in visited_nodes.keys():
        nodes_to_infect.append(top)
        visited_nodes[f"{top[0]},{top[1]}"] = True
    if right and f"{right[0]},{right[1]}" not in visited_nodes.keys():
        nodes_to_infect.append(right)
        visited_nodes[f"{right[0]},{right[1]}"] = True
    if bot and f"{bot[0]},{bot[1]}" not in visited_nodes.keys():
        nodes_to_infect.append(bot)
        visited_nodes[f"{bot[0]},{bot[1]}"] = True
    if left and f"{left[0]},{left[1]}" not in visited_nodes.keys():
        nodes_to_infect.append(left)
        visited_nodes[f"{left[0]},{left[1]}"] = True

for row in dig_site:
    area += len([char for char in row if char != "X"])
    
# 55121 too low
print(area)
