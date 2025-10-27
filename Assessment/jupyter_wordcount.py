import json
import sys
import re

def count_words_in_markdown_cells(notebook_path):
    """Count words in markdown cells of a Jupyter notebook."""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{notebook_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: File '{notebook_path}' is not a valid JSON notebook.")
        sys.exit(1)

    total_words = 0

    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "markdown":
            # Join all source lines into one string
            text = "".join(cell.get("source", []))
            # Remove code snippets, LaTeX, and links to get a cleaner word count
            text = re.sub(r'`[^`]*`', '', text)        # remove inline code
            text = re.sub(r'\$\$.*?\$\$', '', text)    # remove LaTeX blocks
            text = re.sub(r'\$.*?\$', '', text)        # remove inline LaTeX
            text = re.sub(r'\[.*?\]\(.*?\)', '', text) # remove markdown links
            words = re.findall(r'\b\w+\b', text)
            total_words += len(words)

    return total_words


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python count_markdown_words.py <notebook.ipynb>")
        sys.exit(1)

    notebook_path = sys.argv[1]
    word_count = count_words_in_markdown_cells(notebook_path)
    print(f"Total words in markdown cells: {word_count}")
