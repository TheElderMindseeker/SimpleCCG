# Format: ID;name;strength;cunning;fortitude;power;abilities
# Abilities = keyword:effect|keyword:effect...


class Card:
    def __init__(self, card_id, name, strength, cunning, fortitude, power, abilities):
        self.card_id = card_id
        self.name = name
        self.strength = strength
        self.cunning = cunning
        self.fortitude = fortitude
        self.power = power
        self.abilities = abilities
        self.priority = -1

    def __str__(self):
        return self.name + ' ' + '*' * self.power + ' #' + str(self.card_id) + '\n' + str(self.abilities) + '\n' +\
                 '<' + str(self.strength) + '|' + str(self.cunning) + '> <' + str(self.fortitude) + '>'
