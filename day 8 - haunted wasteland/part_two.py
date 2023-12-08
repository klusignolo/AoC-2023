import re

with open("nodes.txt", "r") as file:
    lines = file.read().splitlines()
    instructions = [int(instruction) for instruction in lines.pop(0).replace("L", "0").replace("R", "1")]
    nodes = {}
    for line in lines:
        parse = re.findall(r"[A-Z1-9]{3}", line)
        nodes[parse[0]] = [parse[1], parse[2]]
instruction_count = 0
current_nodes = [node for node in nodes.keys() if node.endswith("A")]
denominators = []
for current_node in current_nodes:
    while not current_node.endswith("Z"):
        for instruction in instructions:
            instruction_count += 1
            current_node = nodes[current_node][instruction]
            if current_node.endswith("Z"):
                denominators.append(instruction_count)
                instruction_count = 0
                break

d_copy = denominators.copy()
searching_for_lcm = True
while searching_for_lcm:
    max_denominator = max(d_copy)
    searching_for_lcm = False
    for i, d in enumerate(d_copy):
        if d < max_denominator:
            searching_for_lcm = True
            d_copy[i] += denominators[i]
print(d_copy[0])