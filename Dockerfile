# Use Python 3.13 slim image as base
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Set environment variables for Python and UTF-8
ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock
COPY find_proper_nouns.py find_proper_nouns.py
COPY input.txt input.txt

# Install Python dependencies using uv
RUN uv sync

# Download spaCy language model using uv
RUN uv run python -m spacy download en_core_web_lg

# Set the entry point
ENTRYPOINT ["uv", "run", "python", "find_proper_nouns.py"]

# Default command (can be overridden)
CMD ["input.txt"]
