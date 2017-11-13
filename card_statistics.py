def calculate_card_ii(population, card_set):
    ii_index = dict()
    for card_id in card_set.keys():
        ii_index[card_id] = 0

    for deck in population:
        for card_id in deck.deck:
            ii_index[card_id] += deck.winrate()

    max_ii = max(ii_index.values())
    for key in ii_index.keys():
        ii_index[key] /= max_ii

    return ii_index
