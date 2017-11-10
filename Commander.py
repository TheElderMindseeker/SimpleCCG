class Commander:
    def __init__(self, name, life_total):
        self.name = name
        self.life_total = life_total

    def deal_damage(self, damage):
        self.life_total -= damage

    def heal(self, heal):
        self.life_total += heal

    def is_alive(self):
        return self.life_total > 0
