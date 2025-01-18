import tkinter as tk
from tkinter import ttk
import importlib
import os
from functools import partial

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Application avec Menu de Navigation")
        self.geometry("800x600")
        
        self.container = tk.Frame(self)
        self.container.pack(side="right", expand=True, fill="both")
        
        self.create_navigation_menu()
        self.frames = {}
        self.load_pages()
        
        # Afficher la page d'accueil par défaut
        self.show_frame("HomePage")
    
    def load_pages(self):
        """Chargement des pages."""
        pages_directory = 'pages'
        for filename in os.listdir(pages_directory):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = f"{pages_directory}.{filename[:-3]}"
                module = importlib.import_module(module_name)
                for attr in dir(module):
                    Page = getattr(module, attr)
                    if isinstance(Page, type) and issubclass(Page, tk.Frame):
                        page_name = Page.__name__
                        frame = Page(self.container, self)
                        self.frames[page_name] = frame
                        frame.grid(row=0, column=0, sticky="nsew")
    
    def create_navigation_menu(self):
        """Création du menu de navigation."""
        menu_frame = tk.Frame(self, bg="#f0f0f0")
        menu_frame.pack(side="left", fill="y")
        
        buttons = [
            ("Accueil", "HomePage"),
            ("DDoS", "DdosPage"),
            ("Certificat SSL", "CryptoPage"),
            ("Sniffer", "SnifferPage"),
            ("Path Traversal", "PathTraversalPage"),
            ("XSS", "XssPage"),
            ("Nmap", "NmapPage"),
            ("Scan", "ScanPage"),
            ("Info", "InfoPage"),
            ("Privilege Check", "PrivilegeCheckPage"),
            ("Vulnerable Components", "VulnerableComponentsPage"),
            ("BruteForce", "bruteforcePage"),
            ("Access Control", "AccessControlPage"),
            ("Buffer Overflow", "bufferoverflowPage")

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

if __name__ == "__main__":
    app = App()
    app.mainloop()
