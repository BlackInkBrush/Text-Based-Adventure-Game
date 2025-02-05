import os
import json
from termcolor import colored


class AdventureGame:
    def __init__(self):
        self.allowed_commands_nums = {1, 2, 3}
        self.allowed_commands_cmd = {"start", "load", "quit"}
        self.allowed_difficulty = {1, 2, 3}
        self.allowed_difficulty_cmd = {"easy": 5, "medium": 3, "hard": 1}
        self.starting_phrase = "***Welcome to the Journey to Mount Qaf***"
        self.user_name = None
        self.inventory = {"Snack": None, "Weapon": None, "Tool": None}
        self.attributes = {"Name": None, "Species": None, "Gender": None}
        self.initial_snack = None
        self.initial_weapon = None
        self.initial_tool = None
        self.difficulty = None
        self.remaining_lives = None
        self.available_commands = {"/i": "Shows inventory.", "/q": "Exits the game.",
                                   "/c": "Shows the character traits.", "/h": "Shows help.",
                                   "/s": "Save the game"}
        self.story_file_name = "story.json"
        self.story_file_path = os.path.join(os.getcwd(), "data", self.story_file_name)
        self.story = self.load_story_json(self.story_file_path)
        self.level = "level1"
        self.scene = "scene1"
        # New attribute: list of active inventory items.
        self.inventory_content = []

    def start(self):
        print(colored("Starting a new game...", "green", on_color="on_black", attrs=["bold"]))
        go_to_main_menu = self.enter_username()
        if not go_to_main_menu:
            self.main_menu()
        self.create_character()
        self.create_inventory()
        self.choose_difficulty()
        self.show_stats()
        self.main_loop()

    def quit(self):
        print(colored("Goodbye!", "green", on_color="on_black", attrs=["bold"]))

    def load_save_file(self):
        print("Choose username (/b - back):")
        files = [f[:-5] for f in os.listdir("./data/saves") if f.endswith(".json")]
        if files:
            for file in files:
                print(file)
        else:
            print(colored("No saved data found!", "green", on_color="on_black", attrs=["bold"]))
            self.main_menu()
        user_input = input().lower()
        while user_input not in files:
            if user_input == "/b":
                self.main_menu()
            else:
                print("Unknown input! Please enter a valid one.")
                user_input = input().lower()
        print("Loading your progress...")
        self.user_name = user_input
        file_path = os.path.join("./data/saves", f"{user_input}.json")
        progress = self.load_story_json(file_path)
        return progress

    def load(self, progress):
        character = progress["character"]
        inventory = progress["inventory"]
        story_progression = progress["progress"]
        self.attributes["Name"] = character["name"]
        self.attributes["Species"] = character["species"]
        self.attributes["Gender"] = character["gender"]
        self.inventory["Snack"] = inventory["snack_name"]
        self.inventory["Weapon"] = inventory["weapon_name"]
        self.inventory["Tool"] = inventory["tool_name"]
        self.initial_snack = inventory["snack_name"]
        self.initial_weapon = inventory["weapon_name"]
        self.initial_tool = inventory["tool_name"]
        # Load the active inventory list from save file
        self.inventory_content = inventory["content"]
        self.remaining_lives = progress["lives"]
        self.difficulty = progress["difficulty"]
        self.level = story_progression["level"]
        self.scene = story_progression["scene"]
        current_level = self.level.replace("level", "")
        print(f"Level {current_level}")
        self.main_loop()

    def load_story_json(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    def validate_user_input(self, user_input):
        if isinstance(user_input, int):
            if user_input not in self.allowed_commands_nums:
                print(colored("Unknown input! Please enter a valid one.", "green", on_color="on_black", attrs=["bold"]))
                return False
        elif isinstance(user_input, str):
            if user_input.lower() not in self.allowed_commands_cmd:
                print(colored("Unknown input! Please enter a valid one.", "green", on_color="on_black", attrs=["bold"]))
                return False
        return True  # Input is valid

    def validate_difficulty_level(self, user_input):
        if isinstance(user_input, int):
            if user_input not in self.allowed_difficulty:
                print(colored("Unknown input! Please enter a valid one.", "green", on_color="on_black", attrs=["bold"]))
                return False
        elif isinstance(user_input, str):
            if user_input.lower() not in self.allowed_difficulty_cmd:
                print(colored("Unknown input! Please enter a valid one.", "green", on_color="on_black", attrs=["bold"]))
                return False
        return True

    def get_user_input(self):
        user_text = input()
        if user_text.isdigit():
            return int(user_text)
        return user_text.lower()

    def enter_username(self):
        username = input(colored("Enter a username ('/b' to go back):", "green", on_color="on_black", attrs=["bold"]))
        if username.lower() != "/b":
            self.user_name = username
            return True
        return False

    def show_game_options(self):
        print(colored("""
        1. Start a new game (START)
        2. Load your progress (LOAD)
        3. Quit the game (QUIT)
        """, "green", on_color="on_black", attrs=["bold"]))

    def create_character(self):
        print(colored("Create your character:", "green", on_color="on_black", attrs=["bold"]))
        for attribute in self.attributes.keys():
            current_attribute = input(colored(f"{attribute}: ", "green", on_color="on_black", attrs=["bold"]))
            self.attributes[attribute] = current_attribute

    def create_inventory(self):
        print(colored("Pack your bag for the journey:", "green", on_color="on_black", attrs=["bold"]))
        for key in self.inventory.keys():
            inventory_choosing = input(colored(f"{key}: ", "green", on_color="on_black", attrs=["bold"]))
            if key == "Snack" and not inventory_choosing.strip():
                inventory_choosing = "cookie"
            self.inventory[key] = inventory_choosing
        self.initial_weapon = self.inventory["Weapon"]
        self.initial_tool = self.inventory["Tool"]
        self.initial_snack = self.inventory["Snack"]
        # Set the active inventory list to the base items
        self.inventory_content = [
            self.inventory["Snack"],
            self.inventory["Weapon"],
            self.inventory["Tool"]
        ]

    def show_stats(self):
        print(colored(f"""
        Good luck on your journey, {self.user_name}!
        Your character: {self.attributes['Name']}, {self.attributes['Species']}, {self.attributes['Gender']}
        Your inventory: {self.inventory['Snack']}, {self.inventory['Weapon']}, {self.inventory['Tool']}
        Difficulty: {self.difficulty}
        Number of lives: {self.remaining_lives}
        """, "green", on_color="on_black", attrs=["bold"]))

    def replace_placeholder(self, s):
        if self.inventory["Tool"]:
            s = s.replace("{tool}", self.inventory["Tool"])
        if self.inventory["Snack"]:
            s = s.replace("{snack}", self.inventory["Snack"])
        if self.inventory["Weapon"]:
            s = s.replace("{weapon}", self.inventory["Weapon"])
        return s

    def show_inventory(self):
        # Show the active inventory (the content list)
        print(colored("Inventory: " + ", ".join(self.inventory_content), "green", on_color="on_black", attrs=["bold"]))

    def show_character(self):
        print(colored("Your character: " + ", ".join(map(str, self.attributes.values())), "green", on_color="on_black", attrs=["bold"]))
        print(colored(f"Lives remaining: {str(self.remaining_lives)}", "green", on_color="on_black", attrs=["bold"]))

    def help_page(self):
        print(colored("Type the number of option you want to choose.\nCommands you can use:", "green", on_color="on_black", attrs=["bold"]))
        for command, text in self.available_commands.items():
            print(colored(f"{command} => {text}", "green", on_color="on_black", attrs=["bold"]))

    def main_loop(self):
        while self.level != "level4":
            current_level = self.story[self.level]
            current_scene = current_level["scenes"][self.scene]
            print(self.scene)
            print(colored(current_scene["text"], "green", on_color="on_black", attrs=["bold"]))
            for index, option in enumerate(current_scene["options"], start=1):
                print(colored(f"{str(index)}. {self.replace_placeholder(option['option_text'])}", "green", on_color="on_black", attrs=["bold"]))
            user_input = input()
            while not user_input.isdigit():
                user_input = user_input.lower()
                if user_input == "/i":
                    self.show_inventory()
                elif user_input == "/c":
                    self.show_character()
                elif user_input == "/q":
                    print(colored("Thanks for playing!", "green", on_color="on_black", attrs=["bold"]))
                    exit()
                elif user_input == "/h":
                    self.help_page()
                elif user_input == "/s":
                    self.save_progress()
                    print(self.scene)
                else:
                    print(colored("Unknown input! Please enter a valid one.", "green", on_color="on_black", attrs=["bold"]))
                user_input = input()

            decision = int(user_input) - 1

            self.scene = current_scene["options"][decision]["next"]
            result_text = self.replace_placeholder(current_scene["options"][decision]["result_text"])
            print(colored(result_text, "green", on_color="on_black", attrs=["bold"]))
            self.perform_actions(current_scene["options"][decision]["actions"])
            if self.scene == "end":
                if self.level == "level1":
                    self.level = "level2"
                    self.scene = "scene1"
                    print(colored("Level 2", "green", on_color="on_black", attrs=["bold"]))
                elif self.level == "level2":
                    self.level = "level3"
                    self.scene = "scene1"
                    print(colored("Level 3", "purple", on_color="on_black", attrs=["bold"]))

    def perform_actions(self, actions):
        for action in actions:
            action = self.replace_placeholder(action)
            if action == "hit" or action == "heal":
                if action == "hit":
                    if self.remaining_lives == 1:
                        self.user_died()
                    else:
                        self.remaining_lives -= 1
                else:
                    self.remaining_lives += 1
                print(colored(f"Lives remaining: {str(self.remaining_lives)}", "green", on_color="on_black", attrs=["bold"]))
            elif action.startswith('+'):
                # Add extra item to active inventory
                item = action.replace("+", "")
                self.inventory_content.append(item)
                print(colored(f"Item added: {item}", "green", on_color="on_black", attrs=["bold"]))
            elif action.startswith('-'):
                # Remove item from active inventory, if present
                item = action.replace("-", "")
                if item in self.inventory_content:
                    self.inventory_content.remove(item)
                    print(colored(f"Item removed: {item}", "green", on_color="on_black", attrs=["bold"]))

    def save_progress(self):
        file_name = f"{self.user_name}.json"
        file_path = "./data/saves"
        full_file_path = os.path.join(file_path, file_name)
        data = self.create_new_file()

        print(f"Saving progress: Level={self.level}, Scene={self.scene}")  # Debug-Print

        with open(full_file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)
        print(colored("Game saved!", "green", on_color="on_black", attrs=["bold"]))

    def create_new_file(self):
        character = {"character": {k.lower(): v for (k, v) in self.attributes.items()}}
        inventory = {
            "inventory": {
                "snack_name": self.initial_snack,
                "weapon_name": self.initial_weapon,
                "tool_name": self.initial_tool,
                "content": self.inventory_content
            }
        }
        progress = {
            "progress": {"level": self.level, "scene": self.scene},
            "lives": self.remaining_lives,
            "difficulty": self.difficulty
        }
        file_content = {**character, **inventory, **progress}
        return file_content

    def user_died(self):
        print(colored("You died", "green", on_color="on_black", attrs=["bold"]))
        self.level = "level1"
        self.scene = "scene1"
        self.main_loop()

    def choose_difficulty(self):
        print(colored("Choose your difficulty: ", "green", on_color="on_black", attrs=["bold"]))
        print(colored("""
        1. Easy
        2. Medium
        3. Hard
        """, "green", on_color="on_black", attrs=["bold"]))
        user_input = self.get_user_input()
        while not self.validate_difficulty_level(user_input):
            user_input = self.get_user_input()
        if user_input == 1 or user_input == "easy":
            self.difficulty = "easy"
        elif user_input == 2 or user_input == "medium":
            self.difficulty = "medium"
        else:
            self.difficulty = "hard"
        self.remaining_lives = self.allowed_difficulty_cmd[self.difficulty]

    def main_menu(self):
        print(colored(self.starting_phrase, "green", on_color="on_black", attrs=["bold"]))
        print(colored("\n", "green", on_color="on_black", attrs=["bold"]))
        self.show_game_options()
        user_command = None

        while user_command != 3 and user_command != "quit":
            user_command = self.get_user_input()
            while not self.validate_user_input(user_command):
                user_command = self.get_user_input()
            if user_command == 1 or user_command == "start":
                self.start()
            elif user_command == 2 or user_command == "load":
                self.load(self.load_save_file())
            elif user_command == 3 or user_command == "quit":
                self.quit()
                break


game = AdventureGame()
game.main_menu()
