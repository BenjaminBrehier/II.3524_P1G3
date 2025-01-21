import tkinter as tk
import requests

class SubdomainEnumerationPage(tk.Frame):
    def __init__(self, parent, controller, global_url, show_button):
        super().__init__(parent)
        self.global_url = global_url
        self.controller = controller
        self.show_button = show_button
        self.create_widgets()

    def create_widgets(self):
        """Création des éléments de l'interface utilisateur."""
        tk.Label(self, text="Subdomain Enumeration", font=("Helvetica", 16)).pack(pady=10)

        tk.Label(self, text="Entrez l'URL cible :").pack(pady=5)
        self.url_entry = tk.Entry(self, width=50)
        self.url_entry.pack(pady=5)
        self.url_entry.insert(0, self.global_url)
        self.result_text = tk.Text(self, height=15, width=80, state=tk.DISABLED)
        self.result_text.pack(pady=10)

        if self.show_button:
            tk.Button(self, text="Démarrer l'analyse", command=self.enumerate_subdomains).pack(pady=5)

    def enumerate_subdomains(self):
        """Effectue l'énumération des sous-domaines."""
        url = self.url_entry.get().strip()
        domain = url.split("//")[-1].split("/")[0]
        if not domain:
            self.result_text.insert("end", "Veuillez entrer une URL valide.\n")
            return

        subdomains = open("subdomainsPossibilities.txt", "r").read().splitlines()

        found_subdomains = []
        self.result_text.delete("1.0", "end")
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert("end", f"Analyse des sous-domaines pour : {domain}\n\n")

        for sub in subdomains:
            url = f"http://{sub}.{domain}"
            try:
                response = requests.get(url, timeout=3)
                found_subdomains.append(url)
                self.result_text.insert("end", f"[FOUND] {url} (Code: {response.status_code})\n")
            except requests.exceptions.RequestException:
                print(f"[ERROR] {url} inaccessible")

        self.result_text.insert("end", "\nAnalyse terminée.\n")
        if found_subdomains:
            self.result_text.insert("end", f"Sous-domaines trouvés : {', '.join(found_subdomains)}\n")
            with open("report.md", "a", encoding="utf-8") as file:
                file.write("## Subdomain Enumeration :\n")
                for subdomain in found_subdomains:
                    file.write(f"- {subdomain}\n")
        else:
            self.result_text.insert("end", "Aucun sous-domaine trouvé.\n")
        self.result_text.config(state=tk.DISABLED)

    def start_attack(self):
        """Method to start the analysis externally."""
        self.enumerate_subdomains()
