with open("reflections.txt", "r") as file:
    reflections = [foo.splitlines() for foo in file.read().replace(".","0").replace("#","1").split("\n\n")]
answer = 0
for reflection in reflections:
    rows = [int(row,2) for row in reflection]
    cols = ["" for _ in range(len(reflection[0]))]
    for row in range(len(reflection)):
        for col in range(len(reflection[row])):
            cols[col] += reflection[row][col]
    cols = [int("".join(col), 2) for col in cols]
    
    # check for vertical reflection
    v_reflect_check = []
    is_vertical = False
    while len(cols) > 1:
        v_reflect_check.insert(0, cols.pop(0))
        is_reflection = True
        for i in range(min(len(v_reflect_check), len(cols))):
            if v_reflect_check[i] != cols[i]:
                is_reflection = False
                break
        if is_reflection:
            is_vertical = True
            answer += len(v_reflect_check)
            break
    if is_vertical: continue
    # check for horizontal
    h_reflect_check = []
    while len(rows) > 1:
        h_reflect_check.insert(0, rows.pop(0))
        is_reflection = True
        for i in range(min(len(h_reflect_check), len(rows))):
            if h_reflect_check[i] != rows[i]:
                is_reflection = False
                break
        if is_reflection:
            answer += 100 * len(h_reflect_check)
            break
print(answer)