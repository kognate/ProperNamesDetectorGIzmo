# ProperNamesDetectorGizmo

A Python tool for detecting proper names and performing find-and-replace operations on text files using spaCy's natural language processing.

## Overview

**ProperNamesDetectorGizmo** leverages spaCy's named entity recognition (NER) to identify and extract proper nouns from text files. It also supports powerful find-and-replace functionality with options for case-sensitive matching, dry-run previews, and automatic backups.

## Requirements

- **Python 3.13+**
- **spaCy 3.8.7+** - For natural language processing and named entity recognition

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ProperNamesDetectorGIzmo
```

2. Install dependencies using `uv`:
```bash
uv sync
```

3. Download the spaCy English language model:
```bash
python -m spacy download en_core_web_lg
```

## Usage

The tool has two main modes: **Detection Mode** and **Find & Replace Mode**.

### Detection Mode

Find and list all proper nouns in a file with their line and column numbers:

```bash
python find_proper_nouns.py input.txt
```

Example output:
```
Detection Mode: Finding all proper nouns

Found 9 proper nouns:

Line   Col    Text                       Type
------------------------------------------------------
3      1      John Smith                 PERSON
3      21     Google                     ORG
3      33     California                 GPE
4      15     New York                   GPE
6      1      Jane Doe                   PERSON
6      21     Apple                      ORG
7      16     San Francisco              GPE
12     1      John                       PERSON
12     24     Jane                       PERSON
```

Detected entity types include:
- **PERSON** - Individual person names
- **ORG** - Organizations and companies
- **GPE** - Geopolitical entities (countries, cities, states)
- **PRODUCT** - Commercial products
- **EVENT** - Named events
- **WORK_OF_ART** - Artistic works
- **LAW** - Legal documents
- **LANGUAGE** - Language names
- **DATE** - Dates and time expressions
- **TIME** - Time expressions

### Find & Replace Mode

#### Basic replacement:
```bash
python find_proper_nouns.py input.txt --find "John" --replace "Jane"
```

#### Dry-run (preview changes without modifying):
```bash
python find_proper_nouns.py input.txt --find "John" --replace "Jane" --dry-run
```

#### Case-sensitive matching:
```bash
python find_proper_nouns.py input.txt --find "John" --replace "Jane" --case-sensitive
```

#### Create a backup before replacing:
```bash
python find_proper_nouns.py input.txt --find "John" --replace "Jane" --backup
```

#### Combined options:
```bash
python find_proper_nouns.py input.txt --find "Google" --replace "Microsoft" --dry-run --backup --case-sensitive
```

## Options

- `filename` - Path to the text file to analyze or modify
- `--find TEXT` - Text to find (requires `--replace`)
- `--replace TEXT` - Replacement text (requires `--find`)
- `--dry-run` - Preview changes without modifying the file
- `--case-sensitive` - Perform case-sensitive matching (default: case-insensitive)
- `--backup` - Create a timestamped backup before making replacements

## Example

The project includes `test_input.txt` with sample text for testing:

```
The quick brown fox jumped over the lazy dog.

John Smith works at Google in California.
He was born in New York on January 15, 1990.

Jane Doe also works at Apple.
They met in 2020 at a conference in San Francisco.

John mentioned that Google stock increased significantly.
Jane said Apple is a great company to work for.

John and Jane are now colleagues at Microsoft in Seattle.
```

Run detection:
```bash
python find_proper_nouns.py test_input.txt
```

Try a dry-run replacement:
```bash
python find_proper_nouns.py test_input.txt --find "John" --replace "John Doe" --dry-run
```

## Features

-  Automatic spaCy model detection and error handling
-  Location reporting (line and column numbers) for detected entities
-  Case-sensitive and case-insensitive find-and-replace
-  Dry-run mode for safe preview of changes
-  Automatic backup creation with timestamps
-  Context-aware replacement reporting
-  Robust encoding and error handling

## Project Status

This is an early-stage project. The current functionality provides:
- Proper noun detection with precise location tracking
- Flexible find-and-replace operations with multiple options
- Safe replacement with preview and backup capabilities

## Notes

- Ensure the spaCy English large model (`en_core_web_lg`) is downloaded before running
- Use `--dry-run` to preview changes before making them permanent
- Use `--backup` to create timestamped backup files of modified files
- Default matching is case-insensitive; use `--case-sensitive` for exact case matching
