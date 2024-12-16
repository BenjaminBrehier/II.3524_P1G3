#Scanner de Routes :
#L'outil pourrait automatiser la recherche de chemins sensibles accessibles sans authentification ou avec des permissions incorrectes.
#Fonctionnalité :
#L'utilisateur entre une URL de base (par exemple, http://example.com/).
#L'outil explore les routes possibles (ex. /admin, /settings, /hidden) pour voir lesquelles sont accessibles.
#Utilisation : Vérifie si des endpoints ou pages sensibles sont exposés par erreur.

import requests
import tkinter as tk
from tkinter import messagebox

class AccessControlPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Titre de la page
        tk.Label(self, text="Access Control Scanner", font=("Arial", 16)).pack(pady=20)

        # Champ pour l'URL de base
        tk.Label(self, text="URL de base :").pack(pady=5)
        self.url_entry = tk.Entry(self, width=40)
        self.url_entry.pack(pady=5)

        # Bouton pour scanner les routes
        self.scan_button = tk.Button(self, text="Scanner les routes", command=self.start_scan)
        self.scan_button.pack(pady=10)

        # Zone pour afficher les résultats avec scrollbar
        self.result_frame = tk.Frame(self)
        self.result_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.result_text = tk.Text(self.result_frame, height=15, width=60, state=tk.DISABLED, wrap=tk.WORD)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.result_frame, command=self.result_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=self.scrollbar.set)

    def start_scan(self):
        """Démarre le scan des routes communes."""
        url_base = self.url_entry.get().rstrip('/')
        
        if not url_base:
            messagebox.showerror("Erreur", "Veuillez entrer une URL de base.")
            return

        common_paths = [
            '/admin', '/settings', '/hidden', '/api', '/dashboard',
            '/config', '/login', '/logout', '/register', '/backup',
            '/data', '/private', '/secure', '/test'
        ]

        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)

        for path in common_paths:
            full_url = f"{url_base}{path}"
            try:
                response = requests.get(full_url)
                if response.status_code == 200:
                    self.result_text.insert(tk.END, f"Accessible: {full_url} (200 OK)\n")
                else:
                    self.result_text.insert(tk.END, f"Refusé: {full_url} (Code: {response.status_code})\n")
            except requests.RequestException as e:
                self.result_text.insert(tk.END, f"Erreur: {full_url} ({str(e)})\n")

        self.result_text.config(state=tk.DISABLED)
