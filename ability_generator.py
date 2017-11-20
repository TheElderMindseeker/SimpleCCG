from random import choice, randint


def generate_ability(keyword='battlecry'):
    if keyword == 'battlecry':
        ability = choice(('strike', 'heal', 'draw'))
        if ability == 'strike':
            target = choice(('enemy_commander', 'ally_commander'))
            if target == 'enemy_commander':
                multiplier = 1
            elif target == 'ally_commander':
                multiplier = -1
            else:
                multiplier = 0

            damage = randint(1, 5)
            cost = multiplier * damage
            return (ability, target, str(damage)), cost

        elif ability == 'heal':
            effect = choice(('all', 'ally_commander'))
            if effect == 'all':
                target = choice(('allies',))
                heal = randint(1, 5)
                cost = 3 * heal
                return (ability, effect, target, heal), cost

            elif effect == 'ally_commander':
                target = effect
                heal = randint(1, 5)
                return (ability, target, heal), heal

            else:
                print("Not an ally_commander or all")
                return None

        elif ability == 'draw':
            cards = randint(1, 4)
            return (ability, cards), 0.5 * cards

        else:
            print("Not a strike or heal or draw")
            return None

    elif keyword == 'duel':
        ability = choice(('strike', 'heal'))
        if ability == 'strike':
            target = choice(('enemy_commander', 'ally_commander', 'opponent_creature'))
            if target == 'enemy_commander' or 'opponent_creature':
                multiplier = 1
            elif target == 'ally_commander':
                multiplier = -1
            else:
                multiplier = 0

            damage = randint(1, 5)
            cost = 0.8 * multiplier * damage
            return (ability, target, str(damage)), cost

        elif ability == 'heal':
            effect = choice(('all', 'ally_commander'))
            if effect == 'all':
                target = choice(('allies',))
                heal = randint(1, 5)
                cost = 2.4 * heal
                return (ability, effect, target, heal), cost

            elif effect == 'ally_commander':
                target = effect
                heal = randint(1, 5)
                cost = 0.8 * heal
                return (ability, target, heal), cost

            else:
                print("Not an ally_commander or all")
                return None

        else:
            print("Not a strike or heal")
            return None

    else:
        print("Invalid keyword")
        return None
