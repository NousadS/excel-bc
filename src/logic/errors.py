# {name} is not an .xlsx file
class FileWrongExtensionError(Exception):
    def __init__(self, file: str, *args):
        super().__init__(*args)

        self.file: str = file


# {name} does not exist
class WorkbookDoesNotExistError(FileNotFoundError): ...


# The header {name} appears more than once
class HeaderAppearsTwiceError(Exception):
    def __init__(self, header: str, *args):
        super().__init__(*args)

        self.header: str = header


# No value found below the {name} header
class NoHeaderValueError(Exception):
    def __init__(self, header: str, *args):
        super().__init__(*args)

        self.header: str = header


# {folder} does not exist
class CommonFolderNotExistError(FileNotFoundError): ...


# {folder} does not exist
class InitialFolderNotExistError(FileNotFoundError): ...


# Warning of operation ({source} -> {dest}) has not been resolved
class CriticalProblemNotResolvedError(Exception): ...


# Missing header(s) in the workbook:
class MissingHeadersError(Exception):
    def __init__(self, missing: list[str], *args):
        super().__init__(*args)

        self.missing: list[str] = missing


# The amount of file names and destinations aren't equal
class WrongValueAmountsError(Exception):
    def __init__(self, old_files: int, new_files: int, destinations: int, *args):
        super().__init__(*args)

        self.old_files: int = old_files
        self.new_files: int = new_files
        self.destinations: int = destinations
