from game_engine import Game
from set_reader import import_card_set_from_file


decks = (
    [x for y in range(4) for x in (1, 1, 1, 1, 1)],
    [x for y in range(4) for x in (2, 1, 1, 1, 1)],
    [x for y in range(4) for x in (1, 1, 1, 3, 1)],
    [2, 2, 2, 1, 2, 2, 1, 3, 1, 3, 2, 1, 3, 3, 3, 1, 1, 3, 1, 3],
    [3, 1, 3, 3, 3, 3, 2, 3, 2, 3, 2, 3, 3, 1, 3, 3, 1, 1, 1, 2],
    [2, 2, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 2, 2, 2, 2, 1, 2]
)


if __name__ == "__main__":
    card_set = import_card_set_from_file("test_set.scg")
    game = Game(card_set, (decks[3], decks[5]))
    game.play()
