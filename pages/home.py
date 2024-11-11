import tkinter as tk

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="Bienvenue sur la page d'accueil", font=("Arial", 16))
        label.pack(pady=20)
