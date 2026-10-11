import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog as fd
from tkinter import messagebox, ttk
from tkinter import messagebox as ms

from interface.action import ActionsFrame
from interface.file import FileFrame
from interface.info import InfoFrame
from interface.operations import OperationsFrame
from logic.state import (
    CommonFolderNotExistError,
    CriticalProblemNotResolvedError,
    FileWrongExtensionError,
    HeaderAppearsTwiceError,
    InitialFolderNotExistError,
    MissingHeadersError,
    NoHeaderValueError,
    State,
    WorkbookDoesNotExistError,
    WrongValueAmountsError,
)


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        ##

        self.enable_dpi_awareness()
        self.title("ExBC v2.0.0")
        self.geometry("1000x740+100+100")
        self.resizable(True, True)
        self.icon()
        self.style()

        ##

        self.state: State = State()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.file_frame = FileFrame(self, on_choose=self.choose, on_reload=self.reload)
        self.info_frame = InfoFrame(self)
        self.actions_frame = ActionsFrame(
            self,
            on_copy=self.execute,
            on_back=self.back,
            on_quit=self.quit,
            on_credits=self.show_credits,
        )
        self.operations_frame = OperationsFrame(self, self.actions_frame)

        self.file_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        self.info_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(8, 0))
        self.operations_frame.grid(
            row=2, column=0, sticky="nsew", padx=10, pady=(10, 0)
        )
        self.actions_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(10, 10))

    ##

    def enable_dpi_awareness(self) -> None:
        if sys.platform != "win32":
            return

        try:
            from ctypes import windll

            try:
                windll.shcore.SetProcessDpiAwareness(2)  # per-monitor DPI aware
            except Exception:  # noqa: BLE001
                windll.user32.SetProcessDPIAware()  # fallback
        except Exception:  # noqa: BLE001, S110
            pass

    def get_resource_path(self, filename: str) -> Path | None:
        if (
            hasattr(sys, "_MEIPASS")
            and (p := (Path(sys._MEIPASS) / filename)).exists()  # pyright: ignore[reportAttributeAccessIssue]
            or (p := Path(__file__).parent / filename).exists()
            or (p := Path(__file__).parent.parent / filename).exists()
        ):
            return p

        return None

    def icon(self) -> None:
        if p := self.get_resource_path("icon.ico"):
            self.iconbitmap(p)

    def style(self) -> None:
        style = ttk.Style(self)

        if "vista" in style.theme_names():
            style.theme_use("vista")

        style.configure(
            ".",
            font=("Segoe UI", 12),
        )

        style.configure(
            "Path.TLabel",
            background="#aeafb0",
            foreground="#1b1b1b",
            padding=5,
        )
        style.configure(
            "Empty.Path.TLabel",
            background="#aeafb0",
            foreground="#696969",
            padding=5,
        )

        style.configure(
            "Hint.TLabel",
            foreground="#6b7280",
        )

        style.configure(
            "Head.TLabel",
            foreground="#374151",
            font=(
                "Segoe UI",
                9,
                "bold",
            ),
        )

    ##

    def choose(self) -> None:
        filename = fd.askopenfilename(
            title="Tabellendatei öffnen",
            initialdir="C:\\Users\\nousa\\Desktop\\New folder\\test\\",
            filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")),
        )

        if not filename:
            return

        self.state.reset()
        self.load(Path(filename))

    def back(self) -> None:
        self.state.reset()
        self.operations_frame.display([], False)
        self.info_frame.display()
        self.file_frame.display(
            str(self.state.workbook)
            if self.state.workbook and self.state.workbook != ""
            else None
        )

    def reload(self) -> None:
        if self.state.workbook:
            self.load(self.state.workbook)

    ##

    def load(self, path: Path) -> None:
        msg: str | None = None

        corr_msg: str = "\n\nBitte korrigieren Sie die Fehler in der Controlling-Tabelle und klicken Sie dann auf 'Neu laden'."

        try:
            self.state.parse(path)
        except FileWrongExtensionError as exc:
            msg = f"Die Datei '{exc.file}' hat kein gültiges Format. Bitte wähle eine .xlsx-Datei."
        except WorkbookDoesNotExistError as exc:
            msg = f"Die Excel-Datei '{exc.filename}' wurde nicht gefunden."
        except HeaderAppearsTwiceError as exc:
            msg = (
                f"Die Kopfzeile '{exc.header.title()}' kommt mehrfach in der Tabelle vor."
                + corr_msg
            )
        except NoHeaderValueError as exc:
            msg = (
                f"Unter der Kopfzeile '{exc.header.title()}' wurde kein gültiger Wert gefunden."
                + corr_msg
            )
        except CommonFolderNotExistError:
            msg = (
                "Der angegebene Hauptordner (Common Folder) existiert nicht." + corr_msg
            )
        except InitialFolderNotExistError:
            msg = (
                "Der angegebene Quellordner (Initial Folder) existiert nicht."
                + corr_msg
            )
        except MissingHeadersError as exc:
            msg = (
                f"Folgende notwendige Kopfzeilen fehlen in der Tabelle: \n - {', \n - '.join(h.title() for h in exc.missing)}"
                + corr_msg
            )
        except WrongValueAmountsError as exc:
            msg = (
                f"Die Anzahl der Werte stimmt nicht überein\n(Alt-Dateien: {exc.old_files}, Neu-Dateien: {exc.new_files}, Ziel-Ordner: {exc.destinations})."
                + corr_msg
            )
        except Exception as exc:  # noqa: BLE001
            msg = repr(exc)

        if msg:
            self.actions_frame.disable()
            ms.showerror("Tabellendatei konnte nicht gelesen werden", msg)

        self.info_frame.display(
            self.state.extension if self.state.extension != "" else None,
            self.state.common_folder if self.state.common_folder != "" else None,
        )

        self.file_frame.display(
            str(self.state.workbook)
            if self.state.workbook and self.state.workbook != ""
            else None
        )

        # Shows operations message boxes and controls self.action_frame
        self.operations_frame.display(self.state.operations, False)

    def execute(self) -> None:
        try:
            self.state.execute()
        except CriticalProblemNotResolvedError:
            ms.showerror(
                "Kritische Fehler",
                "Eine der kritischen Fehler wurde nicht gelöst. Das Kopieren ist nicht möglich.",
            )

        # Shows operations message boxes and controls self.action_frame
        self.operations_frame.display(self.state.operations, True)

        self.info_frame.display(
            self.state.extension if self.state.extension != "" else None,
            self.state.common_folder if self.state.common_folder != "" else None,
        )

        self.file_frame.display(
            str(self.state.workbook)
            if self.state.workbook and self.state.workbook != ""
            else None
        )

    ##

    def quit(self) -> None:
        self.winfo_toplevel().destroy()

    ##

    def show_credits(self) -> None:
        try:
            if credits_path := self.get_resource_path("CREDITS"):
                with credits_path.open("r", encoding="utf-8") as file:
                    credits_text = file.read()
            else:
                raise FileNotFoundError("No CREDITS file could be found.")

            if license_path := self.get_resource_path("LICENSE"):
                with license_path.open("r", encoding="utf-8") as file:
                    license_text = file.read()
            else:
                raise FileNotFoundError("No LICENSE file could be found.")

            credits_window = tk.Toplevel(
                width=1000,
                height=740,
            )
            credits_window.title("Credits & Licenses")

            text_widget = tk.Text(
                credits_window,
                wrap="word",
                width=125,
                height=40,
                relief="solid",
            )
            text_widget.insert(
                "1.0",
                credits_text + "\nLICENSE OF THIS APPLICATION\n\n" + license_text,
            )
            text_widget.config(state="disabled")
            text_widget.pack(padx=0, pady=0, fill="both", expand=True)
        except Exception as e:  # noqa: BLE001
            messagebox.showerror("Error", f"Could not load credits: {e}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
