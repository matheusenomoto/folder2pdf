# Folder2PDF
![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)

![fpdf2](https://img.shields.io/badge/fpdf2-2C5BB4?style=for-the-badge)

![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white) ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)


![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)

Export an entire project folder (structure + file contents) into a single PDF. Works on Windows and Linux. Automatically strips characters not supported by the default PDF font to avoid encoding issues.

---

## Features
- Preserves the folder tree in the PDF, with per-file headings.
- Ignores common heavy/system folders by default (`node_modules`, `venv`, `.git`, `__pycache__`, etc.).
- Supports many common text/code formats.
- Safely handles file/dir names for a valid output filename.
- Outputs to ./pdfs/<project-name>.pdf (auto-created).

---

## Supported extensions
- .txt, .json, .js, .ts, .py, .env  
- .gitignore, .dockerignore  
- .css, .html, .ejs, .md  
- .yml, .yaml, .sh

Notes:
- Hidden files (starting with .) are included.
- Files without extensions like Dockerfile or Makefile are not included by default; see “Customize” below if you want them.

---

## Requirements
- Python 3.11+
- fpdf2 (Python library)

Install dependencies:
```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Usage
```sh
python main.py <folder_path>
```

Example:
```sh
python main.py ~/projects/my-app
# ✅ PDF generated successfully: /current/dir/pdfs/my-app.pdf
```

Tips:
- On Windows, wrap paths with spaces in quotes: "C:\path with spaces\project".
- Very large repos can create big PDFs; consider pruning or adding more ignore rules.

---

## Customize
- Ignore folders: edit IGNORE_FOLDERS in main.py.
- File types: edit SUPPORTED_EXTENSIONS (add, e.g., ".toml", ".xml").
- Include special filenames (no extension), e.g. Dockerfile:
  - Add a check in the loop for exact filenames and include them.
- Keep all UTF-8 characters: fpdf2’s core fonts are Latin-1. To keep full Unicode, add a TTF font:
  ```python
  pdf = PDF()
  pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
  pdf.set_font("DejaVu", size=10)
  ```
  Then remove the remove_non_latin1 call.

---

## Troubleshooting
- Permission errors: run from a directory where you can create ./pdfs.
- Empty PDF sections: ensure files are text-based and readable (opened with utf-8 + errors='ignore').
- Output not found: the tool prints the full path on success; check terminal output.

---

## License
This project is licensed under the GNU General Public License v3.0 (GPL-3.0).  
You may use, copy, and modify the software, but any distributed modifications or derivative works must also be licensed under GPL-3.0, ensuring the changes remain open to everyone.

- SPDX-License-Identifier: GPL-3.0-or-later  
- Full text: https://www.gnu.org/licenses/gpl-3.0.en.html {target="_blank"}