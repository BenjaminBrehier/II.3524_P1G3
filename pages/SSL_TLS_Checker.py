import tkinter as tk
import ssl
import socket
from urllib.parse import urlparse
import datetime


class SSLTLSCheckerPage(tk.Frame):
    def __init__(self, parent, controller, global_url, show_button):
        super().__init__(parent)
        self.global_url = global_url
        self.show_button = show_button

        label = tk.Label(self, text="Page SSL/TLS Checker", font=("Arial", 16))
        label.pack(pady=20)

        tk.Label(self, text="URL cible :").pack(pady=5)
        self.url_entry = tk.Entry(self, width=40)
        self.url_entry.pack(pady=10)
        self.url_entry.insert(0, self.global_url)
        if self.show_button:
            self.check_button = tk.Button(self, text="Vérifier la sécurité SSL/TLS", command=self.check_ssl)
            self.check_button.pack(pady=10)

        self.status_label = tk.Label(self, text="", wraplength=600, justify="left")
        self.status_label.pack(pady=10)

        # Text area to display results
        self.results_text = tk.Text(self, wrap="word", height=20, width=60, state="disabled")
        self.results_text.pack(pady=10, padx=10)

    def check_ssl(self):
        url = self.url_entry.get()
        if not url:
            self.status_label.config(text="Erreur : Veuillez entrer une URL valide.")
            return

        # Extraire le nom d'hôte
        try:
            parsed_url = urlparse(url)
            host = parsed_url.netloc if parsed_url.netloc else parsed_url.path
            port = 443  # Port par défaut pour HTTPS

            # Créé une connexion sécurisée
            context = ssl.create_default_context()
            with socket.create_connection((host, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    # Récupère les informations du certificat
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()  # Algorithme de chiffrement utilisé

                    # Vérifie la date d'expiration du certificat
                    cert_expiry_date = datetime.datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                    days_left = (cert_expiry_date - datetime.datetime.utcnow()).days

                    # Récupère l'autorité émettrice du certificat
                    issuer = cert.get('issuer', [])
                    issuer_details = ", ".join(f"{key}={value}" for entry in issuer for key, value in entry)

                    # Récupère les détails du sujet (le propriétaire du certificat)
                    subject = cert.get('subject', [])
                    subject_details = ", ".join(f"{key}={value}" for entry in subject for key, value in entry)

                    # Génère le rapport principal
                    result = f"URL cible : {url}\n"
                    result += f"Algorithme de chiffrement : {cipher[0]}\n"
                    result += f"Niveau de chiffrement : {cipher[1]} bits\n"
                    result += f"Certificat valide jusqu'au : {cert_expiry_date}\n"
                    result += f"Autorité émettrice : {issuer_details}\n"

                    if days_left < 0:
                        result += "⚠️  Certificat expiré !\n"
                    elif days_left < 30:
                        result += f"⚠️  Certificat expire dans {days_left} jours.\n"
                    else:
                        result += f"✅  Certificat valide pour encore {days_left} jours.\n"

                    # Vérifie force du chiffrement
                    weak_ciphers = ["RC4", "DES", "3DES"]
                    if any(weak in cipher[0] for weak in weak_ciphers):
                        result += "⚠️  Algorithme de chiffrement faible détecté !\n"
                    else:
                        result += "✅  Algorithme de chiffrement robuste.\n"

                    self.show_results(result)
                    self.save_results_to_file(result)
        except ssl.SSLError as e:
            self.status_label.config(text=f"Erreur SSL : {e}")
        except Exception as e:
            self.status_label.config(text=f"Erreur : {e}")

    def show_results(self, result):
        """Afficher les résultats dans la zone de texte."""
        self.results_text.config(state="normal")
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert("1.0", result)
        self.results_text.config(state="disabled")

    def save_results_to_file(self, result):
        """Sauvegarde les résultats dans un fichier markdown."""
        with open("report.md", "a", encoding="utf-8") as file:
            file.write("## SSL/TLS Checker\n\n")
            for line in result.splitlines():
                file.write(f"- {line}\n")
            file.write("\n")

    def start_attack(self):
        """Method to start the analysis externally."""
        self.check_ssl()
