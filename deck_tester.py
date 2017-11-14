from game_engine import Game
from set_reader import import_card_set_from_file


decks = (
    [3, 4, 4, 3, 3, 4, 4, 4, 4, 5, 4, 3, 3, 3, 4, 3, 3, 6, 3, 4],
    [6, 5, 6, 6, 6, 6, 4, 5, 5, 6, 6, 6, 6, 4, 6, 6, 6, 5, 5, 4],
    [2, 2, 2, 2, 2, 1, 1, 1, 5, 1, 1, 1, 1, 4, 2, 4, 5, 4, 1, 1],
    [2, 6, 6, 6, 2, 3, 4, 5, 6, 6, 5, 6, 2, 6, 3, 1, 6, 3, 3, 3],
    [2, 5, 7, 2, 2, 7, 7, 7, 7, 7, 2, 2, 2, 3, 2, 2, 7, 7, 2, 7]
)


if __name__ == "__main__":
    card_set = import_card_set_from_file("test_set.scg")
    game = Game(card_set, (decks[2], decks[1]))
    game.play()
