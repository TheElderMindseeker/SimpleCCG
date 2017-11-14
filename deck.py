from random import choice


class Deck:
    def __init__(self, card_set):
        self.deck = [choice(tuple(card_set.keys())) for x in range(20)]
        self.won = 0
        self.lost = 0
        self.draw = 0

    def reset(self):
        self.won = 0
        self.lost = 0
        self.draw = 0

    def winrate(self):
        if self.won == 0:
            return 0
        return self.won / (self.won + self.lost + self.draw)

    def __eq__(self, other):
        for card_id in range(len(other.deck)):
            if self.deck[card_id] != other.deck[card_id]:
                return False
        return True

    def __hash__(self):
        h = 0
        m = 1
        for card in self.deck:
            h += m * card
            m += 7
        return h
