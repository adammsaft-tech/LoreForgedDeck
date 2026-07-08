import customtkinter as ctk
import random

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


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
        self.clear_screen()

        title = ctk.CTkLabel(
            self,
            text="⚔ Loreforged Deck ⚔",
            font=("Arial", 36, "bold")
        )
        title.pack(pady=(50, 10))

        subtitle = ctk.CTkLabel(
            self,
            text="Adventurer's Companion",
            font=("Arial", 18)
        )
        subtitle.pack(pady=(0, 40))

        dice_button = ctk.CTkButton(
            self,
            text="🎲 Dice Roller",
            width=250,
            height=45,
            font=("Arial", 18),
            command=self.show_dice_screen
        )
        dice_button.pack(pady=10)

        character_button = ctk.CTkButton(
            self,
            text="👤 Characters",
            width=250,
            height=45,
            font=("Arial", 18)
        )
        character_button.pack(pady=10)

        settings_button = ctk.CTkButton(
            self,
            text="⚙ Settings",
            width=250,
            height=45,
            font=("Arial", 18)
        )
        settings_button.pack(pady=10)

        version = ctk.CTkLabel(
            self,
            text="Version 0.2",
            font=("Arial", 12)
        )
        version.pack(side="bottom", pady=10)

    def show_dice_screen(self):
        self.clear_screen()

        title = ctk.CTkLabel(
            self,
            text="🎲 Dice Roller",
            font=("Arial", 34, "bold")
        )
        title.pack(pady=(20, 10))

        dice_frame = ctk.CTkFrame(self)
        dice_frame.pack(pady=10)

        dice = [4, 6, 8, 10, 12, 20, 100]

        for die in dice:
            button = ctk.CTkButton(
                dice_frame,
                text=f"D{die}",
                width=90,
                height=45,
                font=("Arial", 16),
                command=lambda d=die: self.roll_die(d)
            )
            button.pack(side="left", padx=5, pady=10)

        modifier_label = ctk.CTkLabel(
            self,
            text="Modifier",
            font=("Arial", 18)
        )
        modifier_label.pack(pady=(15, 5))

        self.modifier_entry = ctk.CTkEntry(
            self,
            width=100,
            font=("Arial", 18),
            justify="center"
        )
        self.modifier_entry.insert(0, "0")
        self.modifier_entry.pack()

        self.result_label = ctk.CTkLabel(
            self,
            text="Choose a die!",
            font=("Arial", 28, "bold")
        )
        self.result_label.pack(pady=15)

        self.history_label = ctk.CTkLabel(
            self,
            text="Roll History",
            font=("Arial", 16),
            justify="left"
        )
        self.history_label.pack(pady=5)

        back_button = ctk.CTkButton(
            self,
            text="← Back",
            width=120,
            command=self.show_home_screen
        )
        back_button.pack(side="bottom", pady=15)

    def roll_die(self, sides):
        self.current_die = sides
        self.roll_animation_count = 0
        self.animation_speeds = [35, 40, 45, 55, 70, 90, 115, 145, 180, 220]
        self.animate_roll()

    def animate_roll(self):
        temp_roll = random.randint(1, self.current_die)
        self.result_label.configure(text=f"Rolling... {temp_roll}")

        delay = self.animation_speeds[self.roll_animation_count]
        self.roll_animation_count += 1

        if self.roll_animation_count < len(self.animation_speeds):
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
        self.add_to_history(f"D{self.current_die}: {roll} + {modifier} = {total}")

    def add_to_history(self, roll_text):
        self.roll_history.insert(0, roll_text)

        if len(self.roll_history) > 8:
            self.roll_history.pop()

        history_text = "Roll History\n\n" + "\n".join(self.roll_history)
        self.history_label.configure(text=history_text)


app = LoreforgedDeck()
app.mainloop()