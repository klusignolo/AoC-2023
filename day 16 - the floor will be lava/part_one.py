with open("beams.txt", "r") as file:
    tile_matrix = [[char for char in line] for line in file.read().splitlines()]
breadth = len(tile_matrix)-1
unique_keys = []
def do_next_beam_paths(beam_keys: list[str]):
    next_paths = []
    for path in beam_keys:
        if path in unique_keys:
            continue
        else:
            unique_keys.append(path)
        x, y, dir = path.split(",")
        x = int(x)
        y = int(y)
        x += 1 if dir == "r" else -1 if dir == "l" else 0
        y += 1 if dir == "d" else -1 if dir == "u" else 0
        if x < 0 or y < 0 or x > breadth or y > breadth:
            continue
        next_tile = tile_matrix[y][x]
        if next_tile == ".":
            next_paths.append(f"{x},{y},{dir}")
        elif next_tile == "|":
            if dir == "u" or dir == "d":
                next_paths.append(f"{x},{y},{dir}")
            else:
                next_paths.extend([f"{x},{y},u",f"{x},{y},d"])
        elif next_tile == "-":
            if dir == "r" or dir == "l":
                next_paths.append(f"{x},{y},{dir}")
            else:
                next_paths.extend([f"{x},{y},l",f"{x},{y},r"])
        elif next_tile == "\\":
            if dir == "r":
                next_paths.append(f"{x},{y},d")
            elif dir == "l":
                next_paths.append(f"{x},{y},u")
            elif dir == "u":
                next_paths.append(f"{x},{y},l")
            else:
                next_paths.append(f"{x},{y},r")
        elif next_tile == "/":
            if dir == "r":
                next_paths.append(f"{x},{y},u")
            elif dir == "l":
                next_paths.append(f"{x},{y},d")
            elif dir == "u":
                next_paths.append(f"{x},{y},r")
            else:
                next_paths.append(f"{x},{y},l")
    return next_paths

next_paths = ["0,0,d"]
while len(next_paths):
    next_paths = do_next_beam_paths(next_paths)

answer = len(set([",".join(key.split(",")[:2]) for key in unique_keys]))
# 7736 HIGH
print(answer)