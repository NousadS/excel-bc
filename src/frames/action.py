import tkinter as tk
from tkinter import ttk

A: list[str] = [
    "Beenden",
    "Dateien kopieren",
]


class ActionFrame(ttk.Frame):
    def __init__(self, container: tk.Misc, on_copy, on_quit) -> None:
        super().__init__(container)

        ttk.Button(self, text=A[0], command=on_quit).pack(side="right")

        self.copy_button = ttk.Button(self, text=A[1], command=on_copy, state="disabled")
        self.copy_button.pack(side="right", padx=(0, 6))
