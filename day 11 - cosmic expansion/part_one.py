with open("stars.txt", "r") as file:
    universe = [[i for i in line] for line in file.read().splitlines()]

def expand(input: list[list[str]], direction: str):
    indices_to_expand = []
    if direction == "ns":
        for i in range(len(input)):
            if len(set(input[i])) == 1:
                indices_to_expand.append(i)
    elif direction == "ew":
        cols = [set() for _ in range(len(input[0]))]
        for i in range(len(input)):
            for j in range(len(input[i])):
                cols[j].add(input[i][j])
        for i in range(len(cols)):
            if len(cols[i]) == 1:
                indices_to_expand.append(i)
    width = len(input[0])
    for i in range(len(indices_to_expand)):
        if direction == "ns":
            input.insert(indices_to_expand[i] + i, ["." for _ in range(width)])
        elif direction == "ew":
            for row in input:
                row.insert(indices_to_expand[i] + i, ".")

class Star:
    def __init__(self, id: int, row: int, col: int, stars_below: list[int]):
        self.id = id
        self.row = row
        self.col = col
        self.stars_below: list[Star] = stars_below

def calculate_distances(universe: list[list[str]]):
    stars: list[Star] = []
    for i, row in enumerate(universe):
        for j, point in enumerate(row):
            if point == "#":
                new_star = Star(id=len(stars)+1, row=i+1, col=j+1, stars_below=[])
                for star in stars:
                    star.stars_below.append(new_star)
                stars.append(new_star)
    distance = 0
    for s1 in stars:
        for s2 in s1.stars_below:
            distance += (max(s2.row, s1.row) - min(s1.row, s2.row)) + (max(s2.col, s1.col) - min(s2.col, s1.col))
    return distance


expand(universe, "ns")
expand(universe, "ew")
for row in universe:
    print(row)
answer = calculate_distances(universe)
print(answer)