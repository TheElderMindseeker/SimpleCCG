class Creature:
    def __init__(self, card):
        self.card_id = card.card_id
        self.name = card.name
        self.strength = card.strength
        self.cunning = card.cunning
        self.fortitude = card.fortitude
        self.power = card.power
        self.activation = 0
        self.abilities = card.abilities

    def activate(self):
        if self.activation < self.power:
            self.activation += 1

    def deal_damage(self, damage):
        self.fortitude -= damage

    def is_active(self):
        return self.activation >= self.power

    def is_alive(self):
        return self.fortitude > 0

    def __str__(self):
        return self.name + ' ' + '*' * self.power + ' #' + str(self.card_id) + '\n' + str(self.abilities) + '\n' + \
               '<' + str(self.strength) + '|' + str(self.cunning) + '> <' + str(self.fortitude) + '>'
