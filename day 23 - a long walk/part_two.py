from copy import deepcopy
from string import ascii_uppercase as letters
""" THIS IS ALL UGLY. GL HF """
def next_letter()-> str:
    for l1 in letters:
        for l2 in letters:
            for l3 in letters:
                yield f"{l1}{l2}{l3}"
chunk_key = next_letter()

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

first_chunk = next(chunk_key)
last_chunk = next(chunk_key)
chunks = {first_chunk: beginning,
          last_chunk: destination}
chunks_in_progress: dict[str,list[list[str]]] = {first_chunk: [[space_key(beginning, "d")]]}
chunk_lengths: dict[str,int] = {}
chunk_conns: dict[str,list[str]] = {}
def trace_next_paths():
    progress_chunks_copy = deepcopy(chunks_in_progress)
    for chunk_name, chunk_paths in progress_chunks_copy.items():
        dead_ends = []
        for path_i, path in enumerate(chunk_paths):
            last_space = path[len(path) - 1]
            parsed_key = last_space.split(",")
            x = int(parsed_key[1])
            y = int(parsed_key[0])
            bearing = parsed_key[2]
            next_x = x if bearing == "u" or bearing == "d" else x+1 if bearing == "r" else x - 1
            next_y = y if bearing == "r" or bearing == "l" else y+1 if bearing == "d" else y - 1
            next_coord = (next_y, next_x)
            up = None if bearing == "d" or next_y == 0 else paths[next_y - 1][next_x]
            right = None if bearing == "l" or next_x == len(paths[0])-1  else paths[next_y][next_x + 1]
            down = None if bearing == "u" or next_y == len(paths)-1 else paths[next_y + 1][next_x]
            left = None if bearing == "r" or next_x == 0 else paths[next_y][next_x - 1]
            next_paths = []
            if up and up != "#":
                up_key = space_key(next_coord, "u")
                if up_key not in path:
                    next_paths.append(up_key)
            if right and right != "#":
                right_key = space_key(next_coord, "r")
                if right_key not in path:
                    next_paths.append(right_key)
            if down and down != "#":
                down_key = space_key(next_coord, "d")
                if down_key not in path:
                    next_paths.append(down_key)
            if left and left != "#":
                left_key = space_key(next_coord, "l")
                if left_key not in path:
                    next_paths.append(left_key)

            if len(next_paths) == 0:
                dead_ends.append(path_i)
                if next_coord == destination:
                    chunk_combo_key = f"{chunk_name}-{last_chunk}"
                    chunk_lengths[chunk_combo_key] = len(path)
                    if chunk_name in chunk_conns:
                        chunk_conns[chunk_name].append(last_chunk)
                    else:
                        chunk_conns[chunk_name] = [last_chunk]
                continue
            elif len(next_paths) > 1:
                # Fork in road!
                if next_coord in chunks.values():
                    if next_coord == chunks[chunk_name]:
                        # Path was a loop dead end
                        dead_ends.append(path_i)
                        continue
                    else:
                        # path hit a known fork in the road
                        for k, v in chunks.items():
                            if v == next_coord:
                                # take longest path between fork A and fork B
                                chunk_combo_key = f"{chunk_name}-{k}"
                                if chunk_name in chunk_conns:
                                    chunk_conns[chunk_name].append(k)
                                else:
                                    chunk_conns[chunk_name] = [k]
                                if chunk_combo_key in chunk_lengths.keys():
                                    chunk_lengths[chunk_combo_key] = max(len(path), chunk_lengths[chunk_combo_key])
                                else:
                                    chunk_lengths[chunk_combo_key] = len(path)
                        dead_ends.append(path_i)
                        continue
                else:
                    # new fork in road
                    next_chunk = next(chunk_key)
                    chunks[next_chunk] = next_coord
                    chunk_combo_key = f"{chunk_name}-{next_chunk}"
                    chunk_lengths[chunk_combo_key] = len(path)
                    dead_ends.append(path_i)
                    chunks_in_progress[next_chunk] = [[path_start] for path_start in next_paths]
                    
                    if chunk_name in chunk_conns:
                        chunk_conns[chunk_name].append(next_chunk)
                    else:
                        chunk_conns[chunk_name] = [next_chunk]
                    if next_chunk in chunk_conns:
                        chunk_conns[next_chunk].append(chunk_name)
                    else:
                        chunk_conns[next_chunk] = [chunk_name]
                    continue
            path_to_append = next_paths.pop(0)
            chunks_in_progress[chunk_name][path_i].append(path_to_append)
        dead_ends.sort(reverse=True)
        for path_i in dead_ends:
            chunks_in_progress[chunk_name].pop(path_i)
        dead_ends = []

unended_paths = 1
while unended_paths > 0:
    trace_next_paths()
    unended_paths = sum([len(tracing_paths) for tracing_paths in chunks_in_progress.values()])

final_paths = []
def calc_chunk_paths(next_chunk: str, incoming_path: str) -> list[str]:
    next_chunks = chunk_conns[next_chunk]
    for nc in next_chunks:
        if nc not in incoming_path:
            new_path = incoming_path + "," + nc
            if nc == last_chunk:
                final_paths.append(new_path)
            else:
                calc_chunk_paths(nc, new_path)
calc_chunk_paths(first_chunk, first_chunk)

mirror_lengths = []
for key, val in chunk_lengths.items():
    foo = key.split('-')
    mirror = f"{foo[1]}-{foo[0]}"
    mirror_lengths.append((mirror, val))
for mirror in mirror_lengths:
    chunk_lengths[mirror[0]] = mirror[1]

path_lengths = []
for final_path in final_paths:
    path_length = 0
    chunk_order = final_path.split(",")
    for i in range(len(chunk_order)-1):
        chunk_combo_key = chunk_order[i]+"-"+chunk_order[i+1]
        path_length += chunk_lengths[chunk_combo_key]
    path_lengths.append((path_length, final_path))
for key, val in chunks.items():
    paths[val[0]][val[1]] = key
for row in paths:
    print("".join(row))
longest_path = max([pl[0] for pl in path_lengths])
print(longest_path)