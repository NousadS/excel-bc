# Excel BC `(v1.0.1)`

## Usage

1. **Prepare Controlling Workbook**:

![](docs/pic1.png)
> **Pic. 1**: Example of a controlling workbook

The input file must be a standard `.xlsx` workbook.

The first worksheet must contain the following headers:

|     Header Name    |  Position   |                                 Description                                       |
| ------------------ | ----------- | --------------------------------------------------------------------------------- |
| `folder`           |   One Cell  | The common root directory path where all files reside.                            |
| `initial folder`   |   One Cell  | The subfolder within the root directory where source files are currently located. |
| `file name auto`   |     List    | List of original source file basenames (without extension).                       |
| `file name manual` |     List    | List of target file basenames (without extension).                                |
| `destination`      |     List    | List of relative destination subfolder paths.                                     |

![](docs/pic2.png)
> **Pic. 2**: Chaotic example of the controlling workbook from *Pic. 1*

The headers are case-insensitive and spaces or underscores are allowed, formatting is ignored:

- `file name auto` can be  `file_name_auto`,  `FILE NAME AUTO`,  `File_NAME auto`, etc.

> **Note:** The number of rows for `file name auto`, `file name manual`, and `destination` must match exactly.

![](docs/pic3.png)
> **Pic. 3**: Example of a result of the controlling workbook from *Pic. 1*

2. **Launch the Application**

3. **Select Excel Sheet**: Click **Browse...** to load your `.xlsx` workbook.

4. **Configure File Extension**: Modify the file extension field if necessary (e.g., `.pdf`).

---

## Build Requirements

- **Python 3.10+**
- **Dependencies**: [`requirements.txt`](requirements.txt)
- **Building**: `.\build.bat` => `build/EXCEL.exe`

---

## License

This project is open-source and available under the [Unlicense](https://unlicense.org).
