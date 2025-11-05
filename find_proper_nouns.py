#!/usr/bin/env python3
"""
Find and report locations of proper nouns in a text file.

This script uses spaCy's NER to identify proper nouns and reports their
locations (line and column numbers) in the input file.

Additionally, it supports finding and replacing specific text in files.
"""

import argparse
import re
import shutil
import sys
from datetime import datetime
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


def create_backup(file_path: str) -> str:
    """
    Create a backup of the file before modifications.

    Args:
        file_path: Path to the file to back up

    Returns:
        Path to the backup file
    """
    path = Path(file_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = path.parent / f"{path.stem}_backup_{timestamp}{path.suffix}"
    shutil.copy2(file_path, backup_path)
    print(f"Backup created: {backup_path}", file=sys.stderr)
    return str(backup_path)


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


def replace_proper_noun(
    file_path: str,
    find_text: str,
    replace_text: str,
    case_sensitive: bool = False,
    dry_run: bool = False
) -> Tuple[int, List[Tuple[int, int, str]], str]:
    """
    Find and replace text in a file.

    Args:
        file_path: Path to the file to process
        find_text: Text to find
        replace_text: Text to replace it with
        case_sensitive: Whether matching should be case-sensitive
        dry_run: If True, don't write to file, just report what would change

    Returns:
        Tuple of (replacement_count, list of (line_num, col_num, context), modified_content)
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

    # Build pattern for finding text
    if case_sensitive:
        pattern = re.escape(find_text)
        flags = 0
    else:
        pattern = re.escape(find_text)
        flags = re.IGNORECASE

    # Find all occurrences
    replacements = []
    lines = content.split('\n')
    char_to_line_col = {}
    char_pos = 0

    for line_num, line in enumerate(lines, start=1):
        for col_num, char in enumerate(line, start=1):
            char_to_line_col[char_pos] = (line_num, col_num)
            char_pos += 1
        char_pos += 1  # Account for newline

    # Find all matches
    for match in re.finditer(pattern, content, flags):
        start_pos = match.start()
        if start_pos in char_to_line_col:
            line_num, col_num = char_to_line_col[start_pos]
        else:
            line_num = content[:start_pos].count('\n') + 1
            col_num = start_pos - content[:start_pos].rfind('\n')

        # Get context around the match
        context_start = max(0, start_pos - 20)
        context_end = min(len(content), match.end() + 20)
        context = content[context_start:context_end].replace('\n', ' ')

        replacements.append((line_num, col_num, context))

    # Perform replacement
    modified_content = re.sub(pattern, replace_text, content, flags=flags)
    replacement_count = len(replacements)

    # Write to file if not dry-run
    if not dry_run and replacement_count > 0:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            print(f"Successfully replaced {replacement_count} occurrence(s).", file=sys.stderr)
        except Exception as e:
            print(f"Error writing to file: {e}", file=sys.stderr)
            sys.exit(1)

    return replacement_count, replacements, modified_content


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Find and report locations of proper nouns in a text file, or find and replace text.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples (Detection Mode):
  python find_proper_nouns.py input.txt
  python find_proper_nouns.py /path/to/document.txt

Examples (Replacement Mode):
  python find_proper_nouns.py input.txt --find "John" --replace "Jane"
  python find_proper_nouns.py input.txt --find "John" --replace "Jane" --dry-run
  python find_proper_nouns.py input.txt --find "John" --replace "Jane" --case-sensitive
        """
    )
    parser.add_argument(
        "filename",
        help="Path to the text file to analyze or modify"
    )
    parser.add_argument(
        "--find",
        type=str,
        default=None,
        help="Text to find for replacement (requires --replace)"
    )
    parser.add_argument(
        "--replace",
        type=str,
        default=None,
        help="Text to replace with (requires --find)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview replacements without modifying the file"
    )
    parser.add_argument(
        "--case-sensitive",
        action="store_true",
        help="Perform case-sensitive matching (default: case-insensitive)"
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Create a backup file before making replacements"
    )

    args = parser.parse_args()

    # Validate find/replace arguments
    if (args.find is None) != (args.replace is None):
        print("Error: --find and --replace must be used together.", file=sys.stderr)
        sys.exit(1)

    # Mode 1: Find and Replace
    if args.find is not None and args.replace is not None:
        print(f"Find and Replace Mode", file=sys.stderr)
        print(f"Finding: '{args.find}'", file=sys.stderr)
        print(f"Replacing with: '{args.replace}'", file=sys.stderr)

        # Create backup if requested
        if args.backup:
            create_backup(args.filename)

        # Perform replacement
        count, replacements, modified_content = replace_proper_noun(
            args.filename,
            args.find,
            args.replace,
            case_sensitive=args.case_sensitive,
            dry_run=args.dry_run
        )

        # Print results
        if count == 0:
            print(f"\nNo matches found for '{args.find}'.")
        else:
            mode = "would replace" if args.dry_run else "replaced"
            print(f"\n{mode.capitalize()} {count} occurrence(s):\n")
            print(f"{'Line':<6} {'Col':<6} {'Context':<50}")
            print("-" * 65)

            for line_num, col_num, context in replacements:
                # Truncate long context
                context_display = context[:47] + "..." if len(context) > 50 else context
                print(f"{line_num:<6} {col_num:<6} {context_display:<50}")

            if args.dry_run:
                print(f"\n(Dry run: no changes were made)")

    # Mode 2: Detection (original behavior)
    else:
        print(f"Detection Mode: Finding all proper nouns", file=sys.stderr)
        # Find proper nouns
        results = find_proper_nouns(args.filename)

        # Print results
        print_results(results)


if __name__ == "__main__":
    main()
