import tkinter as tk
from tkinter import ttk
import importlib
import os
from functools import partial
from pages.AttackSelection import AttackSelectionPage
from pages.WizardPage import WizardPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Outil Hacking")
        self.geometry("1200x1000")
        
        self.container = tk.Frame(self)
        self.container.pack(side="right", expand=True, fill="both")
        
        self.create_navigation_menu()
        self.frames = {}
        self.load_pages()
        
        # Afficher la page d'accueil par défaut
        self.show_frame("AttackSelectionPage")
    
    def load_pages(self):
        """Chargement des pages."""
        pages_directory = 'pages'
        for filename in os.listdir(pages_directory):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = f"{pages_directory}.{filename[:-3]}"
                module = importlib.import_module(module_name)
                for attr in dir(module):
                    Page = getattr(module, attr)
                    if isinstance(Page, type) and issubclass(Page, tk.Frame) and Page is not WizardPage:
                        page_name = Page.__name__
                        frame = Page(self.container, self, "", True)
                        self.frames[page_name] = frame
                        frame.grid(row=0, column=0, sticky="nsew")
        
        # Manually add the AttackSelectionPage
        attack_selection_page = AttackSelectionPage(self.container, self, "", True)
        self.frames["AttackSelectionPage"] = attack_selection_page
        attack_selection_page.grid(row=0, column=0, sticky="nsew")
    
    def create_navigation_menu(self):
        """Création du menu de navigation."""
        menu_frame = tk.Frame(self)
        menu_frame.pack(side="left", fill="y")
        
        buttons = [
            ("Attaques multiples", "AttackSelectionPage"),
        ]
        
        for text, page in buttons:
            button = tk.Button(
                menu_frame, text=text, command=partial(self.show_frame, page),
                padx=10, pady=5
            )
            button.pack(fill="x")
        
        # Add a gray space between "Attaques multiples" and the rest
        spacer = tk.Frame(menu_frame, height=20)
        spacer.pack(fill="x")
        
        buttons = [
            ("DDoS", "DdosPage"),
            ("ICMP DDoS", "ICMPDdosPage"),
            ("Certificat SSL", "SSLTLSCheckerPage"),
            ("Sniffer", "SnifferPage"),
            ("Path Traversal", "PathTraversalPage"),
            ("XSS", "XssPage"),
            ("SQL Injection", "SQLiPage"),
            ("Nmap", "NmapPage"),
            ("Vulnerable Components", "VulnerableComponentsPage"),
            ("BruteForce", "bruteforcePage"),
            ("Access Control", "AccessControlPage"),
            ("Buffer Overflow", "bufferoverflowPage"),
            ("SubDomain Enumeration", "SubdomainEnumerationPage"),
            ("CSRF", "CsrfPage")
        ]
        
        for text, page in buttons:
            button = tk.Button(
                menu_frame, text=text, command=partial(self.show_frame, page),
                padx=10, pady=5
            )
            button.pack(fill="x")
    
    def show_frame(self, page_name):
        """Afficher la page spécifiée par son nom."""
        frame = self.frames[page_name]
        frame.tkraise()

    def show_wizard(self, selected_attacks, global_url):
        """Show the wizard page with the selected attacks."""
        wizard_page = WizardPage(self.container, self, selected_attacks, global_url)
        self.frames["WizardPage"] = wizard_page
        wizard_page.grid(row=0, column=0, sticky="nsew")
        self.show_frame("WizardPage")

if __name__ == "__main__":
    app = App()
    app.mainloop()
