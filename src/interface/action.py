import tkinter as tk
import webbrowser
from collections.abc import Callable
from tkinter import ttk


class ActionsFrame(ttk.Frame):
    def __init__(
        self,
        container: tk.Misc,
        on_copy: Callable[[], None],
        on_back: Callable[[], None],
        on_quit: Callable[[], None],
        on_credits: Callable[[], None],
    ) -> None:
        super().__init__(container)

        ##

        self.help_english_button = ttk.Button(
            self,
            text="Hilfe (EN)",
            command=lambda: self.on_help("EN"),
        )

        self.help_german_button = ttk.Button(
            self,
            text="Hilfe",
            command=lambda: self.on_help("DE"),
        )

        self.credits_button = ttk.Button(
            self,
            text="Credits",
            command=on_credits,
        )

        self.copy_button = ttk.Button(
            self,
            text="Dateien kopieren",
            command=lambda: on_copy(),
        )

        self.back_button = ttk.Button(
            self,
            text="Zurück",
            command=lambda: on_back(),
        )

        self.quit_button = ttk.Button(
            self,
            text="Beenden",
            command=lambda: on_quit(),
        )

        ##

        self.credits_button.pack(side="left")
        self.help_german_button.pack(side="left", padx=(6, 0))
        self.help_english_button.pack(side="left", padx=(6, 0))

        self.quit_button.pack(side="right")

        self.to_copy()
        self.disable()

    ##

    def disable(self) -> None:
        self.copy_button["state"] = "disabled"

    def enable(self) -> None:
        self.copy_button["state"] = "normal"

    def to_back(self) -> None:
        self.copy_button.pack_forget()
        self.back_button.pack(side="right", padx=(0, 6))

    def to_copy(self) -> None:
        self.back_button.pack_forget()
        self.copy_button.pack(side="right", padx=(0, 6))

    ##

    def on_help(self, lang: str = "DE") -> None:
        lang = "-" + lang if lang != "EN" else ""

        webbrowser.open(
            f"https://github.com/NousadS/excel-bc/blob/main/README{lang}.md"
        )
