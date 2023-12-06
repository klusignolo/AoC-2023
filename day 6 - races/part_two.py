with open("races.txt", "r") as file:
    time_and_distance = file.read().splitlines()
    race_time = int("".join(time_and_distance[0].split()[1:]))
    race_distance = int("".join(time_and_distance[1].split()[1:]))

def get_distance_traveled(hold_ms: int, race_time: int):
    travel_time = race_time - hold_ms
    return travel_time * hold_ms

ways_to_win = 0
for i in range(race_time):
    if get_distance_traveled(i, race_time) > race_distance:
        ways_to_win = race_time - i - i + 1
        break
print(ways_to_win)
    