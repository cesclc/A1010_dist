# Improved Prompts - Lab 04 Part 2 Solutions

This document contains improved versions of the ineffective prompts from Part 2 of the lab exercise.

## Exercise 1: Performance Optimization

### Original (Ineffective) Prompt
```
Make my code faster
```

### Problems with Original
- No specific function or file mentioned
- No context about what "faster" means
- No indication of current performance issues
- No guidance on constraints or requirements

### Improved Prompt
```
The process_data() function in app.py is processing large datasets inefficiently. 
Please analyze the code for performance bottlenecks and suggest optimizations, specifically:

1. Identify inefficient pandas operations that could be optimized
2. Suggest more memory-efficient alternatives for data transformation
3. Recommend any relevant pandas optimizations or vectorization techniques
4. Provide example code for the optimized solution
5. Consider parallel processing options for the report generation section
6. Estimate the expected performance improvement

Context:
- Current dataset size: ~100,000 rows
- Running on a machine with 8 CPU cores
- Memory constraint: 8GB RAM
- Need to maintain backwards compatibility with the current API

Please explain the rationale behind each optimization.
```

### Why This Is Better
- ✓ Identifies specific function (`process_data()`) and file (`app.py`)
- ✓ Provides context about the problem (large datasets, inefficiency)
- ✓ Lists specific areas to analyze (pandas operations, memory)
- ✓ Requests concrete deliverables (example code, performance estimates)
- ✓ Mentions constraints (cores, RAM, backwards compatibility)
- ✓ Asks for explanations to aid learning

---

## Exercise 2: Adding Tests

### Original (Ineffective) Prompt
```
Add tests
```

### Problems with Original
- No indication of what to test
- No testing framework specified
- No guidance on test coverage or scenarios
- No mention of testing approach or patterns

### Improved Prompt
```
Please help me write unit tests for the process_data() function in app.py using pytest.

Requirements for the tests:
1. Test successful data processing with valid input
   - Verify all statistics are calculated correctly
   - Confirm data is properly transformed
   - Check that report structure is correct

2. Test error handling with missing required fields
   - Test missing 'id' field
   - Test missing 'value' field
   - Test missing 'category' field

3. Test different data types and categories
   - Multiple categories
   - Single category
   - Numeric edge cases (zero, negative, very large numbers)

4. Test edge cases
   - Empty input list
   - Single record
   - Large datasets (1000+ records)
   - Duplicate IDs

5. Include fixtures for test data
   - Create reusable sample data sets
   - Mock database interactions

6. Add docstrings explaining each test case
   - What is being tested
   - Expected behavior
   - Why it's important

Please organize tests using pytest's class-based structure and include setup/teardown 
methods if needed for database mocking.
```

### Why This Is Better
- ✓ Specifies the function to test (`process_data()`)
- ✓ Names the testing framework (pytest)
- ✓ Lists specific test scenarios with detail
- ✓ Requests specific test patterns (fixtures, mocking)
- ✓ Asks for documentation (docstrings)
- ✓ Provides structure guidance (class-based, setup/teardown)

---

## Additional Example: Refactoring Request

### Original (Ineffective) Prompt
```
This function is too long
```

### Improved Prompt
```
The process_data() function in app.py has multiple responsibilities and needs refactoring. 
Please help me break it into smaller, focused functions following the Single Responsibility Principle.

Current structure analysis:
- Lines 10-25: Data validation
- Lines 27-31: Data transformation
- Lines 33-38: Statistics calculation
- Lines 40-50: Report generation
- Lines 52-53: Database operations

Refactoring requirements:
1. Extract a validate_data() function
   - Input: List[Dict]
   - Output: bool or raise ValidationError
   - Should validate required fields and data types

2. Extract a transform_data() function
   - Input: List[Dict]
   - Output: pd.DataFrame
   - Handle data type conversions and column additions

3. Extract a calculate_statistics() function
   - Input: pd.DataFrame
   - Output: Dict with total, average, max, min

4. Extract a generate_report() function
   - Input: pd.DataFrame
   - Output: Dict with category breakdown

5. Extract a save_to_database() function
   - Input: pd.DataFrame
   - Output: None
   - Include proper error handling

6. Update the main process_data() function to orchestrate these smaller functions

Please:
- Add comprehensive type hints to all functions
- Include docstrings with examples
- Add proper error handling at each stage
- Maintain the same external interface for backwards compatibility
```

### Why This Is Better
- ✓ Provides specific line numbers for context
- ✓ Proposes clear separation of concerns
- ✓ Specifies function signatures (input/output types)
- ✓ Requests specific improvements (type hints, docstrings, error handling)
- ✓ Mentions important constraint (backwards compatibility)

---

## Best Practices Applied

All improved prompts follow these principles:

1. **Specificity**: Name exact files, functions, and line numbers
2. **Context**: Explain the current situation and why change is needed
3. **Structure**: Use numbered lists for clarity
4. **Requirements**: State explicit expectations
5. **Constraints**: Mention limitations and requirements
6. **Deliverables**: Request specific outputs
7. **Learning**: Ask for explanations when appropriate

## Testing Your Prompts

Use this checklist when writing prompts:

- [ ] Have I specified the exact file and function?
- [ ] Have I explained what's wrong or what I want to achieve?
- [ ] Have I listed specific requirements or steps?
- [ ] Have I mentioned important constraints?
- [ ] Have I requested specific output format?
- [ ] Have I asked for explanations if I want to learn?
- [ ] Is my prompt structured and easy to follow?

## Iterative Refinement Example

### Iteration 1 (Too Vague)
```
Fix the sorting function
```

### Iteration 2 (Better, but Missing Details)
```
Improve the basic_sort() function in app.py with better performance
```

### Iteration 3 (Good)
```
The basic_sort() function in app.py uses bubble sort (O(n²)). Please improve it by:
1. Implementing merge sort for O(n log n) performance
2. Adding type hints for List[int] input and output
3. Adding input validation for empty lists
4. Adding comprehensive docstring with complexity analysis
5. Including edge case handling
```

### Iteration 4 (Excellent - After Testing)
```
The basic_sort() function in app.py (lines 67-80) currently uses bubble sort with O(n²) 
time complexity. For our use case (sorting arrays of 1000+ integers), this is too slow.

Please refactor it to:
1. Use merge sort algorithm (O(n log n) time complexity)
2. Return a NEW sorted array without modifying the input
3. Add complete type hints: def merge_sort(arr: List[int]) -> List[int]
4. Add comprehensive docstring including:
   - Description of the algorithm
   - Time and space complexity
   - Example usage
   - Edge case handling

5. Handle these edge cases:
   - Empty list: return []
   - Single element: return [element]
   - Already sorted: should still work efficiently
   - Reverse sorted: should handle gracefully

6. Include inline comments explaining the merge logic

Testing: Please also provide a simple test case that demonstrates the improved performance.

Note: The function must maintain backwards compatibility - same function name and 
external interface.
```

**What improved:** Added line numbers, performance context, specific requirements for 
return value behavior, edge cases discovered during testing, request for test case, 
and noted backwards compatibility requirement.
