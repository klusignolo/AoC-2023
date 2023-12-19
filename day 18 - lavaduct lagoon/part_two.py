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
    hex_instructions = re.findall(r"\(#(\S+)\)", instructions[2])[0]
    moves = int(hex_instructions[:5], 16)
    direction_int = int(hex_instructions[5])
    direction = "R" if direction_int == 0 else "D" if direction_int == 1 else "L" if direction_int == 2 else "U"
# GL HF
