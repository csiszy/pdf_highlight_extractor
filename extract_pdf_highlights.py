import fitz  # PyMuPDF
import argparse
import sys
import os

def extract_highlights(pdf_path, output_txt_path):
    """
    Extracts highlighted text from a PDF and saves it to a text file,
    ordered by appearance (page number, vertical position, horizontal position).

    Args:
        pdf_path (str): Path to the input PDF file.
        output_txt_path (str): Path to the output text file.
    """
    highlights_data = [] # List to store (page_num, y0, x0, text) tuples for sorting

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF file '{pdf_path}': {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Processing '{pdf_path}'...")
    total_highlights = 0

    for page_num, page in enumerate(doc):
        # Using page.annots() is more efficient for retrieving all annotations
        annots = page.annots(types=[8]) 
        
        if not annots:
            continue # Skip pages with no highlight annotations

        page_highlights = [] # Store highlights for the current page before adding to main list

        for annot in annots:
            # --- Get the bounding box of the annotation ---
            # Highlights can be complex (multiple rectangles for multi-line text)
            # We get the quadrilateral points for each part of the highlight
            quad_points = annot.vertices
            
            if not quad_points: # Skip if vertices are not defined
                continue

            # --- Extract text covered by the highlight ---
            # Combine text from all quads associated with this single annotation
            highlight_text_parts = []
            for i in range(0, len(quad_points), 4):
                # Take the four points defining one quad/rectangle
                quad = quad_points[i:i+4]
                # Convert quad points to a rectangle
                rect = fitz.Quad(quad).rect 
                # Extract text within this specific rectangle
                text = page.get_text("text", clip=rect).strip()
                if text:
                     highlight_text_parts.append(text)
            
            if highlight_text_parts:
                 full_highlight_text = " ".join(highlight_text_parts)
                 # Use the top-left corner of the *first* quad for sorting position
                 # This generally represents the start of the highlight.
                 first_quad_rect = fitz.Quad(quad_points[0:4]).rect
                 y0 = first_quad_rect.y0
                 x0 = first_quad_rect.x0
                 page_highlights.append((page_num, y0, x0, full_highlight_text))
                 total_highlights += 1
        
        # Add highlights from this page to the main list
        highlights_data.extend(page_highlights)


    # --- Sort the highlights based on appearance order ---
    # 1. Page number
    # 2. Vertical position (y0, top coordinate - smaller is higher)
    # 3. Horizontal position (x0, left coordinate - smaller is further left)
    highlights_data.sort(key=lambda item: (item[0], item[1], item[2]))

    # --- Write to output file ---
    try:
        with open(output_txt_path, "w", encoding="utf-8") as outfile:
            if not highlights_data:
                outfile.write("No highlights found in the PDF.\n")
                print("No highlights found.")
            else:
                prev_page = -1
                for page_num, y0, x0, text in highlights_data:
                    # Optional: Add page number markers in the output
                    if page_num != prev_page:
                        outfile.write(f"--- Page {page_num + 1} ---\n\n")
                        prev_page = page_num
                    
                    outfile.write(text)
                    outfile.write("\n\n") # Add blank line for separation

                print(f"Successfully extracted {total_highlights} highlights to '{output_txt_path}'.")

    except IOError as e:
        print(f"Error writing to output file '{output_txt_path}': {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        doc.close() # Ensure the PDF document is closed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract highlighted text from a PDF in order of appearance.")
    parser.add_argument("pdf_file", help="Path to the input PDF file.")
    parser.add_argument("-o", "--output", 
                        help="Path to the output TXT file (default: pdf_filename_highlights.txt)")

    args = parser.parse_args()

    # Determine default output path if not provided
    if args.output:
        output_file = args.output
    else:
        base_name = os.path.splitext(os.path.basename(args.pdf_file))[0]
        output_file = f"{base_name}_highlights.txt"

    # Check if input file exists
    if not os.path.exists(args.pdf_file):
        print(f"Error: Input PDF file not found: '{args.pdf_file}'", file=sys.stderr)
        sys.exit(1)
        
    extract_highlights(args.pdf_file, output_file)