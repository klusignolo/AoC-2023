from copy import deepcopy

with open("path.txt", "r") as file:
    paths = [[char for char in line] for line in file.read().splitlines()]

for i, space in enumerate(paths[0]):
    if space == ".":
        beginning = (0, i)
        break
for i, space in enumerate(paths[len(paths) - 1]):
    if space == ".":
        destination = (len(paths)-1, i)
        break

def space_key(coord: tuple[int,int], bearing):
    return f"{coord[0]},{coord[1]},{bearing}"

unended_paths = [[(space_key(beginning, "d"),beginning)]]
finished_paths = []
def trace_next_paths():
    dead_ends = []
    paths_to_trace = deepcopy(unended_paths)
    for path_i, path in enumerate(paths_to_trace):
        coords_so_far = [space[1] for space in path]
        last_space = path[len(path) - 1][0]
        parsed_key = last_space.split(",")
        x = int(parsed_key[1])
        y = int(parsed_key[0])
        bearing = parsed_key[2]
        next_x = x if bearing == "u" or bearing == "d" else x+1 if bearing == "r" else x - 1
        next_y = y if bearing == "r" or bearing == "l" else y+1 if bearing == "d" else y - 1
        next_coord = (next_y, next_x)
        if next_coord in coords_so_far:
            dead_ends.append(path_i)
            continue
        up = None if bearing == "d" or next_y == 0 else paths[next_y - 1][next_x]
        right = None if bearing == "l" or next_x == len(paths[0])-1  else paths[next_y][next_x + 1]
        down = None if bearing == "u" or next_y == len(paths)-1 else paths[next_y + 1][next_x]
        left = None if bearing == "r" or next_x == 0 else paths[next_y][next_x - 1]
        next_paths = []
        if up and up != "#":
            up_key = space_key(next_coord, "u")
            if up_key not in path:
                next_paths.append((up_key, next_coord))
        if right and right != "#":
            right_key = space_key(next_coord, "r")
            if right_key not in path:
                next_paths.append((right_key, next_coord))
        if down and down != "#":
            down_key = space_key(next_coord, "d")
            if down_key not in path:
                next_paths.append((down_key, next_coord))
        if left and left != "#":
            left_key = space_key(next_coord, "l")
            if left_key not in path:
                next_paths.append((left_key, next_coord))
        if len(next_paths) == 0:
            if (next_y, next_x) == destination:
                unended_paths[path_i].append((space_key(next_coord, "d"), next_coord))
            dead_ends.append(path_i)
            continue

        original_path = deepcopy(path)
        do_new_paths = False
        while len(next_paths) > 0:
            path_to_append = next_paths.pop(0)
            if do_new_paths:
                new_path = deepcopy(original_path)
                new_path.append(path_to_append)
                unended_paths.append(new_path)
            else:
                unended_paths[path_i].append(path_to_append)
                do_new_paths = True
    dead_ends.sort(reverse=True)
    for path_i in dead_ends:
        path = unended_paths.pop(path_i)
        last_space = path[len(path) - 1]
        if last_space[1] == destination:
            finished_paths.append(path)
    dead_ends = []


while len(unended_paths) > 0:
    trace_next_paths()
longest_path = 0
for finished_path in finished_paths:
    longest_path = max(longest_path, len(finished_path)-1)
print(longest_path)