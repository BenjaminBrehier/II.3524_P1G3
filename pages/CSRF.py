import tkinter as tk
import requests
from tkinter import scrolledtext

class CsrfPage(tk.Frame):
    def __init__(self, parent, controller, global_url, show_button):
        super().__init__(parent)
        self.controller = controller
        self.global_url = global_url
        self.show_button = show_button
        tk.Label(self, text="Simulation d'attaque CSRF", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="Entrez l'URL de la cible (avec un formulaire vulnérable) :").pack(anchor="w", padx=10)
        self.url_entry = tk.Entry(self, width=50)
        self.url_entry.pack(pady=5, padx=10)
        self.url_entry.insert(0, self.global_url)
        tk.Label(self, text="Paramètres de la requête (format JSON) :").pack(anchor="w", padx=10)
        self.payload_entry = tk.Text(self, height=10, width=50)
        self.payload_entry.pack(pady=5, padx=10)

        tk.Label(self, text="Entrez l'ID de session (copié depuis le navigateur) :").pack(anchor="w", padx=10)
        self.session_id_entry = tk.Entry(self, width=50)
        self.session_id_entry.pack(pady=5, padx=10)
        
        if self.show_button:
            tk.Button(self, text="Lancer l'attaque CSRF", command=self.simulate_csrf).pack(pady=10)

        self.result_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=80, height=20, state=tk.DISABLED)
        self.result_area.pack(padx=10, pady=10)

    def simulate_csrf(self):
        target_url = self.url_entry.get().strip()
        payload_text = self.payload_entry.get("1.0", tk.END).strip()
        session_id = self.session_id_entry.get().strip()
        reportLog = ""

        reportLog += "## Analyse de l'attaque CSRF :\n"

        if not target_url.startswith("http"):
            self.result_area.insert(tk.END, "Veuillez entrer une URL valide.\n")
            return

        if not session_id:
            self.result_area.insert(tk.END, "Veuillez entrer un ID de session valide.\n")
            return

        try:
            payload = eval(payload_text)
            session = requests.Session()

            # Ajouter le cookie de session récupéré du navigateur
            session.cookies.set('PHPSESSID', session_id)

            self.result_area.insert(tk.END, f"Envoi d'une requête CSRF vers : {target_url}\n")
            response = session.post(target_url, data=payload)

            if response.status_code == 200:
                self.result_area.insert(tk.END, f"Succès : L'attaque CSRF a été exécutée.\n")
                self.result_area.insert(tk.END, f"Réponse : {response.text[:500]}...\n")
                reportLog += "Succès : L'attaque CSRF a été exécutée.\n"
            else:
                self.result_area.insert(tk.END, f"Échec : Statut {response.status_code}\n")
                reportLog += f"Échec : Statut {response.status_code}\n"

        except Exception as e:
            self.result_area.insert(tk.END, f"Erreur lors de l'attaque CSRF : {e}\n")
            reportLog += f"Erreur lors de l'attaque CSRF : {e}\n"
        
        with open("report.md", "a", encoding="utf-8") as file:
            file.write(reportLog)
            file.write("\n\n")

    def start_attack(self):
        """Method to start the analysis externally."""
        self.simulate_csrf()