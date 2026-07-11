import customtkinter as ctk
import random

from screens.home_screen import show_home_screen
from screens.dice_screen import show_dice_screen
from screens.character_screen import show_character_screen


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

        if len(self.roll_history) > MAX_HISTORY:
            self.roll_history.pop()

        history_text = "Roll History\n\n" + "\n".join(self.roll_history)
        self.history_label.configure(text=history_text)


app = LoreforgedDeck()
app.mainloop()