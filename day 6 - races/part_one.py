with open("races.txt", "r") as file:
    time_and_distance = file.read().splitlines()
    race_times = [int(i) for i in time_and_distance[0].split()[1:]]
    race_distances = [int(i) for i in time_and_distance[1].split()[1:]]

result = 1
for i in range(len(race_times)):
    for j in range(race_times[i]):
        if j * (race_times[i] - j) > race_distances[i]:
            result *= race_times[i] - j - j + 1
            break
print(result)
    