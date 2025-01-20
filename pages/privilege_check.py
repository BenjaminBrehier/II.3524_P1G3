import tkinter as tk
from tkinter import scrolledtext
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

class PrivilegeCheckPage(tk.Frame):
    def __init__(self, parent, controller, global_url, show_button):
        super().__init__(parent)
        self.global_url = global_url
        self.show_button = show_button

        self.controller = controller
        tk.Label(self, text="Vérification des privilèges des endpoints", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="Entrez l'URL cible :").pack(anchor="w", padx=10)
        self.url_entry = tk.Entry(self, width=50)
        self.url_entry.pack(pady=5, padx=10)
        self.url_entry.insert(0, self.global_url)
        if self.show_button:
            tk.Button(self, text="Analyser", command=self.analyze_endpoints).pack(pady=10)

        # Zone de résultats
        tk.Label(self, text="Résultats de l'analyse :").pack(anchor="w", padx=10, pady=5)
        self.result_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=80, height=20)
        self.result_area.pack(padx=10, pady=10)

    def analyze_endpoints(self):
        target_url = self.url_entry.get().strip()

        if not target_url.startswith("http"):
            self.result_area.insert(tk.END, "Veuillez entrer une URL valide (commençant par http ou https).\n")
            return

        self.result_area.delete(1.0, tk.END)
        self.result_area.insert(tk.END, f"Analyse en cours pour : {target_url}\n\n")

        try:
            # Trouver des endpoints via les scripts JavaScript et le fuzzing
            endpoints = set()
            endpoints.update(self.find_js_endpoints(target_url))
            endpoints.update(self.fuzz_endpoints(target_url))

            if not endpoints:
                self.result_area.insert(tk.END, "Aucun endpoint trouvé.\n")
                return

            self.result_area.insert(tk.END, f"{len(endpoints)} endpoints trouvés :\n")
            for endpoint in endpoints:
                self.result_area.insert(tk.END, f"  - {endpoint}\n")

            # Vérification des privilèges pour toutes les méthodes HTTP
            self.result_area.insert(tk.END, "\nTest des méthodes HTTP sur les endpoints...\n")
            for endpoint in endpoints:
                full_url = urljoin(target_url, endpoint)
                self.test_all_methods(full_url)
        except Exception as e:
            self.result_area.insert(tk.END, f"Erreur : {e}\n")

    def find_js_endpoints(self, url):
        """Recherche d'endpoints dans les fichiers JavaScript."""
        self.result_area.insert(tk.END, "Recherche dans les fichiers JavaScript...\n")
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            js_files = [script['src'] for script in soup.find_all('script') if 'src' in script.attrs]

            endpoints = set()
            for js_file in js_files:
                full_url = urljoin(url, js_file)
                try:
                    js_content = requests.get(full_url, timeout=5).text
                    found_endpoints = re.findall(r'\/[a-zA-Z0-9_/]*', js_content)
                    endpoints.update(found_endpoints)
                except Exception:
                    continue
            return endpoints
        except Exception as e:
            self.result_area.insert(tk.END, f"Erreur lors de l'analyse des scripts : {e}\n")
            return set()

    def fuzz_endpoints(self, url):
        """Fuzzing basique avec une liste prédéfinie."""
        self.result_area.insert(tk.END, "Lancement du fuzzing...\n")
        common_paths = [
            "api/login", "api/register", "api/users", "admin", "test",
            "auth/login", "auth/register", "v1/users", "v1/admin", "public", "settings", "hidden", "api", "dashboard",
            "config", "login", "logout", "register", "backup",
            "data", "private", "secure"
        ]
        endpoints = set()
        for path in common_paths:
            full_url = urljoin(url, path)
            try:
                response = requests.get(full_url, timeout=5)
                print(f"Test for {full_url} : {response.status_code}")
                if response.status_code != 404:
                    endpoints.add(path)
            except Exception:
                print(f"Error for {full_url}")
                continue
        return endpoints

    def test_all_methods(self, url):
        """Teste les méthodes HTTP GET, POST, PUT, DELETE et PATCH."""
        methods = {
            "GET": requests.get,
            "POST": requests.post,
            "PUT": requests.put,
            "DELETE": requests.delete,
            "PATCH": requests.patch
        }
        for method_name, method in methods.items():
            try:
                response = method(url, timeout=5)
                status = response.status_code
                if status == 200:
                    access_status = "Accessible"
                elif status in [401, 403]:
                    access_status = "Protégé"
                else:
                    access_status = f"Inconnu (Code: {status})"

                # Ajouter le résultat à la zone de texte
                self.result_area.insert(
                    tk.END, f"[{access_status}] {method_name} {url}\n"
                )
            except Exception as e:
                self.result_area.insert(
                    tk.END, f"[Erreur] {method_name} {url} - {e}\n"
                )

    def start_attack(self):
        """Method to start the analysis externally."""
        self.analyze_endpoints()