import tkinter as tk
from collections.abc import Callable
from tkinter import ttk


class FileFrame(ttk.Frame):
    def __init__(
        self,
        container: tk.Misc,
        on_choose: Callable[[], None],
        on_reload: Callable[[], None],
    ) -> None:
        super().__init__(container)

        ##

        self.path_var = tk.StringVar()

        ##

        self.workbook_label = ttk.Label(self, text="CONTROLLING-TABELLE:")
        self.choose_button = ttk.Button(self, text="Wählen...", command=on_choose)
        self.reload_button = ttk.Button(self, text="Neu laden", command=on_reload)
        self.path_label = ttk.Label(
            self, textvariable=self.path_var, style="Path.TLabel"
        )

        ##

        self.workbook_label.grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.choose_button.grid(row=0, column=1, sticky="w")
        self.reload_button.grid(row=0, column=2, sticky="w", padx=(6, 0))
        self.path_label.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(6, 0))

        self.columnconfigure(2, weight=1)

        self.display()

    ##

    def display(self, path: str | None = None) -> None:
        self.path_var.set(
            path
            if path is not None
            else "Bitte wählen Sie eine Controlling-Tabelle aus..."
        )
        self.reload_button["state"] = "disabled" if path is None else "normal"

        self.path_label.config(
            style="Path.TLabel" if path is not None else "Empty.Path.TLabel"
        )
