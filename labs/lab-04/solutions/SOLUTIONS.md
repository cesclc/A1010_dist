# Lab 04 Solutions - Prompt Engineering for Development

## Overview

This document contains complete solutions for Lab Exercise 4: Prompt Engineering for Development. All exercises have been implemented with comprehensive code, tests, and documentation.

## Project Structure

```
labs/lab-04/
├── solutions/
│   ├── README.md                 # Solutions overview
│   ├── improved_prompts.md       # Part 2: Improved prompt examples
│   ├── my_prompts.md            # Part 3: Custom prompts
│   ├── app_improved.py          # Complete refactored application
│   ├── requirements.txt         # Dependencies
│   ├── SOLUTIONS.md             # This file
│   └── QUICK_REFERENCE.md       # Quick reference guide
└── tests/
    ├── __init__.py
    └── test_app_improved.py     # Comprehensive test suite (50+ tests)
```

## Part 1: Analyzing Prompt Effectiveness

### Key Takeaways from Examples

**Example 1 - Writing a Function:**
- ✓ Name the specific function and file
- ✓ Request specific improvements (type hints, docstrings, algorithm)
- ✓ Define expected behavior clearly
- ✓ Mention edge cases

**Example 2 - Debugging Code:**
- ✓ Include the exact error message
- ✓ Describe when the error occurs
- ✓ Request structured improvements
- ✓ Ask for documentation

## Part 2: Practice Improving Prompts

### Exercise 1: Performance Optimization

**Solution:** See `solutions/improved_prompts.md`

Key improvements made:
- Named specific function (`process_data()`) and file
- Provided context (dataset size: 100K rows, constraints: 8GB RAM)
- Listed specific optimization areas
- Requested performance estimates
- Asked for explanations

### Exercise 2: Adding Tests

**Solution:** See `solutions/improved_prompts.md`

Key improvements made:
- Specified testing framework (pytest)
- Listed specific test scenarios with detail
- Requested test patterns (fixtures, mocking)
- Asked for documentation
- Provided structure guidance

## Part 3: Creating Your Own Prompts

All three custom prompts are documented in `solutions/my_prompts.md`:

1. **Refactoring process_data()** - Comprehensive prompt breaking function into 6 smaller functions
2. **Adding Input Validation** - Detailed validation requirements for REST API
3. **Database Connection Error Handling** - Complete database manager implementation

Each prompt follows best practices:
- Specific file and line references
- Clear problem statement
- Structured requirements
- Type signatures
- Request for explanations

## Implementation Solutions

### Exercise 1: Refactored process_data()

**Before:** Single 45-line function doing 5 different things

**After:** 6 focused functions following Single Responsibility Principle

```python
# New Functions:
1. validate_input_data()      # Validation only
2. transform_to_dataframe()   # Data transformation
3. calculate_statistics()     # Statistics calculation
4. generate_category_report() # Report generation
5. save_processed_data()      # Database operations
6. process_data()             # Orchestration (refactored)
```

**Benefits:**
- Each function has single responsibility
- Easy to test in isolation
- Better error handling at each stage
- Reusable components
- Clear function signatures with type hints

### Exercise 2: Input Validation for /api/data

**Implemented Validations:**

1. **Content-Type Check:**
   - Returns 415 if not application/json

2. **JSON Parsing:**
   - Catches JSON decode errors
   - Returns 400 with helpful message

3. **Schema Validation:**
   - Validates all required fields
   - Checks data types for each field
   - Verifies ID uniqueness
   - Checks alphanumeric category
   - Returns 422 with specific errors

4. **Business Rules:**
   - Minimum 1 item
   - Maximum 1000 items
   - Positive integer IDs
   - Non-empty categories

5. **Error Response Format:**
   ```json
   {
     "error": "Error type",
     "details": ["Specific error messages"],
     "status": 422
   }
   ```

### Exercise 3: Database Connection Error Handling

**Implemented DatabaseManager Class:**

```python
class DatabaseManager:
    - __init__()                    # Initialize with error handling
    - check_connection()           # Health check
    - execute_with_retry()         # Retry with exponential backoff
```

**Features:**
- Connection pooling configuration
- Exponential backoff retry logic (max 3 attempts)
- Graceful degradation (app starts even if DB fails)
- Comprehensive logging
- Environment variable configuration
- Context manager support

### Additional Improvements

**Improved Sorting Function:**
- Changed from bubble sort O(n²) to merge sort O(n log n)
- Added complete type hints
- Comprehensive docstring with complexity analysis
- Edge case handling (empty, single element)
- Does not modify original array

**Fixed process_user_data():**
- Handles None input gracefully
- Validates tuple/list type
- Validates tuple length
- Type checks for name and age
- Age range validation
- Clear error messages

## Testing Strategy

### Test Coverage

**50+ tests across 10 test classes:**

1. `TestValidateInputData` - 9 tests
   - Valid data, invalid types, missing fields, duplicates, edge cases

2. `TestTransformToDataframe` - 3 tests
   - Basic transformation, type conversion, uppercase conversion

3. `TestCalculateStatistics` - 3 tests
   - Basic stats, empty data, single value

4. `TestGenerateCategoryReport` - 2 tests
   - Multiple categories, single category

5. `TestMergeSort` - 8 tests
   - Basic sort, edge cases, already sorted, reverse sorted, duplicates

6. `TestProcessUserData` - 7 tests
   - Valid input, None, invalid types, wrong length, validation

7. `TestDatabaseManager` - 3 tests
   - Initialization, connection check, failure handling

8. `TestProcessData` - 2 tests
   - Complete pipeline, failed save

9. `TestFlaskAPI` - 4 tests
   - Valid request, missing content-type, invalid JSON, validation errors

### Running Tests

```bash
# Activate virtual environment
source ../../.venv/bin/activate

# Install dependencies
cd solutions
pip install -r requirements.txt

# Run all tests
cd ../tests
pytest test_app_improved.py -v

# Run with coverage
pytest test_app_improved.py --cov=../solutions/app_improved --cov-report=html

# Run specific test class
pytest test_app_improved.py::TestMergeSort -v
```

## Part 4: Testing and Refinement

### Example: Refining the process_data() Prompt

**Iteration 1 (Too Vague):**
```
Refactor this function
```

**Iteration 2 (Better):**
```
Refactor process_data() in app.py into smaller functions
```

**Iteration 3 (Good):**
```
Refactor process_data() in app.py by splitting it into:
1. validate_data()
2. transform_data()
3. calculate_stats()
4. generate_report()
5. save_to_db()
```

**Iteration 4 (Excellent - After Testing):**
```
The process_data() function in app.py (lines 11-56) has multiple 
responsibilities. Please refactor following Single Responsibility Principle:

1. validate_input_data(data: List[Dict]) -> None
   - Validate required fields exist
   - Check data types
   - Raise ValidationError with details

2. transform_to_dataframe(data: List[Dict]) -> pd.DataFrame
   ...
```

**What Improved:**
- Added line numbers
- Specified exact function signatures
- Explained the principle (SRP)
- Requested specific error handling
- More detail for each function

## Best Practices Checklist

When writing prompts, ensure:

- [x] **Specificity**: Named exact files, functions, line numbers
- [x] **Context**: Explained current problems and why change is needed
- [x] **Structure**: Used numbered lists and clear sections
- [x] **Requirements**: Stated explicit expectations
- [x] **Constraints**: Mentioned limitations (backwards compatibility, etc.)
- [x] **Deliverables**: Requested specific outputs (code, docs, tests)
- [x] **Learning**: Asked for explanations and rationale
- [x] **Testing**: Requested test cases and examples

## Common Patterns for Effective Prompts

### 1. Context Setting Pattern
```
I'm working on [file/function] at line [X].
The current code [describe issue].
This is problematic because [explain impact].
```

### 2. Structured Requirements Pattern
```
Please help me:
1. [Specific task with details]
2. [Another specific task]
3. [Third task]

Each should:
- [Requirement A]
- [Requirement B]
```

### 3. Constraints and Preferences Pattern
```
Requirements:
- Must be compatible with [version]
- Should follow [pattern/practice]
- Need to handle [edge cases]
- Maintain [compatibility requirement]
```

### 4. Example-Driven Pattern
```
Please implement [feature] similar to:
[Code example or description]

But adapted to:
- [Specific requirement 1]
- [Specific requirement 2]
```

## Lab Challenge Solution

### Task: Comprehensive Refactoring with Iteration

**Initial Prompt:**
```
Improve the data processing function
```

**Testing Result:** Got generic suggestions, not actionable

**Refined Prompt (Iteration 2):**
```
The process_data() function in app.py does too many things.
Please split it into smaller functions.
```

**Testing Result:** Got function breakdown but inconsistent signatures

**Final Refined Prompt (Iteration 3):**
```
[See my_prompts.md for complete refined prompt]
```

**Testing Result:** ✓ Got complete, working implementation

### What I Learned:

1. **Specificity Matters:** Line numbers and exact names get better results
2. **Type Hints Help:** Requesting signatures ensures consistent interfaces
3. **Context is Key:** Explaining "why" helps AI understand intent
4. **Iteration Works:** Each refinement improved the output
5. **Structure Helps:** Numbered lists are easier to follow
6. **Examples Matter:** Requesting examples ensures understanding

## Key Takeaways

### What Makes a Prompt Effective:

1. **Clarity:** No ambiguity about what you want
2. **Context:** Sufficient background information
3. **Structure:** Well-organized with clear sections
4. **Specificity:** Exact references and requirements
5. **Constraints:** Explicit limitations and requirements
6. **Testability:** Request for examples and test cases

### What Makes a Prompt Ineffective:

1. **Vagueness:** "Make it better" - better how?
2. **No Context:** Missing file names, function names
3. **Unstructured:** Wall of text without organization
4. **Too Broad:** Asking for too many unrelated things
5. **No Constraints:** Missing important requirements
6. **No Examples:** Hard to verify correctness

### Prompt Engineering as a Skill:

- **Iterative Process:** First prompt rarely perfect
- **Test and Refine:** Try it, see results, improve
- **Learn from AI:** Notice what works, what doesn't
- **Document Patterns:** Save effective prompts for reuse
- **Stay Specific:** More detail = better results

## Running the Complete Solution

### Setup
```bash
# Navigate to solutions
cd labs/lab-04/solutions

# Activate virtual environment
source ../../.venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run Application
```bash
python app_improved.py
```

### Test with curl
```bash
# Valid request
curl -X POST http://localhost:5000/api/data \
  -H "Content-Type: application/json" \
  -d '[{"id":1,"value":100,"category":"A"}]'

# Invalid request (missing field)
curl -X POST http://localhost:5000/api/data \
  -H "Content-Type: application/json" \
  -d '[{"id":1,"value":100}]'
```

### Run Tests
```bash
cd ../tests
pytest test_app_improved.py -v
```

## Further Improvements

Consider these additional enhancements:

1. **Caching:** Add Redis for processed results
2. **Async Processing:** Use Celery for background jobs
3. **API Documentation:** Add OpenAPI/Swagger docs
4. **Rate Limiting:** Protect endpoints from abuse
5. **Authentication:** Add JWT or API key auth
6. **Monitoring:** Add metrics and health checks
7. **Docker:** Containerize the application

## Resources

- Original practice project: `labs/prompt-practice-project/`
- Lab instructions: `labs/lab-04-prompt-engineering-for-development.md`
- Improved prompts: `solutions/improved_prompts.md`
- Custom prompts: `solutions/my_prompts.md`
- Quick reference: `solutions/QUICK_REFERENCE.md`

## Conclusion

Effective prompt engineering is a learnable skill that dramatically improves AI coding assistant effectiveness. Key principles:

1. Be specific and provide context
2. Structure requests clearly
3. Iterate and refine based on results
4. Request examples and explanations
5. Mention constraints and requirements
6. Test the output and improve the prompt

This lab demonstrates that well-crafted prompts lead to production-quality code with proper error handling, testing, and documentation.
