# PDF Highlight Extractor

A Python script to extract highlighted text annotations from a PDF file and save them to a text file, ordered by their appearance in the document (page number, top-to-bottom, left-to-right).

## Features

*   Extracts text specifically covered by highlight annotations.
*   Handles multi-line highlights.
*   Sorts extracted highlights based on their position in the PDF:
    1.  Page Number
    2.  Vertical Position (top-to-bottom)
    3.  Horizontal Position (left-to-right)
*   Outputs the extracted text to a `.txt` file.
*   Includes optional page number markers in the output file for clarity.
*   Command-line interface for easy use.

## Requirements

*   Python 3.6+
*   PyMuPDF library

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/csiszy/pdf_highlight_extractor.git
    cd pdf_highlight_extractor 
    ```

2.  **Install dependencies:**
    It's recommended to use a virtual environment:
    ```bash
    # Create a virtual environment (optional but recommended)
    python -m venv venv 
    # Activate it (Linux/macOS)
    source venv/bin/activate 
    # Or (Windows)
    .\venv\Scripts\activate 

    # Install required packages
    pip install -r requirements.txt 
    ```

## How to Use

Run the script from your terminal, providing the path to the input PDF file.

**Basic Usage:**

```bash
python extract_pdf_highlights.py "path/to/your/document.pdf"
