import customtkinter as ctk


def show_dice_screen(app):
    app.clear_screen()

    title = ctk.CTkLabel(
        app,
        text="🎲 Dice Roller",
        font=("Arial", 34, "bold")
    )
    title.pack(pady=(20, 10))

    dice_frame = ctk.CTkFrame(app)
    dice_frame.pack(pady=10)

    dice = [4, 6, 8, 10, 12, 20, 100]

    for die in dice:
        button = ctk.CTkButton(
            dice_frame,
            text=f"D{die}",
            width=90,
            height=45,
            font=("Arial", 16),
            command=lambda d=die: app.roll_die(d)
        )
        button.pack(side="left", padx=5, pady=10)

    modifier_label = ctk.CTkLabel(
        app,
        text="Modifier",
        font=("Arial", 18)
    )
    modifier_label.pack(pady=(15, 5))

    app.modifier_entry = ctk.CTkEntry(
        app,
        width=100,
        font=("Arial", 18),
        justify="center"
    )
    app.modifier_entry.insert(0, "0")
    app.modifier_entry.pack()

    app.result_label = ctk.CTkLabel(
        app,
        text="Choose a die!",
        font=("Arial", 28, "bold")
    )
    app.result_label.pack(pady=15)

    app.history_label = ctk.CTkLabel(
        app,
        text="Roll History",
        font=("Arial", 16),
        justify="left"
    )
    app.history_label.pack(pady=5)

    back_button = ctk.CTkButton(
        app,
        text="← Back",
        width=120,
        command=app.show_home_screen
    )
    back_button.pack(side="bottom", pady=15)
    