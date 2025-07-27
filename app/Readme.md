# PDF Heading Extractor

## Approach
Uses PyMuPDF to analyze fonts and extract headings based on relative size and boldness. Maps larger, bolder fonts to H1–H4 and identifies a title on the first page.

## Run Instructions
```sh
docker build --platform linux/amd64 -t mysolutionname:tag .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none mysolutionname:tag
```

## Dependencies
- PyMuPDF (fitz) for parsing PDFs.

## Model/Size
- No ML model used (no downloads, < 10MB image overhead)
- Offline compatible
