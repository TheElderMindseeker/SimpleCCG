from Card import Card


DEBUG = False


def import_card_set_from_file(file_name):
    card_set = []
    for i, card_info in enumerate(open(file_name, 'r')):
        info = card_info.strip().split(';')
        card_id = i + 1  # int(info[0])
        name = info[1]
        strength = int(info[2])
        cunning = int(info[3])
        fortitude = int(info[4])
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
        card_set.append(Card(card_id, name, strength, cunning, fortitude, power, abilities))
        if DEBUG:
            print(card_set[-1])
    return tuple(card_set)


if __name__ == "__main__":
    card_set = import_card_set_from_file("test_set.scg")
    for card in card_set:
        print(card)
