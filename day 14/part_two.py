with open("rocks.txt", "r") as file:
    rock_matrix = [[char for char in row] for row in file.read().replace(".","1").replace('O','0').splitlines()]
cols = ["" for _ in range(len(rock_matrix[0]))]
for i in range(len(rock_matrix)):
    for j in range(len(rock_matrix[0])):
        cols[j] += (rock_matrix[i][j])
total_weight = 0
# after spin north, shifted col[0] becomes row[0]

current_cols = cols
current_spin_cycle = 0
direction_facing = -1
repeats = {}
for i in range(10000):
    # 01234 == NWSE
    direction_facing += 1 if direction_facing != 3 else -3
    cols_pushed_up = []
    for col in current_cols:
        chunks = ["".join(sorted(chunk)) for chunk in col.split("#")]
        cols_pushed_up.append("#".join(chunks))
    # When cycle has completed, see if configuration already exists
    if direction_facing == 3:
        current_spin_cycle += 1
        hash_key = hash("".join(cols_pushed_up))
        if hash_key in repeats.keys():
            repeat_frequency = current_spin_cycle - repeats[hash_key][0]
            remaining_cycles = (1000000000 - current_spin_cycle) % repeat_frequency
            magic_cycle = repeats[hash_key][0] + remaining_cycles
            for val in repeats.values():
                if val[0] == magic_cycle:
                    cols_pushed_up = val[1]
                    break
            break
        else:
            repeats[hash_key] = [current_spin_cycle, cols_pushed_up]

    current_rows = [col[::-1] for col in cols_pushed_up]
    current_cols = ["" for _ in range(len(rock_matrix[0]))]
    for i in range(len(rock_matrix)):
        for j in range(len(current_rows[0])):
            current_cols[j] += (current_rows[i][j])

# at this point, each col represents a reversed row of north facing matrix
total_weight = 0
for i in range(len(cols_pushed_up)):
    col = cols_pushed_up[i]
    for char in col:
        total_weight += len(cols_pushed_up) - i if char == "0" else 0
print(total_weight)
foo = input("We did it!")