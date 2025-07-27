# PDF Heading Extractor

Here’s a more detailed and polished version of the **Approach** section for your `README.md`, clearly describing the method used to extract headings from PDFs:

---

## Approach

This solution uses **PyMuPDF (fitz)** to parse and analyze the structural text properties of a PDF, without relying on any machine learning models. The extraction of headings is performed based on **font size** and **boldness**, using the following heuristic pipeline:

### 1. **Font Statistics Collection**

* For each span (smallest text unit) on every page, the system collects:

  * Font size (rounded)
  * Font name
  * Boldness flag (`span["flags"] & 16` or if "bold" is in the font name)
* It tallies the frequency of each font size across the document to identify the most common (body) font size.

###  2. **Heading Level Mapping**

* Font sizes **larger than the body font size** and **bold** are considered as potential headings.
* These are mapped hierarchically to heading levels `H1` through `H4`, depending on relative font size.

### 3. **Title Identification**

* On the **first page**, spans are examined to find the **largest bold text** — this is assumed to be the document title.

### 4. **Heading Extraction**

* Every line is analyzed:

  * If its average font size matches a known heading level (from step 2) **and** it's bold, it's added as a heading.
  * Each heading includes its `level` (H1–H4), `text`, and `page` number.

### 5. **Output**

* The output is a JSON file for each input PDF, containing:

  * `"title"`: The inferred document title
  * `"outline"`: A list of extracted headings with levels and page locations

---

This method avoids model downloads, runs fully **offline**, and supports lightweight deployments (<10MB Docker image overhead). It provides robust heuristic-based extraction suitable for structured PDFs.


## Run Instructions
```sh
docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none mysolutionname:somerandomidentifier
```

## Dependencies
- PyMuPDF (fitz) for parsing PDFs.

## Model/Size
- No ML model used (no downloads, < 10MB image overhead)
- Offline compatible
