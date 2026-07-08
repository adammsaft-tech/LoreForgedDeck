import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

app.geometry("800x480")
app.title("Loreforged Deck")

label = ctk.CTkLabel(
    app,
    text="Loreforged Deck",
    font=("Arial", 32, "bold")
)

label.pack(pady=40)

button = ctk.CTkButton(
    app,
    text="Roll D20"
)

button.pack()

app.mainloop()