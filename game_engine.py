from copy import copy
from operator import attrgetter
from random import shuffle, randint
from set_reader import import_card_set_from_file
from Creature import Creature
from Commander import Commander


DEBUG = False
DRAW_BATTLEFIELD = False
DRAW_HAND = False


def add_creature_to_battlefield(battle_row, card):
    creature = Creature(card)
    battle_row.append(creature)
    if DEBUG:
        print("Added " + creature.name + " to the battlefield")


def remove_creature_from_battlefield(battle_row, position):
    if DEBUG:
        print("Removing " + battle_row[position].name + " from the battlefield")
    del battle_row[position]


def draw_card(commander, deck_priority, deck, hand):
    if len(deck) > 0:
        card = deck[0]
        del deck[0]
        hand.append(card)

        for pr, card_id in enumerate(deck_priority):
            if card.card_id == card_id:
                card.priority = pr
                break
        deck_priority[card.priority] = -1

        if DEBUG:
            print("Player drew " + card.name + " to his hand with priority " + str(card.priority))
    else:
        commander.deal_damage(1)
        if DEBUG:
            print("Player's commanders is dealt 1 damage because his deck is empty")


def draw_n_cards(commander, deck_priority, deck, hand, n):
    for i in range(n):
        draw_card(commander, deck_priority, deck, hand)


def summon_creature_to_battlefield(game_state, hand, position, battle_row):
    if len(hand) > 0:
        add_creature_to_battlefield(battle_row, hand[position])
        del hand[position]
        activate_battlecry(game_state, battle_row[len(battle_row) - 1])
        opposing_row = game_state['battlefield'][1 - game_state['active_player']]
        if len(opposing_row) >= len(battle_row):
            activate_duel(game_state, battle_row[len(battle_row) - 1], len(battle_row) - 1)
    else:
        if DEBUG:
            print("Player's hand is empty")


def activate_battlecry(game_state, creature):
    battlecry = creature.abilities.get('battlecry')
    if battlecry:
        if battlecry[0] == 'strike':
            if battlecry[1] == 'enemy_commander':
                damage = int(battlecry[2])
                game_state['commanders'][1 - game_state['active_player']].deal_damage(damage)
                if DEBUG:
                    print(creature.name + " strikes for " + str(damage) + " damage "
                          + game_state['commanders'][1 - game_state['active_player']].name + " leaving it with "
                          + str(game_state['commanders'][1 - game_state['active_player']].life_total))
            elif battlecry[1] == 'ally_commander':
                damage = int(battlecry[2])
                game_state['commanders'][game_state['active_player']].deal_damage(damage)
                if DEBUG:
                    print(creature.name + " strikes for " + str(damage) + " damage "
                          + game_state['commanders'][game_state['active_player']].name + " leaving it with "
                          + str(game_state['commanders'][game_state['active_player']].life_total))
        elif battlecry[0] == 'heal':
            if battlecry[1] == 'ally_commander':
                heal = int(battlecry[2])
                game_state['commanders'][game_state['active_player']].heal(heal)
                if DEBUG:
                    print(creature.name + " heals for " + str(heal) + " points "
                          + game_state['commanders'][game_state['active_player']].name
                          + " up to " + str(game_state['commanders'][game_state['active_player']].life_total))


def activate_duel(game_state, creature, creature_position):
    duel = creature.abilities.get('duel')
    if duel:
        if duel[0] == 'strike':
            if duel[1] == 'opponent':
                opponent = game_state['battlefield'][1 - game_state['active_player']][creature_position]
                damage = int(duel[2])
                opponent.deal_damage(damage)
                if DEBUG:
                    print(creature.name + " strikes for " + str(damage) + " damage " + opponent.name
                          + " leaving it with " + str(opponent.fortitude))
            elif duel[1] == 'enemy_commander':
                enemy_commander = game_state['commanders'][1 - game_state['active_player']]
                damage = int(duel[2])
                enemy_commander.deal_damage(damage)
                if DEBUG:
                    print(creature.name + " strikes for " + str(damage) + " damage "
                          + game_state['commanders'][1 - game_state['active_player']].name + " leaving it with "
                          + str(game_state['commanders'][1 - game_state['active_player']].life_total))


def deal_combat_damage(battlefield, commanders, position, active_player):
    active_creature = battlefield[active_player][position]
    if active_creature.strength > 0:
        if len(battlefield[1 - active_player]) > position:
            opponent = battlefield[1 - active_player][position]
            opponent.deal_damage(active_creature.strength)
            active_creature.deal_damage(opponent.cunning)
            if DEBUG:
                print(active_creature.name + " deals " + str(active_creature.strength) + " damage to " + opponent.name
                      + " leaving it with " + str(opponent.fortitude))
                print(opponent.name + " deals " + str(opponent.cunning) + " damage to " + active_creature.name
                      + " in response leaving it with " + str(active_creature.fortitude))
        else:
            commanders[1 - active_player].deal_damage(active_creature.strength)
            if DEBUG:
                print(active_creature.name + " deals " + str(active_creature.strength) + " damage to "
                      + commanders[1 - active_player].name + " leaving it with "
                      + str(commanders[1 - active_player].life_total))


def remove_dead_from_battlefield(battlefield):
    new_battlefield = []
    for i in (0, 1):
        new_row = []
        for creature in battlefield[i]:
            if creature.is_alive():
                new_row.append(creature)
        new_battlefield.append(new_row)
    return new_battlefield


def draw_battlefield(battlefield):
    creatures_icons = {1: 'V', 2: 'C', 3: 'W', 4: 'A', 5: 'M'}
    max_row = max(len(battlefield[0]), len(battlefield[1]))
    for i in (0, 1):
        print('-' * (1 + 2 * max_row))
        print('|', end='')
        for creature in battlefield[i]:
            print(creatures_icons[creature.card_id], end='|')
        print('')
    print('-' * (1 + 2 * max_row))


def draw_player_hand(hand):
    creatures_icons = {1: 'V', 2: 'C', 3: 'W', 4: 'A', 5: 'M'}
    for card in hand:
        print(creatures_icons[card.card_id], end=' ')
    print('')


def play(card_set, player_decks):
    fp = randint(0, 1)  # first player
    sp = 1 - fp  # second player

    deck_priority = []
    for i in (fp, sp):
        deck_priority.append(list(player_decks[i]))
    deck_priority = tuple(deck_priority)

    decks = ([], [])
    battlefield = ([], [])
    commanders = (Commander("The Angel", 10), Commander("The Demon", 10))
    hands = [[], []]

    for player in (fp, sp):
        for card_id in player_decks[player]:
            decks[player].append(copy(card_set[card_id - 1]))
        shuffle(decks[player])
        draw_n_cards(commanders[player], deck_priority[player], decks[player], hands[player], 3)
    draw_card(commanders[sp], deck_priority[sp], decks[sp], hands[sp])
    for i in (fp, sp):
        hands[i] = list(sorted(hands[i], key=attrgetter('priority')))

    if DRAW_HAND:
        draw_player_hand(hands[fp])
        draw_player_hand(hands[sp])

    game_state = {'decks': decks, 'battlefield': battlefield, 'commanders': commanders, 'hands': hands,
                  'active_player': fp}

    while commanders[fp].is_alive() and commanders[sp].is_alive():
        active_player = game_state['active_player']
        if DEBUG:
            print("It's " + game_state['commanders'][active_player].name + "'s turn!\n")

        draw_card(commanders[active_player], deck_priority[active_player], decks[active_player], hands[active_player])
        hands[active_player] = list(sorted(hands[active_player], key=attrgetter('priority')))
        if DRAW_HAND:
            draw_player_hand(hands[active_player])

        for creature in battlefield[active_player]:
            if DEBUG:
                if creature.activation == creature.power - 1:
                    print("Creature " + creature.name + " is now activated")
            creature.activate()

        for pos, creature in enumerate(battlefield[active_player]):
            if creature.is_active():
                deal_combat_damage(battlefield, commanders, pos, active_player)

        summon_creature_to_battlefield(game_state, hands[active_player], 0, battlefield[active_player])

        battlefield = remove_dead_from_battlefield(battlefield)
        game_state['battlefield'] = battlefield

        if DRAW_BATTLEFIELD:
            draw_battlefield(battlefield)
            print('')

        game_state['active_player'] = (active_player + 1) % 2

    result = [1, 1]
    for i in (fp, sp):
        if not game_state['commanders'][i].is_alive():
            result[i] = 0
            if DEBUG:
                print(game_state['commanders'][i].name + " was defeated!\n")

    return result


if __name__ == "__main__":
    my_deck = tuple([2, 2, 2, 4, 4, 1, 3, 3, 5, 5, 2, 2, 2, 4, 4, 1, 3, 3, 5, 5])
    ser_deck = tuple([1, 5, 3, 2, 4, 2, 1, 3, 2, 2, 1, 5, 3, 2, 4, 2, 1, 3, 2, 2])
    card_set = import_card_set_from_file("test_set.scg")

    angel = 0
    demon = 0
    TESTS = 10000
    for i in range(TESTS):
        result = tuple(play(card_set, (my_deck, ser_deck)))
        angel += result[0]
        demon += result[1]
        if (i + 1) % 1000 == 0:
            print(str(i + 1) + "th test played")

    print("Daniil winrate: " + str(100 * angel / TESTS) + "%")
    print("Sergey winrate: " + str(100 * demon / TESTS) + "%")
    print("Draw rate: " + str(100 * (1 - (angel + demon) / TESTS)) + "%")
