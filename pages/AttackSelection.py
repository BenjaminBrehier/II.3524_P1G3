import tkinter as tk
from tkinter import messagebox, scrolledtext

class AttackSelectionPage(tk.Frame):
    def __init__(self, parent, controller, global_url):
        super().__init__(parent)
        self.controller = controller
        self.global_url = global_url

        # Title
        tk.Label(self, text="Sélection des Attaques", font=("Arial", 16)).pack(pady=20)

        # URL Entry
        tk.Label(self, text="URL Globale:").pack(anchor="w")
        self.global_url_entry = tk.Entry(self, width=50)
        self.global_url_entry.pack(pady=5)
        self.global_url_entry.insert(0, self.global_url)
        # Checkboxes for each attack
        self.attacks = {
            "DDoS": tk.BooleanVar(),
            # "Brute Force": tk.BooleanVar(),
            "Path Traversal": tk.BooleanVar(),
            # "XSS": tk.BooleanVar(),
            "CSRF": tk.BooleanVar(),
            "Subdomain Enumeration": tk.BooleanVar(),
            # "SSL/TLS Check": tk.BooleanVar(),
            "Nmap": tk.BooleanVar(),
            "Buffer Overflow": tk.BooleanVar(),
            "Access Control": tk.BooleanVar(),
            "Vulnerable Components": tk.BooleanVar()
        }

        for attack, var in self.attacks.items():
            tk.Checkbutton(self, text=attack, variable=var).pack(anchor="w")

        # Button to proceed to the wizard
        tk.Button(self, text="Suivant", command=self.go_to_wizard).pack(pady=20)

    def go_to_wizard(self):
        selected_attacks = [attack for attack, var in self.attacks.items() if var.get()]
        if not selected_attacks:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner au moins une attaque.")
            return

        global_url = self.global_url_entry.get().strip()
        if not global_url:
            messagebox.showwarning("Avertissement", "Veuillez entrer une URL globale.")
            return

        # Pass the selected attacks and global URL to the wizard page
        self.controller.show_wizard(selected_attacks, global_url)

    def generate_report(self):
        selected_attacks = [attack for attack, var in self.attacks.items() if var.get()]
        if not selected_attacks:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner au moins une attaque.")
            return

        report = "Rapport des Attaques Sélectionnées:\n\n"
        for attack in selected_attacks:
            if attack == "DDoS":
                num_requests = int(self.ddos_requests.get())
                interval = float(self.ddos_interval.get())
                num_threads = int(self.ddos_threads.get())
                report += f"- DDoS: {self.perform_ddos_attack(num_requests, interval, num_threads)}\n"
            # Add similar conditions for other attacks

        self.report_area.config(state=tk.NORMAL)
        self.report_area.delete(1.0, tk.END)
        self.report_area.insert(tk.END, report)
        self.report_area.config(state=tk.DISABLED)

    def perform_ddos_attack(self, num_requests, interval, num_threads):
        # Placeholder for DDoS attack logic
        return f"DDoS attack with {num_requests} requests, {interval} seconds interval, {num_threads} threads."
