from copy import copy, deepcopy
from operator import attrgetter
from random import shuffle, randint
from set_reader import import_card_set_from_file
from creature import Creature
from commander import Commander

from config import DEBUG, RENDER_BATTLEFIELD, RENDER_HAND, DRAW_INFO, DAMAGE_INFO


class Game:
    def __init__(self, card_set, deck_lists, player_names=("The Angel", "The Demon")):
        self.card_set = deepcopy(card_set)
        self.deck_lists = deepcopy(deck_lists)
        self.player_names = player_names
        self.__reset()

    @staticmethod
    def __opponent(player):
        return 1 - player

    def __toss_coin(self):
        self.__fp = randint(0, 1)
        self.__sp = Game.__opponent(self.__fp)
        self.__active_player = self.__fp

    def __reset(self):
        self.__toss_coin()
        self.__battlefield = ([], [])
        self.__commanders = (Commander(self.player_names[self.__fp], 10), Commander(self.player_names[self.__sp], 10))
        self.__hands = ([], [])
        self.__decks = ([], [])
        self.__deck_priority = ([], [])

        for player in (self.__fp, self.__sp):
            for card_id in self.deck_lists[player]:
                self.__decks[player].append(copy(self.card_set[card_id]))
            shuffle(self.__decks[player])
            self.__deck_priority[player].extend(list(self.deck_lists[player]))

    def __next_player(self):
        self.__active_player = (self.__active_player + 1) % 2

    def __add_creature_to_battlefield(self, card, active_player):
        creature = Creature(card)
        battle_row = self.__battlefield[active_player]
        battle_row.append(creature)
        if DEBUG:
            print("Added " + creature.name + " to the battlefield")

    def __remove_creature_from_battlefield(self, creature_position, player):
        battle_row = self.__battlefield[player]
        creature = battle_row.pop(creature_position)
        if DEBUG:
            print("Removed " + creature.name + " from the battlefield")

    def __draw_card(self, player, auto_sort=True):
        deck = self.__decks[player]
        hand = self.__hands[player]
        commander = self.__commanders[player]
        deck_priority = self.__deck_priority[player]

        if len(deck) > 0:
            card = deck.pop()
            hand.append(card)

            for pr, card_id in enumerate(deck_priority):
                if card.card_id == card_id:
                    card.priority = pr
                    deck_priority[card.priority] = -1
                    break

            if auto_sort:
                self.__sort_hand(player)

            if DRAW_INFO:
                print("Player has drawn " + card.name + " to his hand with priority " + str(card.priority))
        else:
            commander.deal_damage(1)
            if DAMAGE_INFO and DRAW_INFO:
                print("Player's commanders is dealt 1 damage because his deck is empty")

    def __draw_n_cards(self, player, n):
        for i in range(n):
            self.__draw_card(player, auto_sort=False)
        self.__sort_hand(player)

    def __sort_hand(self, player):
        self.__hands[player].sort(key=attrgetter('priority'), reverse=True)

    def __summon_creature_to_battlefield(self, player):
        hand = self.__hands[player]
        battle_row = self.__battlefield[player]

        if len(hand) > 0:
            card = hand.pop()
            self.__add_creature_to_battlefield(card, player)
            self.__activate_battle_cry(battle_row[-1])
            opposing_row = self.__battlefield[self.__opponent(self.__active_player)]
            if len(opposing_row) >= len(battle_row):
                self.__activate_duel(battle_row[-1], len(battle_row) - 1)
        else:
            if DEBUG:
                print("Player's hand is empty")

    def __activate_battle_cry(self, creature):
        battle_cry = creature.abilities.get('battlecry')
        if battle_cry:
            if battle_cry[0] == 'strike':
                if battle_cry[1] == 'enemy_commander':
                    damage = int(battle_cry[2])
                    self.__commanders[self.__opponent(self.__active_player)].deal_damage(damage)
                    if DAMAGE_INFO:
                        print(creature.name + " strikes for " + str(damage) + " damage "
                              + self.__commanders[self.__opponent(self.__active_player)].name + " leaving it with "
                              + str(self.__commanders[self.__opponent(self.__active_player)].life_total)
                              + " life total")
                elif battle_cry[1] == 'ally_commander':
                    damage = int(battle_cry[2])
                    self.__commanders[self.__active_player].deal_damage(damage)
                    if DAMAGE_INFO:
                        print(creature.name + " strikes for " + str(damage) + " damage "
                              + self.__commanders[self.__active_player].name + " leaving it with "
                              + str(self.__commanders[self.__active_player].life_total) + " life total")
            elif battle_cry[0] == 'heal':
                if battle_cry[1] == 'ally_commander':
                    heal = int(battle_cry[2])
                    self.__commanders[self.__active_player].heal(heal)
                    if DAMAGE_INFO:
                        print(creature.name + " heals for " + str(heal) + " points "
                              + self.__commanders[self.__active_player].name + " up to "
                              + str(self.__commanders[self.__active_player].life_total) + " life total")
            elif battle_cry[0] == 'draw':
                self.__draw_n_cards(self.__active_player, int(battle_cry[1]))
                if DRAW_INFO:
                    print(creature.name + " has drawn " + battle_cry[1] + " cards for its commander")

    def __activate_duel(self, creature, creature_position):
        duel = creature.abilities.get('duel')
        if duel:
            if duel[0] == 'strike':
                if duel[1] == 'opponent_creature':
                    opponent = self.__battlefield[self.__opponent(self.__active_player)][creature_position]
                    damage = int(duel[2])
                    opponent.deal_damage(damage)
                    if DAMAGE_INFO:
                        print(creature.name + " strikes for " + str(damage) + " damage " + opponent.name
                              + " leaving it with " + str(opponent.health) + " health")
                elif duel[1] == 'enemy_commander':
                    enemy_commander = self.__commanders[self.__opponent(self.__active_player)]
                    damage = int(duel[2])
                    enemy_commander.deal_damage(damage)
                    if DAMAGE_INFO:
                        print(creature.name + " strikes for " + str(damage) + " damage "
                              + self.__commanders[self.__opponent(self.__active_player)].name + " leaving it with "
                              + str(self.__commanders[self.__opponent(self.__active_player)].life_total)
                              + " life total")
            elif duel[0] == 'draw':
                self.__draw_n_cards(self.__active_player, int(duel[1]))
                if DRAW_INFO:
                    print(creature.name + " has drawn " + duel[1] + " cards for its commander")

    def __deal_combat_damage(self, position):
        attacking_battle_row = self.__battlefield[self.__active_player]
        defending_battle_row = self.__battlefield[self.__opponent(self.__active_player)]

        active_creature = attacking_battle_row[position]
        if active_creature.is_active() and active_creature.attack > 0:
            if len(defending_battle_row) > position:
                opponent = defending_battle_row[position]
                opponent.deal_damage(active_creature.attack)
                active_creature.deal_damage(opponent.defense)
                if DAMAGE_INFO:
                    print(active_creature.name + " deals " + str(active_creature.attack) + " damage to " + opponent.name
                          + " leaving it with " + str(opponent.health) + " health")
                    print(opponent.name + " deals " + str(opponent.defense) + " damage to " + active_creature.name
                          + " in response leaving it with " + str(active_creature.health) + " health")
            else:
                self.__commanders[self.__opponent(self.__active_player)].deal_damage(active_creature.attack)
                if DAMAGE_INFO:
                    print(active_creature.name + " deals " + str(active_creature.attack) + " damage to "
                          + self.__commanders[self.__opponent(self.__active_player)].name + " leaving it with "
                          + str(self.__commanders[self.__opponent(self.__active_player)].life_total) + " life total")

    def __remove_dead_from_battlefield(self):
        new_battlefield = ([], [])
        for battle_row in (self.__fp, self.__sp):
            new_row = []
            for creature in self.__battlefield[battle_row]:
                if creature.is_alive():
                    new_row.append(creature)
            new_battlefield[battle_row].extend(new_row)
        self.__battlefield = new_battlefield

    def __render_battlefield(self):
        creatures_icons = {1: 'V', 2: 'C', 3: 'W', 4: 'A', 5: 'M', 6: 'S'}

        battlefield = self.__battlefield
        max_row = max(len(battlefield[self.__fp]), len(battlefield[self.__sp]))

        for battle_row in (self.__fp, self.__sp):
            print('-' * (1 + 2 * max_row))
            print('|', end='')
            for creature in battlefield[battle_row]:
                print(creatures_icons[creature.card_id], end='|')
            print('')
        print('-' * (1 + 2 * max_row))

    def __render_player_hand(self, player):
        creatures_icons = {1: 'V', 2: 'C', 3: 'W', 4: 'A', 5: 'M', 6: 'S'}

        hand = self.__hands[player]

        for card in hand:
            print(creatures_icons[card.card_id], end=' ')
        print('')

    def play(self):
        self.__reset()

        for player in (self.__fp, self.__sp):
            self.__draw_n_cards(player, 3)
        self.__draw_card(self.__sp)

        if RENDER_HAND:
            self.__render_player_hand(player=self.__fp)
            self.__render_player_hand(player=self.__sp)

        while self.__commanders[self.__fp].is_alive() and self.__commanders[self.__sp].is_alive():
            active_player = self.__active_player
            if DEBUG:
                print("It's " + self.__commanders[active_player].name + "'s turn!\n")

            self.__draw_card(active_player)
            if RENDER_HAND:
                self.__render_player_hand(active_player)

            for creature in self.__battlefield[active_player]:
                if DEBUG:
                    if creature.power == creature.activation - 1:
                        print("Creature " + creature.name + " is now activated")
                creature.activate()

            for pos, creature in enumerate(self.__battlefield[active_player]):
                if creature.is_active():
                    self.__deal_combat_damage(pos)

            self.__summon_creature_to_battlefield(active_player)

            self.__remove_dead_from_battlefield()

            if RENDER_BATTLEFIELD:
                self.__render_battlefield()
                print('')

            self.__next_player()

        result = [1, 1]
        for player in (self.__fp, self.__sp):
            if not self.__commanders[player].is_alive():
                result[player] = 0
                if DEBUG:
                    print(self.__commanders[player].name + " was defeated!\n")

        return result


if __name__ == "__main__":
    my_deck = tuple([2, 2, 6, 4, 4, 1, 3, 3, 5, 5, 2, 2, 6, 4, 4, 1, 3, 3, 5, 5])
    ser_deck = tuple([1, 5, 3, 2, 4, 2, 1, 3, 2, 2, 1, 5, 3, 2, 4, 2, 1, 3, 2, 2])
    card_set = import_card_set_from_file("test_set.scg")

    game = Game(card_set, (my_deck, ser_deck))
    game.play()

    # angel = 0
    # demon = 0
    # TESTS = 1000
    # for i in range(TESTS):
    #     result = tuple(game.play())
    #     angel += result[0]
    #     demon += result[1]
    #     if (i + 1) % 1000 == 0:
    #         print(str(i + 1) + "th test played")
    #
    # print("Daniil winrate: " + str(100 * angel / TESTS) + "%")
    # print("Sergey winrate: " + str(100 * demon / TESTS) + "%")
    # print("Draw rate: " + str(100 * (1 - (angel + demon) / TESTS)) + "%")
