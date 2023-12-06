with open("races.txt", "r") as file:
    time_and_distance = file.read().splitlines()
    race_time = int("".join(time_and_distance[0].split()[1:]))
    race_distance = int("".join(time_and_distance[1].split()[1:]))

for i in range(race_time):
    if i * (race_time - i) > race_distance:
        ways_to_win = race_time - i - i + 1
        break
print(ways_to_win)
    