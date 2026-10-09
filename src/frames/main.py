import pathlib
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as ms
from tkinter import ttk

from state import (
    State,
    FileWrongExtensionError,
    HeaderAppearsTwiceError,
    NoHeaderValueError,
    NoWorkbookSelectedError,
    MissingHeadersError,
    WrongValueAmountsError,
)
from .action import ActionFrame
from .file import FileFrame
from .info import InfoFrame, I
from .operations import OperationFrame

M: list[str] = [
    "Tabellendatei öffnen",
    "Tabellendatei konnte nicht gelesen werden",
    "Nichts zu tun",
    "Keine auszuführenden Aktionen vorhanden.",
    "Bestätigen",
    "{} Datei(en) an die Zielorte kopieren?",
    "\n... und {} mehr.",
    "Abgeschlossen mit Warnungen",
    "Kopiert {} von {} Datei(en).\n{}{}",
    "Erledigt",
    "Kopiert {} Datei(en).",
    "{} ist keine .xlsx-Datei.",
    "Die Kopfzeile {} kommt mehr als einmal vor.",
    "Unter der Kopfzeile {} wurde kein Wert gefunden.",
    "Es wurde kein Dokument ausgewählt.",
    "{} existiert nicht.",
    "Fehlende Kopfzeile(n) in der Dokument: {}",
    "Die Anzahl der Dateinamen und Ziele ist nicht gleich ({} / {} / {}).",
]


class MainFrame(ttk.Frame):
    def __init__(self, container: tk.Misc) -> None:
        super().__init__(container, padding=10)

        self.state: State | None = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.file_section = FileFrame(self, on_choose=self.choose, on_reload=self.reload)
        self.info_section = InfoFrame(self, on_filetype_changed=self.refresh_preview)
        self.operation_list = OperationFrame(self)
        self.action_section = ActionFrame(self, on_copy=self.copy_files, on_quit=self.quit_app)

        self.file_section.grid(row=0, column=0, sticky="ew")
        self.info_section.grid(row=1, column=0, sticky="ew", pady=(8, 0))
        self.operation_list.grid(row=2, column=0, sticky="nsew", pady=(10, 0))
        self.action_section.grid(row=3, column=0, sticky="ew", pady=(10, 0))

    def quit_app(self) -> None:
        self.winfo_toplevel().destroy()

    def choose(self) -> None:
        filename = fd.askopenfilename(title=M[0], initialdir="/", filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))

        if not filename:
            return
        
        self.load_workbook(pathlib.Path(filename))

    def reload(self) -> None:
        if self.state is not None and self.state.workbook is not None:
            self.load_workbook(self.state.workbook)

    def load_workbook(self, path: pathlib.Path) -> None:
        state = State()

        msg: str | None = None

        try:
            state.set_workbook(path)
            state.parse_workbook()
        except FileWrongExtensionError as exc:
            msg = M[11].format(exc.args[0])
        except HeaderAppearsTwiceError as exc:
            msg = M[12].format(exc.args[0])
        except NoHeaderValueError as exc:
            msg = M[13].format(exc.args[0])
        except NoWorkbookSelectedError:
            msg = M[14]
        except FileNotFoundError as exc:
            msg = M[15].format(exc.args[0])
        except MissingHeadersError as exc:
            msg = M[16].format(", ".join(f"`{name}`" for name in exc.missing))
        except WrongValueAmountsError as exc:
            msg = M[17].format(exc.file_name_auto, exc.file_name_manual, exc.destination_folder)
        except Exception as exc:
            msg = str(exc)

        if msg:
            ms.showerror(M[1], msg)
            self.state = None
            self.action_section.copy_button.state(["disabled"])
            self.file_section.reload_button.state(["disabled"])
            self.info_section.common_folder_var.set(I[1])
            self.info_section.initial_folder_var.set(I[2])
            return

        state.filetype = self.info_section.filetype_var.get()
        self.state = state

        self.file_section.path_var.set(str(self.state.workbook))
        self.operation_list.set_operations([])
        self.info_section.common_folder_var.set(state.common_folder)
        self.info_section.initial_folder_var.set(state.initial_folder)
        self.file_section.reload_button.state(["!disabled"])
        self.action_section.copy_button.state(["!disabled"])
        self.refresh_preview()

    def copy_files(self) -> None:
        if self.state is None:
            return

        self.state.filetype = self.info_section.filetype_var.get()
        operations = self.state.get_operations()

        if not operations:
            ms.showinfo(M[2], M[3])
            return

        if not ms.askyesno(M[4], M[5].format(len(operations))):
            return

        copied, problems = self.state.copy_files()
        self.refresh_preview()

        if problems:
            shown = "\n".join(problems[:3])
            more = "" if len(problems) <= 3 else M[6].format(len(problems) - 3)

            ms.showwarning(M[7], M[8].format(copied, len(operations), shown, more))
        else:
            ms.showinfo(M[9], M[10].format(copied))

    def refresh_preview(self) -> None:
        if self.state is None:
            self.operation_list.set_operations([])
            return

        self.state.filetype = self.info_section.filetype_var.get()

        operations = self.state.get_operations()

        self.operation_list.set_operations(operations, prefix=str(self.state.common_folder))
