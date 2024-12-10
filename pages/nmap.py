import tkinter as tk
from tkinter import Toplevel
import socket
from threading import Thread, Event, Lock

class NmapPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.results_displayed = False
        self.stop_event = Event()  # Event to stop the scan
        self.lock = Lock()  # Lock to synchronize access to shared resources
        self.open_ports = []  # Shared list to store open ports
        self.active_threads = 0  # Counter for active threads

        labelNmap = tk.Label(self, text="Page Nmap", font=("Arial", 16))
        labelNmap.pack(pady=20)

        tk.Label(self, text="URL cible :").pack(pady=5)
        self.url_entry = tk.Entry(self, width=40)
        self.url_entry.pack(pady=10)

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

    def start_scan(self):
        url = self.url_entry.get()
        start_port = int(self.start_port_entry.get())
        end_port = int(self.end_port_entry.get())
        num_threads = int(self.threads_entry.get())

        if not url:
            self.status_label.config(text="Erreur : Veuillez entrer une URL valide.")
            return

        self.results_displayed = False
        self.status_label.config(text="Lancement du scan...")
        self.stop_event.clear()
        self.stop_button.config(state="normal") 
        self.start_button.config(state="disabled")  

        # Reset shared resources
        self.open_ports = []
        self.active_threads = num_threads

        # Start the scan in multiple threads
        ports_per_thread = (end_port - start_port + 1) // num_threads
        for i in range(num_threads):
            thread_start_port = start_port + i * ports_per_thread
            thread_end_port = start_port + (i + 1) * ports_per_thread - 1
            if i == num_threads - 1:
                thread_end_port = end_port  # Ensure the last thread covers the remaining ports
            scan_thread = Thread(target=self.custom_scan, args=(url, thread_start_port, thread_end_port))
            scan_thread.daemon = True
            scan_thread.start()

    def custom_scan(self, url, start_port, end_port):
        try:
            ip = socket.gethostbyname(url)
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
                    self.display_results(url)

    def display_results(self, url):
        if self.open_ports:
            results = f"Ports ouverts : {', '.join(map(str, self.open_ports))}"
        else:
            results = "Aucun port ouvert trouvé."

        self.status_label.config(text="Scan terminé.")
        self.show_results(url, results)
        self.reset_buttons()

    def stop_scan(self):
        self.stop_event.set()
        self.status_label.config(text="Scan interrompu.")
        self.reset_buttons()

    def reset_buttons(self):
        self.start_button.config(state="normal") 
        self.stop_button.config(state="disabled") 

    def show_results(self, url, results):
        if self.results_displayed:
            return

        self.results_displayed = True
        results_window = Toplevel(self)
        results_window.title("Résultats du scan")
        results_window.geometry("600x400")

        results_label = tk.Label(results_window, text="Résumé du scan", font=("Arial", 14))
        results_label.pack(pady=10)

        results_text = f"URL cible : {url}\n\nRésultats du scan :\n{results}"
        results_text_widget = tk.Text(results_window, wrap="word")
        results_text_widget.insert("1.0", results_text)
        results_text_widget.config(state="disabled")
        results_text_widget.pack(pady=10, padx=10, fill="both", expand=True)

        close_button = tk.Button(results_window, text="Fermer", command=results_window.destroy)
        close_button.pack(pady=10)
