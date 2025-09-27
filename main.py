import os
import re
import sys
from fpdf import FPDF

# Folders to ignore
IGNORE_FOLDERS = {
    'node_modules', 'venv', '.git', '__pycache__',
    '.idea', '.vscode', 'dist', 'build', 'data'
}

# Supported file extensions
SUPPORTED_EXTENSIONS = {
    '.txt', '.json', '.js', '.ts', '.py', '.env',
    '.gitignore', '.dockerignore', '.dockerfile', '.css',
    '.html', '.ejs', '.md', '.yml', '.yaml', '.sh'
}


def remove_non_latin1(text: str) -> str:
    """Remove characters that cannot be encoded in Latin-1."""
    return text.encode('latin-1', 'ignore').decode('latin-1')


# PDF class
class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.set_font("Courier", size=10)

    def add_title(self, title: str):
        self.set_font("Courier", "B", 12)
        self.cell(0, 10, title, ln=True)
        self.set_font("Courier", size=10)

    def add_code(self, code: str):
        for line in code.splitlines():
            self.multi_cell(0, 5, line)


def export_folder_to_pdf(root_path: str):
    """Export a project folder into a single PDF file."""
    # Clean up quotes from CLI input
    root_path = root_path.strip("\"'")

    # Build safe PDF file name
    pdf_name = os.path.basename(os.path.abspath(root_path))
    pdf_name = re.sub(r'[\\/*?:"<>|]', "_", pdf_name) + ".pdf"

    # Ensure ./pdfs/ exists
    output_dir = os.path.join(os.getcwd(), "pdfs")
    os.makedirs(output_dir, exist_ok=True)

    pdf_path = os.path.join(output_dir, pdf_name)

    pdf = PDF()
    pdf.add_title(f"Project structure: {root_path}")

    for current_root, folders, files in os.walk(root_path):
        # Ignore unwanted folders
        folders[:] = [f for f in folders if f not in IGNORE_FOLDERS]

        level = current_root.replace(root_path, '').count(os.sep)
        indent = ' ' * 4 * level
        pdf.add_title(f"{indent}[{os.path.basename(current_root)}/]")

        for file in files:
            full_path = os.path.join(current_root, file)
            extension = os.path.splitext(file)[1].lower()

            if extension in SUPPORTED_EXTENSIONS or file.startswith('.'):
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        content = remove_non_latin1(content)
                    relative_path = os.path.relpath(full_path, root_path)
                    pdf.add_title(f"{indent}    {relative_path}")
                    pdf.add_code(content)
                except Exception as e:
                    pdf.add_title(f"{indent}    {file} (error reading: {e})")

    pdf.output(pdf_path)
    print(f"✅ PDF generated successfully: {pdf_path}")


# CLI entrypoint
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <folder_path>")
        sys.exit(1)
    export_folder_to_pdf(sys.argv[1])
