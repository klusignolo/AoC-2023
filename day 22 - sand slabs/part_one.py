with open("bricks.txt", "r") as file:
    brick_lines = file.read().splitlines()
# slots 1 - 9 in 3x3 grid
# if same slot and one stack above, x supports y
# make list of stacks. Stack is a matrix of letters
# loop through stacks to determine x supports y
# loop through support stats to determine which bricks don't support anything
# can also use which bricks share support.
# AREA array of tubes filled with equal letters and spaces. When it's time to fall, start at lowest letter
# decrement all ocurrences of that letter until ONE of them would contact another letter. Then move to next letter
class Brick:
    def __init__(self, name: str, dimensions: str):
        self.supports: set[str] = set()
        self.supported_by: set[str] = set()
        d0 = dimensions[0].split(",")
        d1 = dimensions[1].split(",")
        self.name = name
        self.max_x = int(d1[0])
        self.max_y = int(d1[1])
        self.max_z = int(d1[2])
        self.min_x = int(d0[0])
        self.min_y = int(d0[1])
        self.min_z = int(d0[2])
        self.x_range = int(d1[0]) - int(d0[0])
        self.y_range = int(d1[1]) - int(d0[1])
        self.z_range = int(d1[2]) - int(d0[2])
EMPTY = "."
bricks: dict[str, Brick] = {}
id_count = 0
for brick in brick_lines:
    dimensions = brick.split("~")
    bricks[str(id_count)] = Brick(str(id_count), dimensions)
    id_count += 1
max_x = max([brick.max_x for brick in bricks.values()])
max_y = max([brick.max_y for brick in bricks.values()])
max_z = max([brick.max_z for brick in bricks.values()])
stacks = [[[EMPTY for _ in range(max_z+1)] for _ in range(max_x+1)] for _ in range(max_y+1)]
for brick in bricks.values():
    for x in range(brick.min_x, brick.max_x+1):
        for y in range(brick.min_y, brick.max_y+1):
            for z in range(brick.min_z, brick.max_z+1):
                stacks[x][y][z] = brick.name

def can_move_down(brick: Brick):
    for x in range(brick.min_x, brick.max_x+1):
        for y in range(brick.min_y, brick.max_y+1):
            for z in range(brick.min_z, brick.max_z+1):
                if brick.max_z - brick.min_z > 0:
                    if (stacks[x][y][z-1] != EMPTY and stacks[x][y][z-1] != brick.name) or z == 0:
                        return False
                else:
                    if stacks[x][y][z-1] != EMPTY or z == 0:
                        return False
    return True

def move_brick_down(brick: Brick):
    for x in range(brick.min_x, brick.max_x+1):
        for y in range(brick.min_y, brick.max_y+1):
            for z in range(brick.min_z, brick.max_z+1):
                stacks[x][y][z-1] = brick.name
                stacks[x][y][z] = EMPTY
    brick.min_z -= 1
    brick.max_z -= 1

def print_stacks():
    for width in stacks:
        for length in width:
            print(",".join(length))

for brick in sorted(bricks.values(),key= lambda x: x.min_z):
    is_at_bottom = False
    while not is_at_bottom:
        if can_move_down(brick):
            move_brick_down(brick)
            #print_stacks()
        else:
            is_at_bottom = True


for x in range(len(stacks)):
    for y in range(len(stacks[x])):
        for z in range(len(stacks[x][y]) - 1):

            this_brick: Brick = stacks[x][y][z] if stacks[x][y][z] != EMPTY else None
            that_brick: Brick = stacks[x][y][z+1] if stacks[x][y][z+1] != EMPTY else None
            if this_brick:
                if that_brick and this_brick and that_brick != this_brick:
                    bricks[this_brick].supports.add(that_brick)
                    bricks[that_brick].supported_by.add(this_brick)

disappear = 0
for brick in bricks.values():
    can_dissolve = True
    for supported_brick in brick.supports:
        if len(bricks[supported_brick].supported_by) == 1:
            can_dissolve = False
            break
    disappear += 1 if can_dissolve else 0
print(disappear)