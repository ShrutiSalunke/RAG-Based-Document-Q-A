import logging
import pdfplumber
 
logger = logging.getLogger(__name__)
 
 
def extract_pages(file_path: str) -> list[tuple[int, str]]:
    """
    Returns a list of (page_number, page_text) tuples, 1-indexed.
    Pages with no extractable text (e.g. pure-image scans) are skipped.
    """
    pages: list[tuple[int, str]] = []
 
    with pdfplumber.open(file_path) as pdf:
        for index, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            text = text.strip()
            if text:
                pages.append((index, text))
            else:
                logger.warning(
                    "Page %s of %s produced no extractable text "
                    "(likely a scanned image page).",
                    index,
                    file_path,
                )
 
    if not pages:
        raise ValueError(
            "No extractable text found in this PDF. Scanned/image-only "
            "PDFs are not supported in Phase 2 (OCR is out of scope)."
        )
 
    return pages
 
 
def get_page_count(file_path: str) -> int:
    with pdfplumber.open(file_path) as pdf:
        return len(pdf.pages)
