with open("hands.txt", "r") as file:
    hand_bids = [hand_bid.split() for hand_bid in file.read().splitlines()]

hands_grouped_by_type = [[],[],[],[],[],[],[]]
for hand_bid in hand_bids:
    hand_bid[0] = hand_bid[0].replace("K", "B").replace("Q", "C").replace("J", "Z").replace("T", "E").replace("9", "F").replace("8", "G").replace("7", "H").replace("6", "I").replace("5", "J").replace("5", "K").replace("4", "L").replace("3", "M").replace("2", "N")
    hand = hand_bid[0]
    hand_bid[1] = int(hand_bid[1])
    card_dict = {}
    for card in hand:
        if card in card_dict.keys():
            card_dict[card] += 1
        else:
            card_dict[card] = 1
    
    # If any number of jokers (aside from 5) are found, just count them as the next most common card occurrence.
    if "Z" in card_dict.keys() and card_dict["Z"] < 5:
        joker_count = card_dict.pop("Z")
        max_key = max(card_dict, key=card_dict.get)
        card_dict[max_key] += joker_count

    if 5 in card_dict.values(): # 5 of a kind
        hands_grouped_by_type[0].append(hand_bid)
    elif 4 in card_dict.values(): # 4 of a kind
        hands_grouped_by_type[1].append(hand_bid)
    elif 3 in card_dict.values():
        if 2 in card_dict.values(): # full house
            hands_grouped_by_type[2].append(hand_bid)
        else: # 3 of a kind
            hands_grouped_by_type[3].append(hand_bid)
    elif len(card_dict.values()) == 3: # Two Pair
        hands_grouped_by_type[4].append(hand_bid)
    elif len(card_dict.values()) == 4: # One Pair
        hands_grouped_by_type[5].append(hand_bid)
    else: # High Card
        hands_grouped_by_type[6].append(hand_bid)
total_winnings = 0
max_winning_remaining = len(hand_bids)
for i in range(7):
    hands_grouped_by_type[i].sort()
    for j in range(len(hands_grouped_by_type[i])):
        total_winnings += hands_grouped_by_type[i][j][1] * max_winning_remaining
        max_winning_remaining -= 1
print(total_winnings)
