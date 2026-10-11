from __future__ import annotations

from collections import Counter
from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Final

import openpyxl as xl
from openpyxl.worksheet.worksheet import Worksheet

from .errors import (
    CommonFolderNotExistError,
    CriticalProblemNotResolvedError,
    FileWrongExtensionError,
    HeaderAppearsTwiceError,
    InitialFolderNotExistError,
    MissingHeadersError,
    NoHeaderValueError,
    WorkbookDoesNotExistError,
    WrongValueAmountsError,
)
from .operation import Operation


class State:
    HEADERS: Final[tuple[str, ...]] = (
        "folder",
        "initial folder",
        "filetype",
        "file name auto",
        "file name manual",
        "destination",
    )
    OPTIONAL_HEADERS: Final[tuple[str, ...]] = (
        "filetype",
        "file name auto",
        "file name manual",
        "destination",
    )

    SIMPLE_FIELDS: Final[Mapping[str, str]] = {
        "folder": "common_folder",
        "initial folder": "initial_folder",
        "filetype": "extension",
    }
    LIST_FIELDS: Final[Mapping[str, str]] = {
        "file name auto": "_old_files",
        "file name manual": "_new_files",
        "destination": "_destinations",
    }

    def __init__(self) -> None:
        self.workbook: Path | None = None
        self.worksheet: str | None = None

        self.common_folder: str = ""
        self.initial_folder: str = ""
        self.extension: str = ""

        self.operations: list[Operation] = []

        self._old_files: list[str] = []
        self._new_files: list[str] = []
        self._destinations: list[str] = []

    # Public

    def parse(self, path: str | Path) -> None:
        try:
            self._set_workbook(path)

            with self._with_workbook_columns() as columns:
                positions = self._locate_headers(columns)

                self._require_all_headers(positions)
                self._read_single_fields(columns, positions)
                self._read_list_fields(columns, positions)
                self._require_equal_lengths()

            self._prepare_operations()
        except Exception:
            self.reset()
            raise

    def execute(
        self, on_operation_finished: Callable[[Operation], None] = lambda _: None
    ) -> None:
        if self.deny():
            raise CriticalProblemNotResolvedError()

        for op in self.operations:
            if op.status in (Operation.Status.READY, Operation.Status.WARNING):
                op.execute(on_finished=on_operation_finished)

    def deny(self) -> bool:
        # True if any operation is a blocking PROBLEM.
        return any(op.status == Operation.Status.PROBLEM for op in self.operations)

    def reset(self) -> None:
        self.common_folder = ""
        self.initial_folder = ""
        self.extension = ""
        self._old_files = []
        self._new_files = []
        self._destinations = []
        self.operations = []

    # Workbook loading

    def _set_workbook(self, path: str | Path) -> None:
        candidate = Path(path)

        if not candidate.is_file():
            raise WorkbookDoesNotExistError(str(candidate))

        if candidate.suffix.lower() != ".xlsx":
            raise FileWrongExtensionError(candidate.name)

        self.workbook = candidate

    @contextmanager
    def _with_workbook_columns(self) -> Iterator[list[list[Any]]]:
        if self.workbook is None:
            raise ValueError("Set workbook first!")

        workbook = xl.load_workbook(self.workbook, read_only=True, data_only=True)

        try:
            worksheet: Worksheet = workbook.active  # pyright: ignore[reportAssignmentType]

            columns: list[list[Any]] = []

            for row in worksheet.rows:
                while len(columns) < len(row):
                    columns.append([])

                for column, cell in enumerate(row):
                    columns[column].append(cell.value)

            yield columns
        finally:
            workbook.close()

    # Reading the worksheet

    def _locate_headers(self, columns: list[list[Any]]) -> dict[str, tuple[int, int]]:
        positions: dict[str, tuple[int, int]] = {}

        for col, column in enumerate(columns):
            for row, cell in enumerate(column):
                if cell is None:
                    continue

                normalized = str(cell).strip().replace("_", " ").strip().lower()
                header = normalized if normalized in self.HEADERS else None

                if header is None:
                    continue

                if header in positions:
                    raise HeaderAppearsTwiceError(header)

                positions[header] = (col, row)

        return positions

    def _require_all_headers(self, positions: Mapping[str, tuple[int, int]]) -> None:
        if missing := [h for h in self.HEADERS if h not in positions]:
            raise MissingHeadersError(missing)

    def _read_single_fields(
        self,
        columns: list[list[Any]],
        positions: Mapping[str, tuple[int, int]],
    ) -> None:
        for header, attr in self.SIMPLE_FIELDS.items():
            col, row = positions[header]

            value = None

            column = columns[col]
            next_row = row + 1

            if next_row < len(column) and (v := column[next_row]) is not None:
                value = str(v).strip() or None

            if value is None and header not in self.OPTIONAL_HEADERS:
                raise NoHeaderValueError(header)

            if hasattr(self, attr):
                setattr(self, attr, value or "")
            else:
                raise AttributeError(repr(attr))

    def _read_list_fields(
        self,
        columns: list[list[Any]],
        positions: Mapping[str, tuple[int, int]],
    ) -> None:
        for header, attr in self.LIST_FIELDS.items():
            col, row = positions[header]
            values = []

            for value in columns[col][row + 1 :]:
                if value is None or str(value) == "":
                    break

                values.append(str(value))

            if len(values) == 0 and header not in self.OPTIONAL_HEADERS:
                raise NoHeaderValueError(header)

            if hasattr(self, attr):
                setattr(self, attr, values)
            else:
                raise AttributeError(repr(attr))

    def _require_equal_lengths(self) -> None:
        l_old_files: int = len(self._old_files)
        l_new_files: int = len(self._new_files)
        l_destinations: int = len(self._destinations)

        lengths = {l_old_files, l_new_files, l_destinations}

        if len(lengths) != 1:
            raise WrongValueAmountsError(l_old_files, l_new_files, l_destinations)

    # Operations

    def _prepare_operations(self) -> None:
        common = Path(self.common_folder)
        initial = common / self.initial_folder

        if not common.is_dir():
            raise CommonFolderNotExistError()
        if not initial.is_dir():
            raise InitialFolderNotExistError()

        self.operations = [
            Operation(
                common=common,
                source=initial / f"{old}{self.extension}",
                destination=common / destination / f"{new}{self.extension}",
            )
            for old, new, destination in zip(
                self._old_files, self._new_files, self._destinations
            )
        ]

        self._check_operations()
        self._append_unlisted(common, initial)

    def _check_operations(self) -> None:
        source_counts = Counter(op.source for op in self.operations)
        destination_counts = Counter(op.destination for op in self.operations)

        for op in self.operations:
            op.check()

            if op.status != Operation.Status.READY:
                continue

            if source_counts[op.source] > 1:
                op.status = Operation.Status.PROBLEM
                op.problem = Operation.ProblemCause.SOURCE_DUPLICATE
            elif destination_counts[op.destination] > 1:
                op.status = Operation.Status.PROBLEM
                op.problem = Operation.ProblemCause.DESTINATION_DUPLICATE

    def _append_unlisted(self, common: Path, initial: Path) -> None:
        listed = {op.source for op in self.operations}
        unlisted = sorted(
            f for f in initial.iterdir() if f.is_file() and f not in listed
        )

        for file in unlisted:
            op = Operation(common=common, source=file, destination=common)
            op.check(set_warning=Operation.WarningCause.SOURCE_NOT_INCLUDED)
            self.operations.append(op)
