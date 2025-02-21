"""Inventory module for the party member inventories"""
class Item:
    """Class for the player/party member inventory"""
    def __init__(self, name, type, desc, prop) -> None:
        self.name = name
        self.type = type
        self.desc = desc
        self.prop = prop
