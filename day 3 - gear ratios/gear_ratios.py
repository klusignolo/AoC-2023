filename = "schematic.txt"
schematic = None

with open(filename, "r") as file:
    schematic = file.read().splitlines()

gear_dict: dict[list[int]] = {}
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

            near_gear = False
            for i in range(lower_bound - upper_bound + 1):
                if near_gear: break
                row = upper_bound + i
                for j in range(right_bound - left_bound + 1):
                    col = left_bound + j
                    if schematic[row][col] == "*":
                        gear_key = f"{row}-{col}"
                        if gear_key in gear_dict:
                            gear_dict[gear_key].append(int(part_number))
                        else:
                            gear_dict[gear_key] = [int(part_number)]
                        near_gear = True
                        break
            part_number = ""
gear_ratio_sum = 0
for possible_gears in gear_dict.values():
    if len(possible_gears) == 2:
        gear_ratio = possible_gears[0] * possible_gears[1]
        gear_ratio_sum += gear_ratio
print(gear_ratio_sum)
