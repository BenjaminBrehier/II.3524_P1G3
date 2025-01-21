import tkinter as tk
from tkinter import Toplevel
import requests
from threading import Thread, Event
import time

class DdosPage(tk.Frame):
    def __init__(self, parent, controller, global_url, show_button):
        super().__init__(parent)
        self.stop_event = Event()  # Event pour arrêter les threads
        self.attack_start_time = None  # Timer début de l'attaque
        self.attack_end_time = None  # Timer fin de l'attaque
        self.completed_requests = 0  # Compteur des requêtes effectuées
        self.results_displayed = False  # Drapeau pour éviter plusieurs fenêtres
        self.global_url = global_url
        self.show_button = show_button
        labelAttack = tk.Label(self, text="Page DDoS", font=("Arial", 16))
        labelAttack.pack(pady=20)
        
        tk.Label(self, text="URL cible :").pack(pady=5)
        self.url_entry = tk.Entry(self, width=40)
        self.url_entry.pack(pady=10)
        self.url_entry.insert(0, self.global_url)
        tk.Label(self, text="Nombre de requêtes :").pack(pady=5)
        self.nbRequestsVar = tk.StringVar(value="100")
        nbRequestsDropdown = tk.OptionMenu(self, self.nbRequestsVar, "1", "5", "10", "20", "30", "50", "100", "200", "500", "1000")
        nbRequestsDropdown.pack(pady=5)
        
        tk.Label(self, text="Intervalle entre requêtes (secondes) :").pack(pady=5)
        self.requestsInterval = tk.Entry(self, width=10)
        self.requestsInterval.insert(0, "0.1")  # Intervalle par défaut
        self.requestsInterval.pack(pady=5)
        
        tk.Label(self, text="Nombre de threads :").pack(pady=5)
        self.threadsEntry = tk.Entry(self, width=10)
        self.threadsEntry.insert(0, "1")  # Nb threads par défaut
        self.threadsEntry.pack(pady=5)
        
        if self.show_button:
            self.start_button = tk.Button(self, text="Lancer l'attaque DDoS", command=self.start_attack)
            self.start_button.pack(pady=10)
        
        if self.show_button:
            self.stop_button = tk.Button(self, text="Stopper l'attaque", command=self.stop_attack, state="disabled")
            self.stop_button.pack(pady=10)
        
        self.status_label = tk.Label(self, text="")
        self.status_label.pack(pady=10)
        
        self.results_text = tk.Text(self, height=15, width=60, wrap=tk.WORD, state=tk.DISABLED)
        self.results_text.pack(pady=10)
    
    def start_attack(self):
        url = self.url_entry.get()
        if not url: # Vérification URL vide ?
            self.status_label.config(text="Erreur : veuillez entrer une URL valide.")
            return

        # Vérification de l'URL
        try:
            # Test rapide pour valider l'URL
            requests.head(url, timeout=5)# Utilisation de "head" pour minimiser la charge
        except requests.exceptions.MissingSchema:
            self.status_label.config(
                text=f"Erreur : Invalid URL '{url}': No scheme supplied. Perhaps you meant https://{url}?"
            )
            return
        except requests.exceptions.RequestException as e:
            self.status_label.config(text=f"Erreur : URL non valide ({e})")
            return
        
        self.numRequests = int(self.nbRequestsVar.get())
        self.interval = float(self.requestsInterval.get())
        self.numThreads = int(self.threadsEntry.get())
        
        if url:
            self.attack_start_time = time.time() # Enregistre le moment où l'attaque commence
            self.stop_event.clear() # Réinitialise l'Event pour permettre une nouvelle attaque
            self.completed_requests = 0 # Réinitialise le compteur de requêtes
            self.results_displayed = False # Réinitialise le drapeau pour permettre l'affichage des résultats
            self.status_label.config(text="Lancement en cours...")
            if self.show_button:
                self.stop_button.config(state="normal")# Active le bouton "Stopper l'attaque"
                self.start_button.config(state="disabled") # Désactive le bouton "Lancer l'attaque"
            
            # Lance autant de threads que spécifié
            for _ in range(self.numThreads):
                thread = Thread(target=self.ddos_attack, args=(url, self.numRequests, self.interval))
                thread.daemon = True  #  on s'assure que thread se termine avec l'application
                thread.start()
    
    def ddos_attack(self, url, num_requests, interval):
        try:
            for _ in range(num_requests):
                if self.stop_event.is_set(): # Vérifie si un arrêt a été demandé
                    break
                start_time = time.time()# Début de la requête
                requests.get(url) # Exécution de la requête
                self.completed_requests += 1
                elapsed = time.time() - start_time # Durée de la requête
                time_to_wait = max(0, interval - elapsed)# Ajustement de l'intervalle pour respecter le délai total souhaité
                time.sleep(time_to_wait)
        except Exception as e:
            self.status_label.config(text=f"Erreur : {e}")
        finally:
            self.attack_end_time = time.time() # Enregistrement du moment où l'attaque s'arrête
            self.reset_buttons()
            if not self.results_displayed: # Appelle 'show_results' une seule fois
                self.show_results()
                self.results_displayed = True
    
    def stop_attack(self):
        self.stop_event.set() # Signale aux threads de s'arrêter
        self.attack_end_time = time.time() # Enregistrement de l'heure d'arrêt
        self.status_label.config(text="Attaque interrompue.")
        self.reset_buttons()
        if not self.results_displayed: # Appelle 'show_results' une seule fois
            self.show_results()
            self.results_displayed = True
    
    def reset_buttons(self):
        #Réinitialise les boutons après l'arrêt de l'attaque
        if self.show_button:
            self.start_button.config(state="normal") # Réactivation du bouton "Lancer l'attaque"
            self.stop_button.config(state="disabled") # Désactivation du bouton "Stopper l'attaque"
        self.status_label.config(text="") # Réinitialisation du texte de statut
    
    def show_results(self):
        #Affiche les résultats de l'attaque dans une text area.
        if not self.attack_start_time or not self.attack_end_time:
            return # Si l'attaque n'a pas été correctement démarrée ou terminée
        
        elapsed_time = self.attack_end_time - self.attack_start_time # Temps écoulé
        initial_time = self.numRequests * self.interval # Temps initial estimé
        
        results_text = (
            f"URL cible : {self.url_entry.get()}\n"
            f"Temps initial estimé : {initial_time:.2f} secondes\n"
            f"Temps réel de l'attaque : {elapsed_time:.2f} secondes\n"
            f"Nombre de requêtes sélectionnées : {self.numRequests}\n"
            f"Requêtes effectuées : {self.completed_requests}\n"
            f"Intervalle entre les requêtes : {self.interval:.2f} secondes\n"
            f"Nombre de threads : {self.numThreads}\n"
        )

        with open("report.md", "a", encoding="utf-8") as file:
            file.write(f"## DDoS\n")
            lines = results_text.splitlines()
            for line in lines[:-1]:
                file.write(f"- {line}\n")
            file.write("\n\n")
        
        self.results_text.config(state=tk.NORMAL)
        self.results_text.insert(tk.END, results_text)
        self.results_text.config(state=tk.DISABLED)
        self.results_text.yview(tk.END)  # Scroll automatique