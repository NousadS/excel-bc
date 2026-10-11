# ExBC `(v2.0.0)`

## Table of contents

- [Usage](#usage)
  - [1. Prepare Controlling Workbook](#1-prepare-controlling-workbook)
  - [2. Load Controlling Workbook](#2-load-controlling-workbook)
  - [3. Errors while loading a workbook](#3-errors-while-loading-a-workbook)
  - [4. Operation Warnings and Problems](#4-operation-warnings-and-problems)
- [Development](#development)
  - [1. Build Requirements](#1-build-requirements)
  - [2. Source code](#2-source-code)
- [License](#license)
  
## Usage

### 1. Prepare Controlling Workbook

![Example of a standard, neatly arranged controlling workbook](docs/pictures/excel-examples/normal.png)
> **Pic. 1**: Example of a standard, neatly arranged controlling workbook

To get started, create a standard `.xlsx` Excel file as a **controlling workbook**.

![The app reads the currently selected or active worksheet (blue), while unselected worksheets (orange) are ignored](docs/pictures/chosen.png)
> **Pic. 2**: The app reads the currently selected or active worksheet *(blue)*, while unselected worksheets *(orange)* are ignored

Your active (selected) worksheet should include these essential headers:

|             Header             |      Type      |                                    Description                                    |
| :----------------------------- | :------------: | --------------------------------------------------------------------------------- |
| `Folder`                       |  Single Cell   | The common root directory path where all files are stored.                        |
| `Initial Folder`               |  Single Cell   | The subfolder within the root directory where source files are currently located. |
| `Filetype` <sub>optional</sub> |  Single Cell   | Filetype like `.pdf` for all source and destination files.                        |
| `File Name Auto`               |      List      | List of original source file basenames.                                           |
| `File Name Manual`             |      List      | List of target file basenames.                                                    |
| `Destination`                  |      List      | List of relative destination subfolder paths.                                     |

> [!TIP]
> Headers are case-insensitive; spaces or underscores are allowed, and formatting is ignored. For example:
> `File Name Auto` can be `file_name_auto`, `FILE NAME AUTO`, `File_NAME auto`, etc.

> [!IMPORTANT]
> The number of rows for `File Name Auto`, `File Name Manual`, and `Destination` must match exactly.

![An example of a chaotic workbook which is equal to the one from Pic. 1. The app can still read it just fine as long as the necessary headers and values are present](docs/pictures/excel-examples/chaotic.png)
> **Pic. 3**: An example of a chaotic workbook which is equal to the one from *Pic. 1*. The app can still read it just fine as long as the necessary headers and values are present

---

### 2. Load Controlling Workbook

---

<img src="docs/pictures/steps/step1.png" alt="Freshly Launched App" width="315" align="right" />

1. **Launch Application**

   <br>
   <br>
   <br>
   <br>
   <br>
   <br>
   <br>
   <br>

   > **Pic. 4**: **Freshly Launched App.** Ready to select a controlling workbook

---

<img src="docs/pictures/steps/step2.png" alt="Loaded State with Warnings" width="315" align="right" />

2. **Select Workbook**
   Click **Browse...** to load your `.xlsx` workbook. 
   Once loaded, the app displays any warnings or notices directly in the user interface if something requires your attention.
   See error descriptions under [3. Errors while loading a workbook](#3-errors-while-loading-a-workbook) and [4. Operation Warnings and Problems](#4-operation-warnings-and-problems).

   <br>
   <br>
   <br>
   <br>
   <br>

   > **Pic. 5**: **Loaded State with Warnings**

---

<img src="docs/pictures/steps/step3.png" alt="Execution Results" width="315" align="right" />

3. **Copy Files**
   Click **Copy files** to execute the copying process.
   The outcome of the process will be displayed, including file-specific errors or successful transfers.

   <img src="docs/pictures/result/problems.png" alt="Execution results with file errors" width="315" />
   <img src="docs/pictures/result/success.png" alt="Successful execution results" width="315" />

   > **Execution results with file errors** ⁕ **Successful execution results**

   <br>

   > **Pic. 6**: **Execution Results**

---

<img src="docs/pictures/steps/step4.png" alt="Example of an application state after clicking the Back button" width="315" align="right" />

4. **Click 'Back'**
   Clicking **Back** returns you to the initial starting state. 
   The file path of the workbook is preserved, so you can simply click **Reload** to refresh your data.

   <br>
   <br>
   <br>
   <br>
   <br>
   <br>

   > **Pic. 7**: State after clicking the **Back** button

---

### 3. Errors while loading a workbook

<img src="docs/pictures/errors/file-not-found.png" alt="The Excel file 'Beispiel.xlsx' was not found." width="315" align="left" />

#### `The Excel file 'Beispiel.xlsx' was not found.`

**Cause:** The specified workbook file path does not exist. \
**Solution:** Check the file path and ensure the file exists before loading.

<br>

---

<img src="docs/pictures/errors/invalid-format.png" alt="The file 'Beispiel.xlsx' does not have a valid format. Please choose an .xlsx file." width="315" align="left" />

#### `The file 'Beispiel.xlsx' does not have a valid format. Please choose an .xlsx file.`

**Cause:** The selected file is not an Excel workbook with the `.xlsx` extension. \
**Solution:** Select a valid `.xlsx` file.

<br>

---

<img src="docs/pictures/errors/common-folder-not-found.png" alt="The specified main folder (Common Folder) does not exist. ..." width="315" align="left" />

#### `The specified main folder (Common Folder) does not exist. ...`

**Cause:** The root directory path defined in the `Folder` cell does not exist on disk. \
**Solution:** Correct the root folder path in the workbook and reload it.

<br>

---

<img src="docs/pictures/errors/initial-folder-not-found.png" alt="The specified source folder (Initial Folder) does not exist. ..." width="315" align="left" />

#### `The specified source folder (Initial Folder) does not exist. ...`

**Cause:** The subfolder defined in the `Initial Folder` cell does not exist within the root directory. \
**Solution:** Correct the source subfolder path in the workbook and reload it.

<br>

---

<img src="docs/pictures/errors/header-twice.png" alt="The header 'Beispiel' appears multiple times in the table. ..." width="315" align="left" />

#### `The header 'Beispiel' appears multiple times in the table. ...`

**Cause:** A required header (e.g., `Folder`, `Destination`) appears more than once in the active worksheet. \
**Solution:** Remove duplicate headers in your Excel sheet, save the file, and click **Reload**.

<br>

---

<img src="docs/pictures/errors/value-not-found.png" alt="No valid value was found under the header 'Beispiel'. ..." width="315" align="left" />

#### `No valid value was found under the header 'Beispiel'. ...`

**Cause:** A required header contains no value or list items underneath it. \
**Solution:** Fill in the missing values or rows below the header in Excel and reload.

<br>

---

<img src="docs/pictures/errors/missing-headers.png" alt="The following necessary headers are missing in the table: ..." width="315" align="left" />

#### `The following necessary headers are missing in the table: ...`

**Cause:** One or more required headers (`Folder`, `Initial Folder`, `File Name Auto`, `File Name Manual`, `Destination`) are missing. \
**Solution:** Add the missing column headers to your worksheet and reload.

<br>

---

<img src="docs/pictures/errors/wrong-value-amounts.png" alt="The number of values does not match\n(Old files: X, New files: Y, Target folders: Z). ..." width="315" align="left" />

#### `The number of values does not match\n(Old files: X, New files: Y, Target folders: Z). ...`

**Cause:** The row counts for the `File Name Auto`, `File Name Manual`, and `Destination` lists are unequal. \
**Solution:** Ensure all three list columns have the same number of populated rows.

<br>

### 4. Operation Warnings and Problems

When operations are checked, individual file rows may be flagged as warnings or blocking problems.

<img src="docs/pictures/all-problems.png" alt="All problems and warnings" width="600" align="center" />

**Warnings** are marked yellow and **do not block** copying, although executing with warnings is discouraged.
**Problems** are marked red and **do block** copying.

---

#### Warning: `The source file was not found.`

**Description:** The source file was not found.
**Solution:** Ensure the source file exists in the specified source folder.

---

#### Warning: `The source file exists in the source folder, but is missing in the controlling table.`

**Description:** The source file exists in the source folder, but is missing in the controlling table.
**Solution:** Add the file to your controlling table if it needs to be processed, or ignore this if intentional.

---

#### Problem: `This source file is listed multiple times in the controlling table.`

**Description:** This source file is listed multiple times in the controlling table.
**Solution:** Remove duplicate entries of the same source file from the workbook.

---

#### Problem: `The target file already exists.`

**Description:** The target file already exists.
**Solution:** Change the target name or remove the existing file at the destination path.

---

#### Problem: `The parent folder of the target file does not exist.`

**Description:** The parent folder of the target file does not exist.
**Solution:** Create the target subfolder within the root directory.

---

#### Problem: `The name of the target file is too long. Windows might block this operation.`

**Description:** The target file name is too long. Windows might block this operation.
**Solution:** Shorten the target file name or path so the total length is under 255 characters.

---

#### Problem: `The name of the target file contains invalid characters that are not allowed by Windows.`

**Description:** The target file name contains invalid characters that are not allowed by Windows.
**Solution:** Remove invalid Windows filename characters (`<`, `>`, `:`, `"`, `/`, `\`, `|`, `?`, `*`) or reserved device names (`CON`, `AUX`, etc.).

---

#### Problem: `This destination path is already used by another file in the table.`

**Description:** This destination path is already used by another file in the table.
**Solution:** Ensure each row specifies a unique destination path.

---

## Development

### 1. Build Requirements

- **Python 3.11+**
- **Dependencies**: [`requirements.txt`](requirements.txt)
- **Building**: `.\build.bat` => `build/ExBC-vX.X.X-win-x64.exe`

The build process is performed by *PyInstaller*.

### 2. Source code

**UI ([`interface/`](src/interface/)):**

- [`action.py`](src/interface/action.py): Bottom action buttons (`Credits`, `Help`, `Copy/Back`, `Quit`)
- [`file.py`](src/interface/file.py): Managing workbook path display, file selection, and reloading (`Choose`, `Reload`)
- [`info.py`](src/interface/info.py): Displaying active file types and information on the common root folder (`Common Folder`, `Filetype`)
- [`operations.py`](src/interface/operations.py): Displaying source, destination, and warning/problem details, also controls the `ActionsFrame` and shows message dialogs

**Logic ([`logic/`](src/logic/)):**

- [`errors.py`](src/logic/errors.py): Custom exceptions for interactions between UI and logic
- [`operation.py`](src/logic/operation.py): Single operation unit
- [`state.py`](src/logic/state.py): Full state and parsing of the workbook


**[`main.py`](src/main.py) - Entry point + Main class of the Tkinter application**

---

## License

This project is open-source and available under the [Unlicense](https://unlicense.org).
Additional credits can be found under [CREDITS](CREDITS).