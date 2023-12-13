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
    print(f"Calculating extended line {r_num}")
    if line.split()[0].endswith("#"):
        extended_combos = valid_combos_found
    elif line.split()[0].endswith("?"):
        new_line = f"{line.split()[0]}? {line.split()[1]}"
        extended_combos = get_possibilities_for_line(new_line)
    else:
        extended_combos = get_possibilities_for_line("?" + line)
    for _ in range(4):
        valid_combos_found *= extended_combos
    print(f"Line {r_num} yielded {valid_combos_found} combos!")
    possibilities += valid_combos_found
print(possibilities)