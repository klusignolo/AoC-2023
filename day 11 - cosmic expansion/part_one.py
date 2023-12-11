with open("test.txt", "r") as file:
    universe = [[i for i in line] for line in file.read().splitlines()]

def expand(input: list[list[str]], direction: str):
    indices_to_expand = []
    if direction == "ns":
        for i in range(len(input)):
            if len(set(input[i])) == 1:
                indices_to_expand.append(i)
    elif direction == "ew":
        cols = [set() for _ in range(len(input))]
        for i in range(len(input)):
            for j in range(len(input[i])):
                cols[j].add(input[i][j])
        for i in range(len(cols)):
            if len(cols[i]) == 1:
                indices_to_expand.append(i)
    width = len(input[0])
    expanded_so_far = 0
    for i in range(len(indices_to_expand)):
        if direction == "ns":
            input.insert(indices_to_expand[i] + expanded_so_far, ["." for _ in range(width)])
            expanded_so_far += 1
        elif direction == "ew":
            for i in range(len(indices_to_expand)):
                expanded_so_far = 0
                for row in input:
                    row.insert(indices_to_expand[i] + expanded_so_far, ".")
                expanded_so_far += 1

def calculate_distances(universe: list[list[str]]):
    stars = {}

expand(universe, "ns")
expand(universe, "ew")
for row in universe:
    print(row)
answer = calculate_distances()
print(answer)