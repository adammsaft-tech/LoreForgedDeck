import customtkinter as ctk
import random
import json
import os

from screens.home_screen import show_home_screen
from screens.dice_screen import show_dice_screen
from screens.character_screen import (
    show_character_screen,
    show_create_character_screen
)


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

MAX_HISTORY = 5

class LoreforgedDeck(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Loreforged Deck")
        self.geometry("800x480")

        self.current_die = 20
        self.roll_animation_count = 0
        self.roll_history = []

        self.show_home_screen()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_home_screen(self):
        show_home_screen(self)

    def show_dice_screen(self):
        show_dice_screen(self)

    def show_character_screen(self):
        show_character_screen(self)

    def show_create_character_screen(self):
        show_create_character_screen(self)

    def save_character(self):
        name = self.character_name_entry.get().strip()
        character_class = self.character_class_entry.get().strip()
        level_text = self.character_level_entry.get().strip()

        if not name or not character_class:
            print("Character name and class are required.")
            return

        try:
            level = int(level_text)
        except ValueError:
            print("Level must be a number.")
            return

        character_data = {
            "name": name,
            "class": character_class,
            "level": level
        }

        characters_folder = os.path.join(
            os.path.dirname(__file__),
            "characters"
        )

        os.makedirs(characters_folder, exist_ok=True)

        safe_filename = "".join(
            character for character in name
            if character.isalnum() or character in (" ", "-", "_")
        ).strip()

        file_path = os.path.join(
            characters_folder,
            f"{safe_filename}.json"
        )

        with open(file_path, "w", encoding="utf-8") as character_file:
            json.dump(character_data, character_file, indent=4)

        print(f"Saved character: {file_path}")
        self.show_character_screen()

    def load_characters(self):
        characters_folder = os.path.join(
            os.path.dirname(__file__),
            "characters"
        )

        os.makedirs(characters_folder, exist_ok=True)

        characters = []

        for filename in os.listdir(characters_folder):
            if filename.endswith(".json"):
                file_path = os.path.join(characters_folder, filename)

                try:
                    with open(file_path, "r", encoding="utf-8") as character_file:
                        character_data = json.load(character_file)

                    character_data["_filename"] = filename
                    characters.append(character_data)

                except (json.JSONDecodeError, OSError) as error:
                    print(f"Could not load {filename}: {error}")

        return characters

    def show_character_details(self, character):
        self.clear_screen()

        self.selected_character = character

        name = character.get("name", "Unnamed Character")
        character_class = character.get("class", "Unknown Class")
        level = character.get("level", 1)

        title = ctk.CTkLabel(
            self,
            text=name,
            font=("Arial", 34, "bold")
        )
        title.pack(pady=(45, 15))

        details = ctk.CTkLabel(
            self,
            text=f"Level {level} {character_class}",
            font=("Arial", 22)
        )
        details.pack(pady=10)

        edit_button = ctk.CTkButton(
            self,
            text="Edit Character",
            width=200,
            height=42,
            command=self.show_edit_character_screen
        )
        edit_button.pack(pady=10)

        delete_button = ctk.CTkButton(
            self,
            text="Delete Character",
            width=200,
            height=42,
            fg_color="darkred",
            hover_color="red",
            command=self.delete_character
        )
        delete_button.pack(pady=10)

        back_button = ctk.CTkButton(
            self,
            text="← Back to Characters",
            width=180,
            command=self.show_character_screen
        )
        back_button.pack(side="bottom", pady=25)

    def show_edit_character_screen(self):
        self.clear_screen()

        character = self.selected_character

        title = ctk.CTkLabel(
            self,
            text="Edit Character",
            font=("Arial", 32, "bold")
        )
        title.pack(pady=(30, 20))

        name_label = ctk.CTkLabel(
            self,
            text="Character Name",
            font=("Arial", 18)
        )
        name_label.pack(pady=(10, 5))

        self.edit_name_entry = ctk.CTkEntry(
            self,
            width=300,
            height=40
        )
        self.edit_name_entry.insert(0, character.get("name", ""))
        self.edit_name_entry.pack()

        class_label = ctk.CTkLabel(
            self,
            text="Class",
            font=("Arial", 18)
        )
        class_label.pack(pady=(20, 5))

        self.edit_class_entry = ctk.CTkEntry(
            self,
            width=300,
            height=40
        )
        self.edit_class_entry.insert(0, character.get("class", ""))
        self.edit_class_entry.pack()

        level_label = ctk.CTkLabel(
            self,
            text="Level",
            font=("Arial", 18)
        )
        level_label.pack(pady=(20, 5))

        self.edit_level_entry = ctk.CTkEntry(
            self,
            width=100,
            height=40
        )
        self.edit_level_entry.insert(0, str(character.get("level", 1)))
        self.edit_level_entry.pack()

        save_button = ctk.CTkButton(
            self,
            text="Save Changes",
            width=220,
            height=45,
            command=self.update_character
        )
        save_button.pack(pady=25)

        back_button = ctk.CTkButton(
            self,
            text="← Cancel",
            width=120,
            command=lambda: self.show_character_details(
                self.selected_character
            )
        )
        back_button.pack(side="bottom", pady=20)

    def update_character(self):
        name = self.edit_name_entry.get().strip()
        character_class = self.edit_class_entry.get().strip()
        level_text = self.edit_level_entry.get().strip()

        if not name or not character_class:
            print("Character name and class are required.")
            return

        try:
            level = int(level_text)
        except ValueError:
            print("Level must be a number.")
            return

        old_filename = self.selected_character.get("_filename")

        if not old_filename:
            print("Could not find the character file.")
            return

        characters_folder = os.path.join(
            os.path.dirname(__file__),
            "characters"
        )

        old_file_path = os.path.join(
            characters_folder,
            old_filename
        )

        safe_filename = "".join(
            character for character in name
            if character.isalnum() or character in (" ", "-", "_")
        ).strip()

        new_filename = f"{safe_filename}.json"
        new_file_path = os.path.join(
            characters_folder,
            new_filename
        )

        updated_character = {
            "name": name,
            "class": character_class,
            "level": level
        }

        with open(new_file_path, "w", encoding="utf-8") as character_file:
            json.dump(updated_character, character_file, indent=4)

        if old_file_path != new_file_path and os.path.exists(old_file_path):
            os.remove(old_file_path)

        updated_character["_filename"] = new_filename
        self.selected_character = updated_character

        self.show_character_details(updated_character)

    def delete_character(self):
        filename = self.selected_character.get("_filename")

        if not filename:
            print("Could not find the character file.")
            return

        file_path = os.path.join(
            os.path.dirname(__file__),
            "characters",
            filename
        )

        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted character: {file_path}")

        self.selected_character = None
        self.show_character_screen()

    def roll_die(self, sides):
        self.current_die = sides
        self.roll_animation_count = 0
        self.animation_speeds = [35, 40, 45, 55, 70, 90, 115, 145, 180, 220]
        self.animate_roll()

    def animate_roll(self):
        temp_roll = random.randint(1, self.current_die)
        self.result_label.configure(text=f"Rolling... {temp_roll}")

        if self.roll_animation_count < len(self.animation_speeds):
            delay = self.animation_speeds[self.roll_animation_count]
            self.roll_animation_count += 1
            self.after(delay, self.animate_roll)
        else:
            self.finish_roll()

    def finish_roll(self):
        try:
            modifier = int(self.modifier_entry.get())
        except ValueError:
            modifier = 0

        roll = random.randint(1, self.current_die)
        total = roll + modifier

        if self.current_die == 20 and roll == 20:
            result_text = f"✨ NATURAL 20! ✨\nD20: {roll} + {modifier} = {total}"
        elif self.current_die == 20 and roll == 1:
            result_text = f"💀 NATURAL 1! 💀\nD20: {roll} + {modifier} = {total}"
        else:
            result_text = f"D{self.current_die}: {roll} + {modifier} = {total}"

        self.result_label.configure(text=result_text)
        self.add_to_history(
            f"D{self.current_die}: {roll} + {modifier} = {total}"
        )

    def add_to_history(self, roll_text):
        self.roll_history.insert(0, roll_text)

        if len(self.roll_history) > MAX_HISTORY:
            self.roll_history.pop()

        self.history_label.configure(
            text="\n".join(self.roll_history)
        )

    def clear_history(self):
        self.roll_history.clear()
        self.history_label.configure(text="")


app = LoreforgedDeck()
app.mainloop()