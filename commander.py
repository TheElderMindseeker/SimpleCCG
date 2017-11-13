class Commander:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def deal_damage(self, damage):
        self.health -= damage

    def heal(self, heal):
        self.health += heal

    def is_alive(self):
        return self.health > 0
