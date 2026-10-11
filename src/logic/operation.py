import shutil
from collections.abc import Callable
from enum import StrEnum, auto
from pathlib import Path
from threading import Thread


def _valid_windows_path(path: Path) -> bool:
    # Used `or` because it stops to check after one `True`
    return not (
        any(c in '<>:"/\\|?*' for c in path.name)
        or path.name.endswith((" ", "."))
        or path.stem
        in (
            "CON",
            "PRN",
            "AUX",
            "NUL",
            "COM1",
            "COM2",
            "COM3",
            "COM4",
            "COM5",
            "COM6",
            "COM7",
            "COM8",
            "COM9",
            "LPT1",
            "LPT2",
            "LPT3",
            "LPT4",
            "LPT5",
            "LPT6",
            "LPT7",
            "LPT8",
            "LPT9",
        )
    )


class Operation:
    class Status(StrEnum):
        # Pre-checking
        UNKNOWN = auto()  # Preparing or actually unknown

        # Post-checking / Pre-executing
        READY = auto()  # Ready to be executed
        WARNING = auto()  # Warning, ready to be executed
        PROBLEM = auto()  # Problem, can't be executed

        EXECUTING = auto()

        # Post-executing
        COMPLETED = auto()  # Completed without errors
        FAILED = auto()  # Failed due some errors

    class WarningCause(StrEnum):
        UNKNOWN = auto()

        SOURCE_DOES_NOT_EXIST = auto() # Source file does not exist. (Isn't a error intentionally)
        SOURCE_NOT_INCLUDED = auto() # Source file isn't included into the controlling workbook

    class ProblemCause(StrEnum):
        UNKNOWN = auto()

        SOURCE_DUPLICATE = auto() # Source duplicates in the workbook

        DESTINATION_ALREADY_EXISTS = auto() # Destination file exists already
        DESTINATION_FOLDER_DOES_NOT_EXIST = auto() # Destination's parent folder doesn't exist (Isn't a warning intentionally)
        DESTINATION_NAME_TOO_LONG = auto() # Destination's name is too long (255 for safety)
        DESTINATION_INVALID_NAME = auto() # Destination's name isn't valid Windows name
        DESTINATION_DUPLICATE = auto() # Destination duplicates in the workbook

    def __init__(self, common: Path, source: Path, destination: Path):
        self.common: Path = common
        self.source: Path = source
        self.destination: Path = destination

        self.status: Operation.Status = Operation.Status.UNKNOWN
        self.warning: Operation.WarningCause | None = None
        self.problem: Operation.ProblemCause | None = None
        self.comment: str = ""

    def reset(self) -> None:
        self.status = Operation.Status.UNKNOWN
        self.warning = None
        self.problem = None
        self.comment = ""

    def check(self, set_warning: "Operation.WarningCause | None" = None) -> None:
        if self.status not in [
            Operation.Status.UNKNOWN,
            Operation.Status.READY,
            Operation.Status.WARNING,
            Operation.Status.PROBLEM,
        ]:
            raise ValueError(
                "The operation is being executing or was already executed, please use .reset() before rechecking."
            )

        self.status = Operation.Status.READY
        self.warning = None
        self.problem = None
        self.comment = ""

        if set_warning is not None:
            self.status = Operation.Status.WARNING
            self.warning = set_warning

        elif not self.source.exists():
            self.status = Operation.Status.WARNING
            self.warning = Operation.WarningCause.SOURCE_DOES_NOT_EXIST

        elif self.destination.exists():
            self.status = Operation.Status.PROBLEM
            self.problem = Operation.ProblemCause.DESTINATION_ALREADY_EXISTS

        elif not self.destination.parent.exists():
            self.status = Operation.Status.PROBLEM
            self.problem = Operation.ProblemCause.DESTINATION_FOLDER_DOES_NOT_EXIST

        elif len(str(self.destination.absolute())) >= 255:
            self.status = Operation.Status.PROBLEM
            self.problem = Operation.ProblemCause.DESTINATION_NAME_TOO_LONG

        elif not _valid_windows_path(self.destination):
            self.status = Operation.Status.PROBLEM
            self.problem = Operation.ProblemCause.DESTINATION_INVALID_NAME

    def execute(self, on_finished: Callable[["Operation"], None]) -> Thread:
        if self.status == Operation.Status.UNKNOWN:
            raise ValueError("Check before executing!")
        if self.status == Operation.Status.PROBLEM:
            raise ValueError(
                "Operation cannot be executed, because status is 'PROBLEM'. Recheck or reset the operation before executing!"
            )
        if self.status == Operation.Status.EXECUTING:
            raise ValueError("Operation is being executed. Wait!")
        if self.status in [Operation.Status.COMPLETED, Operation.Status.FAILED]:
            raise ValueError("Operation has been already executed. Please reset!")

        def thread() -> None:
            self.status = Operation.Status.EXECUTING
            self.warning = None
            self.problem = None
            self.comment = ""

            try:
                shutil.copy2(self.source, self.destination)

                self.status = Operation.Status.COMPLETED
            except Exception as exc:  # noqa: BLE001
                self.status = Operation.Status.FAILED
                self.comment = str(exc)
                if self.comment == "":
                    self.comment = repr(exc)

            on_finished(self)

        t: Thread = Thread(target=thread)
        t.start()
        t.join()  # For future

        return t

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Operation):
            return NotImplemented
        return self.source == other.source and self.destination == other.destination
