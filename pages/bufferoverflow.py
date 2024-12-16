import tkinter as tk
from tkinter import ttk, messagebox
import requests


class bufferoverflowPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Titre de la page
        self.title_label = tk.Label(self, text="Buffer Overflow Simulation", font=("Arial", 16))
        self.title_label.pack(pady=20)

        # Champ pour l'URL ou le service cible
        self.target_label = tk.Label(self, text="Cible (ex: http://example.com/vulnerable_endpoint):")
        self.target_label.pack(pady=5)
        self.target_entry = tk.Entry(self, width=50)
        self.target_entry.pack(pady=5)

        # Slider pour la taille du buffer
        self.buffer_label = tk.Label(self, text="Taille du buffer à envoyer :")
        self.buffer_label.pack(pady=5)
        self.buffer_size_slider = tk.Scale(self, from_=100, to=10000, orient=tk.HORIZONTAL)
        self.buffer_size_slider.pack(pady=5)

        # Bouton pour démarrer l'attaque
        self.start_button = tk.Button(self, text="Lancer l'attaque", command=self.start_attack)
        self.start_button.pack(pady=10)

        # Champ pour afficher les résultats
        self.result_output = tk.Text(self, height=10, width=60, wrap=tk.WORD, state=tk.DISABLED)
        self.result_output.pack(pady=10)

    def start_attack(self):
        """Démarrer la simulation d'une attaque par Buffer Overflow."""
        target = self.target_entry.get()
        buffer_size = self.buffer_size_slider.get()

        if not target:
            messagebox.showerror("Erreur", "Veuillez spécifier une cible.")
            return

        # Construire un "payload" pour simuler le buffer overflow
        payload = "A" * buffer_size

        try:
            # Envoyer la requête (exemple : une requête POST avec un payload)
            response = requests.post(target, data={'input': payload})
            self.update_result_output(f"Payload envoyé ({buffer_size} octets).\n")
            self.update_result_output(f"Réponse du serveur : {response.status_code}\n{response.text[:200]}...\n")
        except requests.exceptions.RequestException as e:
            self.update_result_output(f"Erreur de connexion : {e}\n")

    def update_result_output(self, text):
        """Met à jour l'affichage des résultats dans le Text widget."""
        self.result_output.config(state=tk.NORMAL)
        self.result_output.insert(tk.END, text)
        self.result_output.config(state=tk.DISABLED)
        self.result_output.yview(tk.END)  # Scroll automatique
