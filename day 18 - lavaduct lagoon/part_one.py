import re
with open("test.txt", "r") as file:
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
        min_left -= growth_needed
        X += growth_needed
        for i in range(moves):
            X -= 1
            dig_site[Y][X] = "#"
    elif direction == "U":
        growth_needed = abs(min(0, Y - moves - min_up))
        for grow_up in range(growth_needed):
            dig_site.insert(0,["." for _ in range(max_right - min_left + 1)])
        min_up -= growth_needed
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
for row in dig_site:
    is_inside = False
    prev_char = "."
    for char in row:
        if char == "." and prev_char == "#":
            is_inside = not is_inside
        prev_char = char
        area += 1 if is_inside or char == "#" else 0

print(area)
