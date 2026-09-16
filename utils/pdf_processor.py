from pathlib import Path
import pymupdf


ALLOWED_EXTENSIONS = {".pdf"}


def extract_text_from_pdf(file_path):

    path = Path(file_path)

    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError("Only PDF files are supported.")

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {path}"
        )

    pages = []

    with pymupdf.open(path) as document:

        for page in document:
            pages.append(page.get_text())

    text = "\n".join(pages).strip()

    if not text:
        raise ValueError(
            "No selectable text found in PDF."
        )

    return text