from set_reader import import_card_set_from_file
from card_generator import generate_set
from card_statistics import calculate_card_ii
from game_engine import Game
from deck import Deck
from operator import methodcaller
from random import choice, randint


card_set = generate_set(100)  # import_card_set_from_file("test_set.scg")


def initialize_population(size):
    return [Deck(card_set) for x in range(size)]


def selection(population, rounds=10):
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
    # print(population[0].deck, population[0].winrate(), sep='\t')
    # print(calculate_card_ii(population, card_set))
    return population[:len(population) // 2]


def pro_tour(population, rounds=100):
    return selection(population, rounds=rounds)


def restore_population(population, size):
    while len(population) < size:
        population.append(Deck(card_set))


def point_mutation(sample, mutations=5):
    for i in range(mutations):
        position = randint(0, len(sample.deck) - 1)
        sample.deck[position] = choice(tuple(card_set.keys()))


def spawn_using_crossover(population):
    parents = list()
    parents.append(choice([x for x in range(len(population))]))
    parents.append(choice([x for x in range(len(population)) if x != parents[0]]))
    new_deck = Deck(card_set)
    for i in range(len(new_deck.deck)):
        new_deck.deck[i] = population[parents[randint(0, 1)]].deck[i]
    # print("Deck hash", hash(new_deck), sep=' ')
    return new_deck


if __name__ == "__main__":
    for card_id in card_set.keys():
        print(card_set[card_id])

    pop_size = 40
    pop_num = 20

    populations = []
    for i in range(pop_num):
        populations.append(initialize_population(pop_size))

    for stage in range(100):
        print("Stage #" + str(stage + 1))

        for i in range(len(populations)):
            new_pop = selection(populations[i])

            spawn_pop = new_pop[:len(new_pop) // 2]
            for j in range(pop_size // 4):
                new_pop.append(spawn_using_crossover(spawn_pop))

            for j, sample in enumerate(new_pop):
                if j < len(new_pop) // 2:
                    point_mutation(sample, mutations=3)
                else:
                    point_mutation(sample, mutations=7)

            restore_population(new_pop, pop_size)
            populations[i] = new_pop

    print("Qualifiers")
    qualified = []
    for population in populations:
        qualified.extend(selection(population, rounds=20))
    print("Pro tour")
    champions = pro_tour(qualified, rounds=40)

    try:
        print(champions[0].deck, 100 * round(champions[0].winrate(), 3))
        print(champions[1].deck, 100 * round(champions[1].winrate(), 3))
        print(champions[2].deck, 100 * round(champions[2].winrate(), 3))
    except:
        pass

    try:
        cards_ii = calculate_card_ii(champions, card_set)
        for card_id in cards_ii.keys():
            print(card_id, round(cards_ii[card_id], 3), sep=':\t\t')
    except:
        pass
