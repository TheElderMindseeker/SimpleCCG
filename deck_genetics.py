from set_reader import import_card_set_from_file
from card_statistics import calculate_card_ii
from game_engine import Game
from deck import Deck
from operator import methodcaller
from random import choice, randint


card_set = import_card_set_from_file("test_set.scg")


def initialize_population(size):
    return [Deck(card_set) for x in range(size)]


def selection(population, rounds=100):
    for deck in population:
        deck.reset()

    for i, deck_1 in enumerate(population):
        for j, deck_2 in enumerate(population):
            if i > j:
                game = Game(card_set, (deck_1.deck, deck_2.deck))
                for k in range(rounds):
                    result = tuple(game.play())
                    if result[0] == 1:
                        deck_1.won += 1
                        deck_2.lost += 1
                    elif result[1] == 1:
                        deck_1.lost += 1
                        deck_2.won += 1
                    else:
                        deck_1.draw += 1
                        deck_2.draw += 1
            else:
                break

    population.sort(key=methodcaller('winrate'), reverse=True)
    for deck in population:
        print(deck.deck, sum(deck.deck), '\t', deck.winrate(), sep=' ')
    print(calculate_card_ii(population, card_set))
    return population[:len(population) // 2]


def pro_tour(population, rounds=100):
    selection(population, rounds=rounds)


def restore_population(population, size):
    while len(population) < size:
        population.append(Deck(card_set))


def point_mutation(sample, mutations=5):
    for i in range(mutations):
        position = randint(0, len(sample.deck) - 1)
        sample.deck[position] = choice(tuple(card_set.keys()))


if __name__ == "__main__":
    pop = initialize_population(40)
    for stage in range(10):
        print("Stage #" + str(stage + 1))
        new_pop = selection(pop, rounds=50)
        for i, sample in enumerate(new_pop):
            if i >= len(new_pop) // 2:
                point_mutation(sample)
        restore_population(new_pop, 40)
        pop = new_pop

    print("Qualifiers")
    pop = selection(pop)
    print("Pro tour")
    pro_tour(pop)
