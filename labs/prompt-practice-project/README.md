# Prompt Engineering Practice Project

This is a Python project designed to help you practice prompt engineering with AI coding assistants. The project contains intentionally problematic code that you can improve through effective prompting.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

## Project Structure

The project is a Flask application with several areas for improvement:

1. `process_data()`: A complex function that needs refactoring
   - Currently handles multiple responsibilities
   - Could be split into smaller, focused functions
   - Needs better error handling

2. `/api/data` endpoint: Needs input validation
   - Currently accepts any JSON data
   - No validation of data types or required fields
   - No error handling for malformed requests

3. Database connection: Needs proper error handling
   - Currently creates connection without try/except
   - No connection pooling
   - No retry logic

4. `basic_sort()`: A simple sorting function that needs improvement
   - Uses bubble sort algorithm
   - Lacks type hints
   - No input validation
   - Minimal documentation
   - Doesn't handle edge cases

5. `process_user_data()`: Contains a TypeError bug
   - Fails when given None as input
   - No input validation
   - No error handling

## Sample Data

To test the API endpoint:
```json
[
  {
    "id": 1,
    "value": 100,
    "category": "A"
  },
  {
    "id": 2,
    "value": 200,
    "category": "B"
  }
]
```

## Exercise Tasks

Use this project to practice writing effective prompts for:

1. Refactoring the complex `process_data()` function
2. Adding input validation to the REST API endpoint
3. Implementing proper database connection error handling
4. Improving the basic sorting function
5. Fixing the TypeError in `process_user_data()`

Refer to the prompt engineering exercise document for guidance on writing effective prompts. 