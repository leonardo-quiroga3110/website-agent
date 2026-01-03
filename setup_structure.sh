#!/bin/bash

# Project structure initialization script for LangGraph Agent

# Create directory structure
mkdir -p src/agent/core
mkdir -p src/agent/graph/nodes
mkdir -p src/agent/graph/edges
mkdir -p src/agent/tools
mkdir -p tests

# Create __init__.py files for modular package structure
touch src/agent/__init__.py
touch src/agent/core/__init__.py
touch src/agent/graph/__init__.py
touch src/agent/graph/nodes/__init__.py
touch src/agent/graph/edges/__init__.py
touch src/agent/tools/__init__.py

echo "Directory structure created successfully at src/ and tests/"
echo "To install dependencies, run: uv sync --extra dev"
