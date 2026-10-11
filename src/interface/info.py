import tkinter as tk
from tkinter import ttk


class InfoFrame(ttk.Frame):
    def __init__(self, container: tk.Misc) -> None:
        super().__init__(container)

        ##

        self.filetype_var = tk.StringVar()
        self.common_folder_var = tk.StringVar()

        ##

        self.filetype_static_label = ttk.Label(
            self,
            text="DATEITYP:",
        )

        self.filetype_label = ttk.Label(
            self,
            textvariable=self.filetype_var,
            style="Path.TLabel",
        )

        self.common_folder_static_label = ttk.Label(
            self,
            text="HAUPTORDNER:",
        )

        self.common_folder_label = ttk.Label(
            self,
            textvariable=self.common_folder_var,
            style="Path.TLabel",
        )

        self.filetype_static_label.grid(
            row=0, column=0, sticky="w", padx=(0, 8), pady=(0, 8)
        )
        self.filetype_label.grid(row=0, column=1, sticky="we", pady=(0, 8))
        self.common_folder_static_label.grid(
            row=1, column=0, sticky="w", padx=(0, 8), pady=(0, 8)
        )
        self.common_folder_label.grid(row=1, column=1, sticky="we", pady=(0, 8))

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        ##

        self.display()

    ##

    def display(
        self,
        filetype: str | None = None,
        common_folder: str | None = None,
    ) -> None:
        self.filetype_var.set(
            filetype
            if filetype is not None
            else "Keine Controlling-Tabelle wurde gewählt..."
        )

        self.common_folder_var.set(
            common_folder
            if common_folder is not None
            else "Keine Controlling-Tabelle wurde gewählt..."
        )

        style: str = "Path.TLabel" if filetype is not None else "Empty.Path.TLabel"

        self.filetype_label.config(style=style)
        self.common_folder_label.config(style=style)
