from sympy.utilities.iterables import multiset_permutations
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

def get_possibilities_for_line_2(line: str):
    record = line.split()[0]
    b_list = [int(i) for i in line.split()[1].split(",")]
    total_b_needed = sum(b_list)
    b_count = len([i for i in record if i == "#"])
    q_count = len([char for char in record if char == "?"])
    b_to_q = total_b_needed - b_count
    p_to_q = q_count - b_to_q
    perm_zero = ("1" * p_to_q) + ("0" * b_to_q)
    if b_to_q == 0:
        perms = [perm_zero]
    else:
        perms = list(multiset_permutations([char for char in perm_zero]))
    possibilities = 0
    c_num = 0
    for perm in perms:
        valid_combo = int("".join(perm), 2)
        record_to_try = record
        while valid_combo > 0:
            char = "." if valid_combo & 1 else "#"
            record_to_try = record_to_try.replace("?", char, 1)
            valid_combo = valid_combo >> 1
        record_to_try = record_to_try.replace("?", "#")
        if does_record_pass(record_to_try, b_list):
            possibilities += 1
        c_num += 1
        print(f"\rBrute forcing {len(perms)} combinations. {c_num}/{len(perms)}", end="")
    return possibilities

# def get_possibilities_for_line(line: str):
#     record = line.split()[0]
#     b_list = [int(i) for i in line.split()[1].split(",")]
#     total_b_needed = sum(b_list)
#     b_count = len([i for i in record if i == "#"])
#     q_count = len([char for char in record if char == "?"])
#     b_to_q = total_b_needed - b_count
#     p_to_q = q_count - b_to_q
#     perm_zero = ("1" * p_to_q) + ("0" * b_to_q)
#     if b_to_q == 0:
#         perms = [perm_zero]
#     else:
#         perms = list(multiset_permutations([char for char in perm_zero]))
#     possibilities = 0
#     c_num = 0
#     for perm in perms:
#         valid_combo = int("".join(perm), 2)
#         record_to_try = record
#         while valid_combo > 0:
#             char = "." if valid_combo & 1 else "#"
#             record_to_try = record_to_try.replace("?", char, 1)
#             valid_combo = valid_combo >> 1
#         record_to_try = record_to_try.replace("?", "#")
#         if does_record_pass(record_to_try, b_list):
#             possibilities += 1
#         c_num += 1
#         print(f"\rBrute forcing {len(perms)} combinations. {c_num}/{len(perms)}", end="")
#     return possibilities

def get_permutations(max_possibilities: int, p_count: int):
    for i in range(max_possibilities):
        i_copy = i
        p_needed = p_count
        while i_copy > 0 and p_needed > 0:
            if i_copy & 1:
                p_needed -= 1
            i_copy = i_copy >> 1
        is_valid = i_copy == 0 and p_needed == 0
        if is_valid:
            yield i

def get_possibilities_for_line_1(line: str):
    record = line.split()[0]
    b_list = [int(i) for i in line.split()[1].split(",")]
    p_count = len(record) - sum(b_list) - len([i for i in record if i == "."])
    q_count = len([char for char in record if char == "?"])
    max_possibilities = int("1" * q_count, 2)
    possibilities = 0
    c_num = 0
    for valid_combo in get_permutations(max_possibilities, p_count):
        record_to_try = record
        while valid_combo > 0:
            char = "." if valid_combo & 1 else "#"
            record_to_try = record_to_try.replace("?", char, 1)
            valid_combo = valid_combo >> 1
        record_to_try = record_to_try.replace("?", "#")
        if does_record_pass(record_to_try, b_list):
            possibilities += 1
        c_num += 1
        if c_num % 10000 == 0:
            print(f"\rBrute forcing combinations. {c_num} tried", end="")
    return max(1, possibilities)

def read_results():
    with open("results2.txt", "r") as file:
        return {int(result.split()[0]): int(result.split()[1]) for result in file.read().splitlines() if result != ''}

def save_results(results: dict[int,int]):
    results = dict(sorted(results.items()))
    with open("results2.txt", "w") as result_file:
        for k, v in results.items():
            result_file.write(f"{k} {v}\n")

possibilities = 0
r_num = 0
for line in records:
    stored_results = read_results()
    max_result = max(stored_results.keys())
    r_num += 1
    if r_num < max_result and r_num in stored_results.keys():
        print(f"\rStored line {r_num} value was {stored_results[r_num]}", end="")
        possibilities += stored_results[r_num]
        continue
    elif r_num == max_result:
        print(f"\rCurrently crunching line {r_num} elsewhere.", end="")
        continue
    else:
        if r_num not in stored_results.keys():
            stored_results[r_num] = -1
            save_results(stored_results)

    print(f"\nCalculating line {r_num}")
    base_combos = get_possibilities_for_line_1(line)

    record = line.split()[0]
    blist = line.split()[1]
    extended_line = f"{record}?{record} {blist},{blist}"
    print(f"\nCalculating extended line {r_num}")
    if record.startswith("#") or record.endswith("#"):
        total_combos = base_combos ** 5
    else:
        extended_combos = get_possibilities_for_line_1(extended_line)
        total_combos = base_combos * (int(extended_combos / base_combos) ** 4)
    stored_results = read_results()
    stored_results[r_num] = total_combos
    save_results(stored_results)
    print(f"\nLine {r_num} had {total_combos} valid combinations")
    possibilities += total_combos
# 1390263395754 LOW
print(possibilities)
fart = input("We did it!")