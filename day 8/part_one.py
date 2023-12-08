import re

with open("nodes.txt", "r") as file:
    lines = file.read().splitlines()
    instructions = [int(instruction) for instruction in lines.pop(0).replace("L", "0").replace("R", "1")]
    nodes = {}
    for line in lines:
        parse = re.findall(r"[A-Z]{3}", line)
        nodes[parse[0]] = [parse[1], parse[2]]
instruction_count = 0
current_nodes = [node for node in nodes.keys() if node.endswith("A")]
still_searching = True
while still_searching:
    for instruction in instructions:
        instruction_count += 1
        current_nodes = [nodes[current_node][instruction] for current_node in current_nodes]

        number_of_z = 0
        for node in current_nodes:
            still_searching = not node.endswith("Z")
            if still_searching:
                number_of_z = 0
                break
            else:
                number_of_z += 1
                if number_of_z > 1:
                    print(f"Found {number_of_z} Zs! Instruction count: {instruction_count}")
        if not still_searching:
            break
print(instruction_count)