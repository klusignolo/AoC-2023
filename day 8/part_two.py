import re

with open("nodes.txt", "r") as file:
    lines = file.read().splitlines()
    instructions = [int(instruction) for instruction in lines.pop(0).replace("L", "0").replace("R", "1")]
    nodes = {}
    for line in lines:
        parse = re.findall(r"[A-Z]{3}", line)
        nodes[parse[0]] = [parse[1], parse[2]]
instruction_count = 0
current_node = "AAA"
while current_node != "ZZZ":
    for instruction in instructions:
        instruction_count += 1
        current_node = nodes[current_node][instruction]
        if current_node == "ZZZ": break
print(instruction_count)