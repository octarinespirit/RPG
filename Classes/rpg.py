"""Importing random to randomize damage"""
import random

class bcolors:
    """Class to create colors to the text prints"""

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Person:
    """Class do define our party members and enemies"""
    def __init__(self, name, hp, mp, atk, magic, items) -> None:
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]

    def generate_damage(self):
        """Method to generate attack damage"""
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        """Method to make someone to take damage"""
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        """Method to heal self"""
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def get_hp(self):
        """Method to check someone's hp"""
        return self.hp

    def get_max_hp(self):
        """Method to check someone's max hp"""
        return self.maxhp

    def get_mp(self):
        """Method to check someone's magic points"""
        return self.mp

    def get_max_mp(self):
        """Method to check someone's max magic points"""
        return self.maxmp

    def reduce_mp(self, cost):
        """Method to reduce someone's magic points when casting a spell"""
        self.mp -= cost

    def choose_action(self):
        """Method to print the available action choices to the player"""
        i = 1
        print("\n" + "    " + bcolors.BOLD + self.name + bcolors.ENDC)
        print(bcolors.OKBLUE + bcolors.BOLD + "    ACTIONS" + bcolors.ENDC)
        for item in self.actions:
            print("        " + str(i) + ".", item)
            i += 1

    def choose_magic(self):
        """Method to print the available magic spells for the player"""
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "    MAGIC" + bcolors.ENDC)
        for spell in self.magic:
            print("        " + str(i) + ".", spell.name, "(cost:", str(spell.cost) + ")")
            i += 1

    def choose_item(self):
        """Method to print the available item choices for the player"""
        i = 1
        print("\n" + bcolors.OKGREEN + bcolors.BOLD + "    ITEMS" + bcolors.ENDC)
        for item in self.items:
            print("        " + str(i) + ".", item["item"].name + ":", item["item"].desc, 
                  " (x" + str(item["quantity"]) + ")")
            i += 1

    def choose_target(self, enemies):
        """Method to print the available enemies to target for the player"""
        valid_choices = [i for i, enemy in enumerate(enemies) if enemy.get_hp() > 0]  
        # Indices of living enemies
        while True:
            print("\n" + bcolors.FAIL + bcolors.BOLD + "    TARGET:" + bcolors.ENDC)
            for i, enemy in enumerate(enemies):
                if enemy.get_hp() > 0:
                    print(f"        {i + 1}. {enemy.name}")  # Display only living enemies

            try:
                choice = int(input("    Choose target: ")) - 1  # Convert input to 0-based index
                if choice in valid_choices:
                    return choice  # Return valid choice
                else:
                    print("Invalid choice. Please choose a valid target.")
            except ValueError:
                print("Invalid input. Please enter a number corresponding to a target.")


    def get_enemy_stats(self):
        """Method to print the enemy stats in the beginning of the turn"""
        hp_bar = ""
        bar_blocks = (self.hp / self.maxhp) * 100 / 2
        while bar_blocks > 0:
            hp_bar += "█"
            bar_blocks -= 1

        while len(hp_bar) < 50:
            hp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 11:
            decreased = 11 - len(hp_string)
            while decreased > 0:
                current_hp += " "
                decreased -= 1
            current_hp += hp_string
        else:
            current_hp = hp_string

        print("                         __________________________________________________ ")
        print(bcolors.BOLD + self.name + " :" + current_hp + " HP " + bcolors.ENDC +  " |" +
        bcolors.FAIL + hp_bar + bcolors.ENDC + "|")

    def get_stats(self):
        """Method to print the party member stats in the beginning of the turn"""
        hp_bar = ""
        bar_blocks = (self.hp / self.maxhp) * 100 / 4
        while bar_blocks > 0:
            hp_bar += "█"
            bar_blocks -= 1

        while len(hp_bar) < 25:
            hp_bar += " "

        mp_bar = ""
        mpbar_blocks = (self.mp / self.maxmp) * 100 / 10
        while mpbar_blocks > 0:
            mp_bar += "█"
            mpbar_blocks -= 1

        while len(mp_bar) < 10:
            mp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 9:
            decreased = 9 - len(hp_string)
            while decreased > 0:
                current_hp += " "
                decreased -= 1
            current_hp += hp_string
        else:
            current_hp = hp_string

        mp_string = str(self.mp) + "/" + str(self.maxmp)
        current_mp = ""

        if len(mp_string) < 7:
            decreased_mp = 7 - len(mp_string)
            while decreased_mp > 0:
                current_mp += " "
                decreased_mp -= 1
            current_mp += mp_string
        else:
            current_mp = mp_string

        print("                       _________________________               __________ ")
        print(bcolors.BOLD + self.name + " : " + current_hp + " HP" + bcolors.ENDC +  " |" +
        bcolors.OKGREEN + hp_bar + bcolors.ENDC   + "|  " +
        bcolors.BOLD + current_mp + " MP" + bcolors.ENDC + " |" + bcolors.OKBLUE + mp_bar 
        + bcolors.ENDC + "|")

    def choose_enemy_spell(self):
        """Method for the enemies to choose the spell they cast. 
        Healing only if below 50% of their hit points"""
        # Loop until a valid spell is chosen
        while True:
            magic_choice = random.randrange(0, len(self.magic))
            spell = self.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            pct = self.hp / self.maxhp * 100  # Calculate health percentage

            # Check if the spell can be cast (enough MP and not white magic if HP > 50%)
            if self.mp >= spell.cost and (spell.type != "white" or pct <= 50):
                return spell, magic_dmg  # Return the valid spell and its damage

            # If the spell is not valid, continue the loop to try another one
            # (No need for recursion here)
