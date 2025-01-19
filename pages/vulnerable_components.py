import tkinter as tk
from tkinter import scrolledtext
import requests
from bs4 import BeautifulSoup
import re
import os


class VulnerableComponentsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        tk.Label(self, text="Analyse des Composants Vulnérables", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="Entrez l'URL cible :").pack(anchor="w", padx=10)
        self.url_entry = tk.Entry(self, width=50)
        self.url_entry.pack(pady=5, padx=10)

        tk.Label(self, text="Nombre de vulnérabilités à afficher :").pack(anchor="w", padx=10)
        self.vuln_count_entry = tk.Entry(self, width=10)
        self.vuln_count_entry.insert(0, "3")  # Valeur par défaut
        self.vuln_count_entry.pack(pady=5, padx=10)

        tk.Button(self, text="Analyser", command=self.analyze_components).pack(pady=10)

        # Zone de résultats
        tk.Label(self, text="Résultats de l'analyse :").pack(anchor="w", padx=10, pady=5)
        self.result_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=80, height=20)
        self.result_area.pack(padx=10, pady=10)

    def analyze_components(self):
        target_url = self.url_entry.get().strip()
        vuln_count = int(self.vuln_count_entry.get().strip())

        if not target_url.startswith("http"):
            self.result_area.insert(tk.END, "Veuillez entrer une URL valide (commençant par http ou https).\n")
            return

        self.result_area.delete(1.0, tk.END)
        self.result_area.insert(tk.END, f"Analyse en cours pour : {target_url}\n\n")

        try:
            # Recherche des composants (bibliothèques et frameworks)
            components = self.find_components(target_url)
            frameworks = self.find_frameworks(target_url)

            if not components and not frameworks:
                self.result_area.insert(tk.END, "Aucun composant ou framework détecté.\n")
                return

            self.result_area.insert(tk.END, f"Composants détectés :\n")
            for name, version in components:
                self.result_area.insert(tk.END, f"  - {name}: {version}\n")

            self.result_area.insert(tk.END, f"\nFrameworks détectés :\n")
            for name, version in frameworks:
                self.result_area.insert(tk.END, f"  - {name}: {version}\n")

            self.result_area.insert(tk.END, "\nVérification des vulnérabilités...\n")
            for name, version in components + frameworks:
                vulnerability_info = self.check_vulnerabilities(name, version, vuln_count)
                self.result_area.insert(tk.END, vulnerability_info + "\n")
        except Exception as e:
            self.result_area.insert(tk.END, f"Erreur : {e}\n")

    def find_components(self, url):
        """Détecte les bibliothèques, composants front-end et technologies serveur."""
        components = {}
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Rechercher des bibliothèques front-end dans les balises script
            scripts = soup.find_all('script', src=True)
            for script in scripts:
                src = script['src'].lower()
                if 'jquery' in src:
                    components['jQuery'] = self.extract_version(src)
                elif 'jquery-ui' in src:
                    components['jQuery UI'] = self.extract_version(src)
                elif 'bootstrap' in src:
                    components['Bootstrap'] = self.extract_version(src)
                elif 'tailwind' in src:
                    components['TailwindCSS'] = self.extract_version(src)
                elif 'bulma' in src:
                    components['Bulma'] = self.extract_version(src)
                # Détecter les scripts PHP
                elif src.endswith('.php'):
                    components['PHP'] = 'Version inconnue'

            # Rechercher des bibliothèques dans les balises link
            links = soup.find_all('link', href=True)
            for link in links:
                href = link['href'].lower()
                if 'font-awesome' in href:
                    components['Font Awesome'] = self.extract_version(href)
                elif 'materialize' in href:
                    components['Materialize'] = self.extract_version(href)
                elif href.endswith('.php'):
                    components['PHP'] = 'Version inconnue'

            # Vérifier les en-têtes HTTP pour des informations serveur
            headers = response.headers
            if 'X-Powered-By' in headers and 'php' in headers['X-Powered-By'].lower():
                version = self.extract_version(headers['X-Powered-By'])
                components['PHP'] = version if version else 'Version inconnue'
            if 'Server' in headers and 'php' in headers['Server'].lower():
                version = self.extract_version(headers['Server'])
                components['PHP'] = version if version else 'Version inconnue'

        except Exception as e:
            self.result_area.insert(tk.END, f"Erreur lors de l'analyse des composants : {e}\n")
        return list(components.items())



    def find_frameworks(self, url):
        """Détecte les frameworks front-end et back-end à partir du HTML et des en-têtes."""
        frameworks = []
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            html_content = response.text.lower()

            # Frameworks front-end
            if soup.find(attrs={"data-reactroot": True}) or "react" in html_content:
                frameworks.append(("React", self.extract_version_from_html(html_content, "react")))
            if soup.find(attrs={"ng-app": True}) or "angular" in html_content:
                frameworks.append(("Angular", self.extract_version_from_html(html_content, "angular")))
            if soup.find(attrs={"id": re.compile(r"vue-")}) or "vue" in html_content:
                frameworks.append(("Vue.js", self.extract_version_from_html(html_content, "vue")))

            # Frameworks back-end (via en-têtes HTTP)
            headers = response.headers
            if 'X-Powered-By' in headers:
                frameworks.append(('Backend Framework', headers['X-Powered-By']))
        except Exception as e:
            self.result_area.insert(tk.END, f"Erreur lors de l'analyse des frameworks : {e}\n")

        return frameworks


    def extract_version_from_html(self, html, keyword):
        """Extrait la version d'un framework à partir du HTML."""
        pattern = re.compile(fr"{keyword}[^\d]*(\d+\.\d+\.\d+)", re.IGNORECASE)
        match = pattern.search(html)
        return match.group(1) if match else "Version inconnue"


    def extract_version(self, url):
        """Extrait la version d'un composant à partir de son URL."""
        match = re.search(r'(\d+\.\d+\.\d+)', url)
        if match:
            return match.group(1)
        return "Version inconnue"

    def query_github_advisory(self, package_name, vuln_count):
        """Rechercher des vulnérabilités pour un package via GitHub GraphQL API."""
        url = "https://api.github.com/graphql"
        token = os.getenv("GITHUB_TOKEN")

        query = """
        query($package: String!, $first: Int!) {
          securityVulnerabilities(first: $first, package: $package) {
            edges {
              node {
                advisory {
                  description
                  severity
                  references {
                    url
                  }
                }
              }
            }
          }
        }
        """

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        variables = {"package": package_name, "first": vuln_count}

        try:
            response = requests.post(
                url, json={"query": query, "variables": variables}, headers=headers
            )

            if response.status_code == 200:
                data = response.json()
                vulnerabilities = data["data"]["securityVulnerabilities"]["edges"]
                return vulnerabilities

            return f"Erreur GitHub : {response.status_code} - {response.text}"
        except Exception as e:
            return f"Erreur lors de l'accès à l'API GitHub : {e}"

    def check_vulnerabilities(self, name, version, vuln_count):
        vulnerabilities = self.query_github_advisory(name, vuln_count)
        if isinstance(vulnerabilities, str):  # Cas d'erreur
            return f"{name}: {vulnerabilities}"
        if not vulnerabilities:
            return f"{name}: Pas de vulnérabilités connues"
        result = f"{name}: {len(vulnerabilities)} vulnérabilité(s) détectée(s):\n"
        for vuln in vulnerabilities:
            advisory = vuln["node"]["advisory"]
            description = advisory["description"]
            severity = advisory["severity"]
            reference = advisory["references"][0]["url"] if advisory["references"] else "Aucun lien"
            result += f"- Gravité : {severity}\n  Description : {description}\n  Référence : {reference}\n"
        return result

    def start_attack(self):
        """Method to start the analysis externally."""
        self.analyze_components()