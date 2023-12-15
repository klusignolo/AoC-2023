with open("reflections.txt", "r") as file:
    reflections = [foo.splitlines() for foo in file.read().replace(".","0").replace("#","1").split("\n\n")]
answer = 0
for reflection in reflections:
    rows = [row for row in reflection]
    cols = ["" for _ in range(len(reflection[0]))]
    for row in range(len(reflection)):
        for col in range(len(reflection[row])):
            cols[col] += reflection[row][col]
    cols = ["".join(col) for col in cols]
    
    # check for vertical reflection
    v_reflect_check = []
    is_vertical = False
    while len(cols) > 1:
        v_reflect_check.insert(0, cols.pop(0))
        is_reflection = True
        one_diffs_remaining = 1
        for i in range(min(len(v_reflect_check), len(cols))):
            diff = 0
            for j in range(len(v_reflect_check[i])):
                if v_reflect_check[i][j] != cols[i][j]:
                    diff += 1
                if diff > 1:
                    is_reflection = False
                    break
            if diff == 1 and one_diffs_remaining != 1:
                is_reflection = False
            elif diff == 1:
                one_diffs_remaining -= 1
        if is_reflection and one_diffs_remaining == 0:
            is_vertical = True
            answer += len(v_reflect_check)
            break
    if is_vertical: continue
    # check for horizontal
    h_reflect_check = []
    while len(rows) > 1:
        h_reflect_check.insert(0, rows.pop(0))
        is_reflection = True
        one_diffs_remaining = 1
        for i in range(min(len(h_reflect_check), len(rows))):
            diff = 0
            for j in range(len(h_reflect_check[i])):
                if h_reflect_check[i][j] != rows[i][j]:
                    diff += 1
                if diff > 1:
                    is_reflection = False
                    break
            if diff == 1 and one_diffs_remaining != 1:
                is_reflection = False
            elif diff == 1:
                one_diffs_remaining -= 1
        if is_reflection and one_diffs_remaining == 0:
            answer += 100 * len(h_reflect_check)
            break
print(answer)