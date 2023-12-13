with open("records.txt", "r") as file:
    records = file.read().splitlines()
def does_record_pass(record: str, hash_counts: list[int]) -> bool:
    b_list = hash_counts.copy()
    curr_broke = b_list.pop(0)
    chars = [char for char in record]
    hash_cnt = 0
    while len(chars) > 0:
        char = chars.pop(0)
        if char == "#":
            if curr_broke is None: return False
            hash_cnt += 1
        elif hash_cnt > 0:
            if curr_broke and hash_cnt != curr_broke:
                return False
            else:
                hash_cnt = 0
                curr_broke = None if not len(b_list) else b_list.pop(0)
        else:
            hash_cnt = 0
    if char == "#" and curr_broke == hash_cnt:
        hash_cnt = 0
        curr_broke = None
    return len(b_list) == 0 and hash_cnt == 0

def get_possibilities_for_line(line: str):
    record = line.split()[0]
    b_list = [int(i) for i in line.split()[1].split(",")]
    p_count = len(record) - sum(b_list) - len([i for i in record if i == "."])
    q_count = len([char for char in record if char == "?"])
    max_possibilities = int("1" * q_count, 2)
    valid_combos = []
    for i in range(max_possibilities):
        i_copy = i
        p_needed = p_count
        while i_copy > 0 and p_needed > 0:
            if i_copy & 1:
                p_needed -= 1
            i_copy = i_copy >> 1
        is_valid = i_copy == 0 and p_needed == 0
        if is_valid:
            valid_combos.append(i)
    possibilities = 0
    if len(valid_combos) == 0:
        possibilities += 1
    for valid_combo in valid_combos:
        record_to_try = record
        while valid_combo > 0:
            char = "." if valid_combo & 1 else "#"
            record_to_try = record_to_try.replace("?", char, 1)
            valid_combo = valid_combo >> 1
        record_to_try = record_to_try.replace("?", "#")
        if does_record_pass(record_to_try, b_list):
            possibilities += 1
    return possibilities
possibilities = 0
r_num = 0
for line in records:
    r_num += 1
    print(f"Calculating line {r_num}")
    valid_combos_found = get_possibilities_for_line(line)
    record = line.split()[0]
    b_list = [int(b) for b in line.split()[1].split(",")]
    if record.endswith("#") or record.startswith("#"):
        new_line = line
    # elif (record.startswith("?") and "#" not in record[0:b_list[0]]) and (record.endswith("?") and "#" not in record[-b_list[len(b_list)-1]:]):
    #     new_line = f"?{line.split()[0]}? {line.split()[1]}"
    # elif record.startswith("?") and "#" not in record[0:b_list[0]-1]:
    #     new_line = "?" + line
    # elif record.endswith("?") and "#" not in record[-b_list[len(b_list)-1]+1:]:
    #     new_line = f"{line.split()[0]}? {line.split()[1]}"
    else:
        # decide which end to put the ? by seeing which has more ??s
        l_count = 0
        r_count = 0
        l_done = False
        r_done = False
        for i in range(len(record)):
            l = record[i]
            r = record[len(record)-i-1]
            if not l_done:
                l_done = l != "?"
                if not l_done:
                    l_count += 1
            if not r_done:
                r_done = r != "?"
                if not r_done:
                    r_count += 1
            if l_done and r_done:
                break
        l_div = float(l_count) / float(b_list[0])
        r_div = float(r_count) / float(b_list[len(b_list)-1])
        choose_right = r_div > l_div
        if choose_right:
            new_line = f"{line.split()[0]}? {line.split()[1]}"
        else:
            new_line = "?" + line
    extended_combos = get_possibilities_for_line(new_line)
    for _ in range(4):
        valid_combos_found *= extended_combos
    #print(f"Line {r_num} yielded {valid_combos_found} combos!")
    possibilities += valid_combos_found
# 1337884717487 LOW
# 1364880608120 LOW
# 1365051289408 LOW
# 1390263395754 LOW
# 1288092254858 LOW?
# 1284720290750 LOW?
# 1287562879561 
# 7102876624527 WRONG?
print(possibilities)