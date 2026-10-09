import sys
import tkinter as tk
from tkinter import ttk
import pathlib

from frames.main import MainFrame

def enable_dpi_awareness() -> None:
    if sys.platform != "win32":
        return

    try:
        from ctypes import windll

        try:
            windll.shcore.SetProcessDpiAwareness(2)  # per-monitor DPI aware
        except Exception:
            windll.user32.SetProcessDPIAware()  # fallback
    except Exception:
        pass


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Excel BC v1.1.0")
        self.geometry("1000x740+100+100")
        self.resizable(True, True)

        icon_path: pathlib.Path | None = None

        if hasattr(sys, "_MEIPASS"):
            icon_path = pathlib.Path(sys._MEIPASS) / "icon.ico"
        else:
            icon_path = pathlib.Path(__file__).parent / "icon.ico"

        if icon_path.exists():
            self.iconbitmap(icon_path)

        style = ttk.Style(self)
        
        style.configure("Path.TLabel", background="#aeafb0", foreground="#1b1b1b", padding=5)
        style.configure("Hint.TLabel", foreground="#6b7280")
        style.configure("Head.TLabel", foreground="#374151", font=("Segoe UI", 9, "bold"))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.main_frame = MainFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    enable_dpi_awareness()
    app = App()
    app.mainloop()
