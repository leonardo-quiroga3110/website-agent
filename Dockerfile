# Use Python 3.11 as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src \
    GRADIO_SERVER_NAME="0.0.0.0"

# Install system dependencies for Docling and Gradio
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Create and set the working directory
WORKDIR /app

# Create a non-root user and set permissions
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Copy the dependency files and install
COPY --chown=user pyproject.toml README.md ./
COPY --chown=user src ./src
RUN pip install --no-cache-dir langgraph-checkpoint-postgres langgraph-checkpoint-sqlite "psycopg[binary]" psycopg-pool
RUN pip install --no-cache-dir .

# Copy the rest of the application
COPY --chown=user . .

# Ensure the chroma_db directory exists and is writable
RUN mkdir -p chroma_db && chmod 777 chroma_db

# Expose the HF Spaces port (default is 7860)
EXPOSE 7860

# Command to run the application
# Default to Gradio UI for HF Spaces, but you can still run main.py for WhatsApp
CMD ["python", "src/ui.py"]
