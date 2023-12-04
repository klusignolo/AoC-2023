with open("scratchcards.txt", "r") as file:
    scratchcards = [raw_line.split(":")[1].split("|") for raw_line in file.read().splitlines()]
total_points = 0
for scratchcard in scratchcards:
    winning_nums = set(scratchcard[0].split())
    my_nums = set(scratchcard[1].split())
    matching_nums = winning_nums.intersection(my_nums)
    if len(matching_nums):
        total_points += 2**(len(matching_nums)-1)
print(total_points)

