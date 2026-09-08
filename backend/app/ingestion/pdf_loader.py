import pdfplumber


def extract_text_column_aware(page) -> str:
    """
    Detects two side-by-side text columns by checking for a gap in word
    x-positions near the page's horizontal center. If found, reads the
    left column fully top-to-bottom, then the right column fully
    instead of pdfplumber's default line-by-line reading, which zippers
    both columns together. Falls back to normal extraction if no clear
    column gap is found.
    """
    words = page.extract_words()
    if not words:
        return page.extract_text() or ""

    mid = page.width / 2
    words_near_center = [w for w in words if w["x0"] < mid + 20 and w["x1"] > mid - 20]
    is_two_column = len(words_near_center) < len(words) * 0.05

    if not is_two_column:
        return page.extract_text() or ""

    left_words = [w for w in words if w["x0"] < mid]
    right_words = [w for w in words if w["x0"] >= mid]

    def words_to_text(word_list):
        word_list = sorted(word_list, key=lambda w: (round(w["top"] / 3), w["x0"]))
        lines, current_line, last_top = [], [], None
        for w in word_list:
            rounded_top = round(w["top"] / 3)
            if last_top is not None and rounded_top != last_top:
                lines.append(" ".join(current_line))
                current_line = []
            current_line.append(w["text"])
            last_top = rounded_top
        if current_line:
            lines.append(" ".join(current_line))
        return "\n".join(lines)

    return words_to_text(left_words) + "\n\n" + words_to_text(right_words)


def extract_pages_with_tables(pdf_path: str) -> list[dict]:
    pages = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = extract_text_column_aware(page)
            tables = page.extract_tables()

            table_text = []
            for table in tables:
                for row in table:
                    cells = [" ".join((c or "").split()) for c in row]
                    cells = [c for c in cells if c]
                    if cells:
                        table_text.append(" | ".join(cells))

            pages.append({
                "page": i + 1,
                "text": text,
                "table_text": "\n".join(table_text)
            })

    return pages

def is_likely_duplicate(table_text: str, page_text: str, threshold: float = 0.5) -> bool:
    table_words = set(table_text.lower().split())
    if not table_words:
        return False
    page_words = set(page_text.lower().split())
    overlap_ratio = len(table_words & page_words) / len(table_words)
    return overlap_ratio > threshold


def build_page_documents(pdf_path: str) -> list[dict]:
    pages = extract_pages_with_tables(pdf_path)
    docs = []
    for page in pages:
        text = page["text"]
        if page["table_text"] and not is_likely_duplicate(page["table_text"], text):
            text += "\n\n" + page["table_text"]
        docs.append({"page": page["page"], "text": text})
    return docs