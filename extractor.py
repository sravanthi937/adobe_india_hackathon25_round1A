import os
import fitz  # PyMuPDF
import json

class PDFOutlineExtractor:
    def __init__(self, pdf_path):
        self.doc = fitz.open(pdf_path)
        self.filename = os.path.basename(pdf_path)
        self.title = ""
        self.outline = []
        self.heading_keywords = {"abstract", "introduction", "methodology", "results", "discussion", "conclusion", "references", "literature review"}

    def extract(self):
        self._extract_title()
        self._extract_headings()
        return {
            "title": self.title.strip(),
            "outline": self.outline
        }

    def _extract_title(self):
        page = self.doc[0]
        spans = self._get_spans(page)
        title_spans = sorted(spans, key=lambda x: -x['size'])[:2]
        self.title = " ".join([span['text'].strip() for span in title_spans])

    def _extract_headings(self):
        font_stats = self._collect_font_stats()
        max_font = font_stats['max']
        avg_font = font_stats['avg']

        for page_num, page in enumerate(self.doc):
            spans = self._get_spans(page)
            for span in spans:
                text = span['text'].strip()
                if not text or len(text) > 120 or len(text.split()) > 15:
                    continue

                size = span['size']
                is_bold = (span['flags'] & 2) != 0
                fontname = span.get('font', '').lower()
                lowercase_text = text.lower().rstrip(":")

                level = None

                # 📌 Rule 1: Keyword override (increase recall)
                if lowercase_text in self.heading_keywords:
                    level = "H1"

                # 📌 Rule 2: Font-size-based fallback
                elif size >= max_font * 0.9:
                    level = "H1"
                elif size >= avg_font * 1.2:
                    level = "H2"
                elif size >= avg_font * 1.05 and is_bold:
                    level = "H3"

                if level:
                    self.outline.append({
                        "level": level,
                        "text": text,
                        "page": page_num + 1
                    })

    def _collect_font_stats(self):
        sizes = []
        for page in self.doc:
            spans = self._get_spans(page)
            for span in spans:
                if span['text'].strip():
                    sizes.append(span['size'])
        return {
            "max": max(sizes),
            "avg": sum(sizes) / len(sizes)
        }

    def _get_spans(self, page):
        spans = []
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    spans.append(span)
        return spans


def process_all_pdfs(input_dir="input", output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            print(f"📘 Processing: {filename}")
            extractor = PDFOutlineExtractor(pdf_path)
            result = extractor.extract()
            json_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved to: {json_path}")

if __name__ == "__main__":
    process_all_pdfs()
