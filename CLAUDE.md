# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ProperNamesDetectorGizmo** is a Python project for detecting proper names. It uses:
- **Python 3.13** (specified in `.python-version`)
- **spaCy 3.8.7+** for NLP tasks (specified in `pyproject.toml`)
- **uv** for package management (`uv.lock` present, `pyproject.toml` defines dependencies)

This is an early-stage project with minimal structure - currently just a `main.py` entry point.

## Development Setup

### Install Dependencies
```bash
uv sync
```

### Run the Project
```bash
python main.py
```

## Architecture Notes

The project is in its initial phase. As it grows, consider organizing code as follows:
- Core detection logic should be in dedicated modules (e.g., `src/detector.py` or similar)
- spaCy model initialization and caching should be centralized to avoid repeated loading
- NLP pipeline configuration should be separate from business logic

The project will likely need:
- Input/output handling for text processing
- Model selection and caching strategy for spaCy pipelines
- Performance optimization for batch processing if handling large datasets

## Key Dependencies

- **spaCy**: Used for natural language processing and named entity recognition (NER). Requires downloading language models (e.g., `python -m spacy download en_core_web_sm`)

## Important Notes

- Ensure spaCy models are downloaded before running the application
- Consider adding test infrastructure as the project grows
- README is currently empty - consider documenting project goals and usage
