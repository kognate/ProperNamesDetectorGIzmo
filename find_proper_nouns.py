#!/usr/bin/env python3
"""
Find and report locations of proper nouns in a text file.

This script uses spaCy's NER to identify proper nouns and reports their
locations (line and column numbers) in the input file.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Tuple

import spacy


def load_spacy_model(model_name: str = "en_core_web_lg"):
    """Load spaCy language model, downloading if necessary."""
    try:
        nlp = spacy.load(model_name)
        return nlp
    except OSError:
        print(f"Error: spaCy model '{model_name}' not found.", file=sys.stderr)
        print(f"Download it with: python -m spacy download {model_name}", file=sys.stderr)
        sys.exit(1)


def find_proper_nouns(file_path: str) -> List[Tuple[str, int, int, str]]:
    """
    Find all proper nouns in a file and their locations.

    Returns:
        List of tuples: (text, line_number, column_number, entity_type)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    # Load spaCy model
    print("Loading spaCy model 'en_core_web_lg'...", file=sys.stderr)
    nlp = load_spacy_model("en_core_web_lg")

    # Process the entire content
    print("Processing text...", file=sys.stderr)
    doc = nlp(content)

    # Split content into lines for location tracking
    lines = content.split('\n')

    # Build a mapping of character positions to line/column
    char_to_line_col = {}
    char_pos = 0
    for line_num, line in enumerate(lines, start=1):
        for col_num, char in enumerate(line, start=1):
            char_to_line_col[char_pos] = (line_num, col_num)
            char_pos += 1
        char_pos += 1  # Account for newline character

    # Extract proper nouns using NER
    # Focus on person, organization, geopolitical entity, and product entities
    proper_noun_types = {'PERSON', 'ORG', 'GPE', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE', 'DATE', 'TIME'}

    results = []
    for ent in doc.ents:
        if ent.label_ in proper_noun_types:
            # Get the line and column of the entity start position
            if ent.start_char in char_to_line_col:
                line_num, col_num = char_to_line_col[ent.start_char]
            else:
                # Fallback: calculate from character position
                line_num = content[:ent.start_char].count('\n') + 1
                col_num = ent.start_char - content[:ent.start_char].rfind('\n')

            results.append((ent.text, line_num, col_num, ent.label_))

    return results


def print_results(results: List[Tuple[str, int, int, str]]):
    """Print results in a readable format."""
    if not results:
        print("No proper nouns found.")
        return

    print(f"\nFound {len(results)} proper nouns:\n")
    print(f"{'Line':<6} {'Col':<6} {'Text':<30} {'Type':<12}")
    print("-" * 60)

    for text, line_num, col_num, entity_type in sorted(results, key=lambda x: (x[1], x[2])):
        # Truncate long text
        text_display = text[:27] + "..." if len(text) > 30 else text
        print(f"{line_num:<6} {col_num:<6} {text_display:<30} {entity_type:<12}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Find and report locations of proper nouns in a text file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python find_proper_nouns.py input.txt
  python find_proper_nouns.py /path/to/document.txt
        """
    )
    parser.add_argument(
        "filename",
        help="Path to the text file to analyze"
    )

    args = parser.parse_args()

    # Find proper nouns
    results = find_proper_nouns(args.filename)

    # Print results
    print_results(results)


if __name__ == "__main__":
    main()
