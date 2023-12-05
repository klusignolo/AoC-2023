from timeit import default_timer as timer
with open("seed_maps.txt", "r") as file:
    sections = file.read().split("\n\n")
    
class RangeMap:
    def __init__(self, s_min, s_max, d_min, d_max):
        self.s_min: int = s_min
        self.s_max: int = s_max
        self.d_min: int = d_min
        self.d_max: int = d_max

class Range:
    def __init__(self, min, max):
        self.min: int = min
        self.max: int = max
start = timer()
seeds = [int(i) for i in sections[0].split()[1:]]
seed_to_soil_map = [[int(j) for j in i.split()] for i in sections[1].splitlines()[1:]]
seed_soil_ranges = sorted([RangeMap(s_min=map[1], s_max=map[1]+map[2]-1, d_min=map[0], d_max=map[0]+map[2]-1) for map in seed_to_soil_map], key=lambda x: x.s_min)
soil_to_fertilizer_map = [[int(j) for j in i.split()] for i in sections[2].splitlines()[1:]]
soil_fertilizer_ranges = sorted([RangeMap(s_min=map[1], s_max=map[1]+map[2]-1, d_min=map[0], d_max=map[0]+map[2]-1) for map in soil_to_fertilizer_map], key=lambda x: x.s_min)
fertilizer_to_water_map = [[int(j) for j in i.split()] for i in sections[3].splitlines()[1:]]
fertilizer_water_ranges = sorted([RangeMap(s_min=map[1], s_max=map[1]+map[2]-1, d_min=map[0], d_max=map[0]+map[2]-1) for map in fertilizer_to_water_map], key=lambda x: x.s_min)
water_to_light_map = [[int(j) for j in i.split()] for i in sections[4].splitlines()[1:]]
water_light_ranges = sorted([RangeMap(s_min=map[1], s_max=map[1]+map[2]-1, d_min=map[0], d_max=map[0]+map[2]-1) for map in water_to_light_map], key=lambda x: x.s_min)
light_to_temp_map = [[int(j) for j in i.split()] for i in sections[5].splitlines()[1:]]
light_temp_ranges = sorted([RangeMap(s_min=map[1], s_max=map[1]+map[2]-1, d_min=map[0], d_max=map[0]+map[2]-1) for map in light_to_temp_map], key=lambda x: x.s_min)
temp_to_humidity_map = [[int(j) for j in i.split()] for i in sections[6].splitlines()[1:]]
temp_humidity_ranges = sorted([RangeMap(s_min=map[1], s_max=map[1]+map[2]-1, d_min=map[0], d_max=map[0]+map[2]-1) for map in temp_to_humidity_map], key=lambda x: x.s_min)
humidity_to_loc_map = [[int(j) for j in i.split()] for i in sections[7].splitlines()[1:]]
humidity_loc_ranges = sorted([RangeMap(s_min=map[1], s_max=map[1]+map[2]-1, d_min=map[0], d_max=map[0]+map[2]-1) for map in humidity_to_loc_map], key=lambda x: x.s_min)

def find_destination_ranges_for_source_range(source: Range, map: list[RangeMap]) -> list[Range]:
    destination_ranges: list[Range] = []
    mapped_source_ranges: list[Range] = []
    for destination_range in map:
        if source.min > destination_range.s_max:
            # no overlap yet
            continue
        elif source.min >= destination_range.s_min and source.max <= destination_range.s_max:
            # destination encompasses source
            start_offset = source.min - destination_range.s_min
            end_offset = destination_range.s_max - source.max
            mapped_range = Range(min=destination_range.d_min + start_offset, max=destination_range.d_max - end_offset)
            destination_ranges.append(mapped_range)
            mapped_source_ranges.append(source) # Full source is accounted for
            break
        elif source.min > destination_range.s_min and source.min <= destination_range.s_max and source.max > destination_range.s_max:
            # source overlaps destination end
            overlap_amount = destination_range.s_max - source.min
            mapped_range = Range(min=destination_range.d_max - overlap_amount, max=destination_range.d_max)
            mapped_source_range = Range(min=source.min, max=destination_range.s_max)
            destination_ranges.append(mapped_range)
            mapped_source_ranges.append(mapped_source_range)
        elif source.min <= destination_range.s_min and source.max >= destination_range.s_max:
            # source encompasses destination
            mapped_range = Range(min=destination_range.d_min, max=destination_range.d_max)
            mapped_source_range = Range(min=destination_range.s_min, max=destination_range.s_max)
            destination_ranges.append(mapped_range)
            mapped_source_ranges.append(mapped_source_range)
        elif source.min < destination_range.s_min and source.max >= destination_range.s_min and source.max < destination_range.s_max:
            # source overlaps destination start
            overlap_amount = source.max - destination_range.s_min
            mapped_range = Range(min=destination_range.d_min, max=destination_range.d_min + overlap_amount)
            mapped_source_range = Range(min=destination_range.s_min, max=source.max)
            destination_ranges.append(mapped_range)
            mapped_source_ranges.append(mapped_source_range)
        elif source.max < destination_range.s_min:
            # no more overlap to check (because the destination_ranges are in order by s_min). just take source
            break
    mapped_source_ranges.sort(key= lambda x: x.min)

    source_copy = Range(source.min, source.max)
    for range in mapped_source_ranges:
        if source_copy.min < range.min:
            destination_ranges.append(Range(source_copy.min, range.min - 1))
            source_copy.min = range.max + 1
        elif source_copy.min == range.min and source_copy.max != range.max:
            source_copy.min = range.max + 1
        elif source_copy.max > range.max:
            destination_ranges.append(Range(range.max + 1, source_copy.max))

    if len(destination_ranges) == 0:
        destination_ranges.append(source)

    return destination_ranges
        
        
possible_location_ranges: list[Range] = []
for i in range(len(seeds)):
    if i % 2 == 1: continue
    seed_range = Range(min=seeds[i], max=seeds[i] + seeds[i+1] - 1)
    soil_ranges = find_destination_ranges_for_source_range(seed_range, seed_soil_ranges)
    fertilizer_ranges = []
    for soil_range in soil_ranges:
        fertilizer_ranges.extend(find_destination_ranges_for_source_range(soil_range, soil_fertilizer_ranges))
    water_ranges = []
    for fertilizer_range in fertilizer_ranges:
        water_ranges.extend(find_destination_ranges_for_source_range(fertilizer_range, fertilizer_water_ranges))
    light_ranges = []
    for water_range in water_ranges:
        light_ranges.extend(find_destination_ranges_for_source_range(water_range, water_light_ranges))
    temp_ranges = []
    for light_range in light_ranges:
        temp_ranges.extend(find_destination_ranges_for_source_range(light_range, light_temp_ranges))
    humidity_ranges = []
    for temp_range in temp_ranges:
        humidity_ranges.extend(find_destination_ranges_for_source_range(temp_range, temp_humidity_ranges))
    location_ranges = []
    for humidity_range in humidity_ranges:
        location_ranges.extend(find_destination_ranges_for_source_range(humidity_range, humidity_loc_ranges))
    possible_location_ranges.extend(location_ranges)
possible_location_ranges.sort(key=lambda x: x.min)
end = timer()
print(f"Location found! Answer is: {possible_location_ranges[0].min} | Total Duration:{round((end-start)*1000, 4)} ms")