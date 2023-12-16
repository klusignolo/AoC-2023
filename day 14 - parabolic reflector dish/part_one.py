with open("rocks.txt", "r") as file:
    rock_matrix = [[char for char in row] for row in file.read().replace(".","1").replace('O','0').splitlines()]
cols = ["" for _ in range(len(rock_matrix[0]))]
for i in range(len(rock_matrix)):
    for j in range(len(rock_matrix[0])):
        cols[j] += (rock_matrix[i][j])
total_weight = 0
# after spin north, shifted col[0] becomes row[0]
for col in cols:
    chunks = ["".join(sorted(chunk)) for chunk in col.split("#")]
    col_pushed_north = "#".join(chunks)
    south_to_north_col = col_pushed_north[::-1]
    for i in range(len(south_to_north_col)):
        total_weight += i + 1 if south_to_north_col[i] == "0" else 0
print(total_weight)