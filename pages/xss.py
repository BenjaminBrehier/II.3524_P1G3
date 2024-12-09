import tkinter as tk
from tkinter import Toplevel
import requests


class XssPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.completed_tests = 0
        self.results_displayed = False

        labelXss = tk.Label(self, text="Page XSS", font=("Arial", 16))
        labelXss.pack(pady=20)

        tk.Label(self, text="URL cible :").pack(pady=5)
        self.url_entry = tk.Entry(self, width=40)
        self.url_entry.pack(pady=10)

        tk.Label(self, text="Nom du paramètre :").pack(pady=5)
        self.param_entry = tk.Entry(self, width=20)
        self.param_entry.pack(pady=10)

        tk.Label(self, text="Payload XSS :").pack(pady=5)
        self.payload_entry = tk.Entry(self, width=40)
        self.payload_entry.insert(0, "<script>alert('XSS')</script>")
        self.payload_entry.pack(pady=10)

        self.start_button = tk.Button(self, text="Lancer le test XSS", command=self.start_test)
        self.start_button.pack(pady=10)

        self.status_label = tk.Label(self, text="")
        self.status_label.pack(pady=10)

    def start_test(self):
        url = self.url_entry.get()
        param_name = self.param_entry.get()
        payload = self.payload_entry.get()

        if not url or not param_name or not payload:  # Vérifie si des champs sont vides
            self.status_label.config(text="Erreur : Veuillez remplir tous les champs.")
            return

        self.completed_tests = 0
        self.results_displayed = False
        self.status_label.config(text="Lancement des tests...")

        # Lancement du test XSS
        self.xss_test(url, param_name, payload)

    def xss_test(self, url, param_name, payload):
        try:
            # Envoie une requête avec le payload et vérifie si le payload est reflété dans la réponse
            params = {param_name: payload}
            response = requests.get(url, params=params)

            if payload in response.text:
                self.status_label.config(text="Vulnérabilité XSS détectée !")
                self.show_results(url, param_name, payload, vulnerable=True)
            else:
                self.status_label.config(text="Pas de vulnérabilité détectée.")

        except Exception as e:
            self.status_label.config(text=f"Erreur : {e}")

    def show_results(self, url, param_name, payload, vulnerable):
        if self.results_displayed:
            return

        self.results_displayed = True
        results_window = Toplevel(self)
        results_window.title("Résultats du test XSS")
        results_window.geometry("400x300")

        results_label = tk.Label(results_window, text="Résumé du test XSS", font=("Arial", 14))
        results_label.pack(pady=10)

        results_text = (
            f"URL cible : {url}\n"
            f"Paramètre testé : {param_name}\n"
            f"Payload XSS utilisé : {payload}\n"
            f"Résultat : {'Vulnérable' if vulnerable else 'Non vulnérable'}\n"
        )
        tk.Label(results_window, text=results_text, justify="left").pack(pady=10, padx=10)

        close_button = tk.Button(results_window, text="Fermer", command=results_window.destroy)
        close_button.pack(pady=10)
