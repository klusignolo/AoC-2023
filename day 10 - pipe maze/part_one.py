with open ("loop.txt", "r") as file:
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
loop_len = 0
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
    loop_len += 1
    finished_loop = curr_char == "S"
furthest = loop_len / 2
print(furthest)
    