import tkinter as tk
from tkinter import Toplevel
import ssl
import socket
from urllib.parse import urlparse
import datetime


class CryptoPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        label = tk.Label(self, text="Page SSL/TLS Checker", font=("Arial", 16))
        label.pack(pady=20)

        tk.Label(self, text="URL cible :").pack(pady=5)
        self.url_entry = tk.Entry(self, width=40)
        self.url_entry.pack(pady=10)

        self.check_button = tk.Button(self, text="Vérifier la sécurité SSL/TLS", command=self.check_ssl)
        self.check_button.pack(pady=10)

        self.status_label = tk.Label(self, text="", wraplength=600, justify="left")
        self.status_label.pack(pady=10)

    def check_ssl(self):
        url = self.url_entry.get()
        if not url:
            self.status_label.config(text="Erreur : Veuillez entrer une URL valide.")
            return

        #Extraire le nom d'hôte
        try:
            parsed_url = urlparse(url)
            host = parsed_url.netloc if parsed_url.netloc else parsed_url.path
            port = 443 # Port par défaut pour HTTPS (80 pour http il me semble)

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

                    #Génère le rapport principal
                    result = f"URL cible : {url}\n"
                    result += f"Algorithme de chiffrement : {cipher[0]}\n"
                    result += f"Niveau de chiffrement : {cipher[1]} bits\n"
                    result += f"Certificat valide jusqu'au : {cert_expiry_date}\n"
                    result += f"Autorité émettrice : {issuer_details}\n" # Ajout de l'autorité de certif émettrice

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
        except ssl.SSLError as e:
            self.status_label.config(text=f"Erreur SSL : {e}")
        except Exception as e:
            self.status_label.config(text=f"Erreur : {e}")

    def show_results(self, result):
        """Afficher les résultats dans une nouvelle fenêtre."""
        results_window = Toplevel(self)
        results_window.title("Résultats SSL/TLS")
        results_window.geometry("500x400")

        results_label = tk.Label(results_window, text="Résumé de la vérification", font=("Arial", 14))
        results_label.pack(pady=10)

        results_text = tk.Text(results_window, wrap="word", height=20, width=60)
        results_text.insert("1.0", result)
        results_text.config(state="disabled") #Rendre le texte non modifiable
        results_text.pack(pady=10, padx=10)

        close_button = tk.Button(results_window, text="Fermer", command=results_window.destroy)
        close_button.pack(pady=10)
