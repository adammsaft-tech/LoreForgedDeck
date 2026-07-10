import customtkinter as ctk


def show_character_screen(app):
    app.clear_screen()

    title = ctk.CTkLabel(
        app,
        text="👤 Character Manager",
        font=("Arial", 32, "bold")
    )
    title.pack(pady=(40, 20))

    message = ctk.CTkLabel(
        app,
        text="No characters created yet.",
        font=("Arial", 20)
    )
    message.pack(pady=20)

    create_button = ctk.CTkButton(
        app,
        text="+ Create Character",
        width=220,
        height=45
    )
    create_button.pack(pady=20)

    back_button = ctk.CTkButton(
        app,
        text="← Back",
        command=app.show_home_screen
    )
    back_button.pack(side="bottom", pady=20)