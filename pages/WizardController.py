import tkinter as tk
from pages.ddos import DdosPage
from pages.bruteforce import bruteforcePage
from pages.pathTraversal import PathTraversalPage
from pages.vulnerable_components import VulnerableComponentsPage
from pages.nmap import NmapPage
from pages.CSRF import CsrfPage
from pages.subdomain_enumeration import SubdomainEnumerationPage
from pages.AccessControl import AccessControlPage
from pages.bufferoverflow import bufferoverflowPage
from pages.xss import XssPage
from pages.sniffer import SnifferPage
from pages.SSL_TLS_Checker import SSLTLSCheckerPage
from pages.icmpddos import ICMPDdosPage
from pages.sqli import SQLiPage
import tkinter.messagebox as messagebox

class WizardController:
    def __init__(self, parent, controller, selected_attacks, global_url):
        self.parent = parent  # This is the WizardPage
        self.controller = controller
        self.selected_attacks = selected_attacks
        self.global_url = global_url
        self.current_index = 0
        self.frames = {}

        self.load_attack_pages()

    def load_attack_pages(self):
        # Ensure Path Traversal is executed last
        if "Path Traversal" in self.selected_attacks:
            self.selected_attacks.remove("Path Traversal")
            self.selected_attacks.append("Path Traversal")

        for attack in self.selected_attacks:
            if attack == "DDoS":
                self.frames[attack] = DdosPage(self.parent, self.controller, self.global_url, False)
            elif attack == "ICMP DDoS":
                self.frames[attack] = ICMPDdosPage(self.parent, self.controller, self.global_url, False)
            elif attack == "Brute Force":
                self.frames[attack] = bruteforcePage(self.parent, self.controller, self.global_url, False)
            elif attack == "Path Traversal":
                self.frames[attack] = PathTraversalPage(self.parent, self.controller, self.global_url, False)
            elif attack == "Vulnerable Components":
                self.frames[attack] = VulnerableComponentsPage(self.parent, self.controller, self.global_url, False)
            elif attack == "Nmap":
                self.frames[attack] = NmapPage(self.parent, self.controller, self.global_url, False)
            elif attack == "CSRF":
                self.frames[attack] = CsrfPage(self.parent, self.controller, self.global_url, False)
            elif attack == "Subdomain Enumeration":
                self.frames[attack] = SubdomainEnumerationPage(self.parent, self.controller, self.global_url, False)
            elif attack == "Access Control":
                self.frames[attack] = AccessControlPage(self.parent, self.controller, self.global_url, False)
            elif attack == "Buffer Overflow":
                self.frames[attack] = bufferoverflowPage(self.parent, self.controller, self.global_url, False)
            elif attack == "XSS":
                self.frames[attack] = XssPage(self.parent, self.controller, self.global_url, False)
            elif attack == "Sniffer":
                self.frames[attack] = SnifferPage(self.parent, self.controller, self.global_url, False)
            elif attack == "SSL/TLS Check":
                self.frames[attack] = SSLTLSCheckerPage(self.parent, self.controller, self.global_url, False)
            elif attack == "SQL Injection":
                self.frames[attack] = SQLiPage(self.parent, self.controller, self.global_url, False)

    def show_current_page(self):
        for frame in self.frames.values():
            frame.pack_forget()  # Hide all frames

        attack = self.selected_attacks[self.current_index]
        frame = self.frames[attack]
        frame.pack(fill="both", expand=True)  # Show the current frame

        # Update button text and command
        if self.current_index == len(self.selected_attacks) - 1:
            self.parent.update_next_button("Lancer les Attaques", self.execute_attacks)
        else:
            self.parent.update_next_button("Suivant", self.next_page)

    def next_page(self):
        if self.current_index < len(self.selected_attacks) - 1:
            self.current_index += 1
            self.show_current_page()

    def previous_page(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_current_page()

    def execute_attacks(self):
        with open("report.md", "w", encoding="utf-8") as file:
            file.write("# Rapport des Attaques\n\n")
        report = "Rapport des Attaques:\n\n"
        for attack in self.selected_attacks:
            frame = self.frames[attack]
            if hasattr(frame, 'start_attack'):
                print(f"Lancement de l'attaque {attack}")
                frame.start_attack()
                self.parent.update() 
            report += f"- {attack}: Résultats de l'attaque...\n"
        messagebox.showinfo("Rapport", report)
