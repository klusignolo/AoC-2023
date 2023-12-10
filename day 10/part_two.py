with open ("test.txt", "r") as file:
    map = [[char for char in line] for line in file.read().splitlines()]

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
path = [curr_coord]
while not finished_loop:
    up = (curr_coord[0], curr_coord[1]-1) if curr_coord[1] > 0 else None
    right = (curr_coord[0] + 1, curr_coord[1]) if curr_coord[0] < len(map[0]) - 1 else None
    down = (curr_coord[0], curr_coord[1] + 1) if curr_coord[1] < len(map) - 1 else None
    left = (curr_coord[0] - 1, curr_coord[1]) if curr_coord[0] > 0 else None
    if up and up != prev_coord and curr_char in ["|", "J", "L", "S"] and map[up[1]][up[0]] in ["|", "7", "F", "S"]:
        prev_coord = curr_coord
        curr_coord = up
        curr_char = map[up[1]][up[0]]
    elif right and right != prev_coord and curr_char in ["-","L","F", "S"] and map[right[1]][right[0]] in ["-","7","J", "S"]:
        prev_coord = curr_coord
        curr_coord = right
        curr_char = map[right[1]][right[0]] 
    elif down and down != prev_coord and curr_char in ["|", "7", "F", "S"] and map[down[1]][down[0]] in ["|", "L", "J", "S"]:
        prev_coord = curr_coord
        curr_coord = down
        curr_char = map[down[1]][down[0]]
    elif left and left != prev_coord and curr_char in ["-", "7", "J", "S"] and map[left[1]][left[0]] in ["-", "F", "L", "S"]:
        prev_coord = curr_coord
        curr_coord = left
        curr_char = map[left[1]][left[0]]
    finished_loop = curr_char == "S"
    if not finished_loop:
        path.append(curr_coord)

# set path to + 
for path_coord in path:
    map[path_coord[1]][path_coord[0]] = "+"

for row in map:
    left = 0
    right = len(row) - 1
    while left != -1 or right != -1:
        if left != -1 and left < len(row) and row[left] != "+":
            row[left] = "O"
            left += 1
        else:
            left = -1
        if right != -1 and right >= 0 and row[right] != "+":
            row[right] = "O"
            right -= 1
        else:
            right = -1
for col in range(len(map[0])):
    top = 0
    bot = len(map) - 1
    while top != -1 or bot != -1:
        if top != -1 and top < len(map) and map[top][col] != "+":
            map[top][col] = "O"
            top += 1
        else:
            top = -1
        if bot != -1 and bot >= 0 and map[bot][col] != "+":
            map[bot][col] = "O"
            bot -= 1
        else:
            bot = -1

for row in map:
    outside_loop = True
    for i in range(len(row)):
        if row[i] == "+":
            outside_loop = not outside_loop
            continue
        elif row[i] == "O":
            continue
        row[i] = "O" if outside_loop else "I"
total = 0
for row in map:
    print(row)
    total += len([char for char in row if char == "I"])
print(total)
    