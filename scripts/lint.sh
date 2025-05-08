#!/bin/bash

# Format code with black
echo "Running black..."
black .

# Sort imports with isort
echo "Running isort..."
isort .

# Run flake8
echo "Running flake8..."
flake8 .

# Run mypy
echo "Running mypy..."
mypy . 