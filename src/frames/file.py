import tkinter as tk
from tkinter import ttk

F: list[str] = [
    "TABELLENDATEI:",
    "Wählen...",
    "Neu laden",
    "-=-",
]


class FileFrame(ttk.Frame):
    def __init__(self, container: tk.Misc, on_choose, on_reload) -> None:
        super().__init__(container)

        self.path_var = tk.StringVar(value=F[3])

        ttk.Label(self, text=F[0]).grid(row=0, column=0, sticky="w", padx=(0, 8))

        self.choose_button = ttk.Button(self, text=F[1], command=on_choose)
        self.reload_button = ttk.Button(self, text=F[2], command=on_reload, state="disabled")

        self.choose_button.grid(row=0, column=1, sticky="w")
        self.reload_button.grid(row=0, column=2, sticky="w", padx=(6, 0))

        ttk.Label(self, textvariable=self.path_var, style="Path.TLabel", anchor="w").grid(row=1, column=0, columnspan=3, sticky="ew", pady=(6, 0))

        self.columnconfigure(2, weight=1)
