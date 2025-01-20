import tkinter as tk
import socket
from threading import Thread, Event, Lock
from urllib.parse import urlparse

class NmapPage(tk.Frame):
    def __init__(self, parent, controller, global_url):
        super().__init__(parent)
        self.global_url = global_url
        self.stop_event = Event()  # Event to stop the scan
        self.lock = Lock()  # Lock to synchronize access to shared resources
        self.open_ports = []  # Shared list to store open ports
        self.active_threads = 0  # Counter for active threads

        labelNmap = tk.Label(self, text="Page Nmap", font=("Arial", 16))
        labelNmap.pack(pady=20)

        tk.Label(self, text="URL cible :").pack(pady=5)
        self.url_entry = tk.Entry(self, width=40)
        self.url_entry.pack(pady=10)
        self.url_entry.insert(0, self.global_url)
        tk.Label(self, text="Port de début :").pack(pady=5)
        self.start_port_entry = tk.Entry(self, width=10)
        self.start_port_entry.insert(0, "1")
        self.start_port_entry.pack(pady=5)

        tk.Label(self, text="Port de fin :").pack(pady=5)
        self.end_port_entry = tk.Entry(self, width=10)
        self.end_port_entry.insert(0, "1024")
        self.end_port_entry.pack(pady=5)

        tk.Label(self, text="Nombre de threads :").pack(pady=5)
        self.threads_entry = tk.Entry(self, width=10)
        self.threads_entry.insert(0, "1")  
        self.threads_entry.pack(pady=5)

        self.start_button = tk.Button(self, text="Lancer le scan Nmap", command=self.start_scan)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self, text="Stopper le scan", command=self.stop_scan, state="disabled")
        self.stop_button.pack(pady=10)

        self.status_label = tk.Label(self, text="")
        self.status_label.pack(pady=10)

        # Text area for displaying results
        self.results_area = tk.Text(self, wrap="word", height=15, width=60)
        self.results_area.pack(pady=10, padx=10)
        self.results_area.config(state="disabled")

    def start_scan(self):
        url = self.url_entry.get()
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname if parsed_url.hostname else url
        start_port = int(self.start_port_entry.get())
        end_port = int(self.end_port_entry.get())
        num_threads = int(self.threads_entry.get())

        if not hostname:
            self.status_label.config(text="Erreur : Veuillez entrer une URL valide.")
            return

        self.status_label.config(text="Lancement du scan...")
        self.stop_event.clear()
        self.stop_button.config(state="normal") 
        self.start_button.config(state="disabled")  

        # Reset shared resources
        self.open_ports = []
        self.active_threads = num_threads

        # Clear previous results
        self.results_area.config(state="normal")
        self.results_area.delete(1.0, tk.END)
        self.results_area.config(state="disabled")

        # Start the scan in multiple threads
        ports_per_thread = (end_port - start_port + 1) // num_threads
        for i in range(num_threads):
            thread_start_port = start_port + i * ports_per_thread
            thread_end_port = start_port + (i + 1) * ports_per_thread - 1
            if i == num_threads - 1:
                thread_end_port = end_port  # Ensure the last thread covers the remaining ports
            scan_thread = Thread(target=self.custom_scan, args=(hostname, thread_start_port, thread_end_port))
            scan_thread.daemon = True
            scan_thread.start()

    def custom_scan(self, hostname, start_port, end_port):
        try:
            ip = socket.gethostbyname(hostname)
            for port in range(start_port, end_port + 1):
                if self.stop_event.is_set():
                    break
                print(f"Scanning port {port}...")
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(1)
                    result = sock.connect_ex((ip, port))
                    if result == 0:
                        print(f"Port {port} ouvert")
                        with self.lock:
                            self.open_ports.append(port)

        except Exception as e:
            self.status_label.config(text=f"Erreur : {e}")
        finally:
            with self.lock:
                self.active_threads -= 1
                if self.active_threads == 0:
                    self.display_results(hostname)

    def display_results(self, hostname):
        if self.open_ports:
            results = f"Ports ouverts : {', '.join(map(str, self.open_ports))}"
        else:
            results = "Aucun port ouvert trouvé."

        self.status_label.config(text="Scan terminé.")
        self.show_results(hostname, results)
        self.reset_buttons()

    def stop_scan(self):
        self.stop_event.set()
        self.status_label.config(text="Scan interrompu.")
        self.reset_buttons()

    def reset_buttons(self):
        self.start_button.config(state="normal") 
        self.stop_button.config(state="disabled") 

    def show_results(self, hostname, results):
        results_text = f"URL cible : {hostname}\n\nRésultats du scan :\n{results}"

        with open("report.md", "a", encoding="utf-8") as file:
            file.write("## Analyse de l'attaque Nmap :\n")
            file.write(results_text)
            file.write("\n\n")
        self.results_area.config(state="normal")
        self.results_area.insert("1.0", results_text)
        self.results_area.config(state="disabled")

    def start_attack(self):
        """Method to start the analysis externally."""
        self.start_scan()
        # Attendre que le scan soit terminé
        while self.active_threads > 0:
            self.update_idletasks()
            self.update()