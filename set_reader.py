from card import Card


DEBUG = False


def import_card_set_from_file(file_name):
    card_set = {}
    for card_info in open(file_name, 'r'):
        if len(card_info.strip()) > 0:
            info = card_info.strip().split(';')
            card_id = int(info[0])
            name = info[1]
            attack = int(info[2])
            defense = int(info[3])
            health = int(info[4])
            power = int(info[5])

            ability_str = info[6]
            if len(ability_str) > 0:
                abilities = dict()
                for ability in ability_str.split('|'):
                    keyword, effect = ability.split(':', maxsplit=1)
                    effect = tuple(effect.lower().split(' '))
                    abilities[keyword.lower()] = effect
            else:
                abilities = dict()

            card_set[card_id] = Card(card_id, name, attack, defense, health, power, abilities)
            if DEBUG:
                print(card_set[card_id])

    return card_set


if __name__ == "__main__":
    card_set = import_card_set_from_file("test_set.scg")
    for card in card_set.values():
        print(card)
