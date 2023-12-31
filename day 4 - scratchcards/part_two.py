with open("scratchcards.txt", "r") as file:
    scratchcards = [raw_line.split(":")[1].split("|") for raw_line in file.read().splitlines()]
scratchcard_copycount = {}
max_scratch_index = len(scratchcards) - 1
for i, scratchcard in enumerate(scratchcards):
    winning_nums = set(scratchcard[0].split())
    my_nums = set(scratchcard[1].split())
    matching_num_count = len(winning_nums.intersection(my_nums))
    # Can't copy beyond length of table
    copy_count = matching_num_count - max(0, matching_num_count - max_scratch_index)
    scratchcard_copycount[i] = matching_num_count

cards_to_scratch = {card_index: 1 for card_index in scratchcard_copycount.keys()}
for card_number in cards_to_scratch.keys():
    for i in range(cards_to_scratch[card_number]):
        copies_to_add = scratchcard_copycount[card_number]
        for j in range(copies_to_add):
            index_of_card_to_add = card_number + 1 + j
            cards_to_scratch[index_of_card_to_add] += 1
total_scratched = sum(cards_to_scratch.values())
print(total_scratched)
