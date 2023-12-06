# Each millisecond adds one millimeter/millisecond
# get number of ways to win
with open("races.txt", "r") as file:
    time_and_distance = file.read().splitlines()
    race_times = [int(i) for i in time_and_distance[0].split()[1:]]
    race_distances = [int(i) for i in time_and_distance[1].split()[1:]]

def get_distance_traveled(hold_ms: int, race_time: int):
    travel_time = race_time - hold_ms
    return travel_time * hold_ms

result = 1
for i in range(len(race_times)):
    ways_to_win = 0
    race_time = race_times[i]
    distance_to_beat = race_distances[i]
    for j in range(race_time):
        if get_distance_traveled(j, race_time) > distance_to_beat:
            ways_to_win += 1
    result *= ways_to_win
print(result)
    