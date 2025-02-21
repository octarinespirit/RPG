"""Importing random to randomize the magic damage"""
import random

class Spell:
    """Initializing class Spell with parameters"""
    def __init__(self, name, cost, dmg, type) -> None:
        self.name = name
        self.cost = cost
        self.dmg = dmg
        self.type = type

    def generate_damage(self):
        """Method to generate magic damage"""
        low = self.dmg - 15
        high = self.dmg + 15
        return random.randrange(low, high)
