with open ("loop.txt", "r") as file:
    map = [[char for char in line] for line in file.read().splitlines()]

class PathItem:
    def __init__(self, coordinate: tuple[int, int], char: str, next_direction: str):
        self.coordinate = coordinate
        self.char = char
        self.next_direction = next_direction

curr_coord = None
for y in range(len(map)):
    if curr_coord: break
    for x in range(len(map[y])):
        if map[y][x] == "S":
            curr_coord = (x, y)
            break
curr_char = "S"
prev_coord = None
finished_loop = False
path = [PathItem(curr_coord, "S", "N")]
step = 0
while not finished_loop:
    up = (curr_coord[0], curr_coord[1]-1) if curr_coord[1] > 0 else None
    right = (curr_coord[0] + 1, curr_coord[1]) if curr_coord[0] < len(map[0]) - 1 else None
    down = (curr_coord[0], curr_coord[1] + 1) if curr_coord[1] < len(map) - 1 else None
    left = (curr_coord[0] - 1, curr_coord[1]) if curr_coord[0] > 0 else None
    if up and up != prev_coord and curr_char in ["|", "J", "L", "S"] and map[up[1]][up[0]] in ["|", "7", "F", "S"]:
        prev_coord = curr_coord
        curr_coord = up
        path[step].next_direction = "N"
        curr_char = map[up[1]][up[0]]
    elif right and right != prev_coord and curr_char in ["-","L","F", "S"] and map[right[1]][right[0]] in ["-","7","J", "S"]:
        prev_coord = curr_coord
        curr_coord = right
        path[step].next_direction = "E"
        curr_char = map[right[1]][right[0]] 
    elif down and down != prev_coord and curr_char in ["|", "7", "F", "S"] and map[down[1]][down[0]] in ["|", "L", "J", "S"]:
        prev_coord = curr_coord
        curr_coord = down
        path[step].next_direction = "S"
        curr_char = map[down[1]][down[0]]
    elif left and left != prev_coord and curr_char in ["-", "7", "J", "S"] and map[left[1]][left[0]] in ["-", "F", "L", "S"]:
        prev_coord = curr_coord
        curr_coord = left
        path[step].next_direction = "W"
        curr_char = map[left[1]][left[0]]
    finished_loop = curr_char == "S"
    if not finished_loop:
        path.append(PathItem(curr_coord, curr_char, ""))
    else:
        path[len(path)-1].next_direction = "N" if up else "E" if right else "Z" if down else "W"
    step += 1

for path_item in path:
    map[path_item.coordinate[1]][path_item.coordinate[0]] = path_item.next_direction

for row in map:
    left = 0
    right = len(row) - 1
    while left != -1 or right != -1:
        if left != -1 and left < len(row) and row[left] not in ["N","S","E","W"]:
            row[left] = "O"
            left += 1
        else:
            left = -1
        if right != -1 and right >= 0 and row[right]  not in ["N","S","E","W"]:
            row[right] = "O"
            right -= 1
        else:
            right = -1
for col in range(len(map[0])):
    top = 0
    bot = len(map) - 1
    while top != -1 or bot != -1:
        if top != -1 and top < len(map) and map[top][col] not in ["N","S","E","W"]:
            map[top][col] = "O"
            top += 1
        else:
            top = -1
        if bot != -1 and bot >= 0 and map[bot][col] not in ["N","S","E","W"]:
            map[bot][col] = "O"
            bot -= 1
        else:
            bot = -1
# N S E W
top_left = min(path, key=lambda i: sum(i.coordinate))
while path[0].coordinate != top_left.coordinate:
    path.append(path.pop(0))

inside = "SE"
for p in path:
    if p.char == "F":
        if p.next_direction == "E":
            inside = "SE" if "E" in inside else "NW"
        else:
            inside = "SE" if "S" in inside else "NW"
    elif p.char == "|":
        inside = "E" if "E" in inside else "W"
    elif p.char == "J":
        if p.next_direction == "W":
            inside = "NW" if "W" in inside else "SE"
        else:
            inside = "NW" if "N" in inside else "SE"
    elif p.char == "L":
        if p.next_direction == "E":
            inside = "NE" if "E" in inside else "SW"
        else:
            inside = "NE" if "N" in inside else "SW"
    elif p.char == "-":
        inside = "N" if "N" in inside else "S"
    elif p.char == "7":
        if p.next_direction == "W":
            inside = "SW" if "W" in inside else "NE"
        else:
            inside = "SW" if "S" in inside else "NE"
    map[p.coordinate[1]][p.coordinate[0]] = inside
for i in range(len(map)):
    row = map[i]
    for j in range(len(row)):
        if map[i][j] not in ["O", "N","S","E","W","NE","NW","SE","SW","I"]:
            left = j - 1
            up = i - 1
            right = j + 1
            down = i + 1
            if left > 0 and ("E" in map[i][left] or "I" in map[i][left]):
                map[i][j] = "I"
                continue
            elif up > 0 and ("S" in map[up][j] or "I" in map[up][j]):
                map[i][j] = "I"
                continue
            elif right < len(row) and ("W" in map[i][right] or "I" in map[i][right]):
                map[i][j] = "I"
                continue
            elif down < len(map) and ("N" in map[down][j] or "I" in map[down][j]):
                map[i][j] = "I"
                continue
            else:
                map[i][j] = "O"

total = 0
for row in map:
    total += len([char for char in row if char == "I"])
print(total)
    