with open("stones.txt", "r") as file:
    hailstones = file.read().splitlines()
Y = 1
X = 0
FLOOR = 200000000000000
CEILING = 400000000000000
class StonePath:
    def __init__(self, x_pos, y_pos, z_pos, x_vel, y_vel, z_vel):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.z_vel = z_vel
        self.moving_left = x_vel < 0
        self.moving_right = x_vel > 0
        self.moving_up = y_vel > 0
        self.moving_down = y_vel < 0
        self.P1 = (x_pos, y_pos)
        self.P2 = (x_pos + x_vel, y_pos + y_vel)

    # Modified from https://www.geeksforgeeks.org/program-for-point-of-intersection-of-two-lines/
    def intersection(self, other: "StonePath") -> tuple[int,int, bool]:
        a1 = self.P2[Y] - self.P1[Y]
        b1 = self.P1[X] - self.P2[X]
        c1 = a1*(self.P1[X]) + b1*(self.P1[Y])
    
        a2 = other.P2[Y] - other.P1[Y]
        b2 = other.P1[X] - other.P2[X]
        c2 = a2*(other.P1[X]) + b2*(other.P1[Y])
    
        determinant = a1*b2 - a2*b1
    
        if (determinant == 0):
            # The lines are parallel.
            return None
        else:
            x = (b2*c1 - b1*c2)/determinant
            y = (a1*c2 - a2*c1)/determinant
            intersection = (x,y)
            is_in_past = False
            if (self.moving_left and intersection[X] > self.P1[X]) or (self.moving_right and intersection[X] < self.P1[X]):
                is_in_past = True
            if (other.moving_left and intersection[X] > other.P1[X]) or (other.moving_right and intersection[X] < other.P1[X]):
                is_in_past = True
            return (x, y, is_in_past)

stones: list[StonePath] = []
for line in hailstones:
    parsed = line.split(" @ ")
    x_pos, y_pos, z_pos = [int(num) for num in parsed[0].split(", ")]
    x_vel, y_vel, z_vel = [int(num) for num in parsed[1].split(", ")]
    stones.append(StonePath(x_pos, y_pos, z_pos, x_vel, y_vel, z_vel))

crossed_paths = 0
for i in range(len(stones)):
    for j in range(i+1, len(stones)):
        intersection_point = stones[i].intersection(stones[j])
        if intersection_point and intersection_point[X] >= FLOOR and intersection_point[X] <= CEILING and intersection_point[Y] >= FLOOR and intersection_point[Y] <= CEILING:
            is_in_past = intersection_point[2]
            if not is_in_past:
                crossed_paths += 1
print(crossed_paths)