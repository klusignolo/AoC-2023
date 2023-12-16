with open("test.txt", "r") as file:
    tile_matrix = [[char for char in line] for line in file.read().splitlines()]
visited_tiles = []
next_beam_key = 0
beams = {next_beam_key: (0,0,"r")}
breadth = len(tile_matrix)-1
while len(beams) > 0:
    dead_beams = []
    new_beams = []
    for beam_key, beam in beams.items():
        x, y, dir = beam
        visited_tiles.append((x, y))
        x += 1 if dir == "r" else -1 if dir == "l" else 0
        y += 1 if dir == "d" else -1 if dir == "u" else 0
        if x < 0 or y < 0 or x > breadth or y > breadth:
            dead_beams.append(beam_key)
            continue
        next_tile = tile_matrix[y][x]
        if next_tile == ".":
            beams[beam_key] = (x, y, dir)
        elif next_tile == "|":
            if dir == "u" or dir == "d":
                beams[beam_key] = (x, y, dir)
            else:
                beams[beam_key] = (x, y, "u")
                new_beams.append((x, y, "d"))
        elif next_tile == "-":
            if dir == "r" or dir == "l":
                beams[beam_key] = (x, y, dir)
            else:
                beams[beam_key] = (x, y, "l")
                new_beams.append((x, y, "r"))
        elif next_tile == "\\":
            if dir == "r":
                beams[beam_key] = (x, y, "d")
            elif dir == "l":
                beams[beam_key] = (x, y, "u")
            elif dir == "u":
                beams[beam_key] = (x, y, "l")
            else:
                beams[beam_key] = (x, y, "r")
        elif next_tile == "/":
            if dir == "r":
                beams[beam_key] = (x, y, "u")
            elif dir == "l":
                beams[beam_key] = (x, y, "d")
            elif dir == "u":
                beams[beam_key] = (x, y, "r")
            else:
                beams[beam_key] = (x, y, "l")
    for key in dead_beams:
        del beams[key]
    for new_beam in new_beams:
        next_beam_key += 1
        beams[next_beam_key] = new_beam
answer = len(set(visited_tiles))
print(answer)