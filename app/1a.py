import os
import fitz  # PyMuPDF
import json
from collections import defaultdict

def is_bold(span):
    return "bold" in span.get("font", "").lower() or (span["flags"] & 16)

def extract_headings(pdf_path):
    doc = fitz.open(pdf_path)

    font_counts = defaultdict(int)
    font_styles = {}

    for page in doc:
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if not text:
                        continue
                    size = round(span["size"], 1)
                    font_counts[size] += 1
                    if size not in font_styles:
                        font_styles[size] = is_bold(span)

    body_size = max(font_counts.items(), key=lambda x: x[1])[0]
    sorted_sizes = sorted(font_counts.keys(), reverse=True)

    font_level_map = {}
    level = 1
    for fs in sorted_sizes:
        if fs > body_size and font_styles.get(fs, False):
            font_level_map[fs] = f"H{level}"
            level += 1
        if level > 4:
            break

    title = ""
    first_page = doc[0]
    spans = [
        (span["text"].strip(), round(span["size"], 1), is_bold(span))
        for block in first_page.get_text("dict")["blocks"]
        for line in block.get("lines", [])
        for span in line.get("spans", [])
        if span["text"].strip()
    ]
    if spans:
        title_candidate = max(spans, key=lambda x: x[1] if x[2] else 0)
        title = title_candidate[0] if title_candidate[2] else ""

    headings = []
    for page_num, page in enumerate(doc):
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                text = ""
                sizes = []
                bolds = []
                for span in line.get("spans", []):
                    span_text = span["text"].strip()
                    if not span_text:
                        continue
                    text += span_text + " "
                    sizes.append(round(span["size"], 1))
                    bolds.append(is_bold(span))
                text = text.strip()
                if not text:
                    continue
                avg_size = round(sum(sizes) / len(sizes), 1)
                is_line_bold = all(bolds)

                if avg_size in font_level_map and is_line_bold:
                    headings.append({
                        "level": font_level_map[avg_size],
                        "text": text,
                        "page": page_num
                    })

    return {"title": title.strip(), "outline": headings}

def main():
    input_dir = "input"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    for file in os.listdir(input_dir):
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, file)
            result = extract_headings(pdf_path)
            out_file = os.path.splitext(file)[0] + ".json"
            with open(os.path.join(output_dir, out_file), "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
  

if __name__ == "__main__":
    main()

