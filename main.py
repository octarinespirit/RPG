"""Importing random to generate random damage or random healing"""
import random
from Utils.utils import action_choice, magic_choice, item_choice, check_battle_status
from Classes.rpg import Person, bcolors
from Classes.magic import Spell
from Classes.inventory import Item

# Create black magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 60, 1400, "black")

# Create white magic
cure = Spell("Small Healing Spell", 25, 620, "white")
cura = Spell("Medium Healing Spell", 35, 1500, "white")
curo = Spell("Super Healing Spell", 60, 5000, "white")

# Create some items
potion = Item("Potion", "potion", "Heals 50 HP", 500)
greatpotion = Item("Great Potion", "potion", "Heals 100 HP", 1000)
superpotion = Item("Super Potion", "potion", "Heals 1000 HP", 3000)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member", 9999)
superelixir = Item("Super Elixir", "elixir", "Fully restores party's HP/MP", 9999)
bomb = Item("Bomb", "attack", "Deals 500 damage", 1500)

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire, meteor, curo]

player_items = [{"item": potion, "quantity": 15},
                {"item": greatpotion, "quantity": 5},
                {"item": superpotion, "quantity": 5},
                {"item": elixir, "quantity": 5},
                {"item": superelixir, "quantity": 5},
                {"item": bomb, "quantity": 5}]

# Instantiate fighters
player1 = Person("Taneli", 4000, 165, 300, player_spells, player_items)
player2 = Person("Juhani", 4000, 165, 300, player_spells, player_items)
player3 = Person("Pertti", 4000, 165, 300, player_spells, player_items)

enemy1 = Person("Graazz", 18000, 700, 800, enemy_spells, [])
enemy2 = Person("Zombie", 1500, 120, 550, enemy_spells, [])
enemy3 = Person("Sarokk", 1500, 120, 550, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

RUNNING = True

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while RUNNING:
    print("=============================================")

    # Display stats once at the beginning of each round
    print("\n\nNAME                   HP                                      MP")
    for player in players:
        player.get_stats()
    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()
    # Player's turn handling
    if RUNNING:
        for player in players:
            if player.get_hp() <= 0:
                continue  # Skip dead players

            player.choose_action()
            action = action_choice()  # Get the action choice

            if action == 1:  # Attack
                dmg = player.generate_damage()
                target_index = player.choose_target(enemies)
                if target_index is not None:
                    enemies[target_index].take_damage(dmg)
                    print(f"You attacked {enemies[target_index].name.replace(' ', '')} for {dmg} points of damage.")

                    if enemies[target_index].get_hp() == 0:
                        print(bcolors.OKGREEN + enemies[target_index].name.replace(" ", "") + " has died." + bcolors.ENDC)
                        del enemies[target_index]

                # Check if there are no enemies left
                RUNNING = check_battle_status(players, enemies)
                if not RUNNING:
                    break  # End the current player's turn if the battle is over

            elif action == 2:  # Magic
                while True:  # Loop for the Magic menu
                    player.choose_magic()
                    magic = magic_choice()

                    if magic == -1:  # Go back to Actions menu
                        print("Returning to Actions menu.")
                        break  # Break the magic loop and return to actions

                    spell = player.magic[magic - 1]
                    if spell.cost > player.get_mp():
                        print(bcolors.FAIL + "\nNot enough MP!" + bcolors.ENDC)
                        continue  # Retry the Magic menu if MP is insufficient

                    # Handle white magic (healing)
                    if spell.type == "white":
                        player.reduce_mp(spell.cost)
                        healing = spell.generate_damage()
                        player.heal(healing)
                        print(f"{player.name} casts {spell.name} on themselves and heals {healing} HP.")

                    # Handle black magic (damage)
                    elif spell.type == "black":
                        if len(enemies) > 0:
                            target_index = player.choose_target(enemies)
                            if target_index is not None:
                                player.reduce_mp(spell.cost)
                                damage = spell.generate_damage()
                                enemies[target_index].take_damage(damage)
                                print(f"{player.name} casts {spell.name} on {enemies[target_index].name} and deals {damage} damage.")
                                if enemies[target_index].get_hp() == 0:
                                    print(bcolors.BOLD + bcolors.OKGREEN +
                                          f"{enemies[target_index].name} has died!" + bcolors.ENDC)
                                    del enemies[target_index]
                    break
            # Check if the battle has ended after magic is used
            RUNNING = check_battle_status(players, enemies)
            if not RUNNING:
                break  # End the current player's turn if the battle is over

            if action == 3:  # Item
                while True:  # Loop for the Item menu
                    player.choose_item()
                    chosen_item = item_choice()

                    if chosen_item == -1:  # Go back to Actions menu
                        break  # Break the item loop and return to actions menu

                    item = player.items[chosen_item - 1]["item"]
                    if player.items[chosen_item - 1]["quantity"] == 0:
                        print(bcolors.FAIL + "\nSorry, you don't have any more of that item!"
                              + bcolors.ENDC)
                        continue  # Retry the Item menu if no more items

                    # Handle items
                    if item.type == "potion":
                        player.heal(item.prop)
                    elif item.type == "elixir":
                        if item.name == "Super Elixir":
                            for member in players:
                                member.hp = member.maxhp
                                member.mp = member.maxmp
                            print(bcolors.OKGREEN +
                                  f"\n{item.name} fully restores the party's HP/MP!"
                                  + bcolors.ENDC)
                        else:
                            player.hp = player.maxhp
                            player.mp = player.maxmp
                            print(bcolors.OKGREEN + f"\n{item.name} fully restores HP/MP!"
                                  + bcolors.ENDC)
                    elif item.type == "attack":
                        target_index = player.choose_target(enemies)
                        if target_index is not None:
                            enemies[target_index].take_damage(item.prop)
                            print(f"{player.name} used a {item.name} on {enemies[target_index].name} dealing {item.prop} damage.")
                            if enemies[target_index].get_hp() == 0:
                                print(bcolors.BOLD + bcolors.OKGREEN +
                                      f"{enemies[target_index].name} has died!" + bcolors.ENDC)
                                del enemies[target_index]

                    player.items[chosen_item - 1]["quantity"] -= 1  # Reduce item count
                    break
            # Check if the battle has ended after using item
            RUNNING = check_battle_status(players, enemies)
            if not RUNNING:
                break  # End the current player's turn if the battle is over

    # Enemy's turn handling
    if RUNNING:
        for enemy in enemies:
            if enemy.get_hp() <= 0:
                continue  # Skip dead enemies

            # Randomly decide to attack or use magic
            enemy_action = random.choice(["attack", "magic"])

            if enemy_action == "magic":
                spell, magic_dmg = enemy.choose_enemy_spell()
                if spell.cost <= enemy.get_mp():  # Ensure enemy has enough MP
                    enemy.reduce_mp(spell.cost)
                    if spell.type == "black":
                        target_index = random.choice([i for i,
                        player in enumerate(players) if player.get_hp() > 0])
                        players[target_index].take_damage(magic_dmg)
                        print(f"{enemy.name} casts {spell.name} on {players[target_index].name} for {magic_dmg} damage.")
                        if players[target_index].get_hp() == 0:
                            print(bcolors.BOLD + bcolors.FAIL +
                                  f"{players[target_index].name} has been defeated!" + bcolors.ENDC)
                            RUNNING = check_battle_status(players, enemies)

                    if not RUNNING:
                        break  # End the current enemy's turn if the battle is over

                    if spell.type == "white":
                        enemy.heal(magic_dmg)
                        print(f"{enemy.name} casts {spell.name} and heals for {magic_dmg} HP.")
                else:
                    enemy_action = "attack"  # Fallback to attack if no MP

            if enemy_action == "attack":
                target_index = random.choice([i for i,
                player in enumerate(players) if player.get_hp() > 0])
                dmg = enemy.generate_damage()
                players[target_index].take_damage(dmg)
                print(f"{enemy.name} attacks {players[target_index].name} for {dmg} points of damage.")
                if players[target_index].get_hp() == 0:
                    print(bcolors.BOLD + bcolors.FAIL +
                          f"{players[target_index].name} has been defeated!" + bcolors.ENDC)
                    RUNNING = check_battle_status(players, enemies)

            if not RUNNING:
                break  # End the current enemy's turn if the battle is over
