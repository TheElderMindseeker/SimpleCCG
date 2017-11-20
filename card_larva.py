from card import Card


class CardLarva:
    def __init__(self, name, attack, defense, health, power, ability_draft):
        self.name = "Creature"
        self.attack = attack
        self.defense = defense
        self.health = health
        self.power = power
        self.abilities = ability_draft

    def generate_card(self, card_id):
        return Card(card_id, self.name, self.attack, self.defense, self.health, self.power,
                    {abil: self.abilities[abil][0] for abil in self.abilities})
