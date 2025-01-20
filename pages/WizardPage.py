import tkinter as tk
from tkinter import messagebox
from pages.WizardController import WizardController

class WizardPage(tk.Frame):
    def __init__(self, parent, controller, selected_attacks, global_url):
        super().__init__(parent)
        self.controller = controller
        self.wizard_controller = WizardController(self, controller, selected_attacks, global_url)

        # Navigation buttons
        tk.Button(self, text="Précédent", command=self.wizard_controller.previous_page).pack(side=tk.LEFT, padx=10, pady=10)
        self.next_button = tk.Button(self, text="Suivant", command=self.wizard_controller.next_page)
        self.next_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Show the first attack configuration page
        self.wizard_controller.show_current_page()

    def update_next_button(self, text, command):
        self.next_button.config(text=text, command=command)

    def execute_attacks(self):
        # Placeholder for executing attacks
        report = "Rapport des Attaques:\n\n"
        for attack in self.selected_attacks:
            report += f"- {attack}: Résultats de l'attaque...\n"

        # Display the report
        messagebox.showinfo("Rapport", report)
