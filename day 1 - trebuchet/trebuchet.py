string_integers = [
    ("one","1"),
    ("two","2"),
    ("three","3"),
    ("four","4"),
    ("five","5"),
    ("six","6"),
    ("seven","7"),
    ("eight","8"),
    ("nine","9")
]

def get_calibration_sum(calibration_values: [str], check_for_numeric_strings: bool = False):
    calibration_sum = 0
    for value in calibration_values:
        left_pointer = 0
        right_pointer = len(value) - 1
        left_digit = None
        right_digit = None
        while (not left_digit or not right_digit) and (left_pointer < len(value) and right_pointer >= 0):
            if left_digit is None and value[left_pointer].isnumeric():
                left_digit = value[left_pointer]
            elif left_digit is None:
                if check_for_numeric_strings:
                    for string_integer in string_integers:
                        if value[left_pointer:].startswith(string_integer[0]):
                            left_digit = string_integer[1]
                if left_digit is None:
                    left_pointer += 1
            
            if right_digit is None and value[right_pointer].isnumeric():
                right_digit = value[right_pointer]
            elif right_digit is None:
                if check_for_numeric_strings:
                    for string_integer in string_integers:
                        if value[:right_pointer + 1].endswith(string_integer[0]):
                            right_digit = string_integer[1]
                if right_digit is None:
                    right_pointer -= 1

        calibration_sum += int(f"{left_digit}{right_digit}")

    return calibration_sum

filepath = "trebuchet.txt"
with open(filepath, "r") as calibration_document:
    calibration_values = calibration_document.readlines()
    part_one_solution = get_calibration_sum(calibration_values)
    part_two_solution = get_calibration_sum(calibration_values, check_for_numeric_strings=True)
    print(f"Solutions: Part 1 - {part_one_solution}, Part 2: {part_two_solution}")

