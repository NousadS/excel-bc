import tkinter as tk
from tkinter import ttk
import webbrowser

A: list[str] = [
    "Beenden",
    "Dateien kopieren",
    "Hilfe (EN)",
    "Hilfe"
]


class ActionFrame(ttk.Frame):
    def __init__(self, container: tk.Misc, on_copy, on_quit) -> None:
        super().__init__(container)

        ttk.Button(self, text=A[0], command=on_quit).pack(side="right")

        self.copy_button = ttk.Button(self, text=A[1], command=on_copy, state="disabled")
        self.copy_button.pack(side="right", padx=(0, 6))

        ttk.Button(self, text=A[2], command=lambda: webbrowser.open("https://github.com/NousadS/excel-bc/blob/main/README.md")).pack(side="right", padx=(0, 6))
        ttk.Button(self, text=A[3], command=lambda: webbrowser.open("https://github.com/NousadS/excel-bc/blob/main/README-DE.md")).pack(side="right", padx=(0, 6))
