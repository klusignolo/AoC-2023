import re
filepath = "day 2 - cube conundrum/cube_games.txt"
cube_games_raw = []

with open(filepath, "r") as file:
    cube_games_raw.extend(file.readlines())

power_sum = 0
for raw_game in cube_games_raw:
    game_turns = raw_game.split(":")[1].split(";")
    max_red, max_green, max_blue = (0,0,0)
    for game_turn in game_turns:
        red_count = re.findall(r"(\d+) red", game_turn)
        if red_count:
            max_red = max(max_red, int(red_count[0]))
        green_count = re.findall(r"(\d+) green", game_turn)
        if green_count:
            max_green = max(max_green, int(green_count[0]))
        blue_count = re.findall(r"(\d+) blue", game_turn)
        if blue_count:
            max_blue = max(max_blue, int(blue_count[0]))
    power_sum += max_red * max_green * max_blue
print(power_sum)
        
        
