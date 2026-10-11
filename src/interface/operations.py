import tkinter as tk
from tkinter import messagebox as ms
from tkinter import ttk

from interface.action import ActionsFrame
from logic.operation import Operation

_WARNING_TEXT: dict[Operation.WarningCause, str] = {
    Operation.WarningCause.SOURCE_DOES_NOT_EXIST: "Die Quelldatei wurde nicht gefunden.",
    Operation.WarningCause.SOURCE_NOT_INCLUDED: "Die Quelldatei existiert zwar im Quellordner, "
    "fehlt aber in der Controlling-Tabelle.",
}

_PROBLEM_TEXT: dict[Operation.ProblemCause, str] = {
    Operation.ProblemCause.SOURCE_DUPLICATE: "Diese Quelldatei ist mehrfach in der Controlling-Tabelle aufgeführt.",
    Operation.ProblemCause.DESTINATION_ALREADY_EXISTS: "Die Zieldatei existiert bereits.",
    Operation.ProblemCause.DESTINATION_FOLDER_DOES_NOT_EXIST: "Der Überordner der Zieldatei existiert nicht.",
    Operation.ProblemCause.DESTINATION_NAME_TOO_LONG: "Der Name der Zieldatei ist zu lang. "
    "Windows könnte diese Operation blockieren.",
    Operation.ProblemCause.DESTINATION_INVALID_NAME: "Der Name der Zieldatei enthält ungültige Zeichen, "
    "die von Windows nicht erlaubt sind.",
    Operation.ProblemCause.DESTINATION_DUPLICATE: "Dieser Zielpfad wird bereits von einer anderen Datei in der Tabelle verwendet.",
}


class OperationsFrame(ttk.Frame):
    def __init__(self, container: tk.Misc, action_frame: ActionsFrame) -> None:
        super().__init__(container)

        self.actions: ActionsFrame = action_frame

        self.description_var = tk.StringVar()
        self.label = ttk.Label(self, textvariable=self.description_var)

        self.tree = ttk.Treeview(
            self,
            columns=("source", "destination", "problems"),
            show="headings",
            selectmode="none",
        )

        self.tree.column("source", width=100, minwidth=100, stretch=True)
        self.tree.column("destination", width=100, minwidth=100, stretch=True)
        self.tree.column("problems", width=600, minwidth=100, stretch=True)

        self.tree.heading("source", text="QUELLDATEI")
        self.tree.heading("destination", text="ZIELDATEI")
        self.tree.heading("problems", text="PROBLEM")

        self.tree.tag_configure("error", foreground="#5e0112", background="#ffd5dd")
        self.tree.tag_configure("complete", foreground="#015e0c", background="#d5ffdb")
        self.tree.tag_configure("warning", foreground="#5e3f01", background="#fff7d5")

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.label.grid(row=0, column=0, sticky="w", pady=(0, 4))
        self.tree.grid(row=1, column=0, sticky="nsew")
        self.scrollbar.grid(row=1, column=1, sticky="ns")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.display([], False)

    # Public

    def display(self, operations: list[Operation], complete: bool) -> None:
        self._clear_tree()

        copied = errors = warnings = problems = 0

        for index, operation in enumerate(operations, start=1):
            tag, problem, category = "", "", ""
            status = operation.status

            if status == Operation.Status.COMPLETED:
                tag, problem, category = "complete", "", "complete"
            elif status == Operation.Status.FAILED:
                tag, problem, category = "error", operation.comment, "error"
            elif status == Operation.Status.PROBLEM:
                tag, problem, category = (
                    "error",
                    _PROBLEM_TEXT.get(
                        operation.problem or Operation.ProblemCause.UNKNOWN, ""
                    ),
                    "problem",
                )
            elif status == Operation.Status.WARNING:
                tag, problem, category = (
                    "warning",
                    _WARNING_TEXT.get(
                        operation.warning or Operation.WarningCause.UNKNOWN, ""
                    ),
                    "warning",
                )
            else:
                # READY, UNKNOWN, EXECUTING
                tag, problem, category = "", "", "ready"

            if category == "complete":
                copied += 1
            elif category == "error":
                errors += 1
            elif category == "warning":
                warnings += 1
            elif category == "problem":
                problems += 1
                
            source = str(operation.source.relative_to(operation.common))
            destination = str(operation.destination.relative_to(operation.common))

            self.tree.insert(
                "",
                "end",
                iid=str(index),
                values=(source, destination, problem),
                tags=(tag,) if tag else (),
            )

        self._show_summary(operations, complete, copied, errors, warnings, problems)

    def show(
        self,
        message: str,
        problem: bool = False,
        warning: bool = False,
        success: bool = False,
    ) -> None:
        self.description_var.set(message)

        if problem:
            self.label.config(background="#ffd5dd")
        elif warning:
            self.label.config(background="#fff7d5")
        elif success:
            self.label.config(background="#d5ffdb")
        else:
            self.label.config(background="")

        if problem or warning:
            self.show_problem_column()
        else:
            self.hide_problem_column()

    def hide_problem_column(self) -> None:
        self.tree.configure(displaycolumns=("source", "destination"))

        half_width = int(self.tree.winfo_width() / 2)
        self.tree.column("source", width=half_width, stretch=True)
        self.tree.column("destination", width=half_width, stretch=True)

    def show_problem_column(self) -> None:
        self.tree.configure(displaycolumns=("source", "destination", "problems"))

        total_width = self.tree.winfo_width()
        self.tree.column("source", width=int(total_width * 0.25), stretch=True)
        self.tree.column("destination", width=int(total_width * 0.25), stretch=True)
        self.tree.column("problems", width=int(total_width * 0.50), stretch=True)

    # Internals

    def _clear_tree(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

    def _show_summary(
        self,
        operations: list[Operation],
        complete: bool,
        copied: int,
        errors: int,
        warnings: int,
        problems: int,
    ) -> None:
        if complete:
            self._show_execution_summary(copied, errors)
        elif problems > 0:
            msg = (
                f"{problems} Datei(en) (markiert rot) enthalten kritische Fehler. "
                "Das Kopieren ist nicht möglich."
            )
            self.show(msg, problem=True)
            ms.showerror("Problem", ".\n".join(msg.split(". ")))
            self.actions.to_copy()
            self.actions.disable()
        elif warnings > 0:
            msg = (
                f"{warnings} Datei(en) (gelb markiert) enthalten unkritische Fehler. "
                "Das Kopieren ist zwar möglich, aber nur eingeschränkt empfohlen."
            )
            self.show(msg, warning=True)
            ms.showwarning("Warnung", ".\n".join(msg.split(". ")))
            self.actions.to_copy()
            self.actions.enable()
        elif len(operations) == 0:
            self.show("")
            self.actions.to_copy()
            self.actions.disable()
        else:
            self.show(
                "Die folgende Dateien werden folgendermassen umbenannt und verschoben:"
            )
            self.actions.to_copy()
            self.actions.enable()

    def _show_execution_summary(self, copied: int, errors: int) -> None:
        if errors > 0:
            msg = (
                f"Die {copied} von {copied + errors} Datei(en) wurden "
                f"erfolgreich verschoben, bei {errors} gibt es Fehler"
            )
            self.show(msg + ":", warning=True)
            ms.showwarning("Warnung", ".\n".join(msg.split(". ")) + ".")
        else:
            msg = (
                f"Die {copied} Datei(en) wurden erfolgreich verschoben, "
                "es gab keine Fehler"
            )
            self.show(msg + ":", success=True)
            ms.showinfo("Erfolg!", ".\n".join(msg.split(". ")) + ".")

        self.actions.to_back()
        self.actions.enable()
