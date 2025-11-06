# Lab 04 Solutions

This directory contains solutions for Lab Exercise 4: Prompt Engineering for Development.

## Structure

- `improved_prompts.md` - Examples of improved prompts from Part 2
- `my_prompts.md` - Custom prompts for Part 3 exercises
- `app_improved.py` - Refactored Flask application with all improvements
- `tests/` - Comprehensive test suite
- `SOLUTIONS.md` - Detailed solutions and explanations
- `QUICK_REFERENCE.md` - Quick reference for prompt engineering

## Quick Start

```bash
# Activate virtual environment
source ../../.venv/bin/activate

# Install dependencies
cd solutions
pip install -r requirements.txt

# Run improved application
python app_improved.py

# Run tests
pytest tests/ -v
```

## What's Improved

1. **Refactored process_data()** - Split into smaller, focused functions
2. **Input Validation** - Added to /api/data endpoint
3. **Error Handling** - Proper database connection handling
4. **Improved Sorting** - Merge sort with type hints and validation
5. **Fixed TypeError** - Added validation to process_user_data()
