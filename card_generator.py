from random import randint, choice
from card import Card
from card_larva import CardLarva
from ability_generator import generate_ability


def card_fitness(card):
    total_points = 10
    real_points = 1.2 * card.attack + 1.1 * card.defense + card.health - 1.4 * card.power
    for abil in card.abilities:
        real_points += card.abilities[abil][1]
    return abs(real_points - total_points)


def create_filler_card_larva():
    larva = CardLarva("", randint(0, 5), randint(0, 5), randint(1, 10), randint(1, 3), {})
    if randint(0, 1) == 1:
        larva.abilities['battlecry'] = generate_ability()
    return larva


def initialize_population(size):
    return [create_filler_card_larva() for i in range(size)]


def selection(population):
    population.sort(key=card_fitness)
    return population[:len(population) // 2]


def restore_population(population, size):
    while len(population) < size:
        population.append(create_filler_card_larva())


def change_bounded(base, delta, lo, hi):
    result = base + delta
    if result < lo:
        result = lo
    elif result > hi:
        result = hi
    return result


def point_mutation(card_larva):
    mutation_type = choice(('reroll', 'buff', 'nerf', 'battlecry', 'duel'))

    if mutation_type == 'reroll':
        stat = choice(('attack', 'defense', 'health', 'power'))
        if stat == 'attack':
            card_larva.attack = randint(0, 5)
        elif stat == 'defense':
            card_larva.defense = randint(0, 5)
        elif stat == 'health':
            card_larva.health = randint(1, 10)
        elif stat == 'power':
            card_larva.power = randint(1, 3)

    elif mutation_type == 'buff':
        stat = choice(('attack', 'defense', 'health', 'power'))
        if stat == 'attack':
            card_larva.attack = change_bounded(card_larva.attack, +randint(1, 2), 0, 30)
        elif stat == 'defense':
            card_larva.defense = change_bounded(card_larva.defense, +randint(1, 2), 0, 30)
        elif stat == 'health':
            card_larva.health = change_bounded(card_larva.health, +randint(1, 2), 0, 100)
        elif stat == 'power':
            card_larva.power = change_bounded(card_larva.power, +1, 1, 3)

    elif mutation_type == 'nerf':
        stat = choice(('attack', 'defense', 'health', 'power'))
        if stat == 'attack':
            card_larva.attack = change_bounded(card_larva.attack, -randint(1, 2), 0, 30)
        elif stat == 'defense':
            card_larva.defense = change_bounded(card_larva.defense, -randint(1, 2), 0, 30)
        elif stat == 'health':
            card_larva.health = change_bounded(card_larva.health, -randint(1, 2), 0, 100)
        elif stat == 'power':
            card_larva.power = change_bounded(card_larva.power, -1, 1, 3)

    elif mutation_type == 'battlecry' or mutation_type == 'duel':
        if mutation_type in card_larva.abilities.keys():
            change = choice(('replace', 'remove'))
            if change == 'replace':
                card_larva.abilities[mutation_type] = generate_ability(mutation_type)
            elif change == 'remove':
                del card_larva.abilities[mutation_type]
        else:
            card_larva.abilities[mutation_type] = generate_ability(mutation_type)


def generate_set(num_cards=10):
    pop = initialize_population(4 * num_cards)
    for i in range(30):
        print("Stage #{}".format(i + 1))
        pop = selection(pop)
        for pos in range(len(pop)):
            if pos >= len(pop) // 2:
                point_mutation(pop[pos])
        restore_population(pop, 4 * num_cards)

    pop = selection(pop)
    final_pop = selection(pop)
    card_set = dict()
    for card_id, card_larva in enumerate(final_pop):
        card_set[card_id + 1] = card_larva.generate_card(card_id + 1)

    return card_set


if __name__ == "__main__":
    card_set = generate_set(20)

    for card_id in card_set:
        print(card_set[card_id])