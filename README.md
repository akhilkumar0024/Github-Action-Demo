# Simple Python Calculator Application

A simple, robust Python application designed to demonstrate GitHub Actions CI/CD workflows (such as linting and automated unit testing).

## Features

- Standard calculator operations: Addition, Subtraction, Multiplication, Division, Power, and Square Root.
- Type annotations for clarity and type safety.
- Comprehensive unit tests written using `pytest`.
- Linting standard checks using `flake8`.

## Project Structure

```
├── .gitignore
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   └── calculator.py
└── tests/
    ├── __init__.py
    └── test_calculator.py
```

## Getting Started

### 1. Prerequisites

Make sure you have Python 3.8+ installed.

### 2. Set Up a Virtual Environment (Optional but Recommended)

```bash
# Create a virtual environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate

# Activate it (macOS/Linux)
source venv/bin/activate
```

### 3. Install Dependencies

Install the development/testing dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Run the Application

Execute the calculator demo script:

```bash
python -m src.calculator
```

### 5. Run Unit Tests

Execute tests using `pytest`:

```bash
pytest
```

### 6. Run Lint Checks

Check for code quality standards using `flake8`:

```bash
flake8 src tests
```
