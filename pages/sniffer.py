import tkinter as tk
from tkinter import ttk
from scapy.all import sniff, TCP, IP
from threading import Thread, Event


class SnifferPage(tk.Frame):
    def __init__(self, parent, controller, global_url):
        super().__init__(parent)
        self.global_url = global_url
        self.stop_event = Event()
        self.sniff_thread = None
        
        label = tk.Label(self, text="Sniffer Réseau", font=("Arial", 16))
        label.pack(pady=20)
        
        tk.Label(self, text="Interface réseau (celle de ton pc, par exemple : Intel(R) Wi-Fi 6 AX201 160MHz)").pack(pady=5)
        self.interface_entry = tk.Entry(self, width=40)
        self.interface_entry.pack(pady=10)
        self.interface_entry.insert(
            0,
            "Intel(R) Wi-Fi 6 AX201 160MHz"
        )


        tk.Label(self, text="Nombre de paquets à capturer :").pack(pady=5)
        self.packet_count_var = tk.StringVar(value="100")
        self.packet_count_dropdown = ttk.Combobox(
            self, textvariable=self.packet_count_var, values=["10", "50", "100", "200", "500", "750", "1000", "10000", "100000"], state="readonly"
        )
        self.packet_count_dropdown.pack(pady=5)
        
        self.start_button = tk.Button(self, text="Démarrer le sniffing", command=self.start_sniffing)
        self.start_button.pack(pady=10)
        
        self.stop_button = tk.Button(self, text="Arrêter le sniffing", command=self.stop_sniffing, state="disabled")
        self.stop_button.pack(pady=10)
        
        self.status_label = tk.Label(self, text="")
        self.status_label.pack(pady=10)
        
        self.results_text = tk.Text(self, wrap="word", state="disabled", height=15)
        self.results_text.pack(pady=10, padx=10)
    
    def start_sniffing(self):
        interface = self.interface_entry.get().strip()
        if not interface:
            self.status_label.config(text="Erreur : veuillez entrer une interface valide.")
            return
        
        try:
            #Test si l'interface est valide en capturant un seul paquet (sans stocker).
            sniff(iface=interface, count=1, timeout=1, store=0)
        except Exception as e:
            self.status_label.config(text=f"Erreur : interface invalide ({e})")
            return
        
        packet_count = int(self.packet_count_var.get())
        self.stop_event.clear()
        self.results_text.config(state="normal")
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(tk.END, "Sniffing en cours...\n")
        self.results_text.config(state="disabled")
        
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.status_label.config(text="Sniffing en cours...")
        
        self.sniff_thread = Thread(target=self.sniff_packets, args=(interface, packet_count))
        self.sniff_thread.daemon = True
        self.sniff_thread.start()

    def sniff_packets(self, interface, packet_count):
        def handle_packet(packet):
            # Vérifie si un arrêt est demandé
            if self.stop_event.is_set():
                return True
            
            # Analyse et affichage des paquets capturés
            if packet.haslayer(TCP):
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                src_port = packet[TCP].sport
                dst_port = packet[TCP].dport
                info = f"TCP : {src_ip}:{src_port} -> {dst_ip}:{dst_port}\n"
            elif packet.haslayer(IP):
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                info = f"IP : {src_ip} -> {dst_ip}\n"
            else:
                info = f"Paquet capturé : {packet.summary()}\n"
            
            self.update_results(info)
            self.save_results_to_file(info)
        
        try:
            sniff(
                iface=interface,
                prn=handle_packet,
                count=packet_count,
                stop_filter=lambda _: self.stop_event.is_set(),
                store=0
            )
        except Exception as e:
            self.status_label.config(text=f"Erreur : {e}")
        finally:
            self.reset_buttons()

    def stop_sniffing(self):
        self.stop_event.set()
        self.status_label.config(text="Sniffing arrêté.")
        self.reset_buttons()

    def update_results(self, text):
        self.results_text.config(state="normal")
        self.results_text.insert(tk.END, text)
        self.results_text.see(tk.END)#Défilement automatique
        self.results_text.config(state="disabled")

    def save_results_to_file(self, text):
        """Sauvegarde les résultats dans un fichier markdown."""
        with open("report.md", "a", encoding="utf-8") as file:
            file.write("## Sniffer\n\n")
            for line in text.splitlines():
                file.write(f"- {line}\n")
            file.write("\n")

    def reset_buttons(self):
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def start_attack(self):
        """Method to start the analysis externally."""
        self.start_sniffing()