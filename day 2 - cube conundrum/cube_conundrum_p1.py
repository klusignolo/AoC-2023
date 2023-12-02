import re
filepath = "day 2 - cube conundrum/cube_games.txt"
cube_games_raw = []
RED_MAX, GREEN_MAX, BLUE_MAX = (12, 13, 14)

with open(filepath, "r") as file:
    cube_games_raw.extend(file.readlines())

possible_games_sum = 0
for raw_game in cube_games_raw:
    game_number = int(re.findall(r"Game (\d+):", raw_game)[0])
    game_turns = raw_game.split(":")[1].split(";")
    is_game_possible = True
    for game_turn in game_turns:
        red_count = re.findall(r"(\d+) red", game_turn)
        if red_count and int(red_count[0]) > RED_MAX:
            is_game_possible = False
            break
        green_count = re.findall(r"(\d+) green", game_turn)
        if green_count and int(green_count[0]) > GREEN_MAX:
            is_game_possible = False
            break
        blue_count = re.findall(r"(\d+) blue", game_turn)
        if blue_count and int(blue_count[0]) > BLUE_MAX:
            is_game_possible = False
            break
    if is_game_possible:
        possible_games_sum += game_number
print(possible_games_sum)
        
        
