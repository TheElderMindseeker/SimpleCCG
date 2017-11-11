class Creature:
    def __init__(self, card):
        self.card_id = card.card_id
        self.name = card.name
        self.attack = card.strength
        self.defense = card.cunning
        self.health = card.fortitude
        self.activation = card.power
        self.power = 0
        self.abilities = card.abilities

    def activate(self):
        if self.power < self.activation:
            self.power += 1

    def deal_damage(self, damage):
        self.health -= damage

    def is_active(self):
        return self.power >= self.activation

    def is_alive(self):
        return self.health > 0

    def __str__(self):
        return self.name + ' ' + '*' * self.activation + ' #' + str(self.card_id) + '\n' + str(self.abilities) + '\n' + \
               '<' + str(self.attack) + '|' + str(self.defense) + '> <' + str(self.health) + '>'
