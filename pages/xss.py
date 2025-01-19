import tkinter as tk
from tkinter import filedialog, messagebox
import re

class XssPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.title_label = tk.Label(self, text="Scanner de Vulnérabilités XSS", font=("Arial", 16))
        self.title_label.pack(pady=20)

        # Bouton pour charger un fichier HTML
        self.load_button = tk.Button(self, text="Charger un fichier HTML", command=self.load_html_file)
        self.load_button.pack(pady=10)

        # Champ pour afficher les résultats du scan
        self.results_text = tk.Text(self, height=15, width=80, wrap=tk.WORD, state=tk.DISABLED)
        self.results_text.pack(pady=10)

        # Champ pour afficher les payloads XSS à tester
        self.payload_label = tk.Label(self, text="Payloads XSS à tester :", font=("Arial", 12))
        self.payload_label.pack(pady=10)
        self.payloads_text = tk.Text(self, height=10, width=80, wrap=tk.WORD, state=tk.DISABLED)
        self.payloads_text.pack(pady=10)

        # Bouton pour supprimer les payloads
        self.delete_button = tk.Button(self, text="Supprimer les Payloads", command=self.delete_payloads)
        self.delete_button.pack(pady=5)

    def load_html_file(self):
        """Ouvre un fichier HTML pour l'analyser."""
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers HTML", "*.html")])

        if not file_path:
            messagebox.showerror("Erreur", "Aucun fichier HTML sélectionné.")
            return

        # Lire le fichier HTML
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
                self.scan_for_xss(html_content, file_path)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire le fichier : {e}")

    def scan_for_xss(self, html_content, file_path):
        """Scanne le fichier HTML à la recherche de vulnérabilités XSS."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)

        vulnerabilities = []
        payloads = []

        # Définir des payloads variés
        common_payloads = [
            "<script>alert('XSS1')</script>",
            "'><script>alert('XSS2')</script>",
            "\" onmouseover=\"alert('XSS3')\" ",
            "<img src='x' onerror='alert(\"XSS4\")'>",
            "<svg onload='alert(\"XSS5\")'>",
            "<iframe src='javascript:alert(`XSS6`)'></iframe>",
            "<details open ontoggle='alert(\"XSS7\")'></details>",
            "<marquee onstart='alert(\"XSS8\")'>Test</marquee>",
            "<input autofocus onfocus='alert(\"XSS9\")'>",
            "<a href='javascript:alert(`XSS10`)'>Click me</a>",
            "<object data='data:text/html,<script>alert(\\'XSS11\\')</script>'></object>",  # Object tag XSS
            "<base href='javascript:alert(\\'XSS12\\')'>"  # Base tag XSS
        ]

        # Recherche d'attributs pouvant contenir du JavaScript (onclick, onload, etc.)
        vuln_patterns = [
            (r'on\w+="[^"]*"', "Attributs contenant des événements JavaScript"),
            (r'(<script[^>]*>[^<]*</script>)', "Balises <script> suspectes"),
            (r'javascript:[^"]*', "Protocole javascript: dans les liens"),
            (r'[^a-zA-Z0-9](eval|setTimeout|setInterval|document\.write|innerHTML)[^a-zA-Z0-9]',
             "Fonctions JavaScript dangereuses"),
            (r'<img[^>]*onerror="[^"]*"', "Balises <img> avec un événement onerror"),
            (r'<iframe[^>]*src="javascript:[^"]*"', "Balises <iframe> avec src=javascript:"),
            (r'<object[^>]*data="data:text/html[^"]*"', "Balises <object> vulnérables"),
            (r'<base[^>]*href="javascript:[^"]*"', "Balises <base> vulnérables")
        ]

        # Vérification des champs de formulaire vulnérables
        form_param_pattern = r'<input[^>]*name="([^"]+)"'
        form_params = re.findall(form_param_pattern, html_content)
        for idx, param in enumerate(form_params):
            vulnerabilities.append(f"Paramètre de formulaire vulnérable : {param}")
            payload = common_payloads[idx % len(common_payloads)]
            payloads.append(f"Tester le paramètre {param} avec : {payload}")

        # Vérification des balises `<a>` et des paramètres dans les URL
        link_param_pattern = r'<a[^>]*href="[^"]*\?([^"]+)"'
        link_params = re.findall(link_param_pattern, html_content)
        for param_set in link_params:
            params = param_set.split('&')
            for idx, param in enumerate(params):
                key = param.split('=')[0]
                vulnerabilities.append(f"Paramètre de lien vulnérable : {key}")
                payload = common_payloads[(idx + 1) % len(common_payloads)]
                payloads.append(f"Tester le paramètre {key} avec : {payload}")

        # Vérifier les vulnérabilités dans le contenu HTML
        for pattern, description in vuln_patterns:
            matches = re.findall(pattern, html_content)
            if matches:
                vulnerabilities.append(f"{description} trouvée(s): {len(matches)} instance(s) détectée(s).")
                for idx, match in enumerate(matches):
                    payload = common_payloads[(idx + 2) % len(common_payloads)]
                    payloads.append(f"Tester cette vulnérabilité avec : {payload}")

        # Afficher les vulnérabilités trouvées
        if vulnerabilities:
            self.results_text.insert(tk.END, f"Vulnérabilités XSS trouvées dans {file_path} :\n")
            for vuln in vulnerabilities:
                self.results_text.insert(tk.END, f"- {vuln}\n")
        else:
            self.results_text.insert(tk.END, "Aucune vulnérabilité XSS trouvée.\n")

        # Afficher les payloads à tester
        self.payloads_text.config(state=tk.NORMAL)
        self.payloads_text.delete(1.0, tk.END)  # Effacer d'abord l'ancien contenu
        for payload in payloads:
            self.payloads_text.insert(tk.END, payload + "\n")  # Ajouter chaque payload
        self.payloads_text.config(state=tk.DISABLED)

        self.results_text.config(state=tk.DISABLED)
        self.payloads_text.config(state=tk.DISABLED)

    def delete_payloads(self):
        """Supprime les payloads XSS affichés."""
        self.payloads_text.config(state=tk.NORMAL)
        self.payloads_text.delete(1.0, tk.END)
        self.payloads_text.config(state=tk.DISABLED)
