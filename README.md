

````markdown
# 📄 Adobe India Hackathon 2025 – Round 1A

This repository contains the submission for **Round 1A** of the Adobe India Hackathon 2025. The goal of this round is to build a **PDF outline extraction system** that intelligently identifies section headings from academic PDFs.

---

## 🧠 Problem Statement

Given an academic or research-style PDF, identify **structural outlines** such as:

- Section and Subsection headings
- Page locations
- Semantic hierarchy (`H1`, `H2`, etc.)

This helps downstream tasks such as question answering, content navigation, and summarization.

---

## 🧰 Tools & Libraries

- `PyMuPDF` (`fitz`) – PDF parsing
- `re` / `string` – Title heuristics
- `json` – Structured output
- Built-in rules for section style detection

---

## 📁 Folder Structure

```bash
.
├── extractor.py             # Main extraction script
├── Dockerfile               # Docker config for reproducibility
├── input/
│   └── sample1.pdf          # Input academic-style PDF
├── output/
│   └── sample1.json         # Extracted outline in JSON format
└── README.md                # This file
````

---

## 🔄 Pipeline Overview

### 🔹 `extractor.py`

1. Loads PDF using `PyMuPDF`
2. Iterates through each page to:

   * Detect headings based on font size, boldness, spacing
   * Clean and normalize text
3. Applies hierarchy tagging (`H1`, `H2`, etc.)
4. Outputs a JSON outline like:

### 📄 Sample Output: `sample1.json`

```json
{
  "title": "Sentiment Analysis of Journals to Measure Meditation Effects on Emotional Well-being",
  "outline": [
    { "level": "H1", "text": "Abstract", "page": 1 },
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H1", "text": "Literature Review", "page": 2 },
    { "level": "H1", "text": "Methodology", "page": 4 },
    { "level": "H1", "text": "Results", "page": 5 },
    { "level": "H1", "text": "Conclusion", "page": 9 },
    { "level": "H1", "text": "References", "page": 10 }
  ]
}
```

---

## 🐳 Dockerized Usage

### 1. Build Docker Image

```bash
docker build -t adobe-outline .
```

### 2. Run Extraction

```bash
docker run --rm ^
  -v "%cd%/input:/app/input" ^
  -v "%cd%/output:/app/output" ^
  --network none adobe-outline
```

✅ Output will be saved in `output/sample1.json`.

---

## 👨‍💻 Author

**SRAVANTHI**
GitHub: [@sravanthi937](https://github.com/sravanthi937)
Submission for Adobe India Hackathon 2025 – Round 1A

---


## 📝 Notes

* Works offline — no internet required
* Designed to generalize across multiple paper formats
* Fast and lightweight (runs in seconds per PDF)


