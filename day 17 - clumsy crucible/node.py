class Node:
    def __init__(self, point: tuple(int,int), heat_loss: int):
        self.point = point
        self.key = f"{point[0]},{point[1]}"
        self.heat_loss = heat_loss
        self.H = self._get_h_score()
        self.G = self._get_g_score()
        self.F = self.H + self.G + self.heat_loss

    def _get_g_score(self):
        distance_x = self.point[0]
        distance_y = self.point[1]
        furthest = max(distance_x, distance_y)
        nearest = min(distance_x, distance_y)
        jumps_needed = math.ceil((furthest - nearest) / 6)
        return (distance_x + distance_y + jumps_needed) * MAX_HEAT_LOSS

    def _get_h_score(self):
        distance_x = DESTINATION[0] - self.point[0]
        distance_y = DESTINATION[1] - self.point[1]
        furthest = max(distance_x, distance_y)
        nearest = min(distance_x, distance_y)
        jumps_needed = math.ceil((furthest - nearest) / 6)
        return (distance_x + distance_y + jumps_needed) * MAX_HEAT_LOSS
    
    def neighbors(self, city: list[list["Node"]]) -> list["Node"]: