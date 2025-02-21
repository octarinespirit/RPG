"""Module containing useful functions for the main.py"""
class bcolors:
    """Class to create colors for the text prints"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def action_choice():
    """Function for the player turn, to get player choice as an input"""
    valid_choices = [1, 2, 3]
    while True:
        try:
            player_input = int(input("Choose action (1: Attack, 2: Magic, 3: Item): ").strip())
            if player_input in valid_choices:
                return player_input
            else:
                print("Invalid choice. Please choose 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number (1, 2, or 3).")

def magic_choice():
    """Function for the player turn, to get the player's magic choice as an input"""
    valid_choices = list(range(1, 8)) + [-1]  # Add -1 for "Go Back"
    while True:
        try:
            player_input = int(input("Choose magic (1-7, or -1 to go back): ").strip())
            if player_input in valid_choices:
                return player_input
            else:
                print("Invalid choice. Please choose 1-7 or -1 to go back.")
        except ValueError:
            print("Invalid input. Please enter a number (1-7, or -1 to go back).")

def item_choice():
    """Function for the player turn, to get the player's item choice as an input"""
    valid_choices = list(range(1, 7)) + [-1]  # Add -1 for "Go Back"
    while True:
        try:
            player_input = int(input("Choose item (1-6, or -1 to go back): ").strip())
            if player_input in valid_choices:
                return player_input
            else:
                print("Invalid choice. Please choose 1-6 or -1 to go back.")
        except ValueError:
            print("Invalid input. Please enter a number (1-6, or -1 to go back).")

def check_battle_status(players, enemies):
    """Function to check if all enemies are dead and if all player's party members are dead"""
    # Check if all enemies are defeated
    if not any(enemy.get_hp() > 0 for enemy in enemies):
        print(bcolors.OKGREEN + "All enemies are defeated! You have won the battle!" + bcolors.ENDC)
        return False  # Game ends with player victory

    # Check if all players are defeated
    if not any(player.get_hp() > 0 for player in players):
        print(bcolors.FAIL + "All players are defeated! The enemies have won the battle!" 
              + bcolors.ENDC)
        return False  # Game ends with enemy victory

    return True  # Game continues
