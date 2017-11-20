# Format: ID;name;attack;defense;health;power;abilities
# Abilities = keyword:effect|keyword:effect...


class Card:
    def __init__(self, card_id, name, attack, defense, health, power, abilities):
        self.card_id = card_id
        self.name = name
        self.attack = attack
        self.defense = defense
        self.health = health
        self.power = power
        self.abilities = abilities
        self.priority = -1

    def __str__(self):
        return self.name + ' ' + '*' * self.power + ' #' + str(self.card_id) + '\n' + str(self.abilities) + '\n' +\
                 '<' + str(self.attack) + '|' + str(self.defense) + '> <' + str(self.health) + '>'
