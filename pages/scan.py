import tkinter as tk

class ScanPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="Page Scan", font=("Arial", 16))
        label.pack(pady=20)
