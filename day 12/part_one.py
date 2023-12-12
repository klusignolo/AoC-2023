with open("test.txt", "r") as file:
    records = file.read().splitlines()
for line in records:
    record = line.split()[0]
    b_list = [int(i) for i in line.split()[1].split(",")]
    w_remain = len(record) - sum(b_list) - len([i for i in record if i == "."])
    sections = [section for section in record.split(".") if len(section) > 0]
    current_b = 0
    for section in sections:
        b_copy = b_list.copy()
        if len(section) > b_list[current_b] + 1:
            pass
    print(sections)
