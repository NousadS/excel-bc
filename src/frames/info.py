import tkinter as tk
from tkinter import ttk

I: list[str] = [
    ".pdf",
    "-=-",
    "-=-",
    "DATEITYP:",
    "z.B. .pdf",
    "GEMEINSAMER ORDNER:",
    "QUELLORDNER:",
]


class InfoFrame(ttk.Frame):
    def __init__(self, container: tk.Misc, on_filetype_changed) -> None:
        super().__init__(container)

        self.filetype_var = tk.StringVar(value=I[0])
        self.common_folder_var = tk.StringVar(value=I[1])
        self.initial_folder_var = tk.StringVar(value=I[2])

        ttk.Label(self, text=I[3]).grid(row=0, column=0, sticky="w", padx=(0, 8))

        ##

        filetype_row = ttk.Frame(self)
        filetype_row.grid(row=0, column=1, columnspan=2, sticky="w")

        ttk.Entry(filetype_row, textvariable=self.filetype_var, width=12).pack(side="left")
        ttk.Label(filetype_row, text=I[4], style="Hint.TLabel").pack(side="left", padx=(8, 0))

        ##

        ttk.Label(self, text=I[5]).grid(row=1, column=0, sticky="w", padx=(0, 8), pady=(6, 0))
        ttk.Label(self, textvariable=self.common_folder_var, style="Path.TLabel", anchor="w").grid(row=1, column=1, columnspan=2, sticky="ew", pady=(6, 0))

        ttk.Label(self, text=I[6]).grid(row=2, column=0, sticky="w", padx=(0, 8), pady=(6, 0))
        ttk.Label(self, textvariable=self.initial_folder_var, style="Path.TLabel", anchor="w").grid(row=2, column=1, columnspan=2, sticky="ew", pady=(6, 0))

        self.columnconfigure(1, weight=1)

        self.filetype_var.trace_add("write", lambda *_: on_filetype_changed())
