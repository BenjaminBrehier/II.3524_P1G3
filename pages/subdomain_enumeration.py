import tkinter as tk
import requests

class SubdomainEnumerationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        """Création des éléments de l'interface utilisateur."""
        tk.Label(self, text="Subdomain Enumeration", font=("Helvetica", 16)).pack(pady=10)

        tk.Label(self, text="Entrez l'URL cible :").pack(pady=5)
        self.url_entry = tk.Entry(self, width=50)
        self.url_entry.pack(pady=5)

        self.result_text = tk.Text(self, height=15, width=80)
        self.result_text.pack(pady=10)

        tk.Button(self, text="Démarrer l'analyse", command=self.enumerate_subdomains).pack(pady=5)

    def enumerate_subdomains(self):
        """Effectue l'énumération des sous-domaines."""
        domain = self.url_entry.get().strip()
        if not domain:
            self.result_text.insert("end", "Veuillez entrer une URL valide.\n")
            return

        subdomains = open("subdomainsPossibilities.txt", "r").read().splitlines()

        found_subdomains = []
        self.result_text.delete("1.0", "end")
        self.result_text.insert("end", f"Analyse des sous-domaines pour : {domain}\n\n")

        for sub in subdomains:
            url = f"http://{sub}.{domain}"
            try:
                response = requests.get(url, timeout=3)
                if response.status_code == 200:
                    found_subdomains.append(url)
                    self.result_text.insert("end", f"[FOUND] {url} (Code: 200)\n")
                else:
                    self.result_text.insert("end", f"[NOT FOUND] {url} (Code: {response.status_code})\n")
            except requests.exceptions.RequestException:
                print(f"[ERROR] {url} inaccessible")

        self.result_text.insert("end", "\nAnalyse terminée.\n")
        if found_subdomains:
            self.result_text.insert("end", f"Sous-domaines trouvés : {', '.join(found_subdomains)}\n")
        else:
            self.result_text.insert("end", "Aucun sous-domaine trouvé.\n")
