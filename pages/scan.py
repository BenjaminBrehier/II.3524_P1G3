import tkinter as tk

class ScanPage(tk.Frame):
    def __init__(self, parent, controller, global_url):
        super().__init__(parent)
        self.global_url = global_url
        label = tk.Label(self, text="Page Scan", font=("Arial", 16))
        label.pack(pady=20)
