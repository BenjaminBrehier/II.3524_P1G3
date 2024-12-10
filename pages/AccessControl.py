import tkinter as tk
from tkinter import messagebox, filedialog
import requests
import threading  # Pour permettre l'arrêt propre de l'attaque

class AccessControlPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Titre de la page
        self.title_label = tk.Label(self, text="Attaque - Contrôle d'Accès Défectueux", font=("Arial", 16))
        self.title_label.pack(pady=20)

        # Champs pour l'URL
        self.url_label = tk.Label(self, text="URL de la cible (ex: http://example.com/protected_page):")
        self.url_label.pack(pady=5)
        self.url_entry = tk.Entry(self, width=40)
        self.url_entry.pack(pady=5)

        # Champs pour le token ou cookie d'authentification
        self.token_label = tk.Label(self, text="Token ou Cookie d'authentification :")
        self.token_label.pack(pady=5)
        self.token_entry = tk.Entry(self, width=40)
        self.token_entry.pack(pady=5)

        # Boutons pour démarrer et arrêter l'attaque
        self.start_button = tk.Button(self, text="Lancer l'attaque", command=self.start_attack)
        self.start_button.pack(pady=10)

        # Bouton "Stop" initialement désactivé
        self.stop_button = tk.Button(self, text="Arrêter l'attaque", command=self.stop_attack, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        # Label pour afficher le statut
        self.status_label = tk.Label(self, text="", font=("Arial", 12))
        self.status_label.pack(pady=10)

        # Créer un champ text pour afficher les tentatives et résultats en temps réel
        self.test_output = tk.Text(self, height=15, width=60, wrap=tk.WORD, state=tk.DISABLED)
        self.test_output.pack(pady=10)

        # Variables pour gérer l'état de l'attaque
        self.is_attack_running = False
        self.stop_requested = False

    def start_attack(self):
        """Démarrer l'attaque en tentant d'accéder à des ressources protégées."""
        url = self.url_entry.get()
        token = self.token_entry.get()

        if not url or not token:
            messagebox.showerror("Erreur", "Veuillez remplir l'URL et le Token d'authentification.")
            return

        # Désactiver le bouton Start et activer le bouton Stop
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.status_label.config(text="L'attaque est en cours...")
        self.update_idletasks()

        # Effacer le texte précédent dans le champ de test
        self.test_output.config(state=tk.NORMAL)
        self.test_output.delete(1.0, tk.END)
        self.test_output.config(state=tk.DISABLED)

        # Indiquer que l'attaque est en cours
        self.is_attack_running = True
        self.stop_requested = False

        # Lancer l'attaque dans un thread séparé
        attack_thread = threading.Thread(target=self.run_attack, args=(url, token))
        attack_thread.start()

    def run_attack(self, url, token):
        """Exploiter un contrôle d'accès défectueux pour accéder à une page protégée."""
        # Simuler une liste de pages protégées que l'attaquant tente d'accéder
        protected_pages = [
            "/admin/dashboard",
            "/admin/settings",
            "/user/profile",
            "/user/settings"
        ]

        for page in protected_pages:
            if self.stop_requested:
                break

            # Construire l'URL complète de la page protégée
            target_url = url + page
            headers = {
                'Authorization': f'Bearer {token}'  # Utilisation du token d'authentification
            }

            # Afficher chaque tentative dans le Text widget en temps réel
            self.update_test_output(f"Tentative d'accès à {target_url}...\n")

            # Tenter d'accéder à la page protégée
            if self.try_access(target_url, headers):
                self.update_test_output(f"Réussi : Accès autorisé à {target_url}\n")
            else:
                self.update_test_output(f"Echec : Accès refusé à {target_url}\n")

        # Afficher les résultats finaux
        self.is_attack_running = False
        self.status_label.config(text="Attaque terminée.")
        messagebox.showinfo("Résultat", "L'attaque est terminée.")

        # Réactiver le bouton Start et désactiver le bouton Stop
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def update_test_output(self, text):
        """Met à jour l'affichage des tests dans le Text widget."""
        self.test_output.config(state=tk.NORMAL)
        self.test_output.insert(tk.END, text)
        self.test_output.config(state=tk.DISABLED)
        self.test_output.yview(tk.END)  # Scroll automatique

    def try_access(self, target_url, headers):
        """Essayer d'accéder à la page protégée avec un token d'authentification."""
        try:
            response = requests.get(target_url, headers=headers)

            # Si le code de réponse est 200, l'accès est autorisé (le contrôle d'accès est défectueux)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de l'accès à {target_url}: {e}")

        return False

    def stop_attack(self):
        """Arrêter l'attaque."""
        self.stop_requested = True
        self.status_label.config(text="L'attaque a été arrêtée.")
        messagebox.showinfo("Arrêt", "L'attaque a été arrêtée.")
        self.update_test_output("Attaque arrêtée.\n")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

