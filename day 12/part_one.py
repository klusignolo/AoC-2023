with open("test.txt", "r") as file:
    records = file.read().splitlines()
for line in records:
    record = line.split()[0]
    b_list = [[int(j) for j in i] for i in line.split()[1].split(",")]
    sections = [section for section in record.split(".") if len(section) > 0]
    current_b = 0
    for section in sections:
        b_copy = b_list.copy()
        if len(section) > b_counts[current_b] + 1:
            
    print(sections)
