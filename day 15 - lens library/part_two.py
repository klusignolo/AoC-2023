import re
def holiday_hash(digest: str) -> int:
    ret_val = 0
    for char in digest:
        ret_val += ord(char)
        ret_val *= 17
        ret_val %= 256
    return ret_val

boxes = {i: {} for i in range(256)}
with open("sequence.txt", "r") as file:
    sequence = file.read().split(",")

for instruction in sequence:
    label = re.findall(r"(\w+)[-=]{1}", instruction)[0]
    focal_length_search = re.findall(r"=(\d+)", instruction)
    focal_length = int(focal_length_search[0]) if len(focal_length_search) else None
    box = boxes[holiday_hash(label)]
    add_to_box = focal_length is not None
    if add_to_box:
        box[label] = focal_length
    else:
        if label in box.keys():
            del box[label]

focusing_power = 0
for box_number, box in boxes.items():
    for slot_number, focal_length in enumerate(box.values()):
        focusing_power += (box_number + 1) * (slot_number + 1) * focal_length
print(focusing_power)
