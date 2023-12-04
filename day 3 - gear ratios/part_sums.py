filename = "schematic.txt"
schematic = None

with open(filename, "r") as file:
    schematic = file.read().splitlines()

def is_special(char: str):
    return not char.isnumeric() and char != "."

part_numbers = []
max_row = len(schematic) - 1
max_col = len(schematic[0]) - 1
for row_index, schematic_row in enumerate(schematic):
    part_number = ""
    left_bound = 0
    right_bound = 0
    upper_bound = 0
    lower_bound = 0
    for col_index, char in enumerate(schematic_row):
        if char.isnumeric():
            if part_number == "":
                left_bound = max(0, col_index-1)
                part_number += char
            else:
                part_number += char
        elif part_number == "":
            continue
        if not char.isnumeric() or col_index == max_col:
            right_bound = min(max_col, col_index)
            upper_bound = max(0, row_index - 1)
            lower_bound = min(max_row, row_index + 1)

            part_found = False
            for i in range(lower_bound - upper_bound + 1):
                if part_found: break
                row = upper_bound + i
                for j in range(right_bound - left_bound + 1):
                    col = left_bound + j
                    if is_special(schematic[row][col]):
                        part_found = True
                        part_numbers.append(int(part_number))
                        break

            part_number = ""
print(sum(part_numbers))
