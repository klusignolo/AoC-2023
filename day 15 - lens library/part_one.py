def holiday_hash(digest: str) -> int:
    ret_val = 0
    for char in digest:
        ret_val += ord(char)
        ret_val *= 17
        ret_val %= 256
    return ret_val

with open("sequence.txt", "r") as file:
    sequence = file.read().split(",")

answer = sum([holiday_hash(instruction) for instruction in sequence])

