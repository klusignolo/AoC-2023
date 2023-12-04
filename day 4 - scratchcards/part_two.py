# with open("scratchcards.txt", "r") as file:
#     scratchcards = [raw_line.split(":")[1].split("|") for raw_line in file.read().splitlines()]
# scratchcards_original = scratchcards
# total_cards_scratched = 0
# original_index = 0
# while len(scratchcards) > 0:
#     total_cards_scratched += 1
#     top_of_deck = scratchcards.pop(0)
#     winning_nums = set(top_of_deck[0].split())
#     my_nums = set(top_of_deck[1].split())
#     matching_nums = winning_nums.intersection(my_nums)
#     count_of_copies = len(matching_nums)
#     for i in range(len(matching_nums)):
#         scratchcards.insert(0, scratchcards_original[count_of_copies - i - 1])
# print(total_cards_scratched)

import time


with open("scratchcards.txt", "r") as file:
    scratchcards = [raw_line.split(":")[1].split("|") for raw_line in file.read().splitlines()]
scratchcard_match_count = []
max_scratch_index = len(scratchcards) - 1
for i, scratchcard in enumerate(scratchcards):
    winning_nums = set(scratchcard[0].split())
    my_nums = set(scratchcard[1].split())
    matching_num_count = len(winning_nums.intersection(my_nums))
    max_copy_index = i + matching_num_count
    matching_num_count -= max(0, matching_num_count - max_scratch_index)
    scratchcard_match_count.append((i, matching_num_count))
CARDS_PROCESSED = 0
def process_copies(card, indexes_already_hit: list[int]):
    global CARDS_PROCESSED
    if card[0] in indexes_already_hit:
        CARDS_PROCESSED += 1
        print(f"Processing COPY {card[0]}. TOTAL: {CARDS_PROCESSED}")
        return
    else:
        CARDS_PROCESSED += 1
        print(f"Processing OG {card[0]}. COPIES: {card[1]} TOTAL: {CARDS_PROCESSED}")
        indexes_already_hit.append(card[0])
        for i in range(card[1]):
            scratchcard_copy_index = card[0] + i + 1
            process_copies(scratchcard_match_count[scratchcard_copy_index], indexes_already_hit)

indexes_already_hit = []
extras_to_add = len(scratchcards)
while len(indexes_already_hit) < len(scratchcard_match_count):
    extras_to_add -= 1
    starting_index = max(0, len(indexes_already_hit))
    process_copies(scratchcard_match_count[starting_index], indexes_already_hit=indexes_already_hit)
CARDS_PROCESSED += extras_to_add
print(CARDS_PROCESSED)