with open("seed_maps.txt", "r") as file:
    sections = file.read().split("\n\n")
seeds = [int(i) for i in sections[0].split()[1:]]
seed_to_soil_map = [[int(j) for j in i.split()] for i in sections[1].splitlines()[1:]]
soil_to_fertilizer_map = [[int(j) for j in i.split()] for i in sections[2].splitlines()[1:]]
fertilizer_to_water_map = [[int(j) for j in i.split()] for i in sections[3].splitlines()[1:]]
water_to_light_map = [[int(j) for j in i.split()] for i in sections[4].splitlines()[1:]]
light_to_temp_map = [[int(j) for j in i.split()] for i in sections[5].splitlines()[1:]]
temp_to_humidity_map = [[int(j) for j in i.split()] for i in sections[6].splitlines()[1:]]
humidity_to_loc_map = [[int(j) for j in i.split()] for i in sections[7].splitlines()[1:]]

def find_destination_for_source(source: int, map: list[list[int]]):
    if source is None: return source
    for mappings in map:
        min_destination = mappings[0]
        min_source = mappings[1]
        range = mappings[2]
        if source >= min_source and source <= min_source + range:
            destination = min_destination + (source - min_source)
            return destination

smallest_location = 999999999999
total_seeds = len(seeds)
for i in range(total_seeds):
    if i % 2 == 1: continue
    for seed in range(seeds[i], seeds[i]+seeds[i+1]+1):
        soil = find_destination_for_source(seed, seed_to_soil_map)
        fertilizer = find_destination_for_source(soil, soil_to_fertilizer_map)
        water = find_destination_for_source(fertilizer, fertilizer_to_water_map)
        light = find_destination_for_source(water, water_to_light_map)
        temp = find_destination_for_source(light, light_to_temp_map)
        humidity = find_destination_for_source(temp, temp_to_humidity_map)
        location = find_destination_for_source(humidity, humidity_to_loc_map)
        if location and location < smallest_location:
            smallest_location = location
            break
print(f"FOUND IT! {smallest_location}")